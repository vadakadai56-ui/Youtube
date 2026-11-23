"""Edit settings for The Snowman Nobody Builds (emotional twist, 1 Dec 2026, toon night street, Quaternius people).
Music: "Late Night Build" from the owner's edit kit (original, free to use), low under the voice, with a warm pad for the
flashback and a soft swell into the two waves. Real winter sound: wind, crunching steps, the lorry's engine and air brakes."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
_D = json.load(open(os.path.join(HERE, "durations.json")))
CUTS, _t = [], 0.0
for _n, _d in _D.items():
    CUTS.append((round(_t, 2), _n)); _t += _d
CUTS.append((round(_t, 2), "END"))
T_END = round(_t + 3.2, 2)
XFADE = {}
CAPTION = {"words": 3, "y": 1300, "size": 84}
KEY = {"december", "snowman", "twelve", "scarf.", "ghost.", "camera.", "four", "lorry", "danny", "three", "minutes.", "eight,",
       "promise.", "her.\"", "waved.", "back."}
END_LINES = [("Who would you build one for?", 62, 900, (255, 255, 255), True, 0.2),
             ("D U S T L I G H T", 56, 1100, (255, 236, 200), False, 1.0)]
SR = 44100
C = {n: t for t, n in CUTS}
KIT = os.path.join(HERE, "..", "..", "assets", "edit-kit")
SFX = os.path.join(KIT, "01 SFX", "Original Synth SFX")
MUSIC = os.path.join(KIT, "02 Music (original, royalty-free)", "Late Night Build (90 BPM, loop).mp3")


def sound(S):
    S.wind(0.0, C["END"] + 3, g=0.05)
    S.sample(MUSIC, 0.0, None, g=0.09, fade=1.5); S.sample(MUSIC, 43.2, None, g=0.09, fade=1.5)   # the 44.7 s loop, twice
    S.steps(C["s9"] + 0.6, 6, every=0.28, g=0.18)                                  # Danny in the snow
    S.steps(C["s12"] + 0.2, 4, every=0.33, g=0.12)
    S.add(S.pad([261.6, 329.6, 392.0], 6.0, 1.5, 2.0), C["s13"], 0.07)              # flashback warmth
    for t in (1.76, 2.8, 3.9):                                                      # each theory pops in
        S.sample(os.path.join(SFX, "02 Caption Air Swells", "Air Swell Soft.wav"), C["s4"] + t - 0.15, g=0.18, fade=0.05)
    S.sample(os.path.join(SFX, "02 Caption Air Swells", "Air Swell Warm Low (tail).wav"), C["s15"] - 0.4, g=0.22, fade=0.2)
    S.sample(os.path.join(SFX, "02 Caption Air Swells", "Air Swell Long (tail).wav"), C["s17"] - 0.3, g=0.25, fade=0.2)


HOOK = "Why does a snowman appear here every year?"
REHOOK = [(23.9, "This year, I didn't sleep…"), (47.1, "He made a promise…")]
REHOOK_Y = 1480
