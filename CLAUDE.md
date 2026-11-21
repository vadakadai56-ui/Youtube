# Dustlight YouTube channel

Read `README.md` (pipeline, rules) and `STATUS.md` (what is live and scheduled) before channel work.

## Every session
1. Check `channel/trends.md`. If it is missing, or its date is more than 7 days old, run `/yt-trends` before anything else and commit the result.
2. Otherwise, mention the top 3 trends from it in one line.
3. Then continue with the owner's request. With no specific request, run `/yt-channel`.

## Skills
The `/yt-*` skills in `.claude/skills/` run the channel. `/yt-channel` is the hub.

## Edit Kit (extra skills, added 21 Nov 2026)
41 third-party video skills (`/edit`, `/director`, `/sound`, `/qa`, `/video-clone`, `/blender-product-film`, ...). They are not in git.
In a fresh session, install them with `bash pipeline/install_editkit.sh` (add `--test` for the self-test).
For Dustlight videos the `/yt-*` skills come first: `/yt-build` builds, `/yt-qc` checks, `/yt-publish` publishes.
Use Edit Kit skills only when the owner asks for them or a `/yt-*` skill has no answer (for example a new look or a transition).
Never use the kit's paid services (Atlas Cloud, Upload-Post, Gemini) without asking.

