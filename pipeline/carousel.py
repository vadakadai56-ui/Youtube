"""Instagram carousel slides (1080x1350, 4:5) from rendered stills.

usage:  python3 pipeline/carousel.py OUT_DIR "still.png|caption line" ["still.png|caption line" ...]
- Each still is cropped to 4:5 around its centre and scaled up to 1080x1350.
- The caption is one line (or two, wrapped) in the lower third, white with a black outline.
- The last slide is the twist: its caption is larger and yellow, and "Follow for more stories" with D U S T L I G H T sits under it.
- Writes OUT_DIR/01.jpg ... NN.jpg (JPEG, which Instagram expects for carousels).
Make stills with anim.py STILLS mode:  STILLS="w1:3,w2:3" PCT=100 ... anim.py stories/<s> OUT_DIR
"""
import os, sys, textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"


def fit(img):
    r = W / H; w, h = img.size
    if w / h > r: nw = int(h * r); img = img.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else: nh = int(w / r); img = img.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    return img.resize((W, H), Image.LANCZOS)


def text(d, y, s, size, fill, width):
    f = ImageFont.truetype(FONT, size)
    for i, ln in enumerate(textwrap.wrap(s, width)):
        d.text((W / 2, y + i * int(size * 1.15)), ln, font=f, fill=fill, anchor="mm", stroke_width=max(5, size // 10), stroke_fill=(0, 0, 0))


def slide(src, cap, last, n, total):
    img = fit(Image.open(src).convert("RGB")); d = ImageDraw.Draw(img)
    if last:
        text(d, 960, cap, 76, (255, 214, 64), 22)
        text(d, 1240, "Follow for more stories", 40, (255, 255, 255), 40)
        text(d, 1292, "D U S T L I G H T", 32, (255, 236, 200), 40)
    else:
        text(d, 1110, cap, 64, (255, 255, 255), 26)
    ImageDraw.Draw(img).text((W - 40, 50), f"{n}/{total}", font=ImageFont.truetype(FONT, 34), fill=(255, 255, 255),
                             anchor="rm", stroke_width=4, stroke_fill=(0, 0, 0))
    return img


if __name__ == "__main__":
    out = sys.argv[1]; items = [a.split("|", 1) for a in sys.argv[2:]]
    os.makedirs(out, exist_ok=True)
    for i, (src, cap) in enumerate(items, 1):
        slide(src, cap, i == len(items), i, len(items)).save(os.path.join(out, f"{i:02d}.jpg"), quality=92)
    print(f"{len(items)} slides -> {out}")
