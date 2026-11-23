"""Edit settings for Once a Day (format 4, town rule + quirk, round bean characters).
Two-word captions with the quirk words in red. Speech bubbles pop up top for every spoken word in the town (an empty bubble when
a word is used up), a bouncy plucked tune by day, a quiet night with crunching snow, three growing "BISCUIT!" bubbles, a bark."""
import json, os, math
from PIL import ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
_D = json.load(open(os.path.join(HERE, "durations.json")))
CUTS, _t = [], 0.0
for _n, _d in _D.items():
    CUTS.append((round(_t, 2), _n)); _t += _d
CUTS.append((round(_t, 2), "END"))
T_END = round(_t + 3.2, 2)
XFADE = {}
CAPTION = {"words": 2, "y": 1300, "size": 92}
KEY = {"once", "twice...", "never", '"sorry"', "fifty", "three", '"biscuit!', "biscuit!", 'biscuit!"', '"good', 'boy"'}
END_LINES = [("Which word would you save?", 60, 900, (255, 255, 255), True, 0.2),
             ("D U S T L I G H T", 56, 1100, (255, 236, 200), False, 1.0)]
SR = 44100
C = {n: t for t, n in CUTS}
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"; _f = {}
_W = json.load(open(os.path.join(HERE, "words.json")))
def _at(word, after=0.0):
    return next(a for w, a, b in _W if w.strip('".,!?').lower() == word and a >= after)

# (start, end, text, x, y, size): text "" = an empty bubble (the word is used up)
B = [(4.0, 4.8, "Hello!", 540, 640, 70), (5.0, 6.7, "", 540, 640, 70)]
for i, (w, x) in enumerate((("morning", 250), ("hello", 450), ("greetings", 660), ("hiya", 850))):
    a = _at(w, 9.0); B.append((a, a + 1.1, w.capitalize() + ".", x, 620 + 60 * (i % 2), 56))
B.append((13.4, 16.4, "hi hello hey yes no maybe hi again", 540, 600, 46))
for k in range(9): B.append((16.6 + k * 0.55, 17.4 + k * 0.55, "sorry!", 200 + (k * 173) % 700, 560 + (k * 97) % 300, 50))
for i, s in enumerate((34.82, 35.80, 36.72)): B.append((s, 37.8, "BISCUIT!", 540, 560 - 40 * i, 70 + 22 * i))
for k in range(5): B.append((42.3 + k * 0.8, 43.3 + k * 0.8, "good boy!", 230 + (k * 211) % 620, 600 + (k * 83) % 220, 54))


def font(n):
    if n not in _f: _f[n] = ImageFont.truetype(FONT, n)
    return _f[n]


def overlay(img, t):
    d = ImageDraw.Draw(img)
    for s, e, txt, x, y, size in B:
        if not (s <= t < e): continue
        k = min(1.0, (t - s) / 0.12); sc = 0.6 + 0.4 * (1 - (1 - k) ** 3)
        f = font(max(20, int(size * sc))); w = max(120 * sc, f.getlength(txt) + 60 * sc); h = size * sc * 1.5
        box = [x - w / 2, y - h / 2, x + w / 2, y + h / 2]
        d.rounded_rectangle(box, radius=int(h / 2), fill=(255, 255, 255), outline=(0, 0, 0), width=5)
        d.polygon([(x - 18 * sc, y + h / 2 - 2), (x + 10 * sc, y + h / 2 - 2), (x - 26 * sc, y + h / 2 + 28 * sc)], fill=(255, 255, 255), outline=(0, 0, 0))
        if txt: d.text((x, y), txt, font=f, fill=(25, 25, 25), anchor="mm")
        else: d.text((x, y), "...", font=f, fill=(170, 170, 170), anchor="mm")


def bark(S, t, g=0.2):
    import numpy as np
    n = int(0.18 * SR); x = np.arange(n) / SR
    f = 520 * np.exp(-x * 6); S.add((np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.4 * S.noise(0.18, 1500)) * S.env(n, 0.005, 0.1), t, g)


def sound(S):
    day_end = C["a6"]
    S.sample("ambience/park", 0.0, day_end, g=0.05, pick=0)
    S.sample("ambience/wind", day_end, C["a10"] - day_end, g=0.07, pick=1)
    S.sample("ambience/night", C["a10"], C["END"] + 3 - C["a10"], g=0.05, pick=0)
    pat = [72, 76, 79, 76, 74, 77, 81, 77]; k, t = 0, 0.2
    while t < day_end - 0.3:
        S.add(S.bell(S.note(pat[k % 8]), 0.45), t, 0.035); t += 0.3; k += 1
    for s, e, txt, x, y, size in B: S.add(S.bell(S.note(88 if txt else 64), 0.25), s, 0.04)      # a pop for every bubble
    S.sample("foley/footsteps", C["a7"], 4.0, g=0.15, pick=2)                                    # crunching snow
    S.add(S.pad([220, 261.6, 329.6], C["a9"] - C["a7"], 1.0, 1.0), C["a7"], 0.04)
    for i, s in enumerate((34.82, 35.80, 36.72)): S.knock(s, 0.15 + 0.08 * i)
    bark(S, C["a9"] + 2.4); bark(S, C["a9"] + 2.8)
    S.add(S.pad([261.6, 329.6, 392.0, 523.3], 5.0, 0.2, 2.5), C["a10"], 0.08)
    for j, m in enumerate([72, 76, 79, 84, 88]): S.add(S.bell(S.note(m), 1.2), C["a10"] + 0.2 + j * 0.2, 0.05)
REHOOK = (C["a7"] + 0.2, "Wait for the third call…")
HOOK = "Is it possible to use up a word for the whole day?"
