"""Edit settings for Remember November (meme story, 30 Nov 2026, toon kitchen, Quaternius family).
The phrase goes yellow every time Stan says it. Music: "Launch Day" from the owner's edit kit (original, free to use), placed so
its drop lands on "December"; a pop on every "Remember...", whooshes on the quick cuts, a hit on the torn page."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
_D = json.load(open(os.path.join(HERE, "durations.json")))
CUTS, _t = [], 0.0
for _n, _d in _D.items():
    CUTS.append((round(_t, 2), _n)); _t += _d
CUTS.append((round(_t, 2), "END"))
T_END = round(_t + 3.2, 2)
XFADE = {}
CAPTION = {"words": 2, "y": 1240, "size": 96}
KEY = {'"remember...', "remember...", "november", "2026", '2026..."', "december", "six", "countdown", "last", "coming.\""}
END_LINES = [("Who says the same thing every day?", 60, 900, (255, 255, 255), True, 0.2),
             ("D U S T L I G H T", 56, 1100, (255, 236, 200), False, 1.0)]
SR = 44100
C = {n: t for t, n in CUTS}
KIT = os.path.join(HERE, "..", "..", "assets", "edit-kit")
SFX = os.path.join(KIT, "01 SFX", "Original Synth SFX")
MUSIC = os.path.join(KIT, "02 Music (original, royalty-free)", "Launch Day (120 BPM, drop at 0-16).mp3")


def sound(S):
    S.sample("ambience/room", 0.0, C["END"] + 3, g=0.05, pick=0)
    S.sample(MUSIC, 19.8, None, g=0.12, offset=0.0, fade=0.8)                      # its drop (0:16) lands on "December" (35.8)
    for t in (4.63, 23.45, 32.68):                                                 # every "Remember..."
        S.sample(os.path.join(SFX, "04 UI Clicks & Pops", "Pop Bright.wav"), t, g=0.35, fade=0.01)
    for sh in ("r3", "r4", "r5", "r6"):                                            # the quick montage
        S.sample(os.path.join(SFX, "01 Whooshes & Transitions", "Whoosh Fast L-R.wav"), C[sh] - 0.12, g=0.22, fade=0.02)
    S.sample(os.path.join(SFX, "03 Risers & Impacts", "Riser 2s.wav"), C["r11"] - 1.6, g=0.2, fade=0.05)
    S.sample(os.path.join(SFX, "03 Risers & Impacts", "Drop Hit.wav"), C["r11"] + 0.3, g=0.4, fade=0.01)   # the page rips
    S.sample(os.path.join(SFX, "03 Risers & Impacts", "Cinematic Impact.wav"), 35.8, g=0.3, fade=0.02)   # "December"


HOOK = "Why does Grandpa say this every day?"
REHOOK = (20.3, "Wait for midnight…")
