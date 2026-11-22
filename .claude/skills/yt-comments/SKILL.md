---
name: yt-comments
description: Read and auto-reply to YouTube (and Instagram, once connected) comments through the Windsor.ai connector, and pick comments worth answering. Use for the daily comment check, when the owner pastes comments, asks how to reply, or wants community ideas from what viewers said.
---
# /yt-comments: replies and community

## Auto-reply (owner's choice, 22 Nov 2026)
Comments are read and answered through the **Windsor.ai for Social Media** connector (YouTube account `112783`; Instagram once it is connected in Windsor). TikTok has no comment actions there.
1. Read: `get_data` connector `youtube`, fields `comment_id, comment_author, comment_text, comment_video_id, comment_published_at, comment_reply_count`, `date_preset` `last_7dT`.
2. Skip our own comments (author `@the.dustlight.stories`) and any `comment_id` already in `channel/comment-log.md`.
3. **Normal comments** (answers to the pinned question, personal stories, praise, jokes, simple questions about the story): reply automatically with `execute_action` `reply_to_comment`, following the reply rules below. One reply per person per video; if someone wrote twice, answer the newest one.
4. **Never auto-reply; ask the owner first:** criticism, anything negative, sad or about death or illness in real life, personal or private information, questions about money, sponsorships, AI or how the channel is made, other languages you are not sure about, anything odd.
5. **Spam, scams, abuse:** hide with `moderate_comment` status `heldForReview` (never `rejected` without the owner), no reply.
6. Log every reply or hold in `channel/comment-log.md` (date, video, comment id, author, comment, our reply or action) and commit. Report the list to the owner in the weekly message.
Windsor is on a trial plan: if its calls start failing with a plan or billing error, stop and tell the owner.

## Manual mode
If Windsor is not connected, the owner pastes comments (or a screenshot) and posts the replies; draft them, never claim to have posted.

## For each batch
1. **Sort**: answers to the pinned question, emotional stories, questions about the story, requests ("part 2?"), praise, criticism, spam or abuse.
2. **Reply drafts** (owner's voice, warm, short, no emojis spam, one at most):
   - Personal stories: thank them, reflect one detail back. Never generic "thanks for watching!".
   - Questions: answer without spoiling other parts.
   - Requests: say if something is coming only if it is in `STATUS.md` or the plan.
   - Criticism: thank and acknowledge, no arguing.
   - Spam, abuse, scams: recommend hide or delete, no reply.
3. **Heart and pin** suggestions: the 1 to 3 comments that make the best social proof.
4. **Ideas**: if viewers keep naming the same object or person, suggest it to `/yt-idea`. Note recurring requests in `STATUS.md`.

Never reveal private information, never promise giveaways, never ask viewers to like or subscribe in replies.
