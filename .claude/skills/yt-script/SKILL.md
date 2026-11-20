---
name: yt-script
description: Write the narration script for a new Short. Use after an idea is chosen, or when the owner asks to write, rewrite or tighten a script. Produces stories/<slug>/narration.txt and waits for the owner's approval.
---
# /yt-script: narration script

## Format (match `stories/the-empty-swing/narration.txt`)
- One spoken line per row. Short sentences. 140 to 190 words total (about 55 to 75 s at George's pace).
- ElevenLabs v4 audio tags in square brackets, sparingly: `[softly]`, `[whispering]`, `[warmly]`, `[giggles]`. At most one per line, only where the delivery changes.
- Ellipses (`...`) for pauses. Numbers spelled out the way they should be spoken ("one hundred and twelve days").

## Structure
1. **Hook, 0 to 3 s.** The first line states something strange and specific. No "Have you ever", no greeting, no channel name. Run `/yt-hook` if unsure.
2. **Open loop.** By line 3 the viewer has a question ("why does he push it?").
3. **Escalate.** Every 2 or 3 lines add a detail that deepens the question (other people react, time passes, weather changes). Each line should be a picture the build can show.
4. **The turn.** One line that moves the camera somewhere new ("Nobody ever looked across the road.").
5. **The twist and payoff.** Reframe the opening. Warm, not saccharine.
6. **Last line echoes the first.** A callback the viewer can feel ("Higher, Daddy.").

## Also write
- `stories/<slug>/` folder with `narration.txt`.
- A shot list draft in chat: one shot per line or two, what we see, 2 to 3 s each, with sets and props. `/yt-build` turns it into `shots.py`.
- A keyword list for yellow captions (the `KEY` set in `edit_config.py`): nouns, numbers, the emotional words.

## Gate
Show the full script and ask the owner to approve or change it. **Do not** generate voice or render anything until they say yes. Record "script approved <date>" in `STATUS.md` once they do.
