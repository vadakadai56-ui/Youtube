"""Instagram kit: highlight covers, Reel cover template + guide, and a profile page mock-up.
usage: python3 channel/instagram/make_kit.py PFP.png OUT_DIR"""
import os, sys, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

F = "/usr/share/fonts/opentype/inter/"
def font(name, size): return ImageFont.truetype(F + name, size)
BLACK = "InterDisplay-Black.otf"
BG = (34, 24, 18); CREAM = (243, 230, 200); YELLOW = (255, 214, 64)
pfp_path, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
pfp = Image.open(pfp_path).convert("RGB")


def dusty(w, h, seed=1, base=BG):
    """Dark warm background with a soft centre glow and dust specks."""
    im = Image.new("RGB", (w, h), base); d = ImageDraw.Draw(im)
    glow = Image.new("L", (w, h), 0); ImageDraw.Draw(glow).ellipse((w * 0.1, h / 2 - w * 0.45, w * 0.9, h / 2 + w * 0.45), fill=70)
    glow = glow.filter(ImageFilter.GaussianBlur(w * 0.15))
    im = Image.composite(Image.new("RGB", (w, h), (92, 62, 38)), im, glow); d = ImageDraw.Draw(im)
    rng = random.Random(seed)
    for _ in range(int(w * h / 9000)):
        x, y, r = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(1, 3.2)
        a = rng.randint(60, 170); d.ellipse((x - r, y - r, x + r, y + r), fill=tuple(int(c * a / 255 + b * (1 - a / 255)) for c, b in zip(CREAM, BG)))
    return im


# ---------------------------------------------------------------- highlight icons (drawn at 4x, centred at cx,cy)
def icon(d, kind, cx, cy, s, col=CREAM):
    lw = int(s * 0.07)
    if kind == "start":
        d.ellipse((cx - s, cy - s, cx + s, cy + s), outline=col, width=lw)
        d.polygon([(cx - s * 0.32, cy - s * 0.48), (cx - s * 0.32, cy + s * 0.48), (cx + s * 0.5, cy)], fill=col)
    elif kind == "stories":
        for sx in (-1, 1):
            pts = [(cx, cy - s * 0.55), (cx + sx * s * 0.95, cy - s * 0.75), (cx + sx * s * 0.95, cy + s * 0.55), (cx, cy + s * 0.75)]
            d.line(pts + [pts[0]], fill=col, width=lw, joint="curve")
            for k in range(3):
                yy = cy - s * 0.3 + k * s * 0.28
                d.line([(cx + sx * s * 0.2, yy), (cx + sx * s * 0.75, yy - s * 0.1)], fill=col, width=int(lw * 0.6))
    elif kind == "yours":
        d.rounded_rectangle((cx - s, cy - s * 0.75, cx + s, cy + s * 0.55), radius=s * 0.35, outline=col, width=lw)
        d.polygon([(cx - s * 0.45, cy + s * 0.5), (cx - s * 0.6, cy + s * 0.95), (cx - s * 0.1, cy + s * 0.5)], fill=col)
        h = s * 0.32; hx, hy = cx, cy - s * 0.12
        d.ellipse((hx - h * 1.05, hy - h * 0.75, hx + h * 0.05, hy + h * 0.3), fill=col)
        d.ellipse((hx - h * 0.05, hy - h * 0.75, hx + h * 1.05, hy + h * 0.3), fill=col)
        d.polygon([(hx - h * 1.0, hy - h * 0.1), (hx + h * 1.0, hy - h * 0.1), (hx, hy + h * 1.0)], fill=col)
    elif kind == "behind":
        d.rounded_rectangle((cx - s, cy - s * 0.35, cx + s, cy + s * 0.8), radius=s * 0.08, outline=col, width=lw)
        top = [(cx - s, cy - s * 0.42), (cx + s * 0.95, cy - s * 0.85), (cx + s * 1.02, cy - s * 0.6), (cx - s * 0.95, cy - s * 0.17)]
        d.polygon(top, outline=col, width=lw)
        for k in range(4):
            x0 = cx - s * 0.75 + k * s * 0.48
            d.line([(x0, cy - s * 0.35), (x0 + s * 0.3, cy + s * 0.05)][:2], fill=col, width=int(lw * 0.8)) if False else None
            d.polygon([(x0, cy - s * 0.35), (x0 + s * 0.22, cy - s * 0.35), (x0 + s * 0.42, cy - s * 0.05), (x0 + s * 0.2, cy - s * 0.05)], fill=col)
    elif kind == "soon":
        w = s * 0.62
        d.line([(cx - w - s * 0.12, cy - s), (cx + w + s * 0.12, cy - s)], fill=col, width=lw)
        d.line([(cx - w - s * 0.12, cy + s), (cx + w + s * 0.12, cy + s)], fill=col, width=lw)
        d.line([(cx - w, cy - s), (cx + w * 0.12, cy), (cx - w, cy + s)], fill=col, width=lw, joint="curve")
        d.line([(cx + w, cy - s), (cx - w * 0.12, cy), (cx + w, cy + s)], fill=col, width=lw, joint="curve")
        d.polygon([(cx - w * 0.6, cy + s * 0.9), (cx + w * 0.6, cy + s * 0.9), (cx, cy + s * 0.45)], fill=col)
        d.polygon([(cx - w * 0.45, cy - s * 0.7), (cx + w * 0.45, cy - s * 0.7), (cx, cy - s * 0.35)], fill=col)


