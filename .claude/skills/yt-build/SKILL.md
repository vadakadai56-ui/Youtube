---
name: yt-build
description: Build the video. Turns an approved script, narration and shot list into shots.py and edit_config.py, renders the frames in Blender (Eevee) and edits the final mp4 with captions, sound and loudness. Use when narration is ready and the owner wants the video rendered.
---
# /yt-build: render and edit

Copy `stories/the-empty-swing/` (or `the-second-cup/`) as the template. Read `pipeline/anim.py`, `pipeline/edit.py` and the template's `shots.py` before writing new ones.

## Steps
```bash
bash pipeline/setup.sh                        # once per fresh session (bpy venv + Mesa)
VENV=~/.dustlight-venv
# shots.py: one shot per 2 to 3 s, matched to words.json; reuse sets/characters from scene.py and world.py
PREVIEW=1 PCT=25 ES=6 $VENV/bin/python pipeline/anim.py stories/<slug> /tmp/frames all   # framing check, ~2 min
```
Look at frame 0 of every shot. Fix framing before the full render.
```bash
PCT=50 ES=12 $VENV/bin/python pipeline/anim.py stories/<slug> /tmp/frames all            # full render, resumable
python3 pipeline/edit.py stories/<slug> /tmp/frames narration.mp3 out/<slug>.mp4
```
- Background jobs stop at 3 hours: render in batches of shots (`anim.py ... s1 s2 s3`) and re-run to resume.
- Confirm with the owner before a render expected to take over an hour.

## edit_config.py
`CUTS` from `durations.json`, `KEY` words in yellow (from `/yt-script`), `XFADE` for the turn and payoff, `END_LINES` for the end card (a quiet closing line, then "D U S T L I G H T"), and `sound(S)`: music that matches the trend's mood (for example tense pulses for a mystery, bouncy plucks for comedy, minor-to-major for an emotional story), a hit at the turn, and story-specific effects. All synthesized, never copyrighted tracks.

## Style (channel kit)
Warm dusty toy world, bulb glow, floating dust, vignette, grain. Captions 1 to 3 words, white with a black outline, keywords #FFD640, around y=1210 to 1240. Cut every 2 to 3 s.

## Done
Run `/yt-qc` on `out/<slug>.mp4`. Commit the story folder (not the mp4) and update `STATUS.md`.
