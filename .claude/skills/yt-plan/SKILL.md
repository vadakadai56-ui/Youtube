---
name: yt-plan
description: Plan the publishing calendar for the coming week or two, and auto-plan it (find the gaps, pick trends and formats, draft every script, line up the production steps). Use when the owner asks "what's the plan this week", "auto plan", wants a content calendar, when there are gaps in the schedule, or when the weekly auto-plan task fires.
---
# /yt-plan: content calendar

## Inputs
- `getScheduledPosts` (brand `7551785`, `Europe/Riga`) for the next 14 days.
- `STATUS.md` (in production, blocked), `stories/ideas.md`, the latest `/yt-analytics` notes.
- `getBestTimeToPostByNetwork` for youtube, one week at a time, if the owner wants data-driven slots. Otherwise the house slot is 16:00 Riga.

## Rules of thumb
- One Short a day is the target; consistency beats volume.
- A series goes out on consecutive slots or 2 h apart on one day (end cards must match: "PART 3 · NEXT").
- Run `/yt-trends` at the start of each plan. Put the trend with the fewest days left in the earliest slot it can be ready for.
- Seasonal stories land 1 to 3 weeks before the date (snow and Christmas stories in early December).
- Leave a production buffer: a video should be rendered and checked 24 h before its slot.
- Work back from each slot: script approved -4 days, voice -3, render -2, qc and schedule -1.

## Auto plan (owner asked for this on 22 Nov 2026)
Run the whole loop without being asked for each step, and stop only at the owner's gates.
1. **Gaps:** `getScheduledPosts` for the next 10 days. A day is a gap if it has no YouTube Short. Target: a new story every 2 days, plus Reels and TikToks of the same videos (YouTube 16:00, Instagram and TikTok 18:00 Riga unless `getBestTimeToPostByNetwork` says otherwise).
2. **Trends:** if `channel/trends.md` is older than 3 days, run `/yt-trends` (it also picks the style for each top trend).
3. **Ideas:** fill each gap with an idea: rotate the formats in `channel/formats.md` (no two of the same format in a row), take scripted-but-unbuilt ideas from `stories/ideas.md` first, and put the trend with the fewest days left in the earliest slot that can be ready in time.
4. **Scripts:** run `/yt-script` for every gap in the next 7 days and write each `narration.txt`.
5. **One approval:** show the owner the whole week in one message: the calendar table, then each script with its format and style recipe. Ask them to approve all, or name the ones to change. Do not voice or render anything before they approve.
6. **Production after approval:** for each approved script, in slot order: `/yt-voice` (confirm the credit cost once for the whole batch), `/yt-build` (render in batches under 3 h, one story at a time), `/yt-qc`, then `/yt-title` and `/yt-publish`. Uploads go through `pipeline/publish_github.py` (Dustlight-Files). Send the owner a phone preview of each finished video before it is scheduled; if they do not object before its upload step, schedule it.
7. **Report:** update the plan table in `STATUS.md` and tell the owner what is scheduled and what is next.

## Output
A 7 or 14-day table: date, slot, video, stage (idea, script, voice, render, ready, scheduled), next action, blocker. Then the 3 most urgent actions with the skill for each. Save the table to `STATUS.md` under "Plan" once the owner agrees.
