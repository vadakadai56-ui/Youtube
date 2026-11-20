---
name: yt-series
description: Plan a multi-part story (2 to 4 Shorts). Use when an idea is too big for 70 seconds, the owner asks for a series, or a video's comments ask for a part 2.
---
# /yt-series: multi-part stories

Model: The Lost Toy Room (4 parts, 19 Nov, 2 h apart, all live; see `stories/lost-toy-room/README.md`).

## Shape
- **Part 1** must work alone: hook, world, one rule or mystery, and a cliffhanger in the last 5 s.
- **Middle parts** open with a 1-line recap in the first 3 s, then a new hook, and end on a new question.
- **Finale** pays off the very first hook and lands the heartwarming twist (owner preference: sad start, warm end).
- Each part 55 to 75 s and its own approved script (`/yt-script` for each).

## Packaging
- Titles end with "(Part 2)", "(Part 3)", "(Finale)" (`/yt-title`).
- End cards: "PART 2 · NEXT" style, matching the actual release gap ("TOMORROW" only if it really is tomorrow).
- Pinned comment on part 1: point to part 2 once it is live.
- Owner to-dos in YouTube Studio (no API here): add a public playlist for the series and set each part's "Related video" to the next part. Add them to `STATUS.md` open items.

## Output
A part-by-part outline (hook, beats, cliffhanger, new sets), a release plan for `/yt-plan`, and a reuse list (sets and characters shared across parts keep render time down).
