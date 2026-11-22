"""Edit settings for Thanksgiving Timeline (Trend Short, blocky family).
A timestamp card for each part of the day ("6:00 AM" in a white box with a clock icon), two-word captions with yellow keywords,
plucky comedy music, a smoke-alarm beep, a fork clink on the frozen turkey and a cheer for Grandma."""
import json, os
import numpy as np
from PIL import ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
_D = json.load(open(os.path.join(HERE, "durations.json")))
CUTS, _t = [], 0.0
for _n, _d in _D.items():
    CUTS.append((round(_t, 2), _n)); _t += _d
CUTS.append((round(_t, 2), "END"))
T_END = round(_t + 3.2, 2)
XFADE = {}
CAPTION = {"words": 2, "y": 1240, "size": 100}
KEY = {"turkey.", "turkey?", "pie.", "frozen.", "grandma", "again.", "smoke", "alarm"}
END_LINES = [("Who saves Thanksgiving in your house?", 54, 900, (255, 255, 255), True, 0.2),
             ("D U S T L I G H T", 56, 1100, (255, 236, 200), False, 1.0)]
SR = 44100
C = {n: t for t, n in CUTS}
STAMP = {"t2": "6:00 AM", "t3": "9:00 AM", "t4": "9:00 AM", "t5": "1:00 PM", "t6": "5:00 PM", "t7": "5:00 PM", "t8": "6:00 PM", "t9": "6:00 PM"}
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"; _f = {}


def _shot(t):
    cur = CUTS[0]
    for c in CUTS:
        if c[0] <= t: cur = c
    return cur


def overlay(img, t):
    st, shot = _shot(t); lab = STAMP.get(shot)
    if not lab: return
    first = CUTS[[n for _, n in CUTS].index(shot) - 1][1] if shot != "t2" else None
    k = min(1.0, (t - st) / 0.15) if STAMP.get(first) != lab else 1.0        # pop in only when the time changes
    if 90 not in _f: _f[90] = ImageFont.truetype(FONT, 84)
    d = ImageDraw.Draw(img); f = _f[90]; w = f.getlength(lab)
    x0, y0 = 70, 220; sc = 0.8 + 0.2 * k
    bw, bh = (w + 150) * sc, 130 * sc
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=int(28 * sc), fill=(255, 255, 255), outline=(0, 0, 0), width=6)
    cx, cy, r = x0 + 62 * sc, y0 + bh / 2, 34 * sc                                   # a little clock
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(0, 0, 0), width=6)
    d.line([(cx, cy), (cx, cy - r * 0.7)], fill=(0, 0, 0), width=6); d.line([(cx, cy), (cx + r * 0.55, cy)], fill=(0, 0, 0), width=6)
    d.text((x0 + 115 * sc, cy), lab, font=ImageFont.truetype(FONT, int(84 * sc)) if sc < 1 else f, fill=(20, 20, 20), anchor="lm")


def beep(S, t, n=6, g=0.06):
    for k in range(n):
        m = int(0.12 * SR); x = np.arange(m) / SR
        S.add(np.sin(2 * np.pi * 3100 * x) * S.env(m, 0.005, 0.02), t + k * 0.33, g)


def sound(S):
    S.sample("ambience/room", 0.0, C["END"] + 3, g=0.05, pick=0)
    pat = [67, 71, 74, 71, 72, 76, 79, 76]                                  # plucky comedy loop
    k, t = 0, 0.1
    while t < C["END"]:
        S.add(S.bell(S.note(pat[k % len(pat)]), 0.45), t, 0.035); t += 0.28; k += 1
    for sh in STAMP:
        if sh in ("t2", "t3", "t5", "t6", "t8"): S.add(S.bell(S.note(88), 0.4), C[sh] + 0.02, 0.07)   # a ding on each new time
    S.sample("human/breath", C["t2"] + 0.5, 1.5, g=0.15, pick=0)
    S.sample("foley/kitchen", C["t4"] + 0.2, 1.0, g=0.2, pick=0)            # the fridge
    beep(S, C["t5"] + 0.3, n=9)
    for k in range(5):                                                      # fork on ice
        S.add(S.bell(S.note(96 + (k % 2)), 0.25), C["t7"] + 0.55 + k * 0.52, 0.07)
    S.sample("foley/door", C["t8"] + 0.05, 1.2, g=0.35, pick=0, fade=0.02)
    S.add(S.pad([261.6, 329.6, 392.0, 523.3], 3.5, 0.2, 1.8), C["t10"], 0.08)
    for j, m in enumerate([72, 76, 79, 84]): S.add(S.bell(S.note(m), 1.2), C["t10"] + 0.1 + j * 0.18, 0.07)
