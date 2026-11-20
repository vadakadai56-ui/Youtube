"""Build the KDP interior PDF and cover-wrap PDF for "Cozy Christmas Critters".

Usage:  python3 build.py [--animals DIR] [--out DIR]

- Animal pages: PNG/JPG files in --animals (default ./animals), sorted by name.
  Missing ones are skipped; the book is padded with pattern pages so it always
  has 24 designs.
- Every design is followed by a blank back (single-sided, no bleed-through).
- Interior: 8.5 x 11 in, no bleed, art kept inside 0.5 in margins.
- Cover: KDP wrap = bleed + back + spine + front + bleed, 300 dpi equivalent vector.
"""
import argparse
import glob
import math
import os
import random

from reportlab.lib.colors import HexColor, Color, white, black
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

import patterns

TITLE = "Cozy Christmas Coloring Book"
SUBTITLE = "Cute Critters, Mandalas & Snowflakes for Kids Ages 4-8"
W, H = 8.5 * inch, 11 * inch
MARGIN = 0.75 * inch  # KDP no-bleed minimum is 0.375 in gutter / 0.25 in outside
N_DESIGNS = 24

pdfmetrics.registerFont(TTFont("Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Reg", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))


def pattern_plan(n, seed=2026):
    kinds = ["mandala", "snowflake", "ornament"]
    return [(kinds[i % 3], seed + i * 7) for i in range(n)]


def _measure(kind, seed, R):
    """Render one design alone and return its ink bounding box in points."""
    import subprocess, tempfile
    import numpy as np
    from PIL import Image
    with tempfile.TemporaryDirectory() as d:
        pdf = os.path.join(d, "m.pdf")
        t = canvas.Canvas(pdf, pagesize=(W * 2, H * 2))
        patterns.GENERATORS[kind](t, W, H, R, seed)
        t.save()
        subprocess.run(["pdftoppm", "-r", "36", "-gray", pdf, os.path.join(d, "m")], check=True)
        img = [f for f in os.listdir(d) if f.endswith(".pgm")][0]
        a = np.asarray(Image.open(os.path.join(d, img))) < 200
    ys, xs = np.where(a)
    k = 72 / 36
    hpx = a.shape[0]
    return xs.min() * k, (hpx - ys.max()) * k, xs.max() * k, (hpx - ys.min()) * k


def draw_pattern_page(c, kind, seed):
    """Draw a design scaled and centred so all ink sits inside MARGIN."""
    R = 3.0 * inch
    x0, y0, x1, y1 = _measure(kind, seed, R)
    pad = 6  # points of safety for line width / rasterising error
    s = min((W - 2 * MARGIN - 2 * pad) / (x1 - x0), (H - 2 * MARGIN - 2 * pad) / (y1 - y0))
    cx_off, cy_off = (x0 + x1) / 2 - W, (y0 + y1) / 2 - H  # bbox centre relative to drawing centre
    c.saveState()
    c.translate(W / 2 - cx_off * s, H / 2 - cy_off * s)
    c.scale(s, s)
    patterns.GENERATORS[kind](c, 0, 0, R, seed, lw=3.2 / s)
    c.restoreState()


def draw_image_page(c, path):
    img = ImageReader(path)
    iw, ih = img.getSize()
    s = min((W - 2 * MARGIN) / iw, (H - 2 * MARGIN) / ih)
    w, h = iw * s, ih * s
    c.drawImage(img, (W - w) / 2, (H - h) / 2, w, h)


def title_page(c):
    c.setFont("Bold", 40)
    c.drawCentredString(W / 2, H * 0.62, "Cozy Christmas")
    c.drawCentredString(W / 2, H * 0.62 - 50, "Coloring Book")
    c.setFont("Reg", 16)
    c.drawCentredString(W / 2, H * 0.62 - 95, SUBTITLE)
    patterns.draw_snowflake(c, W / 2, H * 0.3, 1.4 * inch, 11, lw=2.5)


def belongs_page(c):
    c.setLineWidth(3)
    c.roundRect(MARGIN + 0.4 * inch, H * 0.35, W - 2 * MARGIN - 0.8 * inch, H * 0.32, 30, stroke=1, fill=0)
    c.setFont("Bold", 34)
    c.drawCentredString(W / 2, H * 0.58, "This book belongs to:")
    c.setLineWidth(2)
    c.line(W * 0.22, H * 0.44, W * 0.78, H * 0.44)
    patterns.draw_ornament(c, W / 2, H * 0.17, 0.9 * inch, 5, lw=2.5)


def build_interior(animal_files, out):
    c = canvas.Canvas(out, pagesize=(W, H))
    c.setTitle(TITLE)
    pages = 0
    for fn in (title_page, belongs_page):
        fn(c); c.showPage(); c.showPage(); pages += 2
    pats = iter(pattern_plan(N_DESIGNS))
    animals = iter(animal_files)
    for i in range(N_DESIGNS):
        a = next(animals, None) if i % 2 == 0 else None
        if a:
            draw_image_page(c, a)
        else:
            draw_pattern_page(c, *next(pats))
        c.showPage()
        c.showPage()  # blank back
        pages += 2
    c.save()
    return pages


