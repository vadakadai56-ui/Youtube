---
name: yt-trends
description: Find what is trending on YouTube Shorts right now (topics, formats, hooks, sounds) and rank it by view potential for this channel. Use before /yt-idea, when the owner asks "what's trending", or weekly in /yt-plan. Writes channel/trends.md.
---
# /yt-trends: what is getting views right now

Trends move in days. Always research live; never pitch from memory or from a trends file older than 7 days.

## 1. Research (live)
- Load `WebSearch` with ToolSearch. Run several searches in one turn, `mode` "extended":
  - "trending YouTube Shorts this week <month year>"
  - "viral Shorts format <month year>", "TikTok trend <month year>" (TikTok trends reach Shorts within days)
  - "Google Trends rising searches this week", plus upcoming dates (holidays, launches, events in the next 14 days)
  - Niche: "viral animated story Shorts <month year>", "viral 3D animation Shorts"
- Use the `web-fetch` agent to read the best 3 to 5 results. Note each source's publish date. Drop anything older than 14 days.
- Metricool, if useful: `getAnalyticsAvailableMetrics` for youtube with connector "competitors", then compare competitor Shorts.
- Own data: the latest `/yt-analytics` note in `STATUS.md`. A trend that matches what already worked here ranks higher.

## 2. Separate the kinds of trend
- **Topic**: an event, meme, character type, question everyone is asking.
- **Format**: a structure (POV, "things that…", countdown, "day 1 vs day 100", reveal at the end, ask-the-viewer, mini-mystery).
- **Hook pattern**: an opening line shape that is everywhere this week.
- **Sound or music**: note it, but Dustlight synthesizes its own sound. Never use copyrighted audio.

## 3. Score each trend 1 to 5
- **Momentum**: rising now, not peaked (sources in the last 7 days, growing counts).
- **Shelf life**: days left before it is stale (a 3-day build needs 5+ days).
- **Fit**: can the Blender toy-world pipeline make it in 2 to 3 days?
- **Originality room**: can we make our own version, not a copy?
- **Safety**: no tragedy-baiting, no real people's likeness, no brands, no misinformation, nothing aimed at kids for clicks.

## 4. Output
Write `channel/trends.md`: date, a ranked table (trend, kind, evidence with source and date, scores, days left), and the top 3 with one line on how Dustlight would do each. Commit. Then hand off to `/yt-idea`.

## Rules
- Ride the trend; do not copy a video. Original script, characters, scenes and sound every time. Copying another creator's video risks copyright claims and YouTube's reused-content demonetization.
- Never fake numbers. If you cannot find evidence, say the trend is unconfirmed.
