"""Thanksgiving Timeline (Trend Short, blocky characters, the huss family): Mum yells at the turkey, Dad has no pie, the smoke
alarm joins in, the turkey is still frozen at five, and Grandma walks in at six with a shop-bought pie and a roast chicken.
Render: STYLE=lowpoly ENGINE=EEVEE PCT=50 ES=12 $VENV/bin/python pipeline/anim.py stories/thanksgiving-timeline OUT all"""
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

_D = json.load(open(os.path.join(HERE, "durations.json")))
KID = dict(shirt=(0.85, 0.2, 0.2), pants=(0.15, 0.2, 0.35), style="kid", hat=(0.2, 0.55, 0.85), name="kid")
GRAN = dict(shirt=(0.62, 0.38, 0.6), pants=(0.3, 0.28, 0.35), style="gran", skin="tan", shoes=(0.98, 0.62, 0.78), name="gran")
DAD = dict(shirt=(0.3, 0.5, 0.35), pants=(0.25, 0.22, 0.2), style="dad", skin="brown", name="dad")
MUM = dict(shirt=(0.95, 0.75, 0.3), pants=(0.3, 0.3, 0.45), style="mum", skin="tan", name="mum")
SIS = dict(shirt=(0.4, 0.7, 0.85), pants=(0.5, 0.3, 0.45), style="kid", skin="tan", hair=(0.35, 0.2, 0.1), name="sis")


def p(loc, rot=0.0, **kw): return blocky(loc, rot=rot, **kw)


def arms_up(d, t, rate=7.0, amt=1.0):
    """Yelling: both arms flail up and down."""
    d["L"].rotation_euler[1] = (2.2 + 0.4 * math.sin(t * rate)) * amt; d["R"].rotation_euler[1] = -(2.2 + 0.4 * math.sin(t * rate + 1)) * amt


class Smoke:
    """Big grey puffs pouring out of the oven and rolling up to the ceiling."""
    def __init__(self, base, n=40, rng=None):
        m = mat("smoke", (0.55, 0.55, 0.58), 0.9, alpha=0.55)
        self.base = Vector(base); self.p = [(sphere(base, 0.1, m, seg=12), rng.uniform(0, 2.5), rng.uniform(-1, 1)) for _ in range(n)]
    def update(self, t):
        for o, off, sw in self.p:
            u = ((t + off) % 2.5) / 2.5
            o.location = self.base + Vector((0.4 * sw * u, -0.3 * u, 2.0 * u)); o.scale = (0.5 + 2.5 * u,) * 3


