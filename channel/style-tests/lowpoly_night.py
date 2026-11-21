"""Style test: low-poly faceted characters, a snowy pine forest at night, moonlight blue against campfire orange.
usage: STYLE=lowpoly ~/.dustlight-venv/bin/python channel/style-tests/lowpoly_night.py OUT_DIR"""
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from scene import *
from world import peg
import bpy
out = sys.argv[1]; os.makedirs(out, exist_ok=True)


def forest(rng):
    snow = mat("snowground", (0.30, 0.34, 0.45), 0.9, noise=0.3)
    cube((0, 0, -0.05), (40, 40, 0.1), snow)
    pine = [mat("pine%d" % i, c, 0.85, noise=0.4) for i, c in enumerate([(0.05, 0.12, 0.16), (0.04, 0.10, 0.13), (0.06, 0.14, 0.18)])]
    for _ in range(70):
        a = rng.uniform(0, 2 * math.pi); r = rng.uniform(3.0, 14)
        x, y = math.cos(a) * r, abs(math.sin(a)) * r + 1.5
        h = rng.uniform(1.8, 3.6); m = rng.choice(pine)
        for k in range(3):
            bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=h * (0.34 - k * 0.08), depth=h * 0.5, location=(x, y, h * (0.3 + k * 0.22)))
            o = bpy.context.object; o.data.materials.append(m); o.rotation_euler[2] = rng.uniform(0, 3)
            o.data.materials.append(m)
    sphere((-4, 25, 11), 0.9, mat("moon", (1, 1, 1), 0.5, emit=(0.8, 0.85, 1.0), emit_str=6))
    world_color((0.02, 0.035, 0.09))
    light("SUN", (0, 0, 10), 0.9, col=(0.45, 0.55, 1.0), rot=(math.radians(55), 0, math.radians(200)))


def campfire(loc, rng):
    x, y, z = loc; logm = mat("log", (0.25, 0.13, 0.06), 0.8, noise=0.6)
    for k in range(5):
        a = k * 2 * math.pi / 5
        cyl((x + math.cos(a) * 0.16, y + math.sin(a) * 0.16, z + 0.06), 0.045, 0.42, logm, rot=(0, math.radians(70), a), verts=7)
    flame = mat("flame", (1, 0.6, 0.2), 0.3, emit=(1.0, 0.32, 0.05), emit_str=7)
    core = mat("flamecore", (1, 0.9, 0.5), 0.3, emit=(1.0, 0.6, 0.15), emit_str=12)
    for k in range(6):
        bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=rng.uniform(0.05, 0.09), depth=rng.uniform(0.25, 0.45),
                                        location=(x + rng.uniform(-0.07, 0.07), y + rng.uniform(-0.07, 0.07), z + 0.25))
        bpy.context.object.data.materials.append(core if k < 2 else flame)
    light("POINT", (x, y, z + 0.45), 160, col=(1.0, 0.33, 0.07), size=0.15)
    em = mat("ember", (1, 0.6, 0.2), 0.3, emit=(1.0, 0.5, 0.15), emit_str=30)
    for _ in range(40):
        sphere((x + rng.uniform(-0.5, 0.5), y + rng.uniform(-0.5, 0.5), z + rng.uniform(0.4, 2.2)), rng.uniform(0.006, 0.014), em, seg=6)


rng = random.Random(5); sc = reset("EEVEE")
forest(rng); campfire((0.6, 0.3, 0), rng)
cyl((-0.25, 0.25, 0.12), 0.12, 0.9, mat("seatlog", (0.3, 0.16, 0.08), 0.8, noise=0.6), rot=(0, math.radians(90), 0.3), verts=8)
d = peg((-0.25, 0.25, 0.22), (0.62, 0.18, 0.16), kind="walter", rot=0.55, scarf=(0.85, 0.75, 0.3))
snowm = mat("flake", (1, 1, 1), 0.5, emit=(0.8, 0.85, 1.0), emit_str=1.2)
for _ in range(160):
    sphere((rng.uniform(-2, 2), rng.uniform(-1.5, 3), rng.uniform(0.1, 2.6)), rng.uniform(0.006, 0.012), snowm, seg=6)
# shot A: close-up, fire on his face, forest soft behind
camera((0.45, -1.5, 0.98), (-0.25, 0.25, 0.85), lens=55, dof=1.92, fstop=1.8)
render(os.path.join(out, "closeup.png"))
# shot B: wide, the fire and the forest
camera((1.6, -2.6, 1.3), (0.1, 0.4, 0.5), lens=32, dof=3.1, fstop=2.8)
render(os.path.join(out, "wide.png"))
