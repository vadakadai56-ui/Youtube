---
name: yt-idea
description: Pitch new video ideas built on what is trending right now. Use when the owner asks for video ideas, "what should the next story be", or the pipeline has no approved script. Writes pitches to stories/ideas.md.
---
# /yt-idea: story pitches

## Inputs
- `channel/trends.md`. If it is missing or older than 7 days, run `/yt-trends` first. Ideas come from the current top trends.
- `channel/channel-kit.md`, `stories/ideas.md` (do not re-pitch what is there), `STATUS.md` (what is live), and the latest `/yt-analytics` notes (what worked here).

## What an idea needs
- **A live trend** from `channel/trends.md`: name it, its evidence date and how many days it has left. The video must be live before the trend fades.
- **The trend's own shape.** Use the format and emotion that is getting views now (funny, shocking, satisfying, mystery, wholesome, scary), not a fixed house mood.
- **A one-line hook** that works as the first spoken sentence and as the title: concrete, a number or a time if possible, a question the viewer must have answered. "Every evening at six, a man pushes an empty swing."
- **Any subject.** The channel is no longer tied to toys or "forgotten things". Choose whatever has the most engagement potential. Say which sets, characters and props the build needs: reuse what is in `pipeline/scene.py` and `pipeline/world.py`, and list anything new.
- 55 to 75 s narrated, or 2 to 4 parts for a series (hand off to `/yt-series`).
- Original. Never a retelling of a known film, book, viral video or another channel's story.

## Output
Pitch 3 ideas from 3 different trends, each with: the trend and its days left, title, hook line, the ending or payoff (one sentence), sets and props needed (new vs existing), seasonal fit, single or series. Rank them by engagement potential (the trend's Engagement score first, then momentum and days left) and recommend one.

When the owner picks one, append it to `stories/ideas.md` (or mark it chosen) and hand off to `/yt-script`.