HL = [("start", "Start Here"), ("stories", "Stories"), ("yours", "Your Stories"), ("behind", "Behind"), ("soon", "Coming Soon")]
covers = {}
for i, (k, label) in enumerate(HL):
    im = dusty(1080, 1920, seed=10 + i).resize((4320, 7680)); d = ImageDraw.Draw(im)
    icon(d, k, 2160, 3840, 900)
    im = im.resize((1080, 1920), Image.LANCZOS); im.save(os.path.join(out, f"highlight-{i + 1}-{k}.png"))
    covers[k] = (im, label)


# ---------------------------------------------------------------- Reel cover template
def outlined(d, xy, txt, f, fill, stroke=10):
    d.text(xy, txt, font=f, fill=fill, anchor="mm", stroke_width=stroke, stroke_fill=(0, 0, 0))


def reel_cover(bg, top, key, seed=0):
    """1080x1920. Hook text sits at y 300-700 (inside the 3:4 grid crop y 240-1680, clear of the Reels UI)."""
    im = bg.copy(); d = ImageDraw.Draw(im)
    v = Image.new("L", im.size, 0); ImageDraw.Draw(v).rectangle((0, 0, 1080, 1920), fill=0)
    shade = Image.linear_gradient("L").resize((1080, 1920)).point(lambda p: int(max(0, 160 - p * 0.9)))
    im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, shade); d = ImageDraw.Draw(im)
    f = font(BLACK, 104)
    lines = top + [key]
    y = 520 - (len(lines) - 1) * 62
    for j, ln in enumerate(lines):
        outlined(d, (540, y + j * 124), ln, f, YELLOW if j == len(lines) - 1 else (255, 255, 255))
    d.text((540, 1600), "D U S T L I G H T", font=font(BLACK, 34), fill=CREAM, anchor="mm")
    return im


def scene_bg(seed, tint):
    """Placeholder background: the lantern frame, re-cropped and tinted per post."""
    rng = random.Random(seed); z = rng.uniform(1.6, 2.4)
    w = int(1080 / z * 0.5625 * 1.0); h = int(1080 / z)
    x0 = rng.randint(0, 1080 - w); y0 = rng.randint(0, 1080 - h)
    im = pfp.crop((x0, y0, x0 + w, y0 + h)).resize((1080, 1920), Image.LANCZOS).filter(ImageFilter.GaussianBlur(3))
    return Image.blend(im, Image.new("RGB", im.size, tint), 0.25)


full = pfp.resize((1920, 1920)).crop((420, 0, 1500, 1920))
tpl = reel_cover(full, ["YOUR HOOK", "GOES"], "HERE")
tpl.save(os.path.join(out, "reel-cover-template.png"))
g = tpl.copy(); d = ImageDraw.Draw(g)
d.rectangle((0, 240, 1079, 1680), outline=(80, 220, 120), width=6)
d.text((20, 250), "grid crop 3:4 (1080x1440): keep faces and text inside", font=font("Inter-Bold.otf", 30), fill=(80, 220, 120))
d.rectangle((40, 300, 1040, 700), outline=(255, 120, 80), width=4)
d.text((50, 660), "hook text zone (y 300-700)", font=font("Inter-Bold.otf", 28), fill=(255, 120, 80))
d.rectangle((0, 1680, 1079, 1919), fill=(0, 0, 0)); d.text((540, 1800), "Reels caption and buttons cover this area", font=font("Inter-Bold.otf", 30), fill=(200, 200, 200), anchor="mm")
g.save(os.path.join(out, "reel-cover-guide.png"))