# ---------------------------------------------------------------- set
def home(rng, hour="morning", smoke=False, table=False, frozen=False):
    """The family kitchen-diner: counter and oven on the left, the table on the right, the front door at the back."""
    cube((0, 0, -0.05), (10, 10, 0.1), mat("tfloor", (0.6, 0.45, 0.3), 0.6, noise=0.4))
    wall = mat("twall", (0.95, 0.82, 0.62), 0.9, noise=0.12)
    cube((-1.2, 2.0, 1.5), (2.6, 0.1, 3), wall); cube((1.75, 2.0, 1.5), (2.1, 0.1, 3), wall); cube((0.35, 2.0, 2.55), (0.7, 0.1, 0.9), wall)
    cube((-2.5, 0, 1.5), (0.1, 6, 3), wall); cube((2.8, 0, 1.5), (0.1, 6, 3), wall); cube((0, 0.0, 3.0), (6, 6, 0.1), wall)
    sky = {"morning": (1.0, 0.85, 0.65), "noon": (0.95, 0.95, 1.0), "dusk": (0.95, 0.55, 0.35), "night": (0.15, 0.2, 0.4)}[hour]
    door = empty("tdoorhinge", (0.05, 2.0, 0))
    d = cube((0.35, 2.0, 1.05), (0.6, 0.06, 2.1), mat("tdoor", (0.45, 0.25, 0.15), 0.55, noise=0.4), bevel=0.01)
    d.parent = door; d.location = Vector(d.location) - Vector(door.location)
    cube((0.35, 2.4, 1.05), (1.0, 0.05, 2.2), mat("toutside_" + hour, sky, 0.5, emit=sky, emit_str=1.2))
    cm = mat("counter", (0.85, 0.85, 0.82), 0.4); top = mat("worktop", (0.35, 0.25, 0.2), 0.5, noise=0.4)
    cube((-1.6, 1.0, 0.42), (1.6, 0.6, 0.84), cm); cube((-1.6, 1.0, 0.86), (1.65, 0.65, 0.05), top)
    oven = cube((-1.95, 0.69, 0.42), (0.6, 0.02, 0.6), mat("ovendoor", (0.15, 0.15, 0.16), 0.3, metal=0.5))
    ow = cube((-1.95, 0.675, 0.45), (0.4, 0.01, 0.25), mat("ovenwin", (1.0, 0.45, 0.15), 0.3, emit=(1.0, 0.45, 0.15), emit_str=2))
    tk = turkey((-1.35, 1.0, 0.885))
    if frozen:                                                           # frost and ice cubes on the turkey
        ice = mat("ice", (0.75, 0.9, 1.0), 0.05, coat=1.0, alpha=0.6)
        for _ in range(14): cube((-1.35 + rng.uniform(-0.12, 0.12), 1.0 + rng.uniform(-0.1, 0.1), 0.92 + rng.uniform(0, 0.12)), (0.05, 0.05, 0.05), ice, rot=(rng.uniform(0, 1), rng.uniform(0, 1), 0))
    alarm = cyl((-1.0, 0.6, 2.93), 0.09, 0.04, mat("alarm", (0.95, 0.95, 0.95), 0.4))
    led = sphere((-1.0, 0.52, 2.9), 0.012, mat("led", (1, 0.1, 0.1), 0.3, emit=(1, 0.1, 0.1), emit_str=0))
    tm = mat("dtable2", (0.55, 0.35, 0.2), 0.5, noise=0.5)
    cube((1.2, 0.6, 0.5), (1.2, 0.8, 0.05), tm, bevel=0.01)
    for sx in (0.7, 1.7):
        for sy in (0.3, 0.9): cube((sx, sy, 0.25), (0.05, 0.05, 0.5), tm)
    if table:
        cube((1.2, 0.6, 0.53), (1.0, 0.65, 0.004), mat("tcloth", (0.85, 0.55, 0.25), 0.9, sheen=0.4))
        for x in (0.85, 1.55):
            for y in (0.4, 0.8): plate((x, y, 0.536))
    sm = Smoke((-1.95, 0.6, 0.5), n=40, rng=rng) if smoke else None
    world_color((0.4, 0.38, 0.4))
    light("AREA", (0.35, 1.6, 2.2), 60, col=(1.0, 0.9, 0.75) if hour != "night" else (0.7, 0.75, 1.0), size=2.0, target=(0, 0.5, 0.6))
    light("AREA", (0.3, -2.3, 2.0), 110, col=(1.0, 0.92, 0.85), size=3.0, target=(0, 0.8, 0.7))
    light("POINT", (1.2, 0.6, 2.2), 40, col=(1.0, 0.75, 0.45), size=0.4)
    return {"door": door, "led": led, "smoke": sm, "oven": ow, "turkey": tk}


# ---------------------------------------------------------------- shots
def t1(rng):            # Thanksgiving in my house. A timeline.: the kid to camera, the whole kitchen behind
    home(rng); k = p((0.3, -0.6, 0), **dict(KID, mouth="flat"))
    c = _cam((0.35, -2.1, 0.75), (0.25, 0.2, 0.7), lens=32, fstop=3.5)
    def upd(t): breathe(k, t); c.location.y = -2.1 + 0.08 * t
    return upd


def t2(rng):            # 6 AM. Mum is already yelling at the turkey.
    home(rng); m = p((1.2, 1.25, 0), rot=0.0, **dict(MUM, mouth="open")); turkey((1.2, 0.55, 0.525))
    c = _cam((1.0, -0.9, 0.95), (1.2, 0.8, 0.72), lens=38, fstop=3)
    def upd(t):
        arms_up(m, t); m["root"].location.z = 0.015 * abs(math.sin(t * 10)); m["head"].rotation_euler[0] = -0.1 + 0.05 * math.sin(t * 12)
    return upd


