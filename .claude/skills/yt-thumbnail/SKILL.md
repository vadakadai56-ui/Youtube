---
name: yt-thumbnail
description: Choose or make the cover for a Short. Use before /yt-publish or when the owner asks for a thumbnail or cover frame. Uses pipeline/cover.py.
---
# /yt-thumbnail: Shorts cover

The cover shows on the channel's Shorts tab and in search. A strong one is a single clear image plus 2 to 6 words.

## 1. Find candidate frames
```bash
python3 pipeline/cover.py sheet out/<slug>.mp4 /tmp/cover_sheet.jpg 16
```
Look at the sheet. Pick 3 frames: one clear subject, readable at small size, the mystery visible (the empty swing, the second cup) but not the twist.

## 2. Make covers with text
```bash
python3 pipeline/cover.py make out/<slug>.mp4 <seconds> out/<slug>-cover.jpg "Every evening at 6" "an empty swing"
```
Text: 2 short lines max, last line in yellow, kept in the top third so the Shorts UI never covers it. Make 2 or 3 variants and show them to the owner.

## 3. Hand off
- Upload the chosen jpg with `python3 pipeline/publish.py out/<slug>-cover.jpg /Youtube/covers/<slug>.jpg` and pass the link as `videoThumbnailUrl`, **or** pass `videoCoverMilliseconds` (printed by `cover.py make`) to use the plain frame.
- Metricool rejects the whole post if the thumbnail does not apply (YouTube only shows custom Shorts covers on verified channels where YouTube has enabled it). If unsure, use `videoCoverMilliseconds` or leave both out.
