# Status (19 Nov 2026)

## Published / scheduled (YouTube via Metricool)
| Time (Riga) | Video | Dropbox file |
|---|---|---|
| 19 Nov 16:00 ✅ [live](https://www.youtube.com/shorts/8DlR4Mf9Mx4) | The Lost Toy Room, Part 1: "Every toy you lost is waiting in this room" | `/Youtube/lost-toy-room-part1.mp4` |
| 19 Nov 18:20 ✅ [live](https://www.youtube.com/shorts/kfaWF7kWvTY) | Part 2: "The lost toy room got a phone call… (Part 2)" | `/Youtube/lost-toy-room-part2.mp4` |
| 19 Nov 20:20 ✅ [live](https://www.youtube.com/shorts/jG9lEuLbcAE) | Part 3: "She forgot everyone… except this song (Part 3)" | `/Youtube/lost-toy-room-part3.mp4` |
| 19 Nov 22:20 ✅ [live](https://www.youtube.com/shorts/9re0uEIczkI) | Part 4: "The lost toy room's last rule (Finale)" | `/Youtube/lost-toy-room-part4-finale.mp4` |

Parts 2 and 3 end cards say "PART 3 · NEXT" and "THE FINALE · NEXT", because the parts were released 2 hours apart.

## Scheduled
- **The Second Cup**: 20 Nov 2026 16:00 Riga (Metricool post uuid -1017785154483633580). Source: Dropbox `/Youtube/Video Nov 20 2026, 1 09 42 AM.mp4` (the 52 MB phone copy, 68.6 s).
  - Title: "He makes two cups of tea every morning. Nobody knows why."
  - First comment: "Who would you make the second cup for? 👇"

- **The Empty Swing** ✅ live: [YouTube](https://www.youtube.com/shorts/0V0MVYXim_I) 16:00, [Instagram](https://www.instagram.com/reel/DgAnq_KDTA6/) 18:00, [TikTok](https://www.tiktok.com/@divine.773/video/7710656172256283905) 18:00. Scheduled as 21 Nov 2026 16:00 Riga (Metricool post uuid 8077661360486368967, id 436256054). Source: Dropbox `/Youtube/the-empty-swing.mp4` (full 1080p, 71.7 s, -14.4 LUFS, QC passed). Narration backup: `/Dustlight-backup/the-empty-swing-narration.mp3`.
  - Title: "Every evening at 6, he pushes an empty swing."
  - First comment: "Who would you push the swing for? 👇"

- **The Extra Plate**: script approved 21 Nov 2026 (`stories/the-extra-plate/narration.txt`, 170 words). Rendered 21 Nov: `out/the-extra-plate.mp4` (77.4 s with end card, -14.7 LUFS, true peak -1.4 dBTP, QC ready). **Scheduled 22 Nov:** YouTube 25 Nov 16:00 (uuid -8511954960419764922), Instagram 18:00 (uuid 1428552922414664655), TikTok 18:00 (uuid -7868610168081003976). Media: [Dustlight-Files](https://raw.githubusercontent.com/vadakadai56-ui/Dustlight-Files/main/videos/the-extra-plate.mp4) (76.5 MB 1080p). Title "Every Thanksgiving, she sets one extra plate.", first comment "Who would you set an extra plate for? 👇".

- **A Normal Night** (format 2, anticlimax POV): script approved 21 Nov 2026, voiced (Arthur, deadpan), rendered `out/a-normal-night.mp4`. **Scheduled 22 Nov:** YouTube 23 Nov 16:00 (uuid 5231118787503540207), Instagram 18:00 (uuid 6687967837374663258), TikTok 18:00 (uuid -4573281437109433456). Media: [Dustlight-Files](https://raw.githubusercontent.com/vadakadai56-ui/Dustlight-Files/main/videos/a-normal-night.mp4) (59.1 MB). Title "In my town, a normal night is terrifying.", first comment "What's the scariest normal thing that ever happened in your house? 👇". No #nothingeverhappens / #chud tags.

- **Dustlight Stories Vol. 1** (long-form, 16:9, 9.1 min so mid-rolls are possible once monetized): The Extra Plate, Lost Toy Room (full), The Second Cup, The Empty Swing, The Ice Hotel, A Normal Night. **Scheduled 22 Nov:** YouTube **Thu 26 Nov (Thanksgiving) 16:00** as a normal video (uuid 4801095102161699213), title "6 Animated Stories for Thanksgiving | Dustlight Stories Vol. 1", chapters in the description. Media: [Dustlight-Files](https://raw.githubusercontent.com/vadakadai56-ui/Dustlight-Files/main/videos/dustlight-stories-vol1.mp4) (71.8 MB, 1080p, 1.2 Mbps cap). Full-quality master `out/dustlight-stories-vol1.mp4` (not committed).

- **Huss Huss** (Trend Short, first video with the new blocky characters): script approved 22 Nov 2026 (`stories/huss-huss/narration.txt`, 48 words). Voiced 22 Nov with ElevenLabs "Lip" (DGqQmo441r9TwJq0migX), 25.9 s, 284 credits; mp3 at `audio/huss-huss.mp3` (not committed). Rendering. Planned trend slot Tue 24 Nov: YouTube 10:00, Instagram/TikTok 12:00.

## Plan 23 to 29 Nov 2026 (weekly auto plan; all 10 scripts approved by the owner 22 Nov 2026)
All 10 voiced 22 Nov (mp3s in `audio/`, not committed; ElevenLabs history keeps them): Same Window 28.7 s (George), Thanksgiving Timeline 29.4, One Word 20.2, Number Nine 21.3, A Random Tuesday 17.8, First Snow 18.7, Once a Day 49.5 (all Lip), The Sneeze 59.8 (Sheldon ujcXHLWtGPYXnqBoMBgg), Memory Timer 81.4 (Arthur), The Last Door 59.3 (George). About 5,600 credits.
Built 22 Nov (shots previewed and fixed, edit configs written): all 10. Renders run one at a time in a detached queue (a machine restart kills it: check `frames/queue.log` and relaunch; a check-in task does this every few hours) (`pipeline/render_queue.sh`, logs in the scratchpad `frames/` folder): Same Window, The Sneeze, Thanksgiving Timeline, One Word, Number Nine, Once a Day, A Random Tuesday, Memory Timer, First Snow, The Last Door. New character models: bean (Sneeze, Once a Day, Memory Timer), clay (Number Nine, First Snow, The Last Door), blocky (huss family).
| Day | Trend slot (YT 10:00, IG/TT 12:00) | Story slot (YT 16:00, IG/TT 18:00) |
|---|---|---|
| Mon 23 | Same Window (scheduled: YT 10:00 uuid -3767051276132791506, IG 12:00 -6233062086669546750, TT 12:00 -6172103828770634222, IG Story 13:30 2165347083173970756) | A Normal Night (scheduled) |
| Tue 24 | Huss Huss (scheduled: YT 10:00 uuid -7079588557884931580, IG 12:00 -6704071585776185936, TT 12:00 2712745511836271821) | The Sneeze (approved) |
| Wed 25 | Thanksgiving Timeline (approved) | The Extra Plate (scheduled) |
| Thu 26 | One Word (approved) | Vol. 1 long-form (scheduled) |
| Fri 27 | Number Nine (approved) | Once a Day (approved) |
| Sat 28 | A Random Tuesday (approved) | Memory Timer, format 6 (approved) |
| Sun 29 | First Snow (approved) | The Last Door (approved) |

## Instagram Reels (@dustlightstories, via Metricool, AI label on)
| Time (Riga) | Reel | Metricool uuid |
|---|---|---|
| 21 Nov 18:00 | The Empty Swing | -5308225935741598034 |
| 22 Nov 10:00 | The Second Cup | 6902143095151608622 |
| 22 Nov 18:00 | Ice hotel ("Every winter, they build a hotel out of a frozen river."); YouTube at 16:00 | -7028284931705059524 |
| 22 Nov 19:30 | Story reshare: Ice hotel | -4584513616194157131 |
| 23 Nov 18:00 | A Normal Night (YouTube at 16:00) | 6687967837374663258 |
| 23 Nov 19:30 | Story reshare: A Normal Night | 2995832477754606894 |
| 25 Nov 18:00 | The Extra Plate (YouTube at 16:00) | 1428552922414664655 |
Lost Toy Room is not posted to Instagram (owner's choice, 21 Nov). Times follow Metricool's best Instagram hours (10:00 and 18:00 Riga); YouTube stays at 16:00, its best hour.

## TikTok (@dustlight00, formerly @divine.773, via Metricool, AI label on)
| Time (Riga) | Video | Metricool uuid |
|---|---|---|
| 21 Nov 18:00 | The Empty Swing | -4855298876224879780 |
| 22 Nov 10:00 | The Second Cup | 2666965360092859592 |
| 22 Nov 18:00 | Ice hotel | -2938055666207273225 |
| 23 Nov 18:00 | A Normal Night | -4573281437109433456 |
| 25 Nov 18:00 | The Extra Plate | -7868610168081003976 |
TikTok connected 21 Nov 2026 as @divine.773, renamed @dustlight00 the same day (next rename allowed after 30 days). The account already had 1,197 followers from older content. TikTok's best hours match Instagram's (10:00, 12:00, 18:00).

## Pinterest (board "Dustlight", id 907123618635179948, via Metricool; connected 22 Nov 2026)
Each pin links to its YouTube video. Times 15:00 and 21:00 Riga (Metricool has no Pinterest best-time data).
| Time (Riga) | Pin | Metricool uuid |
|---|---|---|
| 22 Nov 21:00 | The Empty Swing | 1301149360842755431 |
| 23 Nov 15:00 | The Second Cup | 2056834738756208093 |
| 23 Nov 21:00 | Lost Toy Room Part 1 | 7649888654424949990 |
| 24 Nov 15:00 | Lost Toy Room Part 2 | 897888025129141537 |
| 24 Nov 21:00 | Lost Toy Room Part 3 | -3699234649175078871 |
| 25 Nov 15:00 | Lost Toy Room Part 4 | -5808200110130574909 |
To pin once live (need their YouTube ids): Ice hotel (live 22 Nov 16:00), A Normal Night (23 Nov), The Extra Plate (25 Nov), Vol. 1 (26 Nov).

## Rebuilt after the 19 Nov reset (done, tested end to end)
- `pipeline/` toolkit, renderer, aligner, editor and Dropbox publisher. `stories/the-second-cup/` is fully re-renderable.
- Not rebuilt: the Lost Toy Room per-shot camera files (Parts 1 to 4 are finished and live). The set, toys, Bun-Bun, door and silhouettes are in `scene.py`.
- Lost for good: the narration mp3s (ElevenLabs history has them), the rendered frames, and the full-quality "The Second Cup" (the phone copy exists).

## Source copies in Metricool (public static links, reachable from sessions)
Lost Toy Room: Part 1 `7551785-file-2041223862239218930.mp4`, Part 2 `...-14081602158670977575.mp4`, Part 3 `...-13700619248896578994.mp4`, Part 4 `...-7689693484360900601.mp4`; The Empty Swing `...-9944081293849703551.mp4`; Ice hotel `...-14484001482312721434.mp4`; The Second Cup `...-12646092096430351264.mp4`. Prefix: `https://static.metricool.com/planner/202611/`. Download with curl (ffmpeg does not use the proxy).

## Automation
- **Weekly auto plan:** scheduled task "Dustlight weekly auto plan" (trig_01BsS8QAXWsFZhnnJvJ8C6cA), every Sunday 11:33 Riga, first run 22 Nov 2026. It fires into this session and runs `/yt-plan` auto plan mode: gaps, trends, formats, all scripts, then one approval message. Nothing is voiced, rendered or scheduled before the owner approves.
- **Daily comments:** scheduled task "Dustlight daily comments" (trig_017inMtZq6y2ChGEFBKLLo6A), every day 20:34 Riga. `/yt-comments` auto-replies to normal YouTube comments through Windsor.ai (trial plan), holds spam, asks the owner about anything sensitive. Log: `channel/comment-log.md`.
- **Tools:** Metricool publishes (YouTube, Instagram, TikTok, best times). vidIQ (free plan, 150 credits a month, 5 per research or analytics call) is connected to Dustlight YouTube, Instagram @dustlightstories and TikTok @dustlight00: trends, outliers, keywords, own-channel analytics, Instagram insights, reading Instagram and TikTok comments. Never publish from vidIQ. Windsor.ai handles comments and per-video YouTube analytics (Instagram can be added in Windsor; TikTok has no comment actions there).
- **Uploads:** `pipeline/publish_github.py` through the public repo Dustlight-Files. No tokens.

- **Render speed:** about 10 to 20 s per frame on 4 CPU cores with no GPU (about 5 h per story). Owner plans to rent cloud GPU time once the channel earns (10 to 30 times faster). Free option offered but not applied yet: 6 fps for calm shots, ES 8, cheaper shadows (about half the time).

## Open items
- Instagram: connected in Metricool on 21 Nov 2026 as **@dustlightstories** (YouTube is @the.dustlight.stories). Reels can now be scheduled with the YouTube posts.
- Channel: create the "The Lost Toy Room" playlist (public) and set "Related video" on each part to the next part.
- Old ball-sim Shorts were set to private by the owner.

## Analytics (21 Nov 2026, from YouTube Studio screenshot, last 28 days)
- Channel: 8.2K views, 38.8 watch hours, 18 subscribers. Daily views peaked at about 2.7K on 20 Nov (story launch).
- Top Shorts: Scissors was down to 1 (old ball-sim) 1.3K over ~6 days; Last ball standing (ball-sim) 1.2K over ~6 days; Lost Toy Room Part 1 1.1K over ~2 days; **The Second Cup 1.1K in ~1 day**; Lost Toy Room Part 3 1.0K over ~2 days.
- Verdict: the story format gets 2 to 5 times more views per day than the ball-sims and converts subscribers (+13 in 2 days vs +4 from ~3,400 ball-sim views). Single standalone stories with a "strange daily routine" hook (The Second Cup) beat series parts. Make more standalone stories.
- Monetization page still showed data as of 16 Nov (0 qualified Shorts views). Owner to turn on 2-Step Verification.

## Analytics (20 Nov 2026, Metricool, 23 Oct to 20 Nov)
- Per-video data: none returned (connectors "videos published in range" and "all videos" are empty). No per-video ranking possible yet.
- Channel views: 1,118 on 16 Nov and 1,202 on 17 Nov; 1 to 27 a day before that. No view data yet after 17 Nov (YouTube reporting lag).
- Those spikes came before the Lost Toy Room went live (19 Nov), so they came from older uploads, probably the ball-sim Shorts that are now private. Unconfirmed.
- Subscribers: 0 until 16 Nov, then 2 (17 Nov), 4 (18 Nov), 12 (19 Nov). 0 lost.
- Lost Toy Room (19 Nov) is under 48 h old; The Second Cup goes live today. Re-run /yt-analytics on 22 Nov or later.
