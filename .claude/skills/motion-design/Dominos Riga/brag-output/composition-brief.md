# Hyperframes Composition Brief: Domino's Riga 2+1 ad pitch

## Objective
Create a short, internal, launch-style brag video that pitches the Domino's Riga 2+1 ad to the store's MD.

## Output
- Composition directory: `brag-output/composition/`
- Rendered video: `brag-output/brag.mp4`
- Format: vertical — 1080x1920, 30 fps
- Duration: 20 s

## Source Material
- Project root: `.claude/skills/motion-design/Dominos Riga/`
- Primary files read: `ad_v2.html` (the ad), `out/Dominos Riga 2+1 v2 - 1080p.mp4` (rendered ad), `site/promo_21-offer.json` (deal copy),
  `assets/dominos_logo.8a9a8ffbe4ab.png`, `assets/Dominos_21_1440x600_LV.jpg` (the site's own 2+1 banner)
- Product name: Domino's Riga 2+1 ad (pitch)
- Strongest claim: the logo's dots are 2 + 1
- Key UI or visual moment: the rendered ad playing in a phone; the site's 2+1 banner; the official tile
- Copy that must appear verbatim: "Atlaides kods MORE" (site), "2+1 · kods MORE" (ad end card), "dominospizza.lv"

## Creative Direction
- Tone preset: polished
- Creative direction: quiet agency pitch reel for one person, the MD
- Interpretation: five scenes, long holds, soft caused transitions, mixed case, no loud moments
- Angle: the logo always showed the deal; the ad is built on that
- Hook: the tile alone, "Look closely at our logo.", then "2" and "+1" beside its halves
- Outro / punchline: logo, "2+1 · kods MORE", "Ready when you are."
- Avoid: generic SaaS language, abstract filler, invented numbers or results

## Visual Identity
- Background: radial #0E3354 to #04121F
- Text: #FFFFFF
- Accent: #E31837 red, #006491 blue
- Display font: Montserrat 900/800 (bundled); body Montserrat 600
- Visual references: official logo PNG and tile, the site banner, the rendered ad

## Storyboard
Use the storyboard in `brag-plan.md` as the creative contract.
1. Hook — 3.27 s — tile, hook line, "2" and "+1"
2. Deal — 3.82 s — "It's literally our deal.", site banner, "Atlaides kods MORE"
3. The ad — 6.02 s — "So I made it the ad.", phone playing ad 3.0–9.0 s
4. How it's built — 4.36 s — phone plays ad 10.75–15.0 s, three fact chips
5. Outro — 2.53 s — logo, "2+1 · kods MORE", "Ready when you are.", "Internal pitch"

## Audio
- Audio role: warm bed with sparse accents
- Music: `assets/music/happy-beats-business-moves-vol-12-by-ende-dot-app.mp3`, 0.32, fade in 0.4 s, fade out 1.5 s
- Music cue guidance: preset `assets/music/cues/happy-beats-business-moves-vol-12-by-ende-dot-app.music-cues.json` (in the skill);
  seams on beats 3.27 / 7.09 / 13.11 / 17.47; logo locked to strong cue 17.47; chips on 13.64 / 14.73 / 15.84
- Audio-reactive treatment: subtle; a soft brand glow behind the hero breathes with bass energy (extracted with media-use's extract-audio-data.py)
- SFX: drop_001/002 on the numbers, card-place-1 on the banner, click2 on the pill and each chip, bong_001 on the logo; 0.45–0.65
- The ad clip plays muted
