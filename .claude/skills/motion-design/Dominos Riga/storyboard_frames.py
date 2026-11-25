# Rough storyboard frames (540x960) from the real assets. Not the final animation.
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

A = 'assets/'
W, H = 540, 960
BLUE, RED, WHITE, NAVY = (0, 100, 145), (227, 24, 55), (255, 255, 255), (8, 30, 52)
F = lambda s, w='Black': ImageFont.truetype(A + f'Montserrat-{w}.ttf', s)
logo = Image.open(A + 'dominos_logo.8a9a8ffbe4ab.png').convert('RGBA')
tile = logo.crop((0, 0, 500, 500))  # the domino tile is the left square of the logo
pz = {n: Image.open(A + f).convert('RGBA') for n, f in
      [('pep', 'PepperoniTOP.png'), ('mar', 'MargheritaTOP.png'), ('bbq', 'BarbecueTOP.png')]}
os.makedirs('frames', exist_ok=True)


def put(im, src, size, cx, cy, rot=0):
    s = src.copy()
    s.thumbnail((size, size))
    if rot:
        s = s.rotate(rot, resample=Image.BICUBIC, expand=True)
    im.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))


def text(d, s, y, size, fill=WHITE, w='Black', x=W / 2):
    f = F(size, w)
    d.text((x, y), s, font=f, fill=fill, anchor='mm')


def frame(bg):
    im = Image.new('RGBA', (W, H), bg)
    return im, ImageDraw.Draw(im)


# 1 Hook: blue field, domino tile lands centre
im, d = frame(BLUE); put(im, tile, 220, W / 2, H / 2, -12); im.save('frames/1.png')

# 2 Tile dot grows into a white disc filling the frame
im, d = frame(BLUE); put(im, tile, 220, W / 2, H / 2)
d.ellipse((W / 2 - 300, H / 2 - 300, W / 2 + 300, H / 2 + 300), fill=WHITE); im.save('frames/2.png')

# 3 Hero pepperoni spins on red, with the line
im, d = frame(RED); put(im, pz['pep'], 470, W / 2, H / 2 + 40, 20)
text(d, 'Tieši no krāsns.', 170, 46); im.save('frames/3.png')

# 4 Camera pulls back: two pizzas side by side
im, d = frame(NAVY); put(im, pz['pep'], 250, W / 2 - 130, H / 2 + 30); put(im, pz['mar'], 250, W / 2 + 130, H / 2 + 30)
text(d, 'Pērc 2 picas', 190, 52); im.save('frames/4.png')

# 5 Third pizza drops in on top with the +1 badge
im, d = frame(NAVY); put(im, pz['pep'], 230, W / 2 - 130, H / 2 + 120); put(im, pz['mar'], 230, W / 2 + 130, H / 2 + 120)
put(im, pz['bbq'], 260, W / 2, H / 2 - 60)
d.ellipse((W / 2 + 60, H / 2 - 190, W / 2 + 190, H / 2 - 60), fill=RED); text(d, '+1', H / 2 - 125, 54, x=W / 2 + 125)
text(d, 'un saņem 1 dāvanā!', 170, 38); im.save('frames/5.png')

# 6 Red badge grows into the code card
im, d = frame(RED)
d.rounded_rectangle((60, 340, W - 60, 620), 36, fill=WHITE)
text(d, 'Atlaides kods', 400, 30, RED, 'ExtraBold'); text(d, 'MORE', 510, 110, BLUE)
text(d, '2+1', 220, 96); im.save('frames/6.png')

# 7 End card: logo, code, URL, terms
im, d = frame(BLUE); put(im, logo, 440, W / 2, 400)
text(d, '2+1 · kods MORE', 560, 40); text(d, 'dominospizza.lv', 640, 32, WHITE, 'SemiBold')
text(d, 'M vai L izmēra picas · min. pasūtījums €12,50', 880, 15, WHITE, 'SemiBold')
text(d, 'Noteikumi un ierobežojumi dominospizza.lv', 905, 15, WHITE, 'SemiBold')
im.save('frames/7.png')
print('ok')
