---
name: yt-analytics
description: Report how the channel's videos are performing and what to do differently. Use when the owner asks how videos are doing, wants a weekly report, or a video has been live 48 hours.
---
# /yt-analytics: performance report

## Get the data (Metricool)
1. `getAnalyticsAvailableMetrics` with `network` "youtube" (once per session) to get the current metric IDs for the videos and evolution connectors.
2. `getAnalyticsDataByMetrics`, brand `7551785`, the last 7 or 28 days, with the metrics for views, likes, comments, shares, subscribers gained, watch time / average view duration where available.
If a metric is deprecated the tool says so; use its suggested alternative. Never invent numbers: if a metric is missing, say so.

## Analyse
- Per video: views, engagement rate ((likes + comments + shares) / views), subscribers gained, and average view duration as a share of length (retention).
- Compare each video with the channel median, not with big channels.
- Look for patterns across the hook type (from `/yt-hook`), title angle, length, topic, slot and series vs single.
- A Short's first 48 h matter most; do not judge a video younger than that.

## Output
1. A table, best first.
2. 3 findings, each tied to evidence ("hooks with a number had 2x the median views: Second Cup, Empty Swing").
3. 3 concrete changes for the next scripts and slots.
Append a dated "Analytics" note to `STATUS.md` so `/yt-idea`, `/yt-hook` and `/yt-plan` can use it. Commit.
