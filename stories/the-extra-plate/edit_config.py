"""Edit settings for The Extra Plate (used by pipeline/edit.py).
Same Spot, Years Apart: a typed hook headline (0 to 3.4 s) and a Thanksgiving year counter on screen.
Sound: synthesized piano and pads, plus real CC0 recordings from the Dustlight library (pipeline/sfx_library.py)."""
import json, os
import numpy as np
from PIL import ImageDraw, ImageFont

_D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "durations.json")))
CUTS, _t = [], 0.0
for _n, _d in _D.items():
    CUTS.append((round(_t, 2), _n)); _t += _d
CUTS.append((round(_t, 2), "END"))                     # 73.2
T_END = round(_t + 4.2, 2)
XFADE = {"s6": 0.35, "s9": 0.3, "s17": 0.4, "s20": 0.5}
KEY = {"thanksgiving", "nine years", "extra plate", "danny", "postcard", "still warm", "never", "little girl", "tiny chair",
       "year ten", "knock", "my daddy", "nine postcards", "my plate", "every chair", "full"}
END_LINES = [("Some people keep a place for you", 60, 880, (255, 255, 255), True, 0.2),
             ("long after you've gone.", 60, 960, (255, 255, 255), True, 0.2),
             ("D U S T L I G H T", 56, 1160, (255, 236, 200), False, 1.4)]
SR = 44100
CUT = {n: t for t, n in CUTS}

# ---------------------------------------------------------------- on-screen graphics
BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
CREAM, RED = (255, 244, 225), (214, 58, 48)
_F = {}
def _font(n):
    if n not in _F: _F[n] = ImageFont.truetype(BLACK, n)
    return _F[n]

YEAR = {"s1": 2017, "s2": 2017, "s3": 2017, "s4": 2017, "s5": 2018, "s6": 2016, "s9": (2019, 2021), "s10": 2022, "s11": 2024,
        "s12": 2025, "s13": 2026, "s14": 2026, "s15": 2026, "s16": 2026, "s17": 2026, "s18": 2026, "s19": 2026, "s20": 2026}
HOOK = ["she sets one", "extra plate.", "every year."]


def _shot(t):
    cur = None
    for st, n in CUTS:
        if st <= t: cur = (st, n)
    return cur


def overlay(img, t):
    d = ImageDraw.Draw(img); st, shot = _shot(t)
    if t < 3.6:                                                   # typed hook headline, then it fades
        a = 1.0 if t < 3.2 else max(0.0, (3.6 - t) / 0.4); shown = int(max(0, t - 0.1) * 16); y = 300
        for i, line in enumerate(HOOK):
            n = max(0, min(len(line), shown)); shown -= len(line)
            if n == 0: break
            txt = line[:n]; f = _font(104)
            col = tuple(int(c * a) for c in CREAM)
            d.text((80, y), txt, font=f, fill=col, anchor="ls", stroke_width=6, stroke_fill=(0, 0, 0))
            if i == 1 and n == len(line):                          # red underline under "extra plate"
                k = min(1.0, (t - 1.45) / 0.35) if t > 1.45 else 0
                w = f.getlength(line.rstrip("."))
                if k > 0: d.line([(82, y + 22), (82 + w * k, y + 22)], fill=tuple(int(c * a) for c in RED), width=10)
            if n < len(line) or i == len(HOOK) - 1:
                if (t * 2) % 1 < 0.6 and t < 3.2: d.rectangle([80 + f.getlength(txt) + 8, y - 84, 80 + f.getlength(txt) + 18, y + 6], fill=col)
            y += 122
        return
    yr = YEAR.get(shot)
    if yr is None or shot == "END": return
    if isinstance(yr, tuple):                                      # years ticking past in one shot
        k = (t - st) / max(0.01, _D[shot]); yr = int(round(yr[0] + (yr[1] - yr[0]) * min(1, k * 1.3)))
    a = min(1.0, (t - 3.6) / 0.4)
    col = tuple(int(c * a) for c in CREAM)
    label = "THANKSGIVING" if shot != "s6" else "THE LAST ONE HE CAME TO"
    d.text((80, 250), label, font=_font(34), fill=col, anchor="ls", stroke_width=4, stroke_fill=(0, 0, 0))
    d.text((74, 400), str(yr), font=_font(150), fill=col, anchor="ls", stroke_width=7, stroke_fill=(0, 0, 0))
    if shot != "s6": d.line([(80, 425), (80 + 300 * a, 425)], fill=tuple(int(c * a) for c in RED), width=8)


