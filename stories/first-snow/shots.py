"""First Snow (Trend Short, Christmas kickoff, clay characters): the first-snow sledge race down Miller's Hill. Grandma wins
every year. This year I saw how: she uses a tea tray.
Render (no low-poly for clay): ENGINE=EEVEE PCT=50 ES=12 $VENV/bin/python pipeline/anim.py stories/first-snow OUT all"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
import scene                  # noqa
scene.STYLE = "clay"
from world import *           # noqa
from world import cam as _cam
from characters import clay, clay_mat
import bpy
scene.LOOK = os.environ.get("LOOK") or "comedy"      # per-video grade (scene.LOOKS)

_D = json.load(open(os.path.join(HERE, "durations.json")))
KID = dict(col=(0.85, 0.3, 0.25), style="kid", hat=(0.25, 0.5, 0.85), scarf=(0.95, 0.85, 0.3), name="kid")
GRAN = dict(col=(0.6, 0.4, 0.65), style="old", glasses=True, scarf=(0.9, 0.3, 0.35), hat=(0.95, 0.6, 0.7), name="gran")
DAD = dict(col=(0.3, 0.5, 0.35), style="adult", hat=(0.85, 0.2, 0.2), name="dad")
POST = dict(col=(0.2, 0.3, 0.6), style="adult", hat=(0.15, 0.2, 0.45), name="post")
KID2 = dict(col=(0.95, 0.75, 0.3), style="kid", hat=(0.4, 0.75, 0.45), name="kid2")
SLOPE = math.atan2(2.4, 7.0)                                            # Miller's Hill: 2.4 up over 7 along y


def hill_z(y):
    """Height of the hill's surface at y (top at y = 7, bottom at y = 0)."""
    return max(0.0, min(2.4, y * 2.4 / 7.0))


def hill(rng, snowing=True):
    snow = clay_mat("hsnow", (0.95, 0.96, 1.0), 0.8)
    cube((0, 0, -0.05), (40, 40, 0.1), snow)
    s = cube((0, 3.5, 1.2), (6, 7.4, 0.2), snow, rot=(SLOPE, 0, 0)); s.location.z = 1.15
    cube((0, 9.5, 1.2), (12, 5, 2.4), snow)                              # the flat top
    for x, y in ((-3.2, 2), (3.4, 3.5), (-3.6, 5.5), (3.0, 7.5), (-2.6, 9), (2.4, 10)): tree((x, y, hill_z(y)), "snow", rng)
    world_color((0.55, 0.62, 0.78))
    light("SUN", (0, 0, 5), 1.6, col=(1.0, 0.95, 0.88), rot=(0.7, 0.1, 0.5))
    light("AREA", (1.5, -4.0, 3.0), 50, col=(1.0, 0.95, 0.9), size=4, target=(0, 3, 1))
    return Snow((0, 2.0, 0.5), size=(8, 6, 4), n=300, rng=rng) if snowing else None


def sledge(col=(0.75, 0.25, 0.2)):
    m = clay_mat("sledge_%d" % int(col[0] * 100), col); o = [cube((0, 0, 0.05), (0.32, 0.6, 0.04), m)]
    for sx in (-0.14, 0.14): o.append(cube((sx, 0, 0.02), (0.03, 0.66, 0.03), clay_mat("runner", (0.3, 0.3, 0.32))))
    return group("sledge", o, (0, 0, 0))


def tray():
    m = mat("tray", (0.85, 0.86, 0.9), 0.15, metal=1.0)
    return group("tray", [cyl((0, 0, 0.02), 0.26, 0.02, m, verts=32), torus((0, 0, 0.035), 0.26, 0.015, m)], (0, 0, 0))


def ride(d, s, y, x=0.0):
    """Put rider d on sledge s at y on the slope, sitting, tilted with the hill."""
    z = hill_z(y); s.location = (x, y, z); s.rotation_euler = (SLOPE, 0, math.pi)
    d["root"].location = Vector((x, y, z + 0.03)); d["root"].rotation_euler = (-SLOPE, 0, math.pi * 0)
    d["root"].rotation_euler[2] = 0.0
    for l in ("LL", "LR"): d[l].rotation_euler[0] = -math.pi / 2
    d["L"].rotation_euler[0] = d["R"].rotation_euler[0] = -1.2


# ---------------------------------------------------------------- shots
def f1(rng):            # First snow in our town means one thing.: the kid looks up as the first flakes fall
    sn = hill(rng); k = clay((0.0, -0.5, 0), rot=0.0, mouth="open", **KID)
    c = _cam((0.15, -1.6, 0.55), (0.0, -0.5, 0.6), lens=40, fstop=2.4)
    def upd(t): sn.update(t * 0.6); k["head"].rotation_euler[0] = -0.4 * smooth(t / 1.2); c.location.z = 0.55 - 0.05 * t
    return upd


def f2(rng):            # The sledge race. Down Miller's Hill.: the top of the hill, sledges lined up, the town far below
    sn = hill(rng); ss = [sledge(c) for c in ((0.75, 0.25, 0.2), (0.25, 0.45, 0.75), (0.3, 0.6, 0.3), (0.85, 0.7, 0.2))]
    for i, s in enumerate(ss): s.location = (-1.2 + i * 0.8, 7.4, 2.4); s.rotation_euler = (0, 0, math.pi)
    c = _cam((0.6, 9.2, 3.2), (0.0, 3.0, 1.0), lens=28, fstop=6)
    def upd(t): sn.update(t); c.location.x = 0.6 - 0.2 * t
    return upd


