"""Make Fiverr gig images (1280x769) from the rendered book pages.

Usage: python3 make_gig_images.py RENDER_DIR OUT_DIR
RENDER_DIR holds cover-1.png and pg-NN.png from pdftoppm.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
W, H = 1280, 769
RED, GREEN, GOLD, CREAM, INK = (214, 40, 57), (27, 122, 75), (246, 195, 68), (255, 246, 229), (30, 30, 30)
F = "/usr/share/fonts/truetype/dejavu/"
bold = lambda s: ImageFont.truetype(F + "DejaVuSans-Bold.ttf", s)
serif = lambda s: ImageFont.truetype(F + "DejaVuSerif-Bold.ttf", s)


def page(n):
    return Image.open(os.path.join(src, f"pg-{n:02d}.png")).convert("RGB")


def card(im, h, rot=0):
    im = im.copy()
    im.thumbnail((10_000, h))
    pad = 10
    c = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (255, 255, 255, 255))
    c.paste(im, (pad, pad))
    if rot:
        c = c.rotate(rot, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", (c.width + 30, c.height + 30), (0, 0, 0, 0))
    mask = c.split()[3].point(lambda a: 110 if a else 0)
    sh.paste((0, 0, 0, 255), (15, 22), mask)
    sh = sh.filter(ImageFilter.GaussianBlur(9))
    sh.alpha_composite(c, (15, 15))
    return sh


def pill(d, xy, text, font, fill, fg=(255, 255, 255)):
    x, y = xy
    w = d.textlength(text, font=font)
    d.rounded_rectangle((x, y, x + w + 40, y + font.size + 24), radius=(font.size + 24) // 2, fill=fill)
    d.text((x + 20, y + 10), text, font=font, fill=fg)


def gig1():
    """KDP formatting: cover wrap + interior pages."""
    bg = Image.new("RGBA", (W, H), GREEN + (255,))
    d = ImageDraw.Draw(bg)
    d.text((60, 55), "Amazon KDP", font=bold(40), fill=GOLD)
    d.text((60, 105), "Coloring Book", font=serif(52), fill="white")
    d.text((60, 170), "Interior + Cover", font=serif(52), fill="white")
    y = 290
    for t in ["Print-ready PDFs", "Correct trim, margins & spine", "Passes KDP previewer", "Blank backs, title page"]:
        d.ellipse((62, y + 10, 82, y + 30), fill=GOLD)
        d.text((100, y), t, font=bold(30), fill="white")
        y += 58
    pill(d, (60, 560), "Fast delivery", bold(30), RED)
    cov = Image.open(os.path.join(src, "cover-1.png")).convert("RGB")
    bg.alpha_composite(card(cov, 330), (620, 70))
    for i, n in enumerate((5, 7, 9)):
        bg.alpha_composite(card(page(n), 250, rot=(-6, 0, 6)[i]), (610 + i * 215, 440))
    return bg


def gig2():
    """Original pattern colouring pages."""
    bg = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(bg)
    d.rectangle((0, 0, W, 150), fill=RED)
    d.text((60, 28), "Original Mandala & Pattern", font=serif(52), fill="white")
    d.text((60, 92), "Coloring Pages  •  Commercial Use", font=bold(34), fill=GOLD)
    for i, n in enumerate((7, 11, 15, 19, 21)):
        bg.alpha_composite(card(page(n), 430, rot=(-5, 3, 0, -3, 5)[i]), (20 + i * 245, 205 + (i % 2) * 30))
    pill(d, (W - 470, 690), "Unique designs, never reused", bold(26), GREEN)
    return bg


def gig3():
    """Custom KDP cover."""
    bg = Image.new("RGBA", (W, H), RED + (255,))
    d = ImageDraw.Draw(bg)
    cov = Image.open(os.path.join(src, "cover-1.png")).convert("RGB")
    front = cov.crop((cov.width // 2 + 4, 0, cov.width, cov.height))
    bg.alpha_composite(card(front, 640, rot=-4), (60, 40))
    d.text((690, 120), "Eye-catching", font=serif(54), fill="white")
    d.text((690, 195), "KDP Book Cover", font=serif(54), fill=GOLD)
    y = 320
    for t in ["Full wrap: front, spine, back", "Exact spine for your page count", "Barcode space included", "Print-ready PDF"]:
        d.ellipse((692, y + 10, 712, y + 30), fill=GOLD)
        d.text((728, y), t, font=bold(27), fill="white")
        y += 58
    return bg


for name, fn in (("gig1_kdp_formatting", gig1), ("gig2_pattern_pages", gig2), ("gig3_kdp_cover", gig3)):
    fn().convert("RGB").save(os.path.join(out, name + ".png"))
    print("saved", name)
