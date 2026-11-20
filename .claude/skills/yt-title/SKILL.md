---
name: yt-title
description: Write the YouTube title, description, tags and pinned first comment for a Short. Use before /yt-publish, or when the owner asks for title options.
---
# /yt-title: packaging

## Title (Shorts: the title shows small under the video, it should match the hook)
- 5 options, 40 to 70 characters, each a different angle: the strange routine, the number, the reveal-teaser ("Nobody knows why."), the question.
- Never give away the twist. Never promise what the story does not deliver.
- Series: "(Part 2)", "(Finale)" at the end.
- Past titles that shipped: "He makes two cups of tea every morning. Nobody knows why." / "Every evening at 6, he pushes an empty swing."

## Description
```
<one-sentence teaser, no spoilers>

Dustlight: stories about the things we forgot. A new short story every day.
▶ <series or related video, if any>

Every story, character and scene on this channel is original.
#shorts #story #animation
```

## Tags (Metricool `youtubeData.tags`)
8 to 12: the story's nouns, "short story", "animated story", "emotional story", "dustlight". No unrelated trending tags.

## Pinned first comment
A question the viewer answers from their own life, ending with 👇. Past: "Who would you make the second cup for? 👇", "Who would you push the swing for? 👇"

## Output
A block the owner can approve, then save it to `STATUS.md` under the video and hand off to `/yt-publish`.
