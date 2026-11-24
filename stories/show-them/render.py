"""Show Them: kinetic-type short (9:16). PIL frames piped to ffmpeg, synthesized music/SFX, voice from audio/show-them.mp3.
usage: python3 stories/show-them/render.py OUT.mp4 [PREVIEW_SECONDS...]   (preview seconds -> PNG stills instead of video)
"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, END = 1080, 1920, 30, 19.5
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
VOICE = os.path.join(ROOT, "audio/show-them.mp3")
WORDS = [(w[0], w[1], w[2]) for w in json.load(open(os.path.join(HERE, "words.json")))]
F_MED = "/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf"
F_BOLD = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
font = lambda p, s: ImageFont.truetype(p, s)
PAPER, INK, NIGHT, RED = (232, 230, 226), (28, 26, 26), (13, 12, 12), (226, 52, 36)

# scene cuts (seconds), from words.json
CUTS = [0, 3.40, 4.55, 5.85, 7.20, 8.70, 10.20, 13.85, 16.60, END]
POPS = [10.32, 10.81, 11.00, 11.78, 12.03, 12.38, 12.74, 13.07]   # one icon per word in "not all at once. one small thing at a time"

clamp = lambda x, a=0.0, b=1.0: max(a, min(b, x))
smooth = lambda x: (lambda u: u * u * (3 - 2 * u))(clamp(x))
def back(x, s=1.9):
    x = clamp(x) - 1; return 1 + (s + 1) * x ** 3 + s * x ** 2
lerp = lambda a, b, t: a + (b - a) * t

# ---------- pixel icons (auto-outlined, nearest-neighbour scaled) ----------
PAL = {"R": (222, 40, 40), "W": (255, 250, 240), "Y": (246, 196, 38), "O": (196, 128, 20), "D": (70, 70, 76),
       "S": (190, 192, 198), "K": (30, 30, 34), "B": (70, 120, 200), "G": (60, 150, 70), "L": (140, 210, 100),
       "T": (196, 96, 60), "C": (238, 222, 190), "E": (196, 170, 130), "P": (240, 140, 160), "A": (120, 120, 126)}
ICONS = {
 "heart": [".RRR...RRR.", "RRWRR.RRRRR", "RWRRRRRRRRR", "RRRRRRRRRRR", ".RRRRRRRRR.", "..RRRRRRR..", "...RRRRR...", "....RRR....", ".....R....."],
 "coin": ["..YYYYYY..", ".YYYYYYYY.", "YYOOOOOOYY", "YYOYYWYOYY", "YYOYYWYOYY", "YYOYYWYOYY", "YYOYYWYOYY", "YYOOOOOOYY", ".YYYYYYYY.", "..YYYYYY.."],
 "camera": ["...DDD........", ".DDDDDDDDDDDD.", "DSSSSSSSSSSSSD", "DSSKKKKKKSSRSD", "DSKKBBBBKKSSSD", "DSKBBWBBBKSSSD",
            "DSKBBBBBBKSSSD", "DSKKBBBBKKSSSD", "DSSKKKKKKSSSSD", ".DDDDDDDDDDDD."],
 "vinyl": ["...KKKKKK...", "..KKKKKKKK..", ".KKAKKKKKKK.", "KKAKKKKKKKKK", "KKKKRRRRKKKK", "KKKKRWWRKKKK", "KKKKRWWRKKKK",
           "KKKKRRRRKKKK", "KKKKKKKKKAKK", ".KKKKKKKKAK.", "..KKKKKKKK..", "...KKKKKK..."],
 "plant": ["....GG....", ".GG.GG.GG.", ".GGGLGGGG.", "..GGLGLG..", "GG.GLLG.GG", ".GGGLGGGG.", "...GLG....", ".TTTTTTTT.",
           "..TTTTTT..", "..TCTTTT..", "..TTTTTT..", "...TTTT..."],
 "cat": [".K......K...", ".KK....KK...", ".KKKKKKKK...", ".KYKKKKYK...", ".KKKKKKKK...", "..KKPPKK....", "..KKKKKKK..K",
         ".KKKKKKKKK.K", ".KKKKKKKKKKK", ".KK.KK.KKKK."],
 "letter": ["CCCCCCCCCCCCCC", "CECCCCCCCCCCEC", "CCECCCCCCCCECC", "CCCECCCCCCECCC", "CCCCECCCCECCCC", "CCCCCERRECCCCC",
            "CCCCCCRRCCCCCC", "CCCCCCCCCCCCCC", "CCCCCCCCCCCCCC", "CCCCCCCCCCCCCC"],
 "key": [".YYY..........", "YOOOY.........", "YO.OYYYYYYYYYY", "YOOOY....Y.Y.Y", ".YYY.....Y.Y.."],
}
def icon(name, px):
    g = ICONS[name]; h, w = len(g), max(map(len, g))
    a = np.zeros((h + 2, w + 2, 4), np.uint8)
    for y, row in enumerate(g):
        for x, c in enumerate(row):
            if c != ".": a[y + 1, x + 1] = (*PAL[c], 255)
    m = a[..., 3] > 0
    ring = np.zeros_like(m)
    for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)): ring |= np.roll(np.roll(m, dy, 0), dx, 1)
    a[ring & ~m] = (16, 14, 14, 255)
    return Image.fromarray(a).resize(((w + 2) * px, (h + 2) * px), Image.NEAREST)
_icache = {}
def icon_at(name, px):
    k = (name, px)
    if k not in _icache: _icache[k] = icon(name, px)
    return _icache[k]
def paste_icon(img, name, cx, cy, scale=1.0, rot=0.0, px=14):
    if scale <= 0.02: return
    im = icon_at(name, px)
    im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.NEAREST)
    if rot: im = im.rotate(rot, Image.NEAREST, expand=True)
    img.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

# ---------- silhouettes ----------
PROFILE = [(0, 1400), (0, 1200), (120, 1100), (300, 1050), (360, 980), (340, 880), (260, 820), (200, 700), (190, 560), (230, 420),
           (320, 310), (450, 250), (580, 240), (700, 270), (790, 340), (840, 430), (860, 520), (880, 600), (900, 640), (890, 680),
           (920, 760), (960, 820), (930, 850), (900, 860), (910, 900), (895, 920), (905, 950), (880, 975), (870, 1010), (830, 1040),
           (760, 1050), (700, 1040), (680, 1100), (720, 1150), (900, 1230), (1000, 1300), (1000, 1400)]
def profile_mask(scale):
    m = Image.new("L", (int(1000 * scale), int(1400 * scale)), 0); d = ImageDraw.Draw(m)
    d.polygon([(x * scale, y * scale) for x, y in PROFILE], 255)
    for cx, cy, r in ((470, 330, 200), (330, 470, 140)):   # hair volume
        d.ellipse([(cx - r) * scale, (cy - r) * scale, (cx + r) * scale, (cy + r) * scale], 255)
    return m.filter(ImageFilter.GaussianBlur(2))

def gradient(w, h, stops_center, inner, outer, power=1.2):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy, r = stops_center
    t = np.clip(np.hypot(xx - cx * w, yy - cy * h) / (r * max(w, h)), 0, 1) ** power
    return (np.array(inner) * (1 - t[..., None]) + np.array(outer) * t[..., None]).astype(np.uint8)

def build_silhouettes():
    m = profile_mask(0.85)
    warm = Image.fromarray(gradient(m.width, m.height, (0.75, 0.75, 0.9), (255, 214, 80), (205, 40, 18)))
    grey = Image.fromarray(gradient(m.width, m.height, (0.3, 0.2, 1.0), (150, 150, 152), (88, 88, 92)))
    out = {}
    for k, g in (("warm", warm), ("grey", grey)):
        im = g.convert("RGBA"); im.putalpha(m); out[k] = im
    glow = Image.new("RGBA", m.size, (255, 120, 40, 0)); glow.putalpha(m.point(lambda v: v * 0.55).filter(ImageFilter.GaussianBlur(40)))
    out["glow"] = glow
    return out

def hand_mask(size=900):
    """Open hand reaching up, palm facing the viewer, fingers spread."""
    m = Image.new("L", (size, int(size * 1.5)), 0); d = ImageDraw.Draw(m); s = size / 900
    def cap(p, q, wdt):
        d.line([p, q], 255, int(wdt)); r = wdt / 2
        for x, y in (p, q): d.ellipse([x - r, y - r, x + r, y + r], 255)
    cap((450 * s, 1350 * s), (450 * s, 900 * s), 230 * s)                       # wrist/forearm
    d.ellipse([270 * s, 620 * s, 640 * s, 1010 * s], 255)                         # palm
    for (bx, by, ang, ln, wd) in ((330, 700, -112, 330, 86), (420, 660, -95, 400, 90), (510, 670, -80, 380, 86), (590, 720, -62, 300, 78)):
        a = math.radians(ang); cap((bx * s, by * s), ((bx + ln * math.cos(a)) * s, (by + ln * math.sin(a)) * s), wd * s)
    cap((320 * s, 900 * s), (150 * s, 700 * s), 100 * s)                         # thumb
    return m.filter(ImageFilter.GaussianBlur(2))

def build_hands():
    m = hand_mask(560)
    g = Image.fromarray(gradient(m.width, m.height, (0.5, 0.25, 0.9), (255, 210, 90), (200, 50, 20))).convert("RGBA")
    g.putalpha(m)
    left = g.rotate(-32, Image.BICUBIC, expand=True); right = left.transpose(Image.FLIP_LEFT_RIGHT)
    a = np.asarray(left)[..., 3] > 128; ys, xs = np.nonzero(a); i = xs.argmax()   # left hand's fingertip nearest the centre
    return left, right, (xs[i], ys[i])

# ---------- backgrounds, grain ----------
def make_bg(light):
    if light: arr = gradient(W, H, (0.5, 0.42, 0.75), (240, 239, 236), (186, 184, 182), 1.6)
    else: arr = gradient(W, H, (0.5, 0.55, 0.8), (40, 14, 12), NIGHT, 1.1)
    return Image.fromarray(arr).convert("RGBA")
rng = np.random.default_rng(7)
GRAIN = [Image.fromarray(rng.normal(0, 9, (H // 2, W // 2)).clip(-30, 30).astype(np.int16).astype(np.uint8)) for _ in range(4)]

def add_grain(img, i):
    arr = np.asarray(img.convert("RGB")).astype(np.int16)
    g = np.asarray(GRAIN[i % 4].resize((W, H))).astype(np.int8).astype(np.int16)
    return Image.fromarray(np.clip(arr + g[..., None], 0, 255).astype(np.uint8))

# ---------- text ----------
def words_between(a, b): return [w for w in WORDS if a <= w[1] < b]
def typed(t, ws):
    """Text revealed so far: each word types out letter by letter across its spoken duration."""
    out = []
    for w, s, e in ws:
        if t < s: break
        n = len(w) if t >= e else max(1, int(len(w) * (t - s) / max(0.08, e - s)))
        out.append(w[:n])
    return " ".join(out).lower()

def caption(img, t, ws, y, color, size=50, center=True, x=None):
    txt = typed(t, ws); d = ImageDraw.Draw(img); f = font(F_MED, size)
    full = " ".join(w[0] for w in ws).lower()
    fw = d.textlength(full, font=f)
    x0 = (W - fw) / 2 if center else x
    if txt: d.text((x0, y), txt, font=f, fill=color)
    if int(t * 2.4) % 2 == 0:   # blinking cursor
        cx = x0 + d.textlength(txt, font=f) + 10
        d.rectangle([cx, y + 4, cx + 4, y + size + 6], fill=color)

def big_word(img, word, cx, cy, size, color, t_in, t):
    k = back((t - t_in) / 0.35)
    if k <= 0: return
    f = font(F_BOLD, size); d = ImageDraw.Draw(img)
    tw = d.textlength(word, font=f)
    layer = Image.new("RGBA", (int(tw) + 40, size + 60), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((20, 10), word, font=f, fill=color)
    sc = 0.6 + 0.4 * k
    layer = layer.resize((max(1, int(layer.width * sc)), max(1, int(layer.height * sc))), Image.BICUBIC)
    img.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))

def swoosh(img, t, t0, pts, color, width):
    """A brush stroke that draws itself on over 0.35 s."""
    k = smooth((t - t0) / 0.35)
    if k <= 0: return
    n = max(2, int(len(pts) * k)); d = ImageDraw.Draw(img)
    for i in range(n - 1):
        wdt = int(width * math.sin(math.pi * (i + 1) / len(pts)) + 2)
        d.line([pts[i], pts[i + 1]], fill=color, width=wdt)

def star(img, cx, cy, r, color, alpha):
    pts = [(cx + r * math.cos(a) ** 3, cy + r * 1.35 * math.sin(a) ** 3) for a in np.linspace(0, 2 * math.pi, 120)]
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).polygon(pts, (*color, int(255 * alpha)))
    glow = lay.resize((W // 4, H // 4)).filter(ImageFilter.GaussianBlur(18)).resize((W, H))
    img.alpha_composite(glow); img.alpha_composite(glow); img.alpha_composite(lay)

# ---------- scenes ----------
BG_L, BG_D = make_bg(True), make_bg(False)
SIL = build_silhouettes(); HAND_L, HAND_R, TIP = build_hands()
DRIFT = [("letter", 0.22, 0.30), ("coin", 0.72, 0.27), ("camera", 0.80, 0.62), ("heart", 0.20, 0.66), ("key", 0.55, 0.75), ("vinyl", 0.40, 0.22)]
RING = ["heart", "coin", "camera", "cat", "plant", "letter", "vinyl", "key"]
HANDLE = "@the.dustlight.stories"

def scene_open(img, t):
    d = ImageDraw.Draw(img)
    # 1) big boxed "how do", like a hand-lettered title, slides off left
    k = smooth((t - 0.75) / 0.45)
    if k < 1:
        f = font(F_BOLD, 230); x = lerp(70, -900, k); y = 760
        d.text((x, y), "how do", font=f, fill=INK)
        tw = d.textlength("how do", font=f)
        jit = lambda v: v + rng.integers(-3, 4)
        for (a, b) in (((x + tw * 0.55, y + 20), (x + tw + 30, y + 30)), ((x + tw + 30, y + 30), (x + tw + 24, y + 290)),
                       ((x + tw + 24, y + 290), (x + tw * 0.5, y + 296))):
            d.line([(jit(a[0]), jit(a[1])), (jit(b[0]), jit(b[1]))], fill=INK, width=9)
        for yy in (y + 40, y + 260): d.line([(x + tw + 40, yy), (W, yy)], fill=INK, width=3)
    # 2) typewriter question
    if t > 0.9:
        caption(img, t, words_between(0, 1.9), 880, INK, 54)
        if t > 1.9: caption(img, t, words_between(1.9, 3.4), 960, INK, 54)
    # 3) pixel keepsakes drift in, tumbling
    for i, (n, fx, fy) in enumerate(DRIFT):
        a = smooth((t - 1.9 - i * 0.12) / 0.6)
        if a > 0: paste_icon(img, n, fx * W + 30 * math.sin(t * 1.3 + i), fy * H - 40 * t, 0.55 * a, 12 * math.sin(t * 2 + i), 12)
    # 4) cyan star flash into the dark cut
    if t > 3.05:
        k = (t - 3.05) / 0.35
        img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(200 * smooth(k)))))
        star(img, W * 0.3, H * 0.42, lerp(80, 900, k ** 2), (70, 230, 255), clamp(1.2 - k * 0.4))

def scene_profile(img, t, t0, t1, kind):
    k = (t - t0) / (t1 - t0)
    sil = SIL[kind]; sc = 1.0 + 0.06 * k
    s = sil.resize((int(sil.width * sc), int(sil.height * sc)), Image.BILINEAR)
    x, y = int(W / 2 - s.width * 0.42), int(H - s.height)
    if kind == "warm":
        g = SIL["glow"].resize(s.size); img.alpha_composite(g, (x, y))
    img.alpha_composite(s, (x, y))
    col = (245, 240, 235) if kind == "warm" else INK
    caption(img, t, words_between(t0 - 0.1, t1), 640, col, 56)

ONE = {  # one-word cards: (word, icon, light?)
    3: ("do.", "camera", False), 4: ("notice.", "cat", True), 5: ("keep.", "letter", False)}
def scene_word(img, t, idx, t0, t1):
    word, ic, light = ONE[idx]
    k = (t - t0) / (t1 - t0); col = INK if light else (245, 240, 235)
    if not light:
        swoosh(img, t, t0 + 0.05, [(lerp(60, 900, u), 980 - 380 * u + 60 * math.sin(u * 3)) for u in np.linspace(0, 1, 40)], RED, 70)
    paste_icon(img, ic, W * 0.5 + 40 * k, 760, back((t - t0) / 0.4) * 1.05, -6 + 8 * k, 22)
    caption(img, t, [w for w in words_between(t0 - 0.1, t1) if w[0].lower() in ("in", "what", "you")], 1080, col, 50)
    big_word(img, word, W / 2, 1230, 150, col, t0 + 0.55, t)
    if not light:   # red sparks
        for j in range(5):
            a = j * 1.3 + t * 0.6; r = 330 + 30 * math.sin(t * 3 + j)
            ImageDraw.Draw(img).line([(W / 2 + r * math.cos(a), 760 + r * math.sin(a)), (W / 2 + (r + 34) * math.cos(a), 760 + (r + 34) * math.sin(a))], fill=RED, width=10)

def scene_ring(img, t, t0, t1):
    cx, cy, R = W / 2, 820, 360
    pull = smooth((t - 13.3) / 0.5)
    if pull > 0:   # black hole
        r = 30 + 160 * pull; ImageDraw.Draw(img).ellipse([cx - r, cy - r, cx + r, cy + r], fill=(10, 9, 9))
    for i, n in enumerate(RING):
        a = -math.pi / 2 + i * 2 * math.pi / len(RING) + 0.25 * (t - t0)
        rr = R * (1 - pull) ** 1.5
        sc = back((t - POPS[i]) / 0.3) * (1 - pull) * 0.75
        paste_icon(img, n, cx + rr * math.cos(a), cy + rr * math.sin(a), sc, 15 * math.sin(t * 2 + i) + 400 * pull, 16)
    caption(img, t, words_between(t0, t1), 1380, INK, 50)

def scene_hands(img, t, t0, t1):
    k = smooth((t - t0) / (15.56 - t0)); meet_y = 1080
    gap = lerp(420, 14, k)                                            # fingertips close in until "trust"
    lx, ly = W / 2 - gap - TIP[0], meet_y + 140 * (1 - k) - TIP[1]
    img.alpha_composite(HAND_L, (int(lx), int(ly)))
    img.alpha_composite(HAND_R, (int(W / 2 + gap - (HAND_R.width - TIP[0])), int(ly)))
    if t > 15.56:   # the touch: a warm spark between the fingertips
        g = smooth((t - 15.56) / 0.3) * (1 - 0.5 * smooth((t - 16.1) / 0.5))
        star(img, W / 2, meet_y, 50 + 50 * g, (255, 225, 150), g)
    caption(img, t, words_between(t0 - 0.1, 15.2), 520, (245, 240, 235), 54)
    if t > 15.2: caption(img, t, words_between(15.2, t1), 600, (245, 240, 235), 54)

LET = "TRUST"
LSEED = [(rng.uniform(80, W - 80), rng.uniform(300, H - 300), rng.uniform(-200, 200)) for _ in LET]
def scene_end(img, t, t0):
    f = font(F_BOLD, 220); d = ImageDraw.Draw(img)
    total = sum(d.textlength(c, font=f) for c in LET) + 30 * (len(LET) - 1)
    x = (W - total) / 2; cy = 900
    for i, c in enumerate(LET):
        cw = d.textlength(c, font=f)
        k = smooth((t - t0 - 0.12 * i) / 0.9)
        sx, sy, sr = LSEED[i]
        lay = Image.new("RGBA", (int(cw) + 40, 300), (0, 0, 0, 0)); ImageDraw.Draw(lay).text((20, 20), c, font=f, fill=INK)
        lay = lay.rotate(sr * (1 - k), Image.BICUBIC, expand=True)
        px, py = lerp(sx, x + cw / 2, k), lerp(sy, cy, k)
        img.alpha_composite(lay, (int(px - lay.width / 2), int(py - lay.height / 2)))
        if c == "U": ux = x + cw / 2
        x += cw + 30
    k = smooth((t - t0 - 1.3) / 0.6)   # red pen circle around the U ("you")
    if k > 0:
        pts = [(ux + 95 * math.cos(a), cy + 15 + 135 * math.sin(a)) for a in np.linspace(-1.9, -1.9 + 2 * math.pi * 1.08 * k, 60)]
        d.line(pts, fill=RED, width=8, joint="curve")
    a = smooth((t - t0 - 1.5) / 0.5)
    if a > 0:
        f2 = font(F_MED, 46); s = "show them."; d.text(((W - d.textlength(s, font=f2)) / 2, 1130), s, font=f2, fill=(*INK, int(255 * a)))

def frame(t, i):
    sc = next(j for j in range(len(CUTS) - 1) if CUTS[j] <= t < CUTS[j + 1]) if t < END else len(CUTS) - 2
    t0, t1 = CUTS[sc], CUTS[sc + 1]
    light = sc in (0, 2, 4, 6, 8)
    img = (BG_L if light else BG_D).copy()
    if sc == 0: scene_open(img, t)
    elif sc == 1: scene_profile(img, t, t0, t1, "warm")
    elif sc == 2: scene_profile(img, t, t0, t1, "grey")
    elif sc in ONE: scene_word(img, t, sc, t0, t1)
    elif sc == 6: scene_ring(img, t, t0, t1)
    elif sc == 7: scene_hands(img, t, t0, t1)
    else: scene_end(img, t, t0)
    d = ImageDraw.Draw(img); f = font(F_MED, 30)
    d.text((W - 70 - d.textlength(HANDLE, font=f), 120), HANDLE, font=f, fill=(INK if light else (220, 215, 210)))
    # slow push-in on every scene + a 2-frame white flash at each cut
    z = 1 + 0.035 * clamp((t - t0) / (t1 - t0))
    img = img.resize((int(W * z), int(H * z)), Image.BILINEAR).crop((int(W * (z - 1) / 2), int(H * (z - 1) / 2), int(W * (z - 1) / 2) + W, int(H * (z - 1) / 2) + H))
    if 0 < sc and t - t0 < 2 / FPS: img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, 120)))
    return add_grain(img, i)

# ---------- sound ----------
SR = 48000
def tone(f, dur, amp, decay):
    t = np.arange(int(SR * dur)) / SR; return amp * np.sin(2 * np.pi * f * t) * np.exp(-t * decay)
def synth_audio(path):
    n = int(SR * END); mix = np.zeros(n)
    def add(sig, at):
        a = int(at * SR); b = min(n, a + len(sig)); mix[a:b] += sig[:b - a]
    t = np.arange(n) / SR
    # soft pad: Am - F - C - G, 4.5 s each, detuned sines
    chords = [(220, 261.6, 329.6), (174.6, 220, 261.6), (196, 261.6, 329.6), (196, 246.9, 293.7), (220, 261.6, 329.6)]
    for ci, ch in enumerate(chords):
        s, e = ci * 4.5, min(END, ci * 4.5 + 5.2); seg = (t >= s) & (t < e); tt = t[seg] - s
        env = np.minimum(1, tt / 1.2) * np.minimum(1, (e - s - tt) / 1.2)
        for f in ch: mix[seg] += 0.035 * env * (np.sin(2 * np.pi * f * tt) + 0.6 * np.sin(2 * np.pi * f * 1.003 * tt + 1))
    noise = np.random.default_rng(3).normal(0, 1, int(SR * 0.6))
    for c in CUTS[1:-1]:   # whoosh: noise with a rising-then-falling envelope, smoothed
        env = np.sin(np.pi * np.linspace(0, 1, len(noise))) ** 2
        w = np.convolve(noise * env, np.ones(24) / 24, "same") * 0.16
        add(w, c - 0.42)
    for p in POPS: add(tone(880, 0.12, 0.22, 40), p); add(tone(1320, 0.08, 0.08, 60), p)
    for at, f in ((3.40, 55), (15.56, 65), (16.6, 50)): add(tone(f, 1.4, 0.5, 3.2), at)   # sub booms
    for sc in (3, 4, 5): add(tone(620, 0.18, 0.18, 25), CUTS[sc] + 0.55)                     # word-card tick
    stereo = np.stack([mix, mix], 1).clip(-1, 1)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f64le", "-ar", str(SR), "-ac", "2", "-i", "-", path], input=stereo.astype(np.float64).tobytes(), check=True)

def main(out, preview):
    if preview:
        for s in preview: frame(float(s), 0).save(out.replace(".mp4", f"_{float(s):05.2f}.png"))
        return
    bed = out.replace(".mp4", "_bed.wav"); synth_audio(bed)
    raw = out.replace(".mp4", "_raw.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", raw], stdin=subprocess.PIPE)
    for i in range(int(END * FPS)):
        p.stdin.write(frame(i / FPS, i).tobytes())
        if i % 60 == 0: print(f"frame {i}/{int(END * FPS)}", flush=True)
    p.stdin.close(); assert p.wait() == 0
    # voice ducks the bed, then loudness to -14 LUFS
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-i", VOICE, "-i", bed, "-filter_complex",
                    "[1:a]aresample=48000,aformat=channel_layouts=stereo,asplit[v][vk];[2:a][vk]sidechaincompress=threshold=0.05:ratio=4:release=300[b];"
                    "[v][b]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", str(END), out], check=True)
    os.remove(raw); os.remove(bed)

if __name__ == "__main__":
    assert len(WORDS) == 41 and abs(CUTS[-1] - END) < 1e-9
    main(sys.argv[1], sys.argv[2:])
