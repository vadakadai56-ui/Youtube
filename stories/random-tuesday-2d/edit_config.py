"""Edit settings for A Random Tuesday, 2D scrapbook test (frames from remotion/src/index.tsx, split by remotion/split.py).
Same sound and captions as the 3D version, without the home-video REC overlay; two-word captions; a gentle piano-like music box that
lands on a warm chord at "And it was perfect"."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
_D = json.load(open(os.path.join(HERE, "durations.json")))
CUTS, _t = [], 0.0
for _n, _d in _D.items():
    CUTS.append((round(_t, 2), _n)); _t += _d
CUTS.append((round(_t, 2), "END"))
T_END = round(_t + 3.2, 2)
XFADE = {"r2": 0.2, "r3": 0.2, "r4": 0.2, "r5": 0.2, "r6": 0.2, "r7": 0.3}
CAPTION = {"words": 2, "y": 1420, "size": 96}
HOOK_Y = 150
QUESTION_Y = 1750
KEY = {"2026", "miss", "again.", "badly.", "perfect."}
END_LINES = [("Which day would you relive?", 56, 900, (255, 255, 255), True, 0.2),
             ("D U S T L I G H T", 56, 1100, (255, 236, 200), False, 1.0)]
SR = 44100
C = {n: t for t, n in CUTS}
def sound(S):
    S.sample("ambience/room", 0.0, C["END"] + 3, g=0.05, pick=0)
    tune = [76, 74, 72, 74, 76, 76, 76, 74, 74, 74, 76, 79, 79]
    for i, m in enumerate(tune): S.add(S.bell(S.note(m), 1.3), 0.3 + i * 0.6, 0.04)
    S.sample("foley/kitchen", C["r2"] + 0.4, 0.8, g=0.2, pick=1)              # the toaster pops
    S.add(S.pad([196, 246.9, 293.7], C["r7"] - C["r3"], 0.5, 1.0), C["r3"], 0.03)
    S.sample("foley/footsteps", C["r4"], _D["r4"], g=0.25, pick=0)
    S.add(S.pad([261.6, 329.6, 392.0, 493.9], 5.0, 0.3, 2.5), C["r7"], 0.08)
HOOK = "People are beginning to realise the boring days are the ones they miss."
