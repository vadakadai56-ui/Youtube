"""Instagram profile picture: one old lantern glowing in the dark, with floating dust. 1080x1080, Eevee.
usage: ENGINE=EEVEE ~/.dustlight-venv/bin/python channel/instagram/pfp.py OUT.png"""
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from scene import *
rng = random.Random(11); sc = reset("EEVEE")
sc.render.resolution_x = sc.render.resolution_y = 1080; sc.render.resolution_percentage = 100
sc.eevee.taa_render_samples = 48
world_color((0.010, 0.007, 0.006))
brass = mat("brass", (0.55, 0.36, 0.14), 0.35, metal=1.0, noise=0.5)
dark = mat("iron", (0.06, 0.045, 0.035), 0.5, metal=0.6, noise=0.5)
glass = mat("glass", (1.0, 0.8, 0.55), 0.05, emit=(1.0, 0.6, 0.25), emit_str=0.05, alpha=0.06)
flame = mat("flame", (1, 0.8, 0.4), 0.2, emit=(1.0, 0.7, 0.3), emit_str=60)
wood = mat("table", (0.10, 0.06, 0.035), 0.7, noise=0.7)
cube((0, 0, -0.03), (6, 6, 0.06), wood)
cube((0, 1.6, 1.5), (6, 0.1, 3), mat("wall", (0.10, 0.075, 0.06), 0.9, noise=0.5))
cyl((0, 0, 0.03), 0.30, 0.06, dark, bevel=0.01)             # base
cyl((0, 0, 0.08), 0.24, 0.05, brass, bevel=0.01)
g = cyl((0, 0, 0.36), 0.20, 0.50, glass, verts=48); g.visible_shadow = False   # glass chimney
for a in range(4):                                           # cage bars
    t = a * math.pi / 2 + math.pi / 4
    cyl((math.cos(t) * 0.215, math.sin(t) * 0.215, 0.36), 0.012, 0.52, dark)
cyl((0, 0, 0.64), 0.24, 0.05, brass, bevel=0.01)             # cap
cyl((0, 0, 0.71), 0.14, 0.10, dark, bevel=0.01)
torus((0, 0, 0.86), 0.12, 0.014, dark, rot=(math.pi / 2, 0, 0))   # handle
f = sphere((0, 0, 0.30), 0.045, flame, scale=(0.7, 0.7, 1.9)); f.visible_shadow = False   # flame
cyl((0, 0, 0.22), 0.012, 0.06, mat("wick", (0.05, 0.03, 0.02), 0.9))
light("POINT", (0, 0, 0.36), 55, col=(1.0, 0.6, 0.28), size=0.05)
light("AREA", (-1.2, -1.2, 1.4), 6, col=(0.4, 0.45, 1.0), size=2, target=(0, 0, 0.4))
m = mat("mote", (1, 0.9, 0.7), 0.5, emit=(1.0, 0.8, 0.55), emit_str=0.8)
for _ in range(70):
    sphere((rng.uniform(-0.8, 0.8), rng.uniform(-0.5, 0.6), rng.uniform(0.1, 1.1)), rng.uniform(0.002, 0.005), m, seg=6)
camera((0, -2.05, 0.62), (0, 0, 0.42), lens=50, dof=2.05, fstop=2.2)
render(sys.argv[1])
