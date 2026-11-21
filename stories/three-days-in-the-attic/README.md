# Three Days in the Attic (3 parts)

Original series. Chosen 21 Nov 2026 (`stories/ideas.md` #4).
Trends: numbered parts that each end on a cliffhanger (New Engen, 20 Nov 2026, 14+ days left) and the holiday run-up (to Christmas, about 35 days left). Told in the second person ("you"). Each part is one day.

**First hook (the finale pays it off):** "Day one. You're a toy in a box marked GIVE AWAY. The van comes in three days."
**Rule / mystery:** a toy can only leave the box if someone remembers its name.

## Cast
- **You:** a small tin soldier with a chipped red coat and one bent bayonet. Nobody has said your name in 30 years. (New model.)
- **Pip:** the wind-up mouse in the box (`toy_mouse`). He has been in here the longest and knows the rule.
- **The music box:** a ballerina who has forgotten her tune. (New: a box with a lid and a turning dancer.)
- **Anna:** the grown-up child, now about 40 (peg doll, `kind="rose"`). **Maya:** her daughter (peg doll, `h≈0.6`).

## Part 1: "Day one" (55 to 70 s)
- **Hook (0 to 3 s):** the line above, over the label GIVE AWAY on a cardboard box.
- **Beats:** the box opens a crack and dust light comes in. Pip explains: the van comes on Friday, the toys it takes don't come back, and the only way out is to be *remembered*, by name. You try to remember your own name and can't. Snow outside the round window.
- **Cliffhanger (last 5 s):** the attic hatch creaks, footsteps come up the ladder and torchlight sweeps across the box. "Do you hide… or do you let her see you? 👇"

## Part 2: "Day two"
- **Recap (0 to 3 s):** "Day two. Someone came up the ladder."
- **Beats:** it is Anna, looking for the Christmas lights. She opens the box, smiles at the music box and winds it, but it won't play. She holds you for a second, almost says something, then puts you back. Pip says, "She almost had it."
- **Cliffhanger:** she tapes the box shut and carries it down the ladder, toward the door and the van. "One day left. 👇 Would she remember?"

## Part 3: "Day three" (Finale)
- **Recap (0 to 3 s):** "Day three. The box is by the front door. The van is outside."
- **Beats:** the van's headlights and snow. Maya, by the box: "Mum, what did you play with when you were little?" Anna stops, opens the tape, finds you and says your name: "**Captain Button.**" The music box plays at last, a synthesized tune.
- **Payoff:** the van leaves without the box. Anna gives you to Maya: "He kept me brave." You are on a shelf by the Christmas tree. "You were never lost. Just waiting to be remembered."
- **Pinned question:** "What's the name of a toy you'd still remember? 👇"

## New sets and props
- Attic: sloped beams, a round window with `Snow`, a hatch and ladder, a hanging bulb, a cardboard box with a `text()` label (reuses `room()` lighting, `dust_motes` and `shelf`).
- Tin soldier, music box, roll of tape, Christmas lights.
- Hallway and front door: reuse `door(hall=True)`. Van: cubes plus headlight spots, seen through the door. Snowy street: `street()` and `Snow`.
- Living room corner with a small tree (cones plus emissive bulbs) for the last shot.

## Reuse (keeps render time down)
- The attic set carries Parts 1 and 2 and the first half of Part 3. Build it once.
- Same camera rig and lighting across parts. Pip and the box are on screen in every part.

## Release plan (for /yt-plan)
- Not before The Empty Swing (waiting for a Dropbox token, planned for 21 Nov 16:00 Riga).
- Scripts: 21 to 22 Nov (the owner approves each). Builds: 22 to 24 Nov.
- Part 1: **25 Nov 16:00 Riga**. Part 2: **26 Nov 16:00**. Part 3: **27 Nov 16:00**. One day apart, to match "Day one, two, three".
- End cards: "DAY TWO · TOMORROW" and "THE LAST DAY · TOMORROW" (true only with this daily schedule).
- Owner to-dos in YouTube Studio: a public "Three Days in the Attic" playlist, and set "Related video" on each part to the next part.
