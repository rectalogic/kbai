# KBAI - "Ken Burns" AI

Given a list of image URL/filenames, generates a video with "Ken Burns" style pan & zoom effects,
with transitions between each image.

Uses [Grounding DINO](https://huggingface.co/IDEA-Research/grounding-dino-tiny) LLM to identify features
in the images.
Requires the [ffmpeg](https://ffmpeg.org/) tool to be installed.
Builds a filtergraph using the [zoompan](https://ffmpeg.org/ffmpeg-filters.html#zoompan) and
[xfade](https://ffmpeg.org/ffmpeg-filters.html#xfade) filters.