"""Edit settings for Memory Timer (format 6, "What if" + real science, round bean characters).
Timers float over heads (drawn here), each fact gets a card with its study and year, and the two ideas get simple graphs:
Ebbinghaus's forgetting curve (1885) and Kahneman's peak-end rule (1993). A soft ambient pulse, a tick on every timer change,
a rise into "Forever". Facts checked 22 Nov 2026 (see channel/formats.md, format 6 rules)."""
import json, os, math
from PIL import ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
_D = json.load(open(os.path.join(HERE, "durations.json")))
CUTS, _t = [], 0.0
for _n, _d in _D.items():
    CUTS.append((round(_t, 2), _n)); _t += _d
CUTS.append((round(_t, 2), "END"))
T_END = round(_t + 3.4, 2)
XFADE = {"m7": 0.3, "m13": 0.3, "m14": 0.3}
CAPTION = {"words": 3, "y": 1300, "size": 84}
KEY = {"timer.", "minutes.", "hours.", "seconds.", "1885,", "ebbinghaus", "half", "1993", "kahneman", "peak-end", "ends.", "forever.", "years.", "days."}
END_LINES = [("What moment will you never forget?", 54, 900, (255, 255, 255), True, 0.2),
             ("D U S T L I G H T", 56, 1100, (255, 236, 200), False, 1.0)]
SR = 44100
C = {n: t for t, n in CUTS}
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"; _f = {}
GOLD, CREAM, INK = (255, 214, 64), (255, 236, 200), (25, 25, 30)


def font(n):
    if n not in _f: _f[n] = ImageFont.truetype(FONT, n)
    return _f[n]


def _shot(t):
    cur = CUTS[0]
    for c in CUTS:
        if c[0] <= t: cur = c
    return cur


def timer(d, x, y, txt, size=52, col=(255, 255, 255), pop=1.0):
    """A floating timer: a rounded pill with a little stopwatch icon. txt '' = blank."""
    s = 0.7 + 0.3 * pop; f = font(int(size * s)); w = max(150 * s, f.getlength(txt) + 120 * s); h = size * 1.6 * s
    d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], radius=int(h / 2), fill=col, outline=(0, 0, 0), width=5)
    cx, cy, r = x - w / 2 + 42 * s, y, 18 * s
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=5); d.line([(cx, cy), (cx, cy - r * 0.7)], fill=INK, width=4)
    d.rectangle([cx - 5 * s, cy - r - 9 * s, cx + 5 * s, cy - r - 3 * s], fill=INK)
    if txt: d.text((x + 22 * s, y), txt, font=f, fill=INK, anchor="mm")


def card(d, top, lines):
    for i, (txt, size, col) in enumerate(lines):
        d.text((540, top + i * int(size * 1.35)), txt, font=font(size), fill=col, anchor="mm", stroke_width=5, stroke_fill=(0, 0, 0))


def at(t, s): return min(1.0, max(0.0, (t - s) / 0.15))


def overlay(img, t):
    st, shot = _shot(t); lt = t - st; d = ImageDraw.Draw(img)
    if shot == "m2":
        for i, (x, txt) in enumerate(((160, "3 MIN"), (400, "9 SEC"), (680, "2 DAYS"), (920, "20 MIN"))):
            timer(d, x + 30 * lt * (1 if i % 2 else -1), 760, txt, 40, pop=at(lt, 0.3 + 0.25 * i))
    elif shot == "m3" and lt > 2.5: timer(d, 420, 700, "4 MIN", pop=at(lt, 2.5))
    elif shot == "m4" and lt > 0.9: timer(d, 470, 640, "2 HOURS", pop=at(lt, 0.9))
    elif shot == "m5" and lt > 2.4: timer(d, 700, 720, "11 SEC", pop=at(lt, 2.4))
    elif shot == "m6": card(d, 330, [("1885", 120, GOLD), ("HERMANN EBBINGHAUS", 58, CREAM), ("tested his own memory", 44, (255, 255, 255))])
    elif shot == "m7": curve(d, lt)
    elif shot == "m8" and lt > 1.0: timer(d, 720, 720, "2 DAYS" if lt < 3.3 else "3 DAYS", pop=at(lt, 1.0))
    elif shot == "m9":
        txt = "3 DAYS" if lt < 3.16 else ("2 DAYS" if lt < 4.24 else "1 DAY"); timer(d, 740, 700, txt, pop=1.0, col=(235, 235, 240))
    elif shot == "m10" and lt > 0.5: timer(d, 660, 660, "1 DAY", pop=at(lt, 0.5))
    elif shot == "m11":
        if lt < 1.36:                                                        # the digits roll faster and faster
            n = int((lt / 1.36) ** 2 * 40); timer(d, 540, 520, f"{n} YEARS", 64)
        else: timer(d, 540, 520, "40 YEARS", 72, col=GOLD, pop=at(lt, 1.36))
    elif shot == "m12": card(d, 380, [("THE PEAK-END RULE", 74, GOLD)])
    elif shot == "m13": peak_end(d, lt)
    elif shot == "m15":
        g = 2.52
        timer(d, 540, 560, "2 MIN" if lt < g else "", 60, col=(255, 255, 255) if lt < g else (225, 225, 230))
    elif shot == "m16": timer(d, 540, 560, "FOREVER", 80, col=GOLD, pop=at(lt, 0.0))


