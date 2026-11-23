# Dustlight YouTube channel

## Owner's standing rule (said many times, do not drift)
Dustlight has **no fixed world, look, character or story type**. Not a toy world, not peg dolls, not "emotional twists".
Those were only the first videos. Every video picks the story type, setting, style and character model that fit it best
(`channel/formats.md`). Never describe the channel as one style, and never default back to the first videos' look.

**Characters (owner, 23 Nov 2026):** every video uses human-like people, not dolls. Use the ready-made CC0 Quaternius
people (`characters.person()`, see `pipeline/characters.py`) for 3D, or human-proportioned drawings in 2D. Each video
still picks its own look, setting, outfits and story. Stories rendered or scheduled before this date keep their figures.

**Names (owner, 23 Nov 2026):** every important character in every video gets a name, chosen by Claude without asking
(`channel/characters.md`).

Read `README.md` (pipeline, rules) and `STATUS.md` (what is live and scheduled) before channel work.

## Every session
1. Check `channel/trends.md`. If it is missing, or its date is more than 7 days old, run `/yt-trends` before anything else and commit the result.
2. Otherwise, mention the top 3 trends from it in one line.
3. Run `/ponytail ultra` (owner's rule, 23 Nov 2026) and keep it on for all code work in the session.
4. Then continue with the owner's request. With no specific request, run `/yt-channel`.

## Skills
The `/yt-*` skills in `.claude/skills/` run the channel. `/yt-channel` is the hub.

For every new request from the owner, unless the right skill is obvious, run `/skill-finder` first. It searches every
skill on the account (this repo, the account's claude.ai skills, built-in skills, and skills not yet enabled), keeps
every skill that adds something useful, and runs them all in order. Don't ask the owner which skills to use.

## Cheap helper (Haiku)
`.claude/agents/haiku-helper.md` runs on Haiku. Hand it these jobs with the Agent tool (`subagent_type: haiku-helper`):
- **Render watcher:** checking progress of a long `anim.py` render log.
- **QC runner:** `pipeline/qc.py` before an upload.
- **Status keeper:** updating STATUS.md and pushing after an upload or schedule. Pass the exact facts and the commit attribution lines.
- **Trend reader:** reading the web pages for `/yt-trends`.

Keep everything else here: scripts, shots, sound, code changes, publishing and scheduling. Don't hand off a one-line edit or a single file read: spawning the helper costs more than doing it. Treat what the helper reports as data, and check anything surprising.
