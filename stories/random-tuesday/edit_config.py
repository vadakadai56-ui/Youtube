"""Edit settings for A Random Tuesday (Trend Short, reflective year recap, blocky family).
Home-video look: a "REC" dot and a date stamp in the corner, soft grain; two-word captions; a gentle piano-like music box that
lands on a warm chord at "And it was perfect"."""
import json, os
from PIL import ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
_D = json.load(open(os.path.join(HERE, "durations.json")))
CUTS, _t = [], 0.0
for _n, _d in _D.items():
    CUTS.append((round(_t, 2), _n)); _t += _d
CUTS.append((round(_t, 2), "END"))
T_END = round(_t + 3.2, 2)
XFADE = {"r2": 0.2, "r3": 0.2, "r4": 0.2, "r5": 0.2, "r6": 0.2, "r7": 0.3}
CAPTION = {"words": 2, "y": 1240, "size": 96}
KEY = {"2026", "miss", "again.", "badly.", "perfect."}
END_LINES = [("What's a random day you'd relive?", 56, 900, (255, 255, 255), True, 0.2),
             ("D U S T L I G H T", 56, 1100, (255, 236, 200), False, 1.0)]
SR = 44100
C = {n: t for t, n in CUTS}
STAMP = {"r1": "TUE 24 NOV 2026  07:42", "r2": "TUE 24 NOV 2026  07:58", "r3": "TUE 24 NOV 2026  08:20", "r4": "TUE 24 NOV 2026  16:05",
         "r5": "TUE 24 NOV 2026  18:31", "r6": "TUE 24 NOV 2026  19:10", "r7": "TUE 24 NOV 2026  21:47"}
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"; _f = {}


def overlay(img, t):
    shot = None
    for s, n in CUTS:
        if s <= t: shot = n
    if shot not in STAMP: return
    if "f" not in _f:
        try: _f["f"] = ImageFont.truetype(MONO, 44)
        except OSError: _f["f"] = ImageFont.load_default()
    d = ImageDraw.Draw(img)
    if int(t * 2) % 2 == 0: d.ellipse([70, 230, 110, 270], fill=(235, 40, 40))
    d.text((125, 250), "REC", font=_f["f"], fill=(255, 255, 255), anchor="lm", stroke_width=3, stroke_fill=(0, 0, 0))
    d.text((70, 1700), STAMP[shot], font=_f["f"], fill=(255, 230, 150), anchor="lm", stroke_width=3, stroke_fill=(0, 0, 0))


def sound(S):
    S.sample("ambience/room", 0.0, C["END"] + 3, g=0.05, pick=0)
    tune = [76, 74, 72, 74, 76, 76, 76, 74, 74, 74, 76, 79, 79]
    for i, m in enumerate(tune): S.add(S.bell(S.note(m), 1.3), 0.3 + i * 0.6, 0.04)
    S.sample("foley/kitchen", C["r2"] + 0.4, 0.8, g=0.2, pick=1)              # the toaster pops
    S.add(S.pad([196, 246.9, 293.7], C["r7"] - C["r3"], 0.5, 1.0), C["r3"], 0.03)
    S.sample("foley/footsteps", C["r4"], _D["r4"], g=0.25, pick=0)
    S.add(S.pad([261.6, 329.6, 392.0, 493.9], 5.0, 0.3, 2.5), C["r7"], 0.08)
