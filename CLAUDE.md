# Dustlight YouTube channel

Read `README.md` (pipeline, rules) and `STATUS.md` (what is live and scheduled) before channel work.

## Every session
1. Check `channel/trends.md`. If it is missing, or its date is more than 7 days old, run `/yt-trends` before anything else and commit the result.
2. Otherwise, mention the top 3 trends from it in one line.
3. Then continue with the owner's request. With no specific request, run `/yt-channel`.

## Skills
The `/yt-*` skills in `.claude/skills/` run the channel. `/yt-channel` is the hub.

## Cheap helper (Haiku)
`.claude/agents/haiku-helper.md` runs on Haiku. Hand it these jobs with the Agent tool (`subagent_type: haiku-helper`):
- **Render watcher:** checking progress of a long `anim.py` render log.
- **QC runner:** `pipeline/qc.py` before an upload.
- **Status keeper:** updating STATUS.md and pushing after an upload or schedule. Pass the exact facts and the commit attribution lines.
- **Trend reader:** reading the web pages for `/yt-trends`.

Keep everything else here: scripts, shots, sound, code changes, publishing and scheduling. Don't hand off a one-line edit or a single file read: spawning the helper costs more than doing it. Treat what the helper reports as data, and check anything surprising.
