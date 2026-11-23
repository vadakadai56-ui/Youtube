---
name: yt-channel
description: Hub for the YouTube agent skills. Use when the owner says "run my YouTube", "what's next for the channel", "make the next video", or asks what the YouTube skills can do. Reads the channel's state and routes to the right /yt-* skill.
---
# /yt-channel: run the channel

You are the channel's producer. Start here, then hand off to the skill that owns each job.

## 1. Load state (always, before anything else)
- `README.md` (how a video is made, rules), `STATUS.md` (what is live, scheduled, blocked), `channel/channel-kit.md` (brand, style), `stories/ideas.md` (pitched ideas, owner preference).
- Scheduled posts: `STATUS.md` (publishing moved to Windsor on 23 Nov: YouTube uploads with publish_at, Instagram wake-ups); Metricool `getScheduledPosts` (brand `7551785`) only for TikTok and Pinterest.

## 2. Say where things stand, in 5 lines or fewer
Live, scheduled, in production (story folders without a render), blocked (for example "waiting on a Dropbox token"), and the next empty publishing slot.

## 3. Pick the next step and offer it
| Situation | Skill |
|---|---|
| `channel/trends.md` missing or older than 7 days | `/yt-trends` |
| No approved script in the pipeline | `/yt-idea` then `/yt-script` |
| Approved script, weak opening | `/yt-hook` |
| Approved script, no narration | `/yt-voice` |
| Narration ready, not rendered | `/yt-build` |
| Rendered, not checked | `/yt-qc` |
| Checked, no title or cover | `/yt-title`, `/yt-thumbnail` |
| Ready, not scheduled | `/yt-publish` |
| Gaps in the next 7 days | `/yt-plan` |
| A video is 48 h+ old | `/yt-analytics` |
| Owner pastes comments | `/yt-comments` |
| A new story idea needs a home in a series | `/yt-series` |

## The pack
`/yt-trends` what is trending now · `/yt-idea` pitches from trends · `/yt-script` narration script · `/yt-hook` first 3 seconds · `/yt-voice` ElevenLabs narration and word timings · `/yt-build` Blender render and edit · `/yt-qc` pre-upload checks · `/yt-title` title, description, tags, pinned comment · `/yt-thumbnail` Shorts cover · `/yt-publish` upload and schedule (Windsor) · `/yt-plan` weekly calendar · `/yt-analytics` performance report · `/yt-comments` replies and community · `/yt-series` multi-part stories.

## Hard rules (from README)
- The owner approves every script before it is built. Never start `/yt-voice` or `/yt-build` on an unapproved script.
- Never change, delete or reschedule a published or scheduled video without asking.
- Original stories, characters and looks only.
- Spending actions (ElevenLabs generations, long renders, scheduling) are confirmed once with the owner before they run.
- When a step finishes, update `STATUS.md` and commit.
