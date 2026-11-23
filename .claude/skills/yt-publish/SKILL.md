---
name: yt-publish
description: Upload a finished, checked video and schedule it on YouTube and Instagram (through Windsor.ai), plus TikTok where possible. Use when a video has passed /yt-qc and has a title. Confirms the slot with the owner before scheduling.
---
# /yt-publish: upload and schedule

## Preconditions
`/yt-qc` passed, `/yt-title` approved. Check `STATUS.md` (and Windsor's scheduled list) so you do not double-book a slot.

## 1. Host the file
```bash
python3 pipeline/publish_github.py out/<slug>.mp4 <slug>.mp4
```
It compresses anything over 95 MB and prints a public raw.githubusercontent.com URL. Attach `vadakadai56-ui/Dustlight-Files`
(push) and clone it to `/home/user/dustlight-files` first if it is missing.

## 2. Slot
Default slots (Europe/Riga): YouTube 10:00 or 16:00, Instagram Reel 12:00 or 18:00, an Instagram Story 90 min after a Reel
when the video is 60 s or shorter. **Confirm the date and time with the owner.**

## 3. Schedule (owner, 23 Nov 2026: everything through Windsor; Metricool's free plan is over its limit)
- **YouTube:** Windsor `execute_action` youtube `upload_video`, account `112783`: `video_url`, `title`, `description`
  (the caption plus the pinned question), `tags`, `category_id` (1 Film & Animation, 23 Comedy, 27 Education),
  `made_for_kids` false, `privacy_status` "private" and `publish_at` (ISO with the Riga offset), so YouTube publishes it on
  time. Upload **one at a time**: parallel uploads get rate-limited. If it is still rate-limited, retry later; never claim it is scheduled.
- **Instagram:** Windsor instagram account `17841466758506102` has no scheduling, so set a one-shot wake-up at the slot
  (`send_later` with `at` "YYYY-MM-DDTHH:MM:00[Europe/Riga]") whose message holds the exact `create_video_post`
  (`video_url`, caption, `thumb_offset` for the cover, `share_to_feed` true; `trial_params` for a Trial Reel),
  `create_story` or `create_carousel_post` call, then `create_comment` with the pinned question.
- **TikTok and Pinterest:** Windsor cannot post to them. Use Metricool only if it is back under its limit; otherwise tell
  the owner and send the file and caption so they can post from the app.
- AI labels: Instagram and TikTok need the AI-generated declaration where the tool has one.

## 4. Record
Add the rows to `STATUS.md` (time, platform, title, file URL, the upload or wake-up id), commit and push.

Never edit or delete an already scheduled or live post without the owner asking.