# ---------------------------------------------------------------- sound
def sound(S):
    n = S.note; c = CUT
    # real room: a crackling fireplace and a clock, under everything at the table
    for shot in ("s1", "s2", "s4", "s5", "s9", "s11", "s15", "s16", "s19", "s20"):
        S.sample("ambience/fire", c[shot], _D[shot] + 0.4, g=0.10, pick=2, offset=c[shot] % 20)
    S.sample("ambience/room", c["s12"], _D["s12"] + _D["s13"], g=0.12, pick=0)                 # year nine and ten: only the clock
    S.sample("ambience/rain", c["s6"], _D["s6"], g=0.16, pick=3)                               # the fight
    S.sample("foley/door", c["s6"] + 3.05, 1.5, g=0.55, pick=0, fade=0.02)                     # the door slams
    S.sample("ambience/wind", c["s7"], _D["s7"] + _D["s8"], g=0.10, pick=0)                    # snow at the window
    S.sample("foley/paper", c["s8"] + 0.1, 1.2, g=0.25, pick=1, fade=0.05)
    S.sample("foley/glass", c["s2"] + 0.8, 1.0, g=0.12, pick=1, fade=0.02)                     # cutlery and glasses
    S.sample("foley/kitchen", c["s5"] + 0.6, 1.2, g=0.10, pick=2, fade=0.02)
    S.sample("foley/cloth", c["s11"] + 0.2, 1.5, g=0.14, pick=0)
    S.sample("foley/footsteps", c["s15"] + 0.1, 3.2, g=0.18, pick=2)                          # the girl's little steps
    S.sample("foley/paper", c["s16"] + 0.3, 1.0, g=0.2, pick=1, fade=0.05)                     # the card is picked up
    S.sample("foley/door", c["s17"] - 0.2, 2.0, g=0.18, pick=1)                                # the door creaks open
    for k in range(3): S.knock(c["s14"] + 0.25 + k * 0.3, 0.55)                                # the knock
    # music: a lonely minor piano for the years, near silence at year ten, then the warm major turn
    S.chords([(57, 64, 69, 72), (53, 60, 65, 69), (50, 57, 62, 65), (52, 59, 64, 68)], 0.2, c["s12"], step=3.6, bass=0.11, top=0.06)
    S.add(S.pad([110, 164.8], c["s12"], 3, 2), 0.0, 0.05)
    for i, m in enumerate([76, 74, 72, 71, 69, 72, 71, 69, 67, 69]):                           # a little falling motif each year
        S.add(S.piano(n(m + 12), 2.0), c["s2"] + 0.2 + i * 3.4, 0.035)
    S.add(S.piano(n(69), 4.0), c["s13"] + 0.2, 0.07)                                         # one held note: she almost doesn't
    S.add(S.pad([55, 82.4], c["s15"] - c["s13"], 0.8, 0.6), c["s13"], 0.08)
    S.chords([(57, 61, 64, 69), (54, 57, 61, 66), (50, 54, 57, 62), (52, 56, 59, 64)], c["s15"], c["END"] + 0.4, step=3.0, bass=0.12, top=0.075)
    S.add(S.pad([220, 277.2, 329.6, 440], c["END"] - c["s17"] + 1.5, 1.2, 1.8), c["s17"], 0.09)
    mel = [69, 73, 76, 73, 74, 71, 69, 71, 73, 76, 81]
    for i, m in enumerate(mel): S.add(S.bell(n(m + 12), 1.6), c["s17"] + 0.3 + i * 0.75, 0.04)
    for i, m in enumerate([69, 73, 76, 81, 85]): S.add(S.piano(n(m), 3.5), c["END"] + 0.1 + i * 0.5, 0.07)
    S.add(S.pad([220, 277.2, 329.6], 4.0, 0.5, 2.5), c["END"] + 0.1, 0.07)
