# Dustlight story formats (21 Nov 2026)

Dustlight is a channel for **all kinds of stories**. Emotional twists were only the starting point (the first videos), not the house style: no format is the default. Every script stays original: our own characters, towns,
gags and twists, never another creator's lines. All formats use the same pipeline (Blender low-poly look, an ElevenLabs voice, synthesized music plus real CC0 sounds).

## Look (colour grade) chosen per video (owner, 22 Nov 2026: "why does it feel the same and dull")
Every video sets `scene.LOOK` in its shots.py: **comedy** (Standard transform, contrasty, saturation x1.3, bright complementary palettes, never beige on beige), **dream** (soft, warm, slightly bright), **horror** (dark, high contrast, desaturated), **story** (AgX, gentle). Pick it in the style recipe with the character model. Comedy also needs faster cuts and bouncier motion.

## Character model: chosen per video (owner's rule, 22 Nov 2026)
There is no house character. Peg dolls were the first model, not the channel look. For every new video, pick the design that best fits
its story, format and trend, and write it in the style recipe as **Character**. Models live in `pipeline/characters.py` (same handles as
`world.peg`, so animation code is shared); build a new one the first time a video needs it and render a test still before the shots.

| Model | Status | Best for |
|---|---|---|
| Peg doll (`world.peg`) | built | quiet, nostalgic, wooden-toy stories |
| Blocky (`characters.blocky`) | built 22 Nov, test `channel/style-tests/blocky-test.jpg` | comedy, trend Shorts, game-like memes, town-rule stories, anything with running or sport |
| Round bean (`characters.bean`) | built 22 Nov, test `channel/style-tests/bean-test.jpg` | cute, fast comedy, "you" stories, kids' logic |
| Clay (`characters.clay`) | built 22 Nov, test `channel/style-tests/clay-test.jpg`; render without STYLE=lowpoly | warm handmade family stories, holidays |
| Paper cut-out | idea | fairy-tale or storybook narration, memories |

| # | Format | Shape | Length | Ending | Reference studied |
|---|---|---|---|---|---|
| 1 | **Emotional twist** | A strange daily routine, why?, escalate across time, a twist that reframes it | 60 to 75 s | Callback to the first line; warm or bittersweet | The channel's first videos (The Second Cup did best: 1.1K views in a day) |
| 2 | **Nothing ever happens** | First person, deadpan. Every line builds horror-style tension, then deflates into something boring, about 8 times | 55 to 65 s | "So yeah… nothing happened." | 615K-like POV video, blocky avatars, one huge caption word at a time |
| 3 | **"You" + a power with a cost** | Second person ("You discover that…"). Wish fulfilment first, then the power hurts someone you love, you fix it, a new problem starts | 70 to 100 s | Open cliffhanger (sets up part 2) | 951K-like 2D explainer, "every lie you tell becomes true" |
| 5 | **Trend Short** (daily extra) | One trending topic, format or hook from `channel/trends.md`, done in the Dustlight world: one idea, one payoff, no setup | 15 to 30 s | A question or "comment…" prompt | Made to be cheap: 2 or 3 shots, reused sets, 20 to 60 words of voice |
| 4 | **Weird town rule + quirk** | A town with one strange rule, a hero with a quirk that seems useless, a crisis only the quirk can fix | 25 to 35 s | Interactive call to action ("type your name the way my town says it") | 22.6K-like blocky-town video, voice-password town, hero who can't say R |
| 6 | **"What if" + real science** | Second person ("What if you could see…"). A power shown as a live on-screen number or meter, a real study or fact every 20 to 30 s, the power backfires, being real fixes it, twist in the last beat | 75 to 100 s | Twist ("…you can see them too?"), then a comment question and a series hook | 1:53 flat-2D "see how much people like you" video (liking gap study, 1966 pratfall effect), studied 22 Nov 2026 |
| 7 | **Pause challenge** (Instagram/TikTok only, weekly extra at most) | Hook text "Only 1% can pause with all 3 … in the frame!"; three Dustlight things tumble past a frame or window; exactly one real frame where all three line up; seamless loop | 8 to 12 s | No outro: the last frame cuts straight back to the first, so it replays; caption asks "Did you get it? 👇" and points to the series the objects come from | 9.6 s "pause all 3 cars in the frame" Reel (cars, red outline, Instagram outro), studied 22 Nov 2026 |

