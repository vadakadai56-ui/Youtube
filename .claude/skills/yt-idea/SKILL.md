---
name: yt-idea
description: Pitch new story ideas for the channel. Use when the owner asks for video ideas, "what should the next story be", or the pipeline has no approved script. Writes pitches to stories/ideas.md.
---
# /yt-idea: story pitches

## Inputs
Read `channel/channel-kit.md`, `stories/ideas.md` (do not re-pitch what is there), `STATUS.md` (what is live), and, if `/yt-analytics` has run, its latest notes in `STATUS.md` (what worked).

## What a Dustlight idea needs
- **One forgotten thing** at the centre (a toy, a cup, a swing, a letter, a habit).
- **A sad start with a heartwarming twist ending** (owner preference). The twist reframes the opening, it does not just add to it.
- **A one-line hook** that works as the first spoken sentence and as the title: concrete, a number or a time if possible, a question the viewer must have answered. "Every evening at six, a man pushes an empty swing."
- **Buildable** with the toolkit: `pipeline/scene.py` and `pipeline/world.py` have peg-doll characters, kitchens, streets, care homes, a toy room, snow, steam. Say which new sets or props an idea needs.
- 55 to 75 s narrated, or 2 to 4 parts for a series (hand off to `/yt-series`).
- Original. Never a retelling of a known film, book, viral video or another channel's story.

## Output
Pitch 3 ideas, each with: title, hook line, the twist (one sentence), the emotional payoff, sets and props needed (new vs existing), seasonal fit, single or series. Then a one-line recommendation.

When the owner picks one, append it to `stories/ideas.md` (or mark it chosen) and hand off to `/yt-script`.