def curve(d, lt):
    """The forgetting curve: retention falls steeply in the first hour, then levels off (Ebbinghaus 1885, savings method)."""
    card(d, 300, [("THE FORGETTING CURVE", 64, GOLD)])
    x0, y0, w, h = 150, 1050, 780, 520
    d.line([(x0, y0 - h), (x0, y0), (x0 + w, y0)], fill=(255, 255, 255), width=8)
    d.text((x0 - 20, y0 - h - 40), "remembered", font=font(36), fill=CREAM, anchor="ls")
    d.text((x0 + w, y0 + 50), "time", font=font(36), fill=CREAM, anchor="rs")
    pts = [(0, 1.0), (0.03, 0.58), (0.08, 0.44), (0.2, 0.36), (0.4, 0.34), (0.7, 0.28), (1.0, 0.25)]   # 20 min, 1 h, 9 h, 1 day ... 1 month
    k = min(1.0, lt / 2.5); path = []
    for i in range(len(pts) - 1):
        for j in range(12):
            u = j / 12; px = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * u; py = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * u
            if px <= k: path.append((x0 + px * w, y0 - py * h))
    if len(path) > 1: d.line(path, fill=GOLD, width=10, joint="curve")
    if lt > 2.6:
        hx, hy = x0 + 0.08 * w, y0 - 0.44 * h
        d.ellipse([hx - 14, hy - 14, hx + 14, hy + 14], fill=(255, 90, 90))
        d.text((hx + 30, hy - 40), "1 hour: over half gone", font=font(40), fill=(255, 255, 255), anchor="ls", stroke_width=4, stroke_fill=(0, 0, 0))


def peak_end(d, lt):
    """The peak-end rule: an experience is remembered by its most intense moment and its end, not its length (Kahneman 1993)."""
    card(d, 300, [("1993", 110, GOLD), ("DANIEL KAHNEMAN", 56, CREAM)])
    x0, y0, w, h = 150, 1150, 780, 420
    d.line([(x0, y0), (x0 + w, y0)], fill=(255, 255, 255), width=6)
    pts = [(0, 0.2), (0.15, 0.3), (0.3, 0.25), (0.45, 0.95), (0.6, 0.35), (0.75, 0.3), (0.9, 0.55), (1.0, 0.6)]
    k = min(1.0, lt / 3.0)
    path = [(x0 + x * w, y0 - y * h) for x, y in pts if x <= k]
    if len(path) > 1: d.line(path, fill=(150, 200, 255), width=9, joint="curve")
    if lt > 3.4:
        px, py = x0 + 0.45 * w, y0 - 0.95 * h; d.ellipse([px - 18, py - 18, px + 18, py + 18], fill=GOLD)
        d.text((px, py - 40), "PEAK", font=font(44), fill=GOLD, anchor="ms", stroke_width=4, stroke_fill=(0, 0, 0))
    if lt > 5.8:
        ex, ey = x0 + w, y0 - 0.6 * h; d.ellipse([ex - 18, ey - 18, ex + 18, ey + 18], fill=GOLD)
        d.text((ex, ey - 40), "END", font=font(44), fill=GOLD, anchor="ms", stroke_width=4, stroke_fill=(0, 0, 0))
    if lt > 7.6:
        d.text((540, y0 + 90), "not how long it lasted", font=font(46), fill=(255, 255, 255), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))
        d.line([(x0, y0 + 30), (x0 + w, y0 + 30)], fill=(255, 90, 90), width=4)


def tick(S, t, g=0.06):
    S.add(S.bell(S.note(96), 0.15), t, g)


def sound(S):
    S.sample("ambience/room", 0.0, C["END"] + 3, g=0.04, pick=0)
    S.add(S.pad([130.8, 196.0, 261.6], C["m10"], 2.0, 2.0), 0.0, 0.04)                 # a soft curious bed
    for k in range(int(C["m10"] / 1.2)): S.add(S.bell(S.note(84 if k % 4 else 79), 0.5), 0.3 + k * 1.2, 0.025)
    for s, off in (("m3", 2.5), ("m4", 0.9), ("m5", 2.4), ("m8", 1.0), ("m10", 0.5)): tick(S, C[s] + off)
    for off in (0, 1.18, 2.26): tick(S, C["m9"] + 1.98 + off)
    for i in range(14): tick(S, C["m11"] + 1.36 * (i / 14) ** 0.5, 0.03)
    S.add(S.bell(S.note(88), 1.5), C["m11"] + 1.36, 0.08)
    S.sample("foley/kitchen", C["m10"] + 0.5, 1.2, g=0.2, pick=1)
    S.add(S.pad([174.6, 220.0, 261.6, 349.2], C["m14"] - C["m10"], 1.0, 1.5), C["m10"], 0.05)  # warm
    S.add(S.pad([110, 164.8, 220], C["m16"] - C["m14"], 1.0, 0.5), C["m14"], 0.04)            # the quiet call
    S.add(S.pad([261.6, 329.6, 392.0, 523.3], 6.0, 0.05, 3.0), C["m16"], 0.09)
    for j, m in enumerate([72, 76, 79, 84, 88]): S.add(S.bell(S.note(m), 1.6), C["m16"] + 0.05 + j * 0.15, 0.06)
HOOK = "People are beginning to realise they forget most of today by tomorrow."
REHOOK = [(C["m7"] + 0.2, "Wait for Sunday…"), (C["m13"] + 3.0, "Now wait for the phone call…")]
