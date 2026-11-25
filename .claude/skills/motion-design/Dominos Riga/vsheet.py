# Contact sheet for vertical stills: python3 vsheet.py <dir> <out.jpg> [cols]
import sys, glob, os
from PIL import Image, ImageDraw
fs = sorted(glob.glob(sys.argv[1] + '/*.jpg'), key=lambda f: float(os.path.basename(f)[:-4])); cols = int(sys.argv[3]) if len(sys.argv) > 3 else 10
w, h = 270, 480; rows = -(-len(fs) // cols); sh = Image.new('RGB', (cols * w, rows * (h + 24)), (20, 20, 20)); d = ImageDraw.Draw(sh)
for i, f in enumerate(fs):
    x, y = i % cols * w, i // cols * (h + 24); sh.paste(Image.open(f).resize((w - 4, h)), (x + 2, y + 24)); d.text((x + 6, y + 6), os.path.basename(f)[:-4] + 's', fill='white')
sh.save(sys.argv[2], quality=88)
