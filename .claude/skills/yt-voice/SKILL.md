---
name: yt-voice
description: Generate the narration with ElevenLabs and the word timings for captions. Use after a script is approved, or when the owner asks to re-voice a line. Never run on an unapproved script.
---
# /yt-voice: narration and word timings

## Check first
- `STATUS.md` says the script is approved. If not, stop and ask.
- Confirm once with the owner before generating (it spends ElevenLabs credits). One take.

## Generate
- ElevenLabs connector: `creative_generate_speech`, voice **George** `JBFqnCBsd6RMkjVDRZzb`, model `eleven_v4`, the full text of `stories/<slug>/narration.txt` including audio tags. `generations_count` 1. Never call it twice to retry: poll `creative_get_flow_run_status` until done.
- Download the result to `narration.mp3` in the working directory (mp3s are not committed; they live in Dropbox).

## Word timings
```bash
python3 pipeline/align.py narration.mp3 stories/<slug>/narration.txt stories/<slug>/words.json
```
If alignment is off (captions early or late), use `creative_transcribe_audio` (Scribe) for timings instead.

## Report
Length in seconds (flag if outside 55 to 75), any line that sounds wrong (tag read aloud, mispronunciation), and the path to `words.json`. Then hand off to `/yt-build`.

Optional: upload `narration.mp3` to Dropbox `/Youtube/audio/<slug>.mp3` with `pipeline/publish.py` so it survives a session reset.
