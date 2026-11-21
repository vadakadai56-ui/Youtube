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

## Making a new story (commands)
```bash
bash pipeline/setup.sh                                   # once per fresh session: Blender (bpy) venv + Mesa for Eevee
VENV=~/.dustlight-venv
mkdir -p stories/my-story                                # narration.txt, shots.py, edit_config.py (copy the-second-cup as a template)
# 1. Voice: generate narration.txt with ElevenLabs (George, eleven_v4), save it as narration.mp3 (not committed)
python3 pipeline/align.py narration.mp3 stories/my-story/narration.txt stories/my-story/words.json
# 2. Framing check (frame 0 of every shot, about 2 min)
PREVIEW=1 PCT=25 ES=6 $VENV/bin/python pipeline/anim.py stories/my-story /tmp/frames all
# 3. Full animation (resumable: re-run the same command after a reset and it continues)
PCT=50 ES=12 $VENV/bin/python pipeline/anim.py stories/my-story /tmp/frames all
# 4. Edit: captions, sound, end card, loudness -14 LUFS
python3 pipeline/edit.py stories/my-story /tmp/frames narration.mp3 out/my-story.mp4
# 5. Dropbox upload and public link, then schedule in Metricool
python3 pipeline/publish.py out/my-story.mp4
```
Keep long renders under the 3-hour background-job limit: render in batches of shots (`anim.py ... k1 k2 k3`).

## YouTube agent skills (`.claude/skills/yt-*`)
Claude Code skills that run the channel. Type `/yt-channel` (or "run my YouTube") to see where things stand and what to do next.

| Skill | Job |
|---|---|
| `/yt-channel` | Hub: reads STATUS, Metricool and the story folders, picks the next step |
| `/yt-trends` | Live research: trending topics, formats and hooks, ranked; writes `channel/trends.md` |
| `/yt-idea` | Pitches 3 original ideas built on the current top trends |
| `/yt-script` | Writes `narration.txt` with v4 audio tags; waits for owner approval |
| `/yt-hook` | 10 opening lines, scored, for the first 3 s |
| `/yt-voice` | ElevenLabs narration (George) and `words.json` timings |
| `/yt-build` | `shots.py`, `edit_config.py`, Blender render and edit |
| `/yt-qc` | `pipeline/qc.py`: 9:16, length, -14 LUFS, true peak, hook gaps |
| `/yt-title` | Title options, description, tags, pinned question |
| `/yt-thumbnail` | `pipeline/cover.py`: candidate frames and text covers |
| `/yt-publish` | Dropbox upload and Metricool scheduling |
| `/yt-plan` | 7 to 14-day calendar worked back from each slot |
| `/yt-analytics` | Metricool numbers, patterns, changes for next scripts |
| `/yt-comments` | Reply drafts, pins, ideas from viewers |
| `/yt-series` | Multi-part story outlines and release plans |

## Code
- `pipeline/scene.py`: Blender toolkit (materials, primitives, lights, camera), the Lost Toy Room set, toys, Bun-Bun, door, silhouettes.
- `pipeline/world.py`: peg-doll characters (Walter, Rose, nurse, neighbours), walk and breathe animation, props (cups, teapot, flask), Steam, Snow, sets (kitchen, snowy street, care home, care room).
- `pipeline/anim.py`: Eevee frame renderer for a story's `shots.py`.
- `pipeline/align.py`: word timings from the narration's pauses and the script.
- `pipeline/edit.py`: the editor and sound toolkit; reads the story's `edit_config.py`.
- `pipeline/publish_github.py`: **default publisher (from 22 Nov 2026).** Commits an upload copy (under 95 MB, 1080p) to the public repo `vadakadai56-ui/dustlight-media` and prints its raw.githubusercontent.com URL for Metricool. No expiring tokens. Needs that repo attached and cloned at `/home/user/dustlight-media`.
- `pipeline/publish.py`: Dropbox upload (chunked) and public link. Old route: Dropbox tokens expire after about 4 h and the owner's apps can no longer generate them.
- `pipeline/sfx_library.py`: builds the Dustlight sound library (57 CC0 recordings in 23 categories) from Openverse into `~/dustlight-sfx`. The list is `channel/sfx-library.json`; rebuild with `python3 pipeline/sfx_library.py build`, then `cd .claude/skills/real-sfx && python3 scripts/setup.py add-library dustlight ~/dustlight-sfx --tier main --index`.
- Listening: `earshot describe FILE` (models download on first use, about 1.1 GB). The real-sfx model (`scripts/hear.py`, 3.1 GB) is installed but weak; prefer earshot.
- `pipeline/openverse.py`: search and download openly licensed sounds and images (CC0, public domain, CC-BY, CC-BY-SA only) from the Openverse API. Writes the story's `CREDITS.md`. Put any BY / BY-SA credit lines in the YouTube description.
- `pipeline/qc.py`: pre-upload checks (exit 1 on a fail).
- `pipeline/cover.py`: contact sheet of candidate cover frames, and 1080x1920 covers with caption-style text.

## Rules
- Original stories, characters and scenes only. No copying other channels' stories, characters or looks.
- The owner approves every script before it is built.
- Do not change or delete published videos without asking.
- Large media (renders, mp4s) live in Dropbox, not in git.

## Status
See `STATUS.md`.
