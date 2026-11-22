"""Edit settings for The Sneeze (format 3, round bean characters).
1 to 3 word captions with yellow keywords. Every sneeze: a little "achoo" burst, a rewind whoosh and an on-screen rewind flash
(two triangles and "-10s"). Bouncy plucks while the power is fun, a minor drone once winter comes, a sting on "Oh no"."""
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
CAPTION = {"words": 3, "y": 1240, "size": 96}
KEY = {"sneeze", "sneeze...", "sneeze.", "rewinds", "ten", "seconds", "back.", "again.", "cold.", "grandma.", "flowers", "pepper", "score."}
END_LINES = [("What power would you want?", 60, 900, (255, 255, 255), True, 0.2),
             ("D U S T L I G H T", 56, 1100, (255, 236, 200), False, 1.0)]
SR = 44100
C = {n: t for t, n in CUTS}
_W = json.load(open(os.path.join(HERE, "words.json")))
SNEEZES = [a for w, a, b in _W if w.lower().strip('."?') in ("sneeze", "sneeze...")] + \
          [a for w, a, b in _W if w.lower().strip('.') == "again" and 37.5 < a < 45]
SNEEZES = sorted(set(round(x, 2) for x in SNEEZES))
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
_f = {}


def overlay(img, t):
    """Rewind flash for 0.6 s after each sneeze: a pale blue wash, two back triangles and -10s."""
    hit = [s for s in SNEEZES if 0 <= t - s < 0.6]
    if not hit: return
    k = 1 - (t - hit[-1]) / 0.6
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 0, img.width, img.height], fill=(180, 210, 255, int(70 * k)))
    cx, cy, s = img.width // 2, 520, 70
    for dx in (-s, 0):
        d.polygon([(cx + dx + s * 0.6, cy - s * 0.6), (cx + dx + s * 0.6, cy + s * 0.6), (cx + dx - s * 0.4, cy)], fill=(255, 255, 255, int(235 * k)))
    if 150 not in _f: _f[150] = ImageFont.truetype(FONT, 110)
    d.text((cx, cy + 140), "-10s", font=_f[150], fill=(255, 255, 255, int(235 * k)), anchor="mm", stroke_width=6, stroke_fill=(0, 0, 0, int(200 * k)))


def achoo(S, t, g=0.22):
    """A quick sneeze: an inhale hiss, then a bright burst."""
    S.add(S.noise(0.35, 2500) * S.env(int(0.35 * SR), 0.3, 0.05) * 0.4, t - 0.4, g)
    S.add(S.noise(0.22, 4000) * S.env(int(0.22 * SR), 0.005, 0.18), t, g)


def sound(S):
    S.sample("ambience/room", 0.0, C["s11"], g=0.04, pick=0)
    S.sample("ambience/wind", C["s11"], C["s17"] - C["s11"], g=0.05, pick=0)
    for s in SNEEZES:
        achoo(S, s); S.sample("transitions/whoosh", s + 0.05, 0.5, g=0.3, pick=1, fade=0.02)
    # bouncy plucks while the power is fun
    pat = [72, 76, 79, 76, 74, 77, 81, 77]
    k, t = 0, 0.2
    while t < C["s11"] - 0.3:
        S.add(S.bell(S.note(pat[k % len(pat)]), 0.5), t, 0.04); t += 0.3; k += 1
    S.sample("foley/kitchen", C["s5"] + 1.1, 0.6, g=0.25, pick=1)                 # the cup tipping
    S.knock(C["s8"] + 0.75, 0.35)                                                  # the ball off the rim
    S.add(S.bell(S.note(84), 0.8), C["s8"] + 1.7, 0.08)                            # swish
    # winter: a low minor drone under the cold
    S.add(S.pad([110, 130.8, 164.8], C["s16"] - C["s11"], 1.0, 1.5), C["s11"], 0.05)
    S.add(S.pad([261.6, 329.6, 392], 3.0, 0.3, 1.2), C["s16"], 0.05)               # relief
    for k in range(3): S.add(S.bell(S.note(88), 0.6), C["s17"] + 0.2 + k * 0.45, 0.06)   # the doorbell
    S.add(S.pad([233, 277, 311], 2.5, 0.05, 1.5), C["s19"], 0.07)                    # "oh no"