## "What if" + real science rules (format 6)
- Every fact is real and checkable: name the study or year on screen ("1966 · ARONSON"). Look it up before the script; no made-up numbers.
- The power is visual and cheap to animate: a number, meter or timer over heads that changes live (34 → 33 → 30).
- Our own power, studies and twist every time; never the reference's "like meter" or its lines. Vertical 9:16.
- Look: flat 2D or simple 3D, picked per video like every other format. Flat 2D renders in seconds a frame, so it suits a weekly series.

## Pause challenge rules (format 7)
- **Instagram and TikTok only, never YouTube** (owner's rule, 22 Nov 2026). At most once a week, at 12:00 Riga. It earns rewatches and comments but few followers, so it supports the stories, never replaces them.
- Use objects or characters from our own videos (Lost Toy Room toys, Bun-Bun, the huss ball), so the caption can point to that video.
- It must be possible: one real frame where all three are inside the frame. Check it before publishing (step through the frames).
- No voice; real sound only (whooshes, a soft tick). A seamless loop, no end card. About 30 minutes to render.

## Trend Short rules (format 5)
- Build budget about 1 hour: 2 or 3 shots of 5 to 10 s, sets and characters already in `world.py`, no new props unless trivial.
- Voice: 20 to 60 words (one take), the format's own voice type; captions as the trend's style recipe says.
- Only trends we can make well in our own style and that pass the safety check in `/yt-trends` (no real people, brands or tragedy).
- Never a copy of a trend video: our own take on the topic, format or hook.

## What every format needs
- A hook line in the first 2 s that is also the title.
- A new micro-hook every 5 to 8 s (fake scare, new rule, escalation).
- Captions 1 to 3 words; let captions carry jokes where the format allows (format 4 colours the quirky letters).
- An ending that makes people comment: a question, a callback, a cliffhanger or a "type your…" prompt.

## Weekly rotation (to test, 2 weeks)
Rotate through all four formats with equal slots, plus new formats as they appear in trends. After 2 weeks, give more slots to whichever formats earn the most subscribers per 1,000 views.

## Style recipe per format (from the references studied on 21 Nov 2026)
| | 1 Emotional twist | 2 Anticlimax POV | 3 "You" + a power | 4 Town rule + quirk | 6 What if + science |
|---|---|---|---|---|---|
| **Look** | Low-poly night, candle warm against moonlight blue, shallow focus | Two looks per beat: the scare in horror lighting (dark, one cold light, low angle), the reveal in flat, bright, normal light | Bright, clean daylight, saturated colours; phone and clock inserts as motion graphics | Bright snowy town, chunky shapes, crowds of peg dolls | Dark, moody rooms, flat colours, one accent colour for the numbers; bright for the fact cards |
| **Camera** | Slow push-ins, fixed "same spot" frames | Creeping push-in for the scare, hard cut to a static wide for the reveal | Medium shots on "you", quick inserts on objects | Wide town shots, close-ups on the hero | Static wides of the scene, punch-in on faces and the number when it changes |
| **Pace** | 2 to 3 s per shot | about 1 s per shot; a scare and its reveal every 5 to 7 s | 2 s per shot; a new rule or escalation every 6 to 8 s | 1.5 s per shot; whole story in about 30 s | 2 to 3 s per shot; a number change every 5 s, a fact every 20 to 30 s |
| **Captions** | 1 to 3 words, yellow keywords, typed hook headline | One huge word at a time, top third, white with black outline | 1 to 3 words, yellow keywords | 1 to 3 words; the quirk-related words coloured (red) | Light; on-screen labels carry the story (numbers over heads, study name and year, LIKED MORE ▲) |
| **Voice** | George, warm storyteller, slow | Young, flat, deadpan first person; no drama in the voice | Energetic second-person narrator, quick | Young first person, cheerful, a bit proud | Calm, curious second-person narrator, a little dry |
| **Music** | Piano and pads, minor to major | Silence or low drone under the scare, a horror sting, then a dry comic "deflate" sound on the reveal | Bouncy plucks, a "rewind" whoosh on each use of the power, darker at the cost | Plucky upbeat music, a triumphant hit at the payoff | Soft ambient pulse, a tick or pop on every number change, a rise at the twist |
| **Ending** | Callback to the first line | "So yeah…" deadpan sign-off | Open cliffhanger | "Comment / type your…" prompt | Twist line, "What number… tell me in the comments", "follow for the next what if" |
