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
Follow the format of the trend the idea came from (see `channel/trends.md`). The default beats are the short-form story
structure from the owner's writing guide (23 Nov 2026), adapted from advice videos to stories:
1. **Hook, 0 to 3 s, 1 to 2 lines.** Use the guide's Four S's. **Subject:** who or what the story is about, said in the first line. **Stakes:** a reason to keep watching. **Simple:** plain words. **Superclear:** a punchy line that is easy to follow. Something strange and specific. No "Have you ever", no greeting, no channel name. Run `/yt-hook` if unsure.
2. **Lock-in zone, 2 to 3 lines.** Make the viewer sure the rest is worth it. Do it one of these ways: double down on the strange thing ("for one hundred and twelve days"), show others reacting (the whispering neighbours), or tease the feeling the ending will give. By line 3 the viewer has a question ("why does he push it?").
3. **Beat 1, 3 to 5 lines.** The first escalation. Each line is a picture the build can show.
4. **Re-hook 1, 1 line, around 20 to 25 s.** It resets attention by opening a new question: "Then one snowy night…", "Nobody ever looked across the road." It also goes on screen as `REHOOK` in `edit_config.py`.
5. **Beat 2, 3 to 5 lines.** The second escalation, or the turn. It gives the second "I didn't expect that" moment.
6. **Re-hook 2, 1 line, only in videos over 45 s.** It sets up the payoff ("This year, I finally saw it.").
7. **Payoff.** Deliver what the trend format promises (the reveal, the punchline, the twist). The last line echoes the first if it can ("Higher, Daddy.").
8. **Question to the viewer, 1 line.** It stands in for the guide's call to action. Ask something every viewer can answer about their own life. It goes in `END_LINES` and the pinned comment. Never ask them to like, follow or subscribe, and there is no lead magnet.
**Names:** every important character gets a name (rules and the list of names used in `channel/characters.md`). Pick them yourself, put each in the narration early, and add it to the list.
Cut every line that does not move the story ("reduce fluff"). Keep it as short as the story allows: the guide says 45 to 90 s, and never pad.

## Also write
- `stories/<slug>/` folder with `narration.txt`.
- A shot list draft in chat: one shot per line or two, what we see, 2 to 3 s each, with sets and props. `/yt-build` turns it into `shots.py`.
- A keyword list for yellow captions (the `KEY` set in `edit_config.py`): nouns, numbers, the emotional words.

## Gate
Show the full script and ask the owner to approve or change it. **Do not** generate voice or render anything until they say yes. Record "script approved <date>" in `STATUS.md` once they do.