def f3(rng):            # Kids. Dads. Even the postman.: along the start line, each racer in turn
    sn = hill(rng); riders = []
    for i, kw in enumerate((KID2, DAD, POST)):
        s = sledge(((0.25, 0.45, 0.75), (0.3, 0.6, 0.3), (0.85, 0.7, 0.2))[i]); d = clay((0, 0, 0), **kw)
        s.location = (-0.8 + i * 0.8, 7.3, 2.4); d["root"].location = Vector((-0.8 + i * 0.8, 7.3, 2.43))
        for l in ("LL", "LR"): d[l].rotation_euler[0] = -math.pi / 2
        riders.append(d)
    bag = cube((0.95, 7.15, 2.65), (0.18, 0.08, 0.16), clay_mat("postbag", (0.55, 0.3, 0.15)))
    c = _cam((-0.8, 6.0, 2.85), (-0.8, 7.3, 2.75), lens=40, fstop=3)
    def upd(t):
        sn.update(t); x = -0.8 + 0.8 * min(2, int(t / 0.85)) + 0.05 * math.sin(t * 3)
        c.location.x += (x - c.location.x) * 0.25; look_at(c, Vector((c.location.x, 7.3, 2.75)))
    return upd


def f4(rng):            # And every single year... Grandma wins.: everyone racing down, Grandma flying past them all
    sn = hill(rng); racers = []
    for i, kw in enumerate((KID, DAD, POST, KID2)):
        racers.append((clay((0, 0, 0), **kw), sledge(((0.75, 0.25, 0.2), (0.3, 0.6, 0.3), (0.85, 0.7, 0.2), (0.25, 0.45, 0.75))[i]), -1.2 + i * 0.8))
    g = clay((0, 0, 0), **GRAN); gt = tray()
    c = _cam((2.6, -1.0, 1.4), (0, 3.5, 1.2), lens=30, fstop=6)
    def upd(t):
        sn.update(t)
        for i, (d, s, x) in enumerate(racers): ride(d, s, 7.0 - 1.4 * t + 0.1 * i, x)
        gy = 7.6 - 2.3 * max(0.0, t - 0.6); ride(g, gt, max(0.0, gy), 0.4)
        gt.rotation_euler[2] = t * 6.0                                     # the tray spins as it goes
    return upd


def f5(rng):            # Nobody knows how.: at the bottom, everyone scratching their heads, Grandma already sipping tea
    sn = hill(rng, snowing=True)
    folk = [clay((x, -0.6, 0), rot=r, mouth="flat", **kw) for x, r, kw in ((-0.9, 0.4, KID), (-0.3, 0.2, DAD), (0.3, -0.2, POST), (0.9, -0.4, KID2))]
    g = clay((0.0, 0.2, 0), mouth="smile", **GRAN); cupo, _ = cup((0, 0, 0))
    c = _cam((0.0, -2.2, 0.75), (0.0, -0.2, 0.55), lens=32, fstop=4)
    def upd(t):
        sn.update(t)
        for f in folk: f["R"].rotation_euler[0] = -2.6 + 0.15 * math.sin(t * 8)
        g["R"].rotation_euler[0] = -1.6; cupo.location = g["root"].location + Vector((0.2, -0.22, 0.5))
    return upd


def f6(rng):            # This year, I finally saw it.: the kid hiding behind a tree at the top, peeking
    sn = hill(rng); tree((0.35, 7.6, 2.4), "snow", rng); k = clay((0.6, 7.75, 2.4), rot=1.2, **dict(KID, mouth="open"))
    c = _cam((1.6, 6.6, 2.85), (0.55, 7.8, 2.8), lens=40, fstop=2.8)
    def upd(t): sn.update(t); k["root"].location.x = 0.6 - 0.12 * smooth(t / 1.0); k["head"].rotation_euler[2] = 0.3
    return upd


def f7(rng):            # She doesn't use a sledge.: Grandma at the top, no sledge in sight, pulling something from her coat
    sn = hill(rng); g = clay((0.0, 7.6, 2.4), rot=math.pi, **GRAN)
    c = _cam((0.4, 6.5, 2.7), (0.0, 7.6, 2.75), lens=42, fstop=2.6)
    def upd(t): sn.update(t); g["head"].rotation_euler[2] = 0.4 * math.sin(t * 2.2); g["L"].rotation_euler[0] = -0.8
    return upd


def f8(rng):            # She uses a tea tray.: she sits on a silver tea tray and spins off down the hill, waving
    sn = hill(rng); g = clay((0, 0, 0), **GRAN); gt = tray()
    c = _cam((0.6, 5.4, 2.6), (0.0, 7.0, 2.4), lens=34, fstop=3.5)
    def upd(t):
        sn.update(t); y = 7.4 - 2.5 * smooth((t - 0.6) / 1.6) * (t - 0.6 > 0) * max(0, t - 0.6)
        ride(g, gt, y, 0.0); gt.rotation_euler[2] = 4.0 * max(0, t - 0.6); g["R"].rotation_euler[1] = -2.4 + 0.3 * math.sin(t * 6)
        look_at(c, Vector((0.0, y, hill_z(y) + 0.4)))
    return upd


SHOTS = {n: (globals()[n], _D[n]) for n in _D}

CALM = {"f1", "f5", "f6"}   # slow shots rendered at 6 fps (edit.py blends to 30)
