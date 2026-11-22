---
name: yt-publish
description: Upload a finished, checked video to Dropbox and schedule it on YouTube through Metricool. Use when a video has passed /yt-qc and has a title. Confirms the slot with the owner before scheduling.
---
# /yt-publish: upload and schedule

## Preconditions
`/yt-qc` passed, `/yt-title` approved. Check `getScheduledPosts` so you do not double-book a slot.

## 1. Dropbox
```bash
python3 pipeline/publish.py out/<slug>.mp4 /Youtube/<slug>.mp4
```
Prints a public `dl=1` link. The Dropbox token is a short-lived network secret injected by the proxy; if the upload fails with 401, tell the owner the token expired and needs renewing in the environment's network secrets. Never ask for it in chat.

## 2. Slot
Default: the next free day at 16:00 Europe/Riga (series parts 2 h apart). If the owner wants data, `getBestTimeToPostByNetwork` for youtube over the coming week. **Confirm the date and time with the owner.**

## 3. Schedule (Metricool `createScheduledPost`)
- `blogId` `7551785`, `date` with the Riga offset, `publicationDate` `{dateTime, timezone: "Europe/Riga"}`
- `providers` `[{"network":"youtube"}]`, `media` `[<dropbox link>]`, `text` = the description
- `youtubeData`: `title`, `type` "short", `privacy` "public", `category` "FILM_ANIMATION", `madeForKids` false, `tags`, `isAiGeneratedContent` as decided in `/yt-qc`
- `firstCommentText`: the pinned question
- Cover: `videoCoverMilliseconds` or `videoThumbnailUrl` from `/yt-thumbnail`, only if it applies
- `autoPublish` true, `draft` false

## 4. Record
Add the row to `STATUS.md` (time, title, Dropbox path, Metricool post id, planner URL), commit, and push.

Never edit or delete an already scheduled or live post without the owner asking.


## Upload route (from 22 Nov 2026)
Use `python3 pipeline/publish_github.py out/<slug>.mp4 <slug>.mp4` and give Metricool the printed raw.githubusercontent.com URL. Attach `vadakadai56-ui/Dustlight-Files` (push) and clone it to `/home/user/dustlight-files` first if it is missing. Dropbox (`publish.py`) is the fallback only.
