# KBAI - "Ken Burns" AI

Given a list of image URL/filenames, generates a video with "Ken Burns" style pan & zoom effects,
with transitions between each image.

Uses [Grounding DINO](https://huggingface.co/IDEA-Research/grounding-dino-tiny) LLM to identify features
in the images.
Requires the [ffmpeg](https://ffmpeg.org/) tool to be installed.
Builds a filtergraph using the [zoompan](https://ffmpeg.org/ffmpeg-filters.html#zoompan) and
[xfade](https://ffmpeg.org/ffmpeg-filters.html#xfade) filters.

## Example

```sh-session
$ uv run kbai encode -s 640x480 \
    -i https://picsum.photos/id/22/1280/960 /ft person \
    -i https://picsum.photos/id/26/1280/960 /ft watch /id 2 /td 0.5 /tn circlecrop /te linear \
    -i https://picsum.photos/id/29/1280/960 /ft cloud /id 7 \
    -i https://picsum.photos/id/39/1280/960 /ft "turntable needle" /tn revealup \
    -i https://picsum.photos/id/42/1280/960 /ft people \
    -i https://picsum.photos/id/50/960/1280 /ft bird /if contain \
    -o multiple.mp4 
```
Results in this video: