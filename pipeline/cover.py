"""Shorts cover helper (used by the /yt-thumbnail skill).

usage:
  python3 pipeline/cover.py sheet VIDEO.mp4 OUT.jpg [N]          # contact sheet of N candidate frames, timestamps burned in
  python3 pipeline/cover.py make  VIDEO.mp4 SECONDS OUT.jpg "TOP LINE" ["second line"]
                                                                 # 1080x1920 cover: frame + caption-style text
Text follows the channel caption style: InterDisplay-Black, white, thick black outline, last line in yellow #FFD640.
Text sits between y=300 and y=700 so the Shorts UI (bottom title bar, right-hand buttons) never covers it.
"""
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
YELLOW = (255, 214, 64)
W, H = 1080, 1920


def duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                capture_output=True, text=True).stdout)


def grab(path, t, out):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", path, "-frames:v", "1",
                    "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}", out], check=True)
    return Image.open(out).convert("RGB")


def sheet(path, out, n=12):
    d = duration(path); cols = 4; rows = -(-n // cols); tw, th = 270, 480
    S = Image.new("RGB", (cols * tw, rows * th), (0, 0, 0)); f = ImageFont.truetype(FONT, 30)
    with tempfile.TemporaryDirectory() as tmp:
        for k in range(n):
            t = d * (k + 0.5) / n
            im = grab(path, t, os.path.join(tmp, f"{k}.png")).resize((tw, th))
            ImageDraw.Draw(im).text((10, 10), f"{t:.1f}s", font=f, fill=YELLOW, stroke_width=4, stroke_fill=(0, 0, 0))
            S.paste(im, ((k % cols) * tw, (k // cols) * th))
    S.save(out, quality=90); print("sheet", out)


def fit(d, text, maxw, size):
    while size > 50:
        f = ImageFont.truetype(FONT, size)
        if d.textlength(text, font=f) <= maxw: return f
        size -= 4
    return ImageFont.truetype(FONT, size)


def make(path, t, out, lines):
    with tempfile.TemporaryDirectory() as tmp:
        im = grab(path, t, os.path.join(tmp, "f.png"))
    # darken the top so the text reads on any frame
    shade = Image.new("L", (W, H), 0); sd = ImageDraw.Draw(shade)
    for y in range(900): sd.line([(0, y), (W, y)], fill=int(150 * (1 - y / 900)))
    im = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, shade)
    d = ImageDraw.Draw(im); y = 360
    for i, line in enumerate(lines):
        f = fit(d, line.upper(), W - 120, 120)
        d.text((W / 2, y), line.upper(), font=f, anchor="mm", fill=YELLOW if i == len(lines) - 1 and len(lines) > 1 else (255, 255, 255),
               stroke_width=10, stroke_fill=(0, 0, 0))
        y += int(f.size * 1.15)
    im.save(out, quality=92); print("cover", out, f"from {t:.2f}s", f"(videoCoverMilliseconds={int(t * 1000)})")


if __name__ == "__main__":
    a = sys.argv
    if len(a) >= 4 and a[1] == "sheet": sheet(a[2], a[3], int(a[4]) if len(a) > 4 else 12)
    elif len(a) >= 6 and a[1] == "make": make(a[2], float(a[3]), a[4], a[5:])
    else: sys.exit(__doc__)