# ---------------- cover ----------------
RED, DRED, GREEN, GOLD, CREAM = (HexColor(x) for x in ("#D62839", "#8E1B2A", "#1B7A4B", "#F6C344", "#FFF6E5"))
PALETTE = [HexColor(x) for x in ("#D62839", "#1B7A4B", "#F6C344", "#2E86DE", "#FF8FAB", "#7FDBDA", "#FFFFFF")]


def colour_bauble(c, x, y, r, col, band):
    c.setStrokeColor(black); c.setLineWidth(r * 0.06)
    c.setFillColor(GOLD)
    c.rect(x - r * 0.22, y + r * 0.9, r * 0.44, r * 0.25, stroke=1, fill=1)
    c.setFillColor(col)
    c.circle(x, y, r, stroke=1, fill=1)
    c.saveState()
    p = c.beginPath(); p.circle(x, y, r); c.clipPath(p, stroke=0, fill=0)
    c.setFillColor(band)
    c.rect(x - r, y - r * 0.18, 2 * r, r * 0.36, stroke=1, fill=1)
    c.setFillColor(white)
    for k in range(-2, 3):
        c.circle(x + k * r * 0.42, y, r * 0.09, stroke=0, fill=1)
    c.restoreState()
    c.setFillColor(white)
    c.circle(x - r * 0.4, y + r * 0.45, r * 0.14, stroke=0, fill=1)


def colour_flake(c, x, y, r, col):
    c.setStrokeColor(col); c.setLineWidth(r * 0.12); c.setLineCap(1)
    for k in range(6):
        a = math.pi / 2 + k * math.pi / 3
        ex, ey = x + math.cos(a) * r, y + math.sin(a) * r
        c.line(x, y, ex, ey)
        for t, L in ((0.55, 0.35), (0.8, 0.22)):
            bx, by = x + math.cos(a) * r * t, y + math.sin(a) * r * t
            for s in (1, -1):
                ba = a + s * math.radians(50)
                c.line(bx, by, bx + math.cos(ba) * r * L, by + math.sin(ba) * r * L)


def front_cover(c, x0, y0, cw, ch, hero=None):
    # background
    c.setFillColor(DRED); c.rect(x0, y0, cw, ch, stroke=0, fill=1)
    steps = 30
    for i in range(steps):
        t = i / steps
        c.setFillColorRGB(0.84 - 0.25 * t, 0.16 - 0.06 * t, 0.22 - 0.06 * t)
        c.rect(x0, y0 + ch * (1 - (i + 1) / steps), cw, ch / steps + 1, stroke=0, fill=1)
    rng = random.Random(4)
    for _ in range(60):
        colour_flake(c, x0 + rng.uniform(0, cw), y0 + rng.uniform(0, ch), rng.uniform(6, 20),
                     Color(1, 1, 1, alpha=rng.uniform(0.25, 0.6)))
    # snowy hill
    c.setFillColor(white)
    p = c.beginPath(); p.moveTo(x0, y0)
    p.lineTo(x0, y0 + ch * 0.2)
    p.curveTo(x0 + cw * 0.3, y0 + ch * 0.28, x0 + cw * 0.6, y0 + ch * 0.14, x0 + cw, y0 + ch * 0.22)
    p.lineTo(x0 + cw, y0); p.close()
    c.drawPath(p, stroke=0, fill=1)
    # hero art (coloured page preview) in a white rounded card
    cx = x0 + cw / 2
    card_w, card_h = cw * 0.62, ch * 0.46
    card_y = y0 + ch * 0.2
    c.setFillColor(white); c.setStrokeColor(GOLD); c.setLineWidth(10)
    c.roundRect(cx - card_w / 2, card_y, card_w, card_h, 30, stroke=1, fill=1)
    if hero:
        img = ImageReader(hero); iw, ih = img.getSize()
        s = min((card_w - 40) / iw, (card_h - 40) / ih)
        c.drawImage(img, cx - iw * s / 2, card_y + (card_h - ih * s) / 2, iw * s, ih * s)
    else:
        c.setFillColor(white); c.setStrokeColor(black)
        c.saveState(); c.translate(0, 0)
        patterns.draw_ornament(c, cx, card_y + card_h * 0.48, card_h * 0.33, 3, lw=4)
        c.restoreState()
    # baubles
    for (fx, fy, r, col, band) in [(0.12, 0.27, 46, PALETTE[2], PALETTE[0]), (0.88, 0.3, 52, PALETTE[1], PALETTE[2]),
                                   (0.9, 0.62, 34, PALETTE[3], PALETTE[6]), (0.1, 0.58, 38, PALETTE[4], PALETTE[1])]:
        colour_bauble(c, x0 + cw * fx, y0 + ch * fy, r, col, band)
    # title banner
    c.setFillColor(GOLD)
    c.setFont("Bold", 56)
    for dy, txt in ((0.87, "Cozy Christmas"), (0.785, "Coloring Book")):
        c.setFillColor(DRED)
        c.drawCentredString(cx + 4, y0 + ch * dy - 4, txt)
        c.setFillColor(white)
        c.drawCentredString(cx, y0 + ch * dy, txt)
    c.setFillColor(GOLD)
    c.setFont("Sans", 22)
    c.drawCentredString(cx, y0 + ch * 0.725, "CRITTERS • MANDALAS • SNOWFLAKES")
    # badge
    c.setFillColor(GREEN); c.setStrokeColor(white); c.setLineWidth(4)
    c.roundRect(cx - cw * 0.33, y0 + ch * 0.07, cw * 0.66, 0.62 * inch, 22, stroke=1, fill=1)
    c.setFillColor(white); c.setFont("Sans", 19)
    c.drawCentredString(cx, y0 + ch * 0.07 + 0.22 * inch, "24 Festive Designs  •  Ages 4-8")


