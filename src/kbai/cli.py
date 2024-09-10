# Copyright (C) 2024 Andrew Wason
# SPDX-License-Identifier: AGPL-3.0-or-later

from argparse import SUPPRESS, Action, ArgumentParser, Namespace

from .main import detect_main, encode_main
from .structs import Size, Transition


class ImageAction(Action):
    image_parser = ArgumentParser(add_help=False)
    image_parser.add_argument("image", help="Image url or path to detect features in.")
    image_parser.add_argument(
        "-id", dest="image_duration", type=float, default=SUPPRESS, help="Image duration in seconds."
    )
    image_parser.add_argument(
        "-tn",
        dest="transition_name",
        type=Transition,
        default=SUPPRESS,
        help="Transition name for transitioning to next image.",
    )
    image_parser.add_argument(
        "-td",
        dest="transition_duration",
        type=float,
        default=SUPPRESS,
        help="Duration of transition in seconds.",
    )
    image_parser.add_argument(
        "-ft", dest="feature_text", action="append", default=SUPPRESS
    )  # XXX how can user specify None?

    def __init__(self, option_strings, dest=None, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest=dest, nargs="+", **kwargs)  # XXX "+" eats the output filename

    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        values,
        option_string: str | None = None,
    ) -> None:
        images = getattr(namespace, self.dest) or []
        image = vars(self.image_parser.parse_args([values[0]] + [a.replace("/", "-") for a in values[1:]]))
        images.append(image)
        setattr(namespace, self.dest, images)

    def format_usage(self) -> str:
        return self.image_parser.format_usage().replace("--", "/").replace("-", "/")


def parse_size(value: str) -> Size:
    w, h = value.split("x")
    return Size(int(w), int(h))


def build_encode_parser(subparsers: Action) -> None:
    parser = subparsers.add_parser("encode", description="Encode images with pan/zoom into a video.")

    parser.add_argument("-o", "--output", help="Output video filename (with extension).")
    parser.add_argument("-r", "--framerate", type=int, default=25, help="Output video framerate (FPS).")
    parser.add_argument(
        "-s",
        "--size",
        type=parse_size,
        default="640x360",
        help="Output video size (WxH).",
    )
    parser.add_argument(
        "-did", "--default-image-duration", type=float, default=5, help="Default image duration."
    )
    parser.add_argument(
        "-dtn",
        "--default-transition-name",
        type=Transition,
        choices=[str(t) for t in Transition],
        default=Transition.fade,
        help="Default image transition name.",
    )
    parser.add_argument(
        "-dtd",
        "--default-transition-duration",
        type=float,
        default=1,
        help="Default image transition duration.",
    )
    parser.add_argument(
        "-dft",
        "--default-feature-text",
        action="append",
        default=["a human face", "a person", "a dog", "a cat"],
        help="Default image feature detection text.",
    )
    parser.add_argument(
        "-i",
        "--image",
        action=ImageAction,
        required=True,  # help="Image filenames with options"
        # XXX figure out help
        help=ImageAction.image_parser.format_help(),
    )
    parser.set_defaults(func=encode_main)


def build_detect_parser(subparsers: Action) -> None:
    parser = subparsers.add_parser(
        "detect", description="Detect features in image and display bounding boxes (useful for debugging)."
    )
    parser.add_argument("image", help="Image url or path to detect features in.")
    parser.add_argument("feature", action="append", help="Feature description.")
    parser.set_defaults(func=detect_main)


def main() -> None:
    parser = ArgumentParser(description="'Ken Burns' AI - automatic image pan and zoom.")
    subparsers = parser.add_subparsers(title="commands", required=True)
    build_encode_parser(subparsers)
    build_detect_parser(subparsers)
    args = parser.parse_args()
    args.func(args)
