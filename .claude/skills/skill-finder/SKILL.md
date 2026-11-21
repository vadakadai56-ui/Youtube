---
name: skill-finder
description: Find and run the right skill (or chain of skills) for the owner's request, searching every skill available to the account, not just this repo. Covers the repo's skills (yt-*, motion-design, real-sfx, real-sound, earshot), the account's enabled claude.ai skills (anthropic-skills:*, e.g. docs, pptx, canvas-design, ghost, deep-research), claude.ai built-in skills, and account skills not yet enabled. Use when the owner says "find the skill", "which skill", "/skill-finder", shares a prompt and wants Claude to pick the tool itself, when a request could match several skills, or after a new skill is installed. Ranks them, keeps every skill that adds something useful, and runs all of them in a sensible order without asking.
---

# skill-finder: find every useful skill and run them all

The owner shares a prompt. Find **every** skill that adds something useful to it, not only the best match, and run them
all. Don't ask which skills to use: that is this skill's job.

## 1. Shortlist from every source
1. Run:
   ```bash
   python3 .claude/skills/skill-finder/scripts/find.py "<the owner's request, verbatim>" --useful
   ```
   It ranks every SKILL.md on disk by how well its name, description and instructions match the words of the request:

   | Source label | Where | How to run it |
   |---|---|---|
   | `repo` | this repo's `.claude/skills/` | Skill tool, `skill: NAME` |
   | `account` | the account's enabled claude.ai skills, synced to `~/.claude/skills/synced/` | Skill tool, `skill: anthropic-skills:NAME` |
   | `user` | `~/.claude/skills/` | Skill tool, `skill: NAME` |
   | `built-in`, `built-in example` | claude.ai's own skills in `/mnt/skills/` (not loaded as tools here) | Read the SKILL.md and follow it step by step |

   It is a word match, not understanding: treat the list as candidates, not as the answer.
2. Also check the skills in this session's available-skills list. Plugin skills there may not be on disk.
3. If nothing on the shortlist really fits, search the account for skills that are not enabled. Load
   `SearchSkills` with ToolSearch, then call it with 2 to 4 keyword phrases from the request. A good match that is not
   enabled cannot be run yet: show it with `SuggestSkills` (or name it) and tell the owner to enable it, then do the task
   the best available way meanwhile.

## 2. Decide: keep every useful skill
`--useful` lists every skill that scores at least 35% of the top match (up to 12). For each one, ask: does this skill
add something real to the result? Keep it if it does:
- **The main skill** that does the task.
- **Skills that improve it:** a hook or title skill for a script, a trends check before ideas, a cover for a video,
  a style or theme skill for a design, the writing-style skill for text the owner sends as their own.
- **Skills that check it:** `yt-qc` before an upload, earshot listening on a mix, a critique step.
- **Skills that finish it:** credits, the status update, a phone-size copy.

Drop a candidate only when it does not apply (a word match with no real use, such as `pptx` for a "thumbnail"), when
another kept skill already does the same job (keep the one the routing table names), or when it would publish,
schedule, spend credits or message someone without the owner asking.

Then put the kept skills in order: research, then create, then improve, then check, then finish. Example for "make the
next video": `yt-trends` (if stale), `yt-idea`, `yt-hook`, `yt-script` (stop for approval), `yt-voice`, `yt-build`,
`real-sfx` / `real-sound`, `yt-qc`, `yt-thumbnail`, `yt-title`, `yt-publish` (stop to confirm the slot).

If no skill fits at all, say so in one line and do the task directly.

## 3. Run
- Before starting, list the plan in one line, e.g. "Using yt-hook, yt-script, then yt-title."
- Run every kept skill, one at a time, in that order. Invoke each with the Skill tool (name as in the table above), passing the owner's request as `args`.
  For a `built-in` skill, read its SKILL.md (and any file it points to) and follow it yourself. Then follow that skill's
  instructions exactly, including its gates (owner approval of scripts, confirming a slot before scheduling).
- Carry each result forward into the next skill. Stop at any gate that needs the owner (script approval, the
  posting slot, spending credits), and continue the rest of the plan after they answer.
- At the end, report in one short table which skills ran and what each added.

## Routing rules (Dustlight)

When two skills do the same job, keep the one named here. Skills that do different jobs are all kept.

| Request is about | Use | Not |
|---|---|---|
| Story ideas, what to make next | `yt-idea` (after `yt-trends` if trends.md is older than 7 days) | `yt-channel` unless they ask for the overview |
| Writing or rewriting narration | `yt-script` | `yt-idea` |
| A multi-part story | `yt-series` | |
| Opening line only | `yt-hook` | |
| Narration audio, word timings | `yt-voice` | |
| Rendering the 3D story video | `yt-build` | `motion-design` |
| Checking a finished video | `yt-qc` | |
| Title, description, tags, pinned comment | `yt-title` | |
| Cover frame or thumbnail | `yt-thumbnail` | |
| Upload and schedule | `yt-publish` | |
| Calendar for the week | `yt-plan` | |
| Views, performance | `yt-analytics` | |
| Replying to comments | `yt-comments` | |
| "Run my channel", what's next overall | `yt-channel` | |
| Logo reveal, channel trailer, motion graphic, brand animation (8 to 20 s) | `motion-design` | `yt-build` |
| Full soundtrack for a finished video from licensed recordings | `real-sound` | |
| Sound effects placed on an existing video's moments | `real-sfx` | |
| One specific sound (a footstep, a swing creak, a fire bed), or "how does this sound" | `earshot` | |
| Finding free sounds or images with licences | `pipeline/openverse.py` (README), no skill | |
| A document (plan, report, letter, proposal) | `anthropic-skills:docs` | `docx` unless they name Word |
| A Word file, deck file, spreadsheet file, PDF | `anthropic-skills:docx` / `pptx` / `xlsx` / `pdf` | |
| A poster, banner, static artwork | `anthropic-skills:canvas-design` | |
| Text the owner sends as their own (emails, posts, sponsor pitches) | `anthropic-skills:ghost` | |
| Research across many sources into a report | `anthropic-skills:deep-research` | `yt-trends` (that is only Shorts trends) |
| Understanding how something works | `anthropic-skills:learn` | |
| Making or improving a skill | `anthropic-skills:skill-creator` | |
| Short replies | `anthropic-skills:caveman` (when the owner asks) | |

Sound skills, in one line: `earshot` makes or listens to single sounds, `real-sfx` places effects on a video's
moments, `real-sound` runs the whole soundtrack workflow (and calls earshot for listening).

## Keep this skill current
When a new skill is installed, add a row to the routing table if it overlaps an existing one, and commit.