# ---------------------------------------------------------------- profile page mock-up (1080 wide)
SAMPLES = [(["THIS IS"], "DUSTLIGHT", full), (["SHE WAITED"], "40 YEARS", None), (["THE LAST"], "LETTER", None),
           (["NOBODY CAME"], "EXCEPT ONE", None), (["HE KEPT"], "THE LIGHT ON", None), (["ONE MORE"], "DAY", None)]
tints = [(40, 60, 120), (120, 60, 30), (30, 80, 60), (90, 40, 70), (100, 90, 40)]
tiles = []
for i, (top, key, bg) in enumerate(SAMPLES):
    bg = bg if bg is not None else scene_bg(i, tints[(i - 1) % len(tints)])
    tiles.append(reel_cover(bg, top, key).crop((0, 240, 1080, 1680)))
W, P = 1080, 40; H = 2340
m = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(m)
ui = lambda s: font("Inter-Bold.otf", s); reg = lambda s: font("Inter-Regular.otf", s); med = lambda s: font("Inter-Medium.otf", s)
d.text((P, 60), "dustlightstories", font=ui(46), fill=(0, 0, 0))
# avatar
av = pfp.resize((250, 250), Image.LANCZOS); mask = Image.new("L", (250, 250), 0); ImageDraw.Draw(mask).ellipse((0, 0, 250, 250), fill=255)
d.ellipse((P - 6, 160 - 6, P + 256, 160 + 256), outline=(220, 220, 220), width=3); m.paste(av, (P, 160), mask)
for j, (n, lab) in enumerate([("6", "posts"), ("0", "followers"), ("1", "following")]):
    x = 430 + j * 220
    d.text((x, 245), n, font=ui(44), fill=(0, 0, 0), anchor="mm"); d.text((x, 300), lab, font=reg(32), fill=(0, 0, 0), anchor="mm")
y = 450
d.text((P, y), "Dustlight | Stories that stay", font=ui(36), fill=(0, 0, 0)); y += 52
d.text((P, y), "Digital creator", font=reg(32), fill=(115, 115, 115)); y += 50
bx = P + d.textlength("stories about the things we forgot ", font=reg(34)); by = y + 6   # candle (the mock-up font has no emoji)
d.rectangle((bx + 8, by + 18, bx + 20, by + 38), fill=(240, 236, 228), outline=(170, 160, 150))
d.ellipse((bx + 9, by + 2, bx + 19, by + 18), fill=(255, 170, 40))
for ln in ["stories about the things we forgot", "tiny 3D stories, new every few days", "watch the full ones on YouTube ↓"]:
    d.text((P, y), ln, font=reg(34), fill=(0, 0, 0)); y += 48
d.text((P, y), "youtube.com/@the.dustlight.stories", font=med(33), fill=(0, 55, 107)); y += 80
bw = (W - 2 * P - 20) // 2
for j, lab in enumerate(["Follow", "Message"]):
    x = P + j * (bw + 20)
    d.rounded_rectangle((x, y, x + bw, y + 80), radius=18, fill=(0, 149, 246) if j == 0 else (239, 239, 239))
    d.text((x + bw / 2, y + 40), lab, font=ui(32), fill=(255, 255, 255) if j == 0 else (0, 0, 0), anchor="mm")
y += 130
for j, (k, _) in enumerate(HL):
    im, label = covers[k]; c = im.crop((0, 420, 1080, 1500)).resize((150, 150), Image.LANCZOS)
    mk = Image.new("L", (150, 150), 0); ImageDraw.Draw(mk).ellipse((0, 0, 150, 150), fill=255)
    x = P + j * 205
    d.ellipse((x - 8, y - 8, x + 158, y + 158), outline=(210, 210, 210), width=3); m.paste(c, (x, y), mk)
    d.text((x + 75, y + 195), label, font=reg(28), fill=(0, 0, 0), anchor="mm")
y += 270
d.line([(0, y), (W, y)], fill=(230, 230, 230), width=2); y += 4
tw = (W - 2 * 4) // 3; th = int(tw * 4 / 3)
for i, t in enumerate(tiles):
    x = (i % 3) * (tw + 4); yy = y + (i // 3) * (th + 4)
    m.paste(t.resize((tw, th), Image.LANCZOS), (x, yy))
    if i < 3:
        px, py = x + tw - 46, yy + 22                       # pinned marker
        d.ellipse((px, py, px + 22, py + 22), fill=(255, 255, 255)); d.line([(px + 11, py + 20), (px + 11, py + 40)], fill=(255, 255, 255), width=4)
m = m.crop((0, 0, W, y + 2 * (th + 4)))
m.save(os.path.join(out, "profile-mockup.png"))
print("ok")
