---
name: skill-finder
description: Find and run the right skill (or chain of skills) for the owner's request, searching every skill available to the account, not just this repo. Covers the repo's skills (yt-*, motion-design, real-sfx, real-sound, earshot), the account's enabled claude.ai skills (anthropic-skills:*, e.g. docs, pptx, canvas-design, ghost, deep-research), claude.ai built-in skills, and account skills not yet enabled. Use when the owner says "find the skill", "which skill", "/skill-finder", shares a prompt and wants Claude to pick the tool itself, when a request could match several skills, or after a new skill is installed. Ranks them, picks the best, and runs it without asking.
---

# skill-finder: pick the right skill and run it

The owner shares a prompt. Find the skill that fits it best, then use it. Don't ask which skill to use: that is this skill's job.

## 1. Shortlist from every source
1. Run:
   ```bash
   python3 .claude/skills/skill-finder/scripts/find.py "<the owner's request, verbatim>" --n 5
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

## 2. Decide
- Read the descriptions of the top candidates and pick the one whose stated purpose matches the request. If
  needed, read the top two SKILL.md files in full.
- Apply the routing rules below when skills overlap.
- If the request needs several steps, plan a chain (for example `yt-script` then `yt-voice` then `yt-build`).
- If no skill fits (the best one does not do what was asked), say so in one line and do the task directly.

## 3. Run
- Invoke the chosen skill with the Skill tool (name as in the table above), passing the owner's request as `args`.
  For a `built-in` skill, read its SKILL.md (and any file it points to) and follow it yourself. Then follow that skill's
  instructions exactly, including its gates (owner approval of scripts, confirming a slot before scheduling).
- For a chain, run one skill at a time and carry results forward. Stop at any gate that needs the owner.
- Tell the owner in one line which skill was chosen and why, e.g. "Using real-sound: full soundtrack with licensed
  recordings."

## Routing rules (Dustlight)

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