def t3(rng):            # 9 AM. Dad says he's got the pie.: thumbs up, very confident
    home(rng); d = p((0.9, -0.2, 0), rot=-0.2, **DAD)
    c = _cam((0.7, -1.6, 0.8), (0.9, -0.2, 0.62), lens=40, fstop=2.6)
    def upd(t):
        breathe(d, t); d["R"].rotation_euler[0] = -1.4 * smooth(t / 0.4); d["head"].rotation_euler[2] = 0.15 * math.sin(t * 2)
    return upd


def t4(rng):            # He does not have the pie.: the fridge door swings open on one sad egg
    home(rng)
    fr = cube((2.3, 1.2, 0.9), (0.7, 0.7, 1.8), mat("fridge", (0.92, 0.94, 0.96), 0.3, coat=0.4))
    cube((2.3, 0.84, 0.9), (0.66, 0.02, 1.7), mat("fridgein", (0.98, 0.98, 1.0), 0.5, emit=(0.9, 0.95, 1.0), emit_str=1.5))
    sphere((2.3, 0.88, 0.9), 0.035, mat("egg", (0.98, 0.95, 0.85), 0.6), scale=(1, 1, 1.25))
    d = p((1.75, 0.3, 0), rot=-1.2, **dict(DAD, mouth="open"))
    c = _cam((1.2, -0.9, 0.95), (2.2, 0.8, 0.8), lens=34, fstop=3)
    def upd(t):
        d["L"].rotation_euler[1] = 0.9 * smooth((t - 0.8) / 0.4); d["R"].rotation_euler[1] = -0.9 * smooth((t - 0.8) / 0.4)   # the shrug
        d["root"].location.z = 0.03 * smooth((t - 0.8) / 0.4)
    return upd


def t5(rng):            # 1 PM. The smoke alarm agrees with Mum.: smoke pours from the oven, the alarm blinks, Mum yells
    h = home(rng, "noon", smoke=True); m = p((-0.9, 0.0, 0), rot=math.pi * 0.85, **dict(MUM, mouth="open"))
    c = _cam((0.4, -1.4, 1.5), (-1.2, 0.6, 1.6), lens=28, fstop=4)
    led = bsdf(bpy.data.materials["led"])
    def upd(t):
        h["smoke"].update(t); arms_up(m, t, rate=9)
        led.inputs["Emission Strength"].default_value = 20.0 * (int(t * 3) % 2)
        c.location.x = 0.4 + 0.02 * math.sin(t * 35)
    return upd


def t6(rng):            # 5 PM. Everyone's starving.: the family slumped at the empty table
    home(rng, "dusk", table=True)
    fam = [p((0.7, 0.4, 0.05), rot=math.pi / 2 + math.pi, **dict(DAD, mouth="flat")), p((1.7, 0.4, 0.05), rot=-math.pi / 2 + math.pi, **dict(MUM, mouth="flat")),
           p((0.7, 0.85, 0.05), rot=math.pi / 2 + math.pi, **dict(SIS, mouth="flat")), p((1.7, 0.85, 0.05), rot=-math.pi / 2 + math.pi, **dict(KID, mouth="flat"))]
    for i, f in enumerate(fam):
        for k in ("LL", "LR"): f[k].rotation_euler[0] = -math.pi / 2
        f["root"].rotation_euler[2] = (-math.pi / 2 if f["root"].location.x < 1.2 else math.pi / 2)
    c = _cam((1.2, -1.9, 1.55), (1.2, 0.6, 0.65), lens=28, fstop=5)
    def upd(t):
        for i, f in enumerate(fam):
            f["head"].rotation_euler[0] = 0.35 + 0.05 * math.sin(t * 1.5 + i)          # heads drooping
            f["root"].location.z = 0.05 - 0.04 * smooth(t / 2.0)
    return upd


def t7(rng):            # The turkey? Still frozen.: Dad taps it with a fork, it clinks
    home(rng, "dusk", frozen=True); d = p((-1.2, 0.45, 0), rot=math.pi, **dict(DAD, mouth="flat"))
    fork = cube((0, 0, 0), (0.012, 0.012, 0.22), mat("fork", (0.85, 0.85, 0.88), 0.2, metal=1.0))
    c = _cam((-1.0, 0.15, 1.15), (-1.35, 1.0, 0.92), lens=42, fstop=2.4)
    def upd(t):
        tap = abs(math.sin(t * 6)) * (t > 0.5)
        fork.location = (-1.32, 0.82 + 0.05 * tap, 1.02 + 0.04 * tap); fork.rotation_euler = (0.9, 0, 0)
        d["R"].rotation_euler[0] = -1.1
    return upd


