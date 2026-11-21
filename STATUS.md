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

## Rebuilt after the 19 Nov reset (done, tested end to end)
- `pipeline/` toolkit, renderer, aligner, editor and Dropbox publisher. `stories/the-second-cup/` is fully re-renderable.
- Not rebuilt: the Lost Toy Room per-shot camera files (Parts 1 to 4 are finished and live). The set, toys, Bun-Bun, door and silhouettes are in `scene.py`.
- Lost for good: the narration mp3s (ElevenLabs history has them), the rendered frames, and the full-quality "The Second Cup" (the phone copy exists).

## Open items
- Instagram: connected in Metricool on 21 Nov 2026 as **@dustlightstories** (YouTube is @the.dustlight.stories). Reels can now be scheduled with the YouTube posts.
- Channel: create the "The Lost Toy Room" playlist (public) and set "Related video" on each part to the next part.
- Old ball-sim Shorts were set to private by the owner.

## Analytics (20 Nov 2026, Metricool, 23 Oct to 20 Nov)
- Per-video data: none returned (connectors "videos published in range" and "all videos" are empty). No per-video ranking possible yet.
- Channel views: 1,118 on 16 Nov and 1,202 on 17 Nov; 1 to 27 a day before that. No view data yet after 17 Nov (YouTube reporting lag).
- Those spikes came before the Lost Toy Room went live (19 Nov), so they came from older uploads, probably the ball-sim Shorts that are now private. Unconfirmed.
- Subscribers: 0 until 16 Nov, then 2 (17 Nov), 4 (18 Nov), 12 (19 Nov). 0 lost.
- Lost Toy Room (19 Nov) is under 48 h old; The Second Cup goes live today. Re-run /yt-analytics on 22 Nov or later.
