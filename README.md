# Dustlight

YouTube Shorts channel **Dustlight** (@the.dustlight.stories), *stories about the things we forgot*.

Short narrated 3D stories in a cosy toy-world style, with an original script, AI narration, word-by-word captions and synthesized sound.

## How a video gets made

1. **Script.** Written with Claude and approved by the owner before building. See `stories/`.
2. **Voice.** ElevenLabs, voice **George** (`JBFqnCBsd6RMkjVDRZzb`), model `eleven_v4`, one take.
3. **Word timings.** ElevenLabs Scribe transcription, or `ffmpeg silencedetect` aligned to the script's phrases.
4. **Scenes.** Built procedurally in Blender (`bpy` 5.0.1 for Python 3.11, installed with pip into a venv).
   - Stills: Cycles, CPU, 40 samples, 540x960, upscaled to 1080x1920.
   - **Animation (from "The Second Cup" on): Eevee.** It needs Mesa: `apt-get install -y libegl1 libgl1-mesa-dri libegl-mesa0 libgles2`. About 6 to 10 s per frame at 540x960, 12 samples, 12 fps, blended to 30 fps in the edit.
5. **Edit.** Python, PIL and ffmpeg: camera moves, crossfades, grain, vignette, captions (InterDisplay-Black, yellow keywords), synthesized music and sound effects, narration ducking. Then `loudnorm` to -14 LUFS, with a second gain pass if the result is under -14.
6. **Upload.** Dropbox API (`/Youtube` folder, chunked upload sessions over 150 MB, public share link). The Dropbox token is short-lived, about 4 h. It is saved as an environment network secret and never pasted in chat.
7. **Schedule.** Metricool (brand id `7551785`, timezone Europe/Riga), YouTube `short`, category `FILM_ANIMATION`, madeForKids false, with a pinned first comment that asks a question.

## Rules
- Original stories, characters and scenes only. No copying other channels' stories, characters or looks.
- The owner approves every script before it is built.
- Do not change or delete published videos without asking.
- Large media (renders, mp4s) live in Dropbox, not in git.

## Status
See `STATUS.md`.
