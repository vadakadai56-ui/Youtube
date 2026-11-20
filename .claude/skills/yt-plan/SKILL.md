---
name: yt-plan
description: Plan the publishing calendar for the coming week or two. Use when the owner asks "what's the plan this week", wants a content calendar, or there are gaps in the schedule.
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

## Output
A 7 or 14-day table: date, slot, video, stage (idea, script, voice, render, ready, scheduled), next action, blocker. Then the 3 most urgent actions with the skill for each. Save the table to `STATUS.md` under "Plan" once the owner agrees.
