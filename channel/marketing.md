# Free growth playbook (owner's ask 22 Nov 2026: push the algorithm, no new videos)

What the algorithms reward: people watching to the end, rewatching, commenting, sharing and saving, then watching the next video
(session time). Everything here is free and uses videos that already exist.

## Claude does automatically
| Lever | How | When |
|---|---|---|
| Reply to every normal comment fast | `/yt-comments` through Windsor (YouTube) | daily 20:34 task, plus on request |
| Reel to Story reshare | Metricool Instagram STORY with the same video (videos up to 60 s), 90 min after the Reel | every Reel that fits 60 s |
| Pinned question comment | first comment on every YouTube post | every upload |
| Best hours only | YouTube 16:00, Instagram/TikTok 10:00, 12:00, 18:00 (Metricool best times) | every schedule |
| Keyword titles on new posts | vidIQ keyword check before scheduling (5 credits) | new uploads only |
| Pinterest video pins | Metricool, board "Dustlight" (907123618635179948), pin links to the YouTube video; pin each story the day after it is live, 15:00 or 21:00 Riga, at most 2 a day | every upload |
| Add videos to playlists | Windsor `add_video_to_playlist`, once the owner has created the playlists | after each upload |
| Instagram Trial Reels | Re-post an older live video as `TRIAL_REEL` (shown to non-followers first) with a new on-screen hook burned in for the first 3 s | Tue and Fri, 20:00 |
| Instagram Carousels | 6 to 8 stills (anim.py `STILLS` mode, then `pipeline/carousel.py`), 1080x1350, one caption line per slide, the twist on the last slide, posted as an Instagram POST with several images | Wed and Sun, 20:00 |

Rules: never edit or repost a published video without the owner's yes; no fake engagement, no follow-for-follow, no buying views.

## Owner, about 10 minutes once (YouTube Studio app, things no tool can do)
1. **Playlists:** create "The Lost Toy Room" (Parts 1 to 4 in order) and "Dustlight Stories" (every story). Then tell Claude, who adds the videos.
2. **Related video on every Short:** Studio, Short, Edit, "Related video": Lost Toy Room Part 1 points to Part 2 and so on; every other Short points to Vol. 1 once it is live (26 Nov). This is the strongest free session-time push.
3. **End screen on Vol. 1** after it publishes: subscribe button plus "best for viewer".
4. **Pin and heart:** heart every viewer comment (counts as engagement). Pin the best viewer answer over our question when one arrives.
5. **TikTok:** pin the 3 best videos to the top of the profile. Turn on Business account (free) for analytics.
6. **Instagram:** add each Reel to a Highlight ("Stories"), and use "Share to Story" with a poll or question sticker when you have a minute (stickers cannot be added through the API).
7. **Communities (by hand, follow each one's rules):** share a making-of still on r/blender or r/lowpoly (they like process posts, not channel links). Never spam links.

## Tracking
Each weekly `/yt-analytics` compares views per post with and without these levers.
