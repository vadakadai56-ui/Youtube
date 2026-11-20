---
name: yt-qc
description: Check a finished video before upload. Use after /yt-build, before /yt-publish, or when the owner asks "is this ready". Runs pipeline/qc.py and a visual spot check.
---
# /yt-qc: ready to upload?

## 1. Technical check
```bash
python3 pipeline/qc.py out/<slug>.mp4
```
Checks 9:16, 1080x1920, fps, codec, length (Shorts max 180 s, channel target 55 to 75 s), loudness -14 LUFS +/- 1, true peak, silence or black at the start. Exit 1 means a FAIL: fix it before publishing.
- Loudness off: re-run the edit's `loudnorm` pass (README step 5).
- True peak over -1 dBTP: add `alimiter=limit=0.89` before `loudnorm`.

## 2. Look at it
```bash
python3 pipeline/cover.py sheet out/<slug>.mp4 /tmp/qc_sheet.jpg 12
```
Open the sheet and check: frame 1 shows the hook; no caption runs off screen or sits under the bottom 300 px (Shorts title bar) or the right 140 px (buttons); no black or broken frames; the end card is readable.

## 3. Listen
Extract 3 spots (start, the turn, the end) with `ffmpeg -ss T -t 6` and check narration is above the music.

## 4. Policy
- YouTube requires disclosure of realistic AI-altered content. Dustlight is stylised 3D with an AI voice: set `isAiGeneratedContent` honestly when publishing; ask the owner if unsure.
- No copyrighted music or footage. All Dustlight sound is synthesized in `edit.py`.

Report PASS/WARN/FAIL in a short table, then hand off to `/yt-title` and `/yt-thumbnail`.