def t8(rng):            # 6 PM. Grandma walks in.: the front door opens, Grandma steps in
    h = home(rng, "night", table=True); g = p((0.35, 2.4, 0), **GRAN)
    k = p((-0.7, -0.1, 0), rot=math.pi * 0.85, **dict(KID, mouth="open"))
    c = _cam((1.1, -1.1, 1.0), (0.35, 1.8, 0.85), lens=32, fstop=4)
    def upd(t):
        h["door"].rotation_euler[2] = 1.6 * smooth(t / 0.6)
        g["root"].location.y = 2.4 - 0.8 * smooth((t - 0.4) / 1.6)
        sg = math.sin(t * 8) * (0.4 < t < 2.0); g["LL"].rotation_euler[0] = 0.4 * sg; g["LR"].rotation_euler[0] = -0.4 * sg
    return upd


def t9(rng):            # Shop-bought pie. A roast chicken.: close on Grandma holding them up, a supermarket sticker on the pie
    home(rng, "night", table=True); g = p((0.35, 1.3, 0), **GRAN)
    pi_ = group("pieg", pie((0, 0, 0)), (0, 0, 0)); ch = group("chick", turkey((0, 0, 0))[1:], (0, 0, 0))
    sticker = cube((0, 0, 0), (0.07, 0.003, 0.04), mat("sticker", (1.0, 0.85, 0.1), 0.5, emit=(1.0, 0.85, 0.1), emit_str=0.3))
    c = _cam((0.4, 0.25, 0.85), (0.35, 1.3, 0.72), lens=40, fstop=2.4)
    def upd(t):
        up = smooth(t / 0.5); g["L"].rotation_euler[0] = -1.4 * up; g["R"].rotation_euler[0] = -1.4 * up
        hz = g["hand_z"] + 0.05 + 0.25 * up
        pi_.location = (0.35 - 0.2, 1.15, hz)
        ch.location = (0.35 + 0.2, 1.15, hz)
        sticker.location = (0.15, 1.08, hz + 0.05)
    return upd


def t10(rng):           # Grandma wins Thanksgiving. Again.: everyone cheers, a paper crown, a row of old photos of her winning
    home(rng, "night", table=True)
    g = p((1.2, 1.2, 0), rot=0.0, **GRAN)
    crown = cyl((0, 0, 0), 0.12, 0.08, mat("crown", (1.0, 0.82, 0.2), 0.3, metal=0.8), verts=10)
    fam = [p((0.35, 0.9, 0), rot=-0.9, **dict(DAD, mouth="open")), p((2.05, 0.9, 0), rot=0.9, **dict(MUM, mouth="open")),
           p((0.6, 0.15, 0), rot=-0.5, **dict(KID, mouth="open")), p((1.8, 0.15, 0), rot=0.5, **dict(SIS, mouth="open"))]
    fm = mat("pframe", (0.6, 0.4, 0.2), 0.5); ph = mat("photo", (0.9, 0.85, 0.7), 0.6)
    for i in range(4):                                                   # every year, the same photo: Grandma with a pie
        x = 0.75 + i * 0.3; cube((x, 1.94, 1.75), (0.22, 0.03, 0.28), fm); cube((x, 1.92, 1.75), (0.18, 0.01, 0.24), ph)
        cyl((x, 1.91, 1.7), 0.05, 0.01, mat("photopie", (0.85, 0.55, 0.2), 0.6), rot=(math.pi / 2, 0, 0))
    c = _cam((1.2, -2.0, 1.15), (1.2, 0.9, 0.9), lens=30, fstop=5)
    def upd(t):
        crown.location = g["root"].location + Vector((0, 0.0, 0.98)); g["R"].rotation_euler[1] = -2.6 + 0.2 * math.sin(t * 6)
        for i, f in enumerate(fam): arms_up(f, t + i, rate=8, amt=0.9); f["root"].location.z = 0.03 * abs(math.sin(t * 8 + i))
        c.location.y = -2.0 + 0.12 * t
    return upd


SHOTS = {n: (globals()[n], _D[n]) for n in _D}
