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

- **The Empty Swing**: 21 Nov 2026 16:00 Riga (Metricool post uuid 8077661360486368967, id 436256054). Source: Dropbox `/Youtube/the-empty-swing.mp4` (full 1080p, 71.7 s, -14.4 LUFS, QC passed). Narration backup: `/Dustlight-backup/the-empty-swing-narration.mp3`.
  - Title: "Every evening at 6, he pushes an empty swing."
  - First comment: "Who would you push the swing for? 👇"

- **The Extra Plate**: script approved 21 Nov 2026 (`stories/the-extra-plate/narration.txt`, 170 words). Target: live 25 Nov 16:00 Riga, in the low-poly night style. Next: voice, then build.

## Instagram Reels (@dustlightstories, via Metricool, AI label on)
| Time (Riga) | Reel | Metricool uuid |
|---|---|---|
| 21 Nov 18:00 | The Empty Swing | -5308225935741598034 |
| 22 Nov 10:00 | The Second Cup | 6902143095151608622 |
| 22 Nov 18:00 | Ice hotel ("Every winter, they build a hotel out of a frozen river."); YouTube at 16:00 | -7028284931705059524 |
| 25 Nov 18:00 | The Extra Plate (to schedule after the render; YouTube at 16:00) | |
Lost Toy Room is not posted to Instagram (owner's choice, 21 Nov). Times follow Metricool's best Instagram hours (10:00 and 18:00 Riga); YouTube stays at 16:00, its best hour.

## TikTok (@dustlight00, formerly @divine.773, via Metricool, AI label on)
| Time (Riga) | Video | Metricool uuid |
|---|---|---|
| 21 Nov 18:00 | The Empty Swing | -4855298876224879780 |
| 22 Nov 10:00 | The Second Cup | 2666965360092859592 |
| 22 Nov 18:00 | Ice hotel | -2938055666207273225 |
| 25 Nov 18:00 | The Extra Plate (after the render) | |
TikTok connected 21 Nov 2026 as @divine.773, renamed @dustlight00 the same day (next rename allowed after 30 days). The account already had 1,197 followers from older content. TikTok's best hours match Instagram's (10:00, 12:00, 18:00).

## Rebuilt after the 19 Nov reset (done, tested end to end)
- `pipeline/` toolkit, renderer, aligner, editor and Dropbox publisher. `stories/the-second-cup/` is fully re-renderable.
- Not rebuilt: the Lost Toy Room per-shot camera files (Parts 1 to 4 are finished and live). The set, toys, Bun-Bun, door and silhouettes are in `scene.py`.
- Lost for good: the narration mp3s (ElevenLabs history has them), the rendered frames, and the full-quality "The Second Cup" (the phone copy exists).

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