def back_cover(c, x0, y0, cw, ch):
    c.setFillColor(GREEN); c.rect(x0, y0, cw, ch, stroke=0, fill=1)
    rng = random.Random(9)
    for _ in range(50):
        colour_flake(c, x0 + rng.uniform(0, cw), y0 + rng.uniform(0, ch), rng.uniform(6, 18),
                     Color(1, 1, 1, alpha=rng.uniform(0.2, 0.5)))
    cx = x0 + cw / 2
    c.setFillColor(CREAM); c.setStrokeColor(GOLD); c.setLineWidth(8)
    c.roundRect(x0 + cw * 0.1, y0 + ch * 0.38, cw * 0.8, ch * 0.45, 30, stroke=1, fill=1)
    c.setFillColor(DRED); c.setFont("Bold", 34)
    c.drawCentredString(cx, y0 + ch * 0.76, "Get Cozy & Color!")
    c.setFillColor(black); c.setFont("Reg", 17)
    lines = ["Snuggly animals, sparkly snowflakes", "and merry ornaments are waiting", "for your favorite colors.", "",
             "• 24 big, bold, easy-to-color designs", "• Single-sided pages: no bleed-through",
             "• Perfect for crayons, pencils & markers", "• A sweet Christmas gift or stocking stuffer"]
    for i, ln in enumerate(lines):
        c.drawCentredString(cx, y0 + ch * 0.69 - i * 27, ln)
    for k, (col, band) in enumerate([(PALETTE[0], PALETTE[2]), (PALETTE[2], PALETTE[1]), (PALETTE[3], PALETTE[6])]):
        colour_bauble(c, x0 + cw * (0.28 + 0.22 * k), y0 + ch * 0.27, 40, col, band)
    # KDP barcode area (lower right): 2 x 1.2 in, keep white & empty
    c.setFillColor(white)
    c.rect(x0 + cw - 0.25 * inch - 2.0 * inch, y0 + 0.25 * inch, 2.0 * inch, 1.2 * inch, stroke=0, fill=1)


def build_cover(interior_pages, out, hero=None, paper_in=0.002252):
    bleed = 0.125 * inch
    spine = interior_pages * paper_in * inch
    cw, ch = W, H
    total_w = bleed + cw + spine + cw + bleed
    total_h = ch + 2 * bleed
    c = canvas.Canvas(out, pagesize=(total_w, total_h))
    c.setTitle(TITLE + " - Cover")
    # back panel incl. its bleed, then spine, then front incl. its bleed
    back_cover(c, 0, 0, bleed + cw, total_h)
    c.setFillColor(DRED); c.rect(bleed + cw, 0, spine, total_h, stroke=0, fill=1)
    front_cover(c, bleed + cw + spine, 0, cw + bleed, total_h, hero)
    c.save()
    return total_w / inch, total_h / inch, spine / inch


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--animals", default=os.path.join(here, "animals"))
    ap.add_argument("--out", default=os.path.join(here, "output"))
    ap.add_argument("--hero", default=None, help="image for the front cover card")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    files = sorted(glob.glob(os.path.join(a.animals, "*.png")) + glob.glob(os.path.join(a.animals, "*.jpg")))
    n = build_interior(files, os.path.join(a.out, "interior.pdf"))
    hero = a.hero or (files[0] if files else None)
    w, h, s = build_cover(n, os.path.join(a.out, "cover.pdf"), hero)
    print(f"interior: {n} pages ({len(files)} animal pages used)")
    print(f"cover: {w:.3f} x {h:.3f} in, spine {s:.4f} in")
