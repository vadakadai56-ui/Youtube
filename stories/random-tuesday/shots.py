"""A Random Tuesday (Trend Short, reflective year recap, blocky family): nothing happens all day, and it is perfect.
Shot like a home video (a date stamp in edit_config.overlay).
Render: STYLE=lowpoly ENGINE=EEVEE PCT=50 ES=12 $VENV/bin/python pipeline/anim.py stories/random-tuesday OUT all"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
os.environ.setdefault("STYLE", "lowpoly")
import scene                  # noqa
scene.STYLE = os.environ["STYLE"]
from world import *           # noqa
from world import cam as _cam
from characters import blocky
import bpy
scene.LOOK = os.environ.get("LOOK") or "dream"      # per-video grade (scene.LOOKS)

_D = json.load(open(os.path.join(HERE, "durations.json")))
KID = dict(shirt=(0.85, 0.2, 0.2), pants=(0.15, 0.2, 0.35), style="kid", hat=(0.2, 0.55, 0.85), name="kid")
GRAN = dict(shirt=(0.62, 0.38, 0.6), pants=(0.3, 0.28, 0.35), style="gran", skin="tan", name="gran")
DAD = dict(shirt=(0.3, 0.5, 0.35), pants=(0.25, 0.22, 0.2), style="dad", skin="brown", name="dad")
MUM = dict(shirt=(0.95, 0.75, 0.3), pants=(0.3, 0.3, 0.45), style="mum", skin="tan", name="mum")
SIS = dict(shirt=(0.85, 0.2, 0.2), pants=(0.5, 0.3, 0.45), style="kid", skin="tan", hair=(0.35, 0.2, 0.1), name="sis")   # in my red hoodie


def p(loc, rot=0.0, **kw): return blocky(loc, rot=rot, **kw)


def room(rng, wall=(0.92, 0.85, 0.7), floor=(0.55, 0.4, 0.28), light_col=(1.0, 0.85, 0.65), morning=True):
    cube((0, 0, -0.05), (10, 10, 0.1), mat("rfloor", floor, 0.6, noise=0.4))
    w = mat("rwall_%d" % int(wall[0] * 100), wall, 0.9, noise=0.12)
    cube((0, 1.6, 1.5), (6, 0.1, 3), w); cube((-2.0, 0, 1.5), (0.1, 6, 3), w); cube((2.0, 0, 1.5), (0.1, 6, 3), w)
    cube((0.6, 1.54, 1.4), (0.9, 0.02, 0.8), mat("rwin", (1.0, 0.92, 0.75), 0.5, emit=(1.0, 0.9, 0.7), emit_str=2.5 if morning else 0.3))
    world_color((0.35, 0.32, 0.3))
    light("AREA", (0.6, 1.3, 1.5), 60 if morning else 10, col=light_col, size=1.0, rot=(math.pi / 2, 0, 0))
    light("AREA", (0.3, -2.4, 2.0), 80, col=(1.0, 0.9, 0.8), size=3, target=(0, 0.6, 0.6))


def r1(rng):            # A random Tuesday in 2026 that I'm going to miss one day.: morning, the kid at the window with a cereal bowl
    room(rng); k = p((0.4, 0.9, 0), rot=math.pi * 0.85, **KID)
    bowl = cyl((0, 0, 0), 0.08, 0.05, mat("bowl", (0.95, 0.95, 0.95), 0.3, coat=0.5))
    c = _cam((-0.5, -1.4, 1.05), (0.4, 0.9, 0.7), lens=34, fstop=3)
    def upd(t):
        k["L"].rotation_euler[0] = -1.1; bowl.location = k["root"].location + Vector((-0.12, -0.2, 0.42)); breathe(k, t)
        c.location.x = -0.5 + 0.05 * t
    return upd


def r2(rng):            # Mum burnt the toast. Again.: black toast pops up, smoke, Mum's hand on her face
    room(rng); cube((-0.3, 0.8, 0.42), (2.0, 0.6, 0.84), mat("rcounter", (0.85, 0.85, 0.82), 0.4))
    toaster = cube((-0.3, 0.8, 0.95), (0.25, 0.15, 0.18), mat("toaster", (0.75, 0.75, 0.78), 0.3, metal=0.7), bevel=0.02)
    toast = [cube((-0.35 + dx, 0.8, 1.0), (0.1, 0.02, 0.1), mat("burnt", (0.08, 0.06, 0.05), 0.9, noise=0.3)) for dx in (0.0, 0.1)]
    sm = Steam((-0.3, 0.8, 1.1), n=14, rng=rng); m = p((0.25, 0.4, 0), rot=math.pi * 0.85, **dict(MUM, mouth="flat"))
    c = _cam((0.2, -0.8, 1.15), (-0.15, 0.7, 0.95), lens=38, fstop=2.8)
    def upd(t):
        up = smooth((t - 0.4) / 0.2)
        for o in toast: o.location.z = 1.0 + 0.07 * up
        sm.update(t, strength=3.0 * up); m["R"].rotation_euler[0] = -2.3 * smooth((t - 1.4) / 0.3)    # the facepalm
    return upd


def r3(rng):            # Dad sang in the car. Badly.: inside the car, Dad belting it out, the kid's flat side-eye
    cube((0, 0, 0.1), (1.4, 2.0, 0.2), mat("carfloor", (0.2, 0.2, 0.22), 0.7))
    seat = mat("seat", (0.35, 0.3, 0.3), 0.8)
    for x in (-0.3, 0.3):
        cube((x, 0.2, 0.35), (0.42, 0.42, 0.1), seat); cube((x, 0.42, 0.65), (0.42, 0.08, 0.55), seat)
    cube((0, -0.45, 0.65), (1.3, 0.3, 0.3), mat("dash", (0.15, 0.15, 0.17), 0.5))
    wheel = torus((-0.3, -0.22, 0.85), 0.14, 0.018, mat("wheel", (0.1, 0.1, 0.1), 0.4), rot=(1.2, 0, 0))
    cube((0, -0.9, 1.1), (1.6, 0.05, 0.6), mat("windscreen", (0.6, 0.7, 0.85), 0.2, emit=(0.6, 0.7, 0.85), emit_str=1.5))
    d = p((-0.3, 0.2, 0.25), rot=0.0, **dict(DAD, mouth="open")); k = p((0.3, 0.2, 0.25), rot=-0.4, **dict(KID, mouth="flat"))
    for f in (d, k):
        for l in ("LL", "LR"): f[l].rotation_euler[0] = -math.pi / 2
    world_color((0.3, 0.35, 0.45))
    pass_l = light("POINT", (1.5, 0, 1.2), 60, col=(1.0, 0.8, 0.55), size=0.3)
    light("AREA", (0, -1.5, 1.6), 50, col=(0.85, 0.9, 1.0), size=2, target=(0, 0.2, 0.8))
    c = _cam((0.05, -0.75, 1.0), (0, 0.25, 0.8), lens=26, fstop=3)
    def upd(t):
        d["head"].rotation_euler[0] = -0.2 + 0.12 * math.sin(t * 7); d["R"].rotation_euler[1] = -1.6 - 0.3 * math.sin(t * 7)
        pass_l.location = Vector((1.5, 1.5 - (t * 3.0) % 3.0, 1.2))             # street lights sliding past
        k["head"].rotation_euler[2] = 0.35
    return upd


def r4(rng):            # My sister stole my hoodie.: she runs past in my red hoodie, grinning
    room(rng, wall=(0.75, 0.85, 0.92)); s = p((-1.2, 0.3, 0), rot=-1.4, **SIS)
    k = p((0.8, 0.6, 0), rot=0.6, **dict(KID, shirt=(0.95, 0.95, 0.95), mouth="open"))         # me in just a T-shirt
    c = _cam((0.0, -1.6, 0.85), (0.0, 0.4, 0.6), lens=30, fstop=4)
    def upd(t):
        x = -1.2 + 1.3 * t; s["root"].location.x = x; ph = t * 14
        s["LL"].rotation_euler[0] = 0.6 * math.sin(ph); s["LR"].rotation_euler[0] = -0.6 * math.sin(ph); s["root"].location.z = 0.03 * abs(math.sin(ph))
        k["head"].rotation_euler[2] = 0.5 * smooth(t / 1.5) - 0.25
    return upd


def r5(rng):            # Grandma called. Just to ask if I'd eaten.: split: Grandma on her phone in her kitchen, cardigan, smiling
    room(rng, wall=(0.95, 0.8, 0.75)); g = p((0.0, 0.5, 0), rot=-0.2, **GRAN)
    ph = cube((0, 0, 0), (0.05, 0.02, 0.1), mat("gphone", (0.15, 0.15, 0.17), 0.3))
    pl = cyl((0.9, 1.3, 0.9), 0.08, 0.12, mat("pot", (0.75, 0.4, 0.25), 0.7)); sphere((0.9, 1.3, 1.05), 0.12, mat("leaf", (0.25, 0.55, 0.25), 0.8))
    c = _cam((0.15, -1.0, 0.85), (0.0, 0.5, 0.72), lens=40, fstop=2.6)
    def upd(t):
        g["R"].rotation_euler[0] = -2.5; ph.location = g["root"].location + Vector((0.16, -0.05, 0.68))
        g["head"].rotation_euler[2] = 0.12 * math.sin(t * 2.5); breathe(g, t)
    return upd


def r6(rng):            # Nothing happened.: the kid flat on the sofa, staring at the ceiling
    room(rng, morning=False); sofa = mat("sofa", (0.45, 0.55, 0.7), 0.9, sheen=0.5)
    cube((0, 0.8, 0.22), (1.6, 0.6, 0.35), sofa, bevel=0.06); cube((0, 1.05, 0.5), (1.6, 0.15, 0.5), sofa, bevel=0.06)
    k = p((0.0, 0.8, 0.42), **dict(KID, mouth="flat")); k["root"].rotation_euler = (-math.pi / 2, 0, math.pi / 2)
    c = _cam((0.0, -0.2, 1.6), (0.0, 0.8, 0.45), lens=34, fstop=3)
    def upd(t): breathe(k, t, 0.4)
    return upd


def r7(rng):            # And it was perfect.: evening, the whole family squashed on the sofa in the TV glow
    room(rng, morning=False); sofa = mat("sofa", (0.45, 0.55, 0.7), 0.9, sheen=0.5)
    cube((0, 0.8, 0.22), (2.2, 0.6, 0.35), sofa, bevel=0.06); cube((0, 1.05, 0.5), (2.2, 0.15, 0.5), sofa, bevel=0.06)
    fam = [p((x, 0.75, 0.3), **kw) for x, kw in ((-0.75, DAD), (-0.25, dict(SIS, mouth="smile")), (0.25, KID), (0.75, MUM))]
    for f in fam:
        for l in ("LL", "LR"): f[l].rotation_euler[0] = -math.pi / 2
    tv = light("AREA", (0, -1.2, 0.9), 40, col=(0.55, 0.7, 1.0), size=0.8, target=(0, 0.8, 0.6))
    c = _cam((0.0, -1.9, 0.95), (0, 0.8, 0.65), lens=30, fstop=4)
    def upd(t):
        tv.data.energy = 40 + 12 * math.sin(t * 9) * math.sin(t * 3.3)
        for i, f in enumerate(fam): f["head"].rotation_euler[2] = 0.05 * math.sin(t + i)
        c.location.y = -1.9 - 0.12 * t
    return upd


SHOTS = {n: (globals()[n], _D[n]) for n in _D}

CALM = {"r1", "r5", "r6", "r7"}   # slow shots rendered at 6 fps (edit.py blends to 30)
