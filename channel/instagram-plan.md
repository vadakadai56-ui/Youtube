# Dustlight: Instagram page plan (draft, 20 Nov 2026)

Forward-looking: the page is built around the brand, not around earlier stories.

## Profile
- Name field: `Dustlight | Stories that stay` (searchable)
- Handle: `@dustlightstories` (connected to Metricool 21 Nov 2026; YouTube is `@the.dustlight.stories`)
- Profile picture: one warm glowing object (a lit window or an old lamp) on a dark background, readable at tiny sizes, not tied to a character.
- Category: Digital Creator
- Bio:
  ```
  stories about the things we forgot 🕯️
  tiny 3D stories, new every few days
  watch the full ones on YouTube ↓
  ```
- Link: the YouTube channel.

## Highlights (cream icons on dusty dark-brown circles)
1. Start Here: what Dustlight is, in about 15 s
2. Stories: new episodes
3. Your Stories: followers' replies to the pinned questions
4. Behind: clay renders turning into final shots
5. Coming Soon: teaser frames

## Grid
- The grid crops to 3:4: keep the title and faces inside the central 1080x1440 of each 1080x1920 cover.
- One formula for every cover: a dark scene with one warm light, a 3-to-5-word hook in InterDisplay-Black (cream, one yellow #FFD640 keyword), always in the same spot.
- Pin: a channel intro Reel, the best story, and a "comment who you'd do this for" post.

## Content mix
- Reels (main): each new story, 60 to 75 s, with the hook in the first 2 s.
- Carousels (weekly): a story in 6 to 8 stills with short captions.
- Stories (daily): polls, behind-the-scenes clips, teasers.

## Captions
Hook line, then 2 or 3 story lines, then a question, then 3 to 5 hashtags (#shortstory #3danimation #wholesome #storytime #emotional).

## Kit (channel/instagram/)
- `profile-picture.png`: 1080x1080 lantern, rendered by `pfp.py` (Eevee) plus a glow pass.
- `highlight-1..5-*.png`: 1080x1920 highlight covers (Start Here, Stories, Your Stories, Behind, Coming Soon).
- `reel-cover-template.png` and `reel-cover-guide.png`: hook text at y 300-700, inside the 3:4 grid crop (y 240-1680).
- `profile-mockup.png`: how the page looks. The six grid hooks are placeholders, not real stories.
- Rebuild: `python3 channel/instagram/make_kit.py channel/instagram/profile-picture.png channel/instagram/`
