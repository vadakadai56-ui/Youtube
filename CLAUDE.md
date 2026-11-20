# Dustlight YouTube channel

Read `README.md` (pipeline, rules) and `STATUS.md` (what is live and scheduled) before channel work.

## Every session
1. Check `channel/trends.md`. If it is missing, or its date is more than 7 days old, run `/yt-trends` before anything else and commit the result.
2. Otherwise, mention the top 3 trends from it in one line.
3. Then continue with the owner's request. With no specific request, run `/yt-channel`.

## Skills
The `/yt-*` skills in `.claude/skills/` run the channel. `/yt-channel` is the hub.
