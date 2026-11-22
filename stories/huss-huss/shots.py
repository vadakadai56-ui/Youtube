"""Huss Huss (Trend Short, blocky characters): everybody in town is at Thanksgiving dinner except the kid with a basketball,
until Grandma steals the ball and the whole family ends up playing in the snow.
Render: STYLE=lowpoly ENGINE=EEVEE PCT=50 ES=12 $VENV/bin/python pipeline/anim.py stories/huss-huss OUT all"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
os.environ.setdefault("STYLE", "lowpoly")
import scene                  # noqa
scene.STYLE = os.environ["STYLE"]
from world import *           # noqa
from world import cam as _cam
from characters import blocky, ball, stride, _pin
import bpy

_D = json.load(open(os.path.join(HERE, "durations.json")))
START, _t = {}, 0.0
for _n, _d in _D.items(): START[_n] = _t; _t += _d
_W = json.load(open(os.path.join(HERE, "words.json")))
HITS = [a + 0.08 for w, a, b in _W if w.lower().startswith("huss")]          # the ball hits the snow on every "huss"

KID = dict(shirt=(0.85, 0.2, 0.2), pants=(0.15, 0.2, 0.35), style="kid", hat=(0.2, 0.55, 0.85), name="kid", mouth="flat")
GRAN = dict(shirt=(0.62, 0.38, 0.6), pants=(0.3, 0.28, 0.35), style="gran", skin="tan", shoes=(0.98, 0.62, 0.78), name="gran")
DAD = dict(shirt=(0.3, 0.5, 0.35), pants=(0.25, 0.22, 0.2), style="dad", skin="brown", name="dad")
MUM = dict(shirt=(0.95, 0.75, 0.3), pants=(0.3, 0.3, 0.45), style="mum", skin="tan", name="mum")
SIS = dict(shirt=(0.4, 0.7, 0.85), pants=(0.5, 0.3, 0.45), style="kid", skin="tan", hair=(0.35, 0.2, 0.1), name="sis")


def person(loc, rot=0.0, **kw):
    return blocky(loc, rot=rot, **kw)


def slippers(d):
    """Fluffy pink pom-poms on Grandma's slippers."""
    fur = mat("slipfur", (1.0, 0.75, 0.85), 0.95, sheen=1.0, noise=0.4)
    for k in ("LL", "LR"):
        s = sphere((0, 0, 0), 0.055, fur); s.parent = d[k]; s.location = (0, -0.11, -0.24)


def ball_height(T, hand, floor_r=0.09, hits=HITS):
    """Ball centre height at story time T: touches the snow at each hit, reaches the hand halfway between hits."""
    if not hits: return hand
    prev = max([h for h in hits if h <= T], default=None); nxt = min([h for h in hits if h > T], default=None)
    per = 0.8
    if prev is None: prev = nxt - per
    if nxt is None or nxt - prev > 1.3: nxt = prev + per
    p = (T - prev) / (nxt - prev)
    return floor_r + (hand - floor_r) * math.sin(math.pi * min(1, max(0, p)))


def hold_ball(d, b, T, side="R", dribbling=True):
    """Ball under the hand on `side`, bouncing on the HITS; the arm pumps with it."""
    root = d["root"]; s = root.scale.x; sx = 1 if side == "R" else -1
    a = root.rotation_euler[2]; lx, ly = sx * d["arm_x"] * s, -0.13 * s
    off = root.location + Vector((lx * math.cos(a) - ly * math.sin(a), lx * math.sin(a) + ly * math.cos(a), 0))
    hand = d["hand_z"] * s + root.location.z - 0.05
    z = ball_height(T, hand) if dribbling else hand
    b.location = (off.x, off.y, z)
    d[side].rotation_euler[0] = -0.5 + 0.35 * (z - 0.09) / max(0.01, hand - 0.09)


def porch(rng, door_open=0.0, lights=True):
    """The kid's street from the front garden: a house with a hinged door, glowing windows, snow, lamp."""
    cube((0, 0, -0.05), (40, 40, 0.1), mat("gsnow", (0.82, 0.86, 0.95), 0.7, noise=0.2))
    cube((0, -1.4, 0.003), (0.7, 3.4, 0.006), mat("path", (0.5, 0.48, 0.5), 0.8, noise=0.4))
    cube((0, 0.6, 1.1), (3.2, 1.4, 2.2), mat("hwall", (0.62, 0.42, 0.34), 0.85, noise=0.3))
    cube((0, 0.6, 2.45), (3.5, 1.7, 0.5), mat("hroof", (0.3, 0.2, 0.18), 0.8))
    cube((0, 0.6, 2.75), (3.5, 1.7, 0.12), mat("roofsnow2", (0.95, 0.96, 1.0), 0.7))
    inside = mat("doorway", (1, 0.8, 0.5), 0.5, emit=(1, 0.72, 0.4), emit_str=6)
    cube((0, -0.095, 0.6), (0.6, 0.01, 1.2), inside)                                  # warm light behind the door
    hinge = empty("hinge", (-0.3, -0.13, 0))
    dr = cube((0, -0.13, 0.6), (0.6, 0.04, 1.2), mat("fdoor", (0.25, 0.12, 0.08), 0.6, noise=0.5), bevel=0.01)
    dr.parent = hinge; dr.location = Vector(dr.location) - Vector(hinge.location)
    hinge.rotation_euler[2] = -1.6 * door_open
    win = mat("fwin", (1, 0.8, 0.5), 0.4, emit=(1, 0.75, 0.4), emit_str=5)
    for x in (-0.95, 0.95): cube((x, -0.11, 1.3), (0.6, 0.02, 0.55), win)
    if lights: light("POINT", (0, -0.5, 1.5), 25, col=(1.0, 0.75, 0.45), size=0.2)
    for x in (-5.0, 5.0):                                                             # neighbours, all lit up
        cube((x, 1.0, 1.0), (3.0, 1.6, 2.0), mat("nhouse%d" % (x > 0), (0.4, 0.5, 0.65) if x < 0 else (0.45, 0.6, 0.45), 0.8, noise=0.3))
        cube((x, 1.0, 2.25), (3.2, 1.8, 0.5), mat("roofsnow", (0.95, 0.96, 1.0), 0.7))
        for wx in (-0.7, 0.7): cube((x + wx, 0.19, 1.2), (0.5, 0.02, 0.5), win)
    cyl((1.9, -1.6, 1.0), 0.035, 2.0, mat("lampm", (0.08, 0.08, 0.09), 0.4, metal=0.8))
    sphere((1.9, -1.6, 2.05), 0.1, mat("lampglow", (1, 0.85, 0.6), 0.2, emit=(1, 0.78, 0.45), emit_str=18))
    light("POINT", (1.9, -1.6, 1.95), 60, col=(1.0, 0.75, 0.45), size=0.15)
    world_color((0.03, 0.05, 0.12))
    light("SUN", (0, 0, 5), 0.6, col=(0.55, 0.65, 1.0), rot=(0.9, 0.2, 0.4))
    light("AREA", (0.5, -3.5, 2.2), 30, col=(1.0, 0.85, 0.7), size=2.0, target=(0, -1.5, 0.5))
    return {"door": hinge, "win": win}


def flakes(rng, center=(0, -1.5, 0.2), n=200):
    return Snow(center, size=(5, 4, 3), n=n, rng=rng)


# ---------------------------------------------------------------- shots
def h1(rng):            # in my town... everybody goes to Thanksgiving dinner: the whole lit street, a lone kid in the middle
    street(rng); world_color((0.03, 0.04, 0.09))
    k = person((0, 2.0, 0), rot=0.0, **KID); b = ball((0, 1.9, 0.3))
    c = _cam((0.0, -4.5, 1.5), (0, 3.0, 0.7), lens=30, fstop=5); sn = flakes(rng, (0, 1, 0.2))
    def upd(t): c.location.y = -4.5 + 0.55 * t; hold_ball(k, b, START["h1"] + t, dribbling=False); sn.update(t)
    return upd


def h2(rng):            # except me.: close on the kid, flat face, ball on his hip
    porch(rng); k = person((0.2, -2.0, 0), rot=0.15, **KID); b = ball((0, 0, 0.3))
    c = _cam((0.35, -3.25, 0.75), (0.2, -2.0, 0.66), lens=42, fstop=2.2)
    def upd(t): hold_ball(k, b, START["h2"] + t, dribbling=False); k["head"].rotation_euler[2] = -0.1
    return upd


def h3(rng):            # huss. huss. huss.: medium shot, dribbling on the beat
    porch(rng); k = person((0.2, -2.0, 0), rot=0.15, **KID); b = ball((0, 0, 0.3)); sn = flakes(rng)
    c = _cam((0.9, -3.4, 0.6), (0.2, -2.0, 0.45), lens=38, fstop=2.8)
    def upd(t):
        T = START["h3"] + t; hold_ball(k, b, T)
        k["root"].location.z = 0.01 * abs(math.sin(T * 7)); sn.update(t)
    return upd


def h4(rng):            # every window. turkey. pie. laughing.: inside, the blocky family laughing at the table
    dining_room(rng, outside="snow", card=False)
    fam = [person((-0.62, 0.7, 0.0), rot=math.pi / 2, **DAD), person((0.62, 0.7, 0.0), rot=-math.pi / 2, **MUM),
           person((-0.62, 1.25, 0.0), rot=math.pi / 2, **SIS), person((0.0, 1.85, 0.0), rot=math.pi, **dict(GRAN, shoes=(0.98, 0.62, 0.78)))]
    for f in fam:
        for k in ("LL", "LR"): f[k].rotation_euler[0] = -math.pi / 2
        f["root"].location.z = 0.05
    c = _cam((0.0, -1.5, 1.35), (0, 1.0, 0.6), lens=26, fstop=4)
    def upd(t):
        for i, f in enumerate(fam):                                                  # laughing: shoulders bounce, heads tip back
            ph = t * 9 + i * 1.3
            f["root"].location.z = 0.05 + 0.015 * abs(math.sin(ph)) * (t > 2.4)
            f["head"].rotation_euler[0] = (0.25 + 0.05 * math.sin(ph)) * (t > 2.4)
            f["L"].rotation_euler[0] = -0.9; f["R"].rotation_euler[0] = -0.9 + 0.2 * math.sin(ph) * (t > 2.4)
        c.location.y = -1.5 + 0.12 * t
    return upd


def h5(rng):            # me? huss. huss. huss.: wide and lonely, the kid small against the lit house, snow falling
    porch(rng); k = person((0.4, -2.2, 0), rot=0.1, **KID); b = ball((0, 0, 0.3)); sn = flakes(rng, n=320)
    c = _cam((1.2, -6.0, 1.1), (0.2, -1.0, 0.7), lens=32, fstop=5)
    def upd(t):
        T = START["h5"] + t; hold_ball(k, b, T); sn.update(t); c.location.y = -6.0 - 0.1 * t
    return upd


def h6(rng):            # then a door opened.: warm light spills onto the snow
    h = porch(rng); k = person((0.6, -2.2, 0), rot=-0.4, **KID); b = ball((0, 0, 0.3))
    spill = light("SPOT", (0, 0.1, 1.2), 0, col=(1.0, 0.72, 0.4), target=(0, -2.0, 0), spot=1.0)
    c = _cam((2.2, -4.4, 0.9), (0.3, -1.2, 0.6), lens=30, fstop=4)
    def upd(t):
        o = smooth((t - 0.2) / 1.2); h["door"].rotation_euler[2] = -1.6 * o; spill.data.energy = 300 * o
        hold_ball(k, b, START["h6"] + t, dribbling=False); k["head"].rotation_euler[2] = 0.5
    return upd


def h7(rng):            # Grandma. In her slippers.: she steps out; low shot on the fluffy slippers, tilt up
    h = porch(rng, door_open=1.0); g = person((0, -0.5, 0), rot=0.0, **GRAN); slippers(g)
    light("SPOT", (0, 0.1, 1.2), 300, col=(1.0, 0.72, 0.4), target=(0, -2.0, 0), spot=1.0)
    c = _cam((0.15, -1.6, 0.12), (0, -0.6, 0.1), lens=40, fstop=2.4)
    def upd(t):
        stride(g, t, speed=0.25, amp=0.35, rate=1.4)
        up = smooth((t - 0.9) / 1.0)                                                 # tilt up from the slippers to her face
        look_at(c, Vector((0, g["root"].location.y, 0.1 + 0.6 * up))); c.location.z = 0.12 + 0.45 * up
    return upd


def h8(rng):            # she stole my ball.: Grandma swipes it, the kid freezes
    porch(rng, door_open=1.0)
    k = person((0.35, -2.2, 0), rot=-0.6, **KID); g = person((-0.15, -1.9, 0), rot=0.4, **GRAN); slippers(g); b = ball((0, 0, 0.3))
    c = _cam((-1.3, -3.7, 0.75), (0.1, -2.0, 0.45), lens=36, fstop=3.5)
    def upd(t):
        T = START["h8"] + t
        if t < 0.5: hold_ball(k, b, T, dribbling=False)
        else:
            p = smooth((t - 0.5) / 0.35); hold_ball(g, b, T, side="L", dribbling=False)
            kx = k["root"].location + Vector((0.2, -0.13, 0.45)); gx = Vector(b.location)
            b.location = kx.lerp(gx, p); g["L"].rotation_euler[0] = -1.2 * (1 - p) - 0.5
        k["L"].rotation_euler[1] = -0.5 * smooth((t - 0.6) / 0.3); k["R"].rotation_euler[1] = 0.5 * smooth((t - 0.6) / 0.3)
    return upd


def h9(rng):            # huss. huss. HUSS.: Grandma dribbles, proud, the kid's mouth open
    porch(rng, door_open=1.0); sn = flakes(rng)
    g = person((0.0, -2.0, 0), rot=0.25, **GRAN); slippers(g); k = person((0.9, -2.3, 0), rot=-0.9, **dict(KID, mouth="open")); b = ball((0, 0, 0.3))
    c = _cam((0.5, -3.7, 0.65), (0.35, -2.0, 0.5), lens=34, fstop=3.5)
    def upd(t):
        T = START["h9"] + t; hold_ball(g, b, T, side="L"); sn.update(t)
        g["head"].rotation_euler[0] = -0.15; g["root"].location.z = 0.012 * abs(math.sin(T * 7))
        c.location.y = -3.7 + 0.12 * t
    return upd


def h10(rng):           # now nobody in my town is at dinner. huss.: the whole family playing in the snow, door open, table empty
    porch(rng, door_open=1.0); sn = flakes(rng, n=300)
    cast = [person((-0.8, -2.2, 0), **GRAN), person((0.6, -2.5, 0), **KID), person((1.4, -1.8, 0), **DAD),
            person((-1.6, -1.6, 0), **MUM), person((0.0, -1.3, 0), **SIS)]
    slippers(cast[0]); b = ball((0, 0, 0.3))
    c = _cam((0.0, -6.2, 1.5), (0, -1.6, 0.6), lens=30, fstop=6)
    path = [(-0.8, -2.2), (0.6, -2.5), (1.4, -1.8), (-1.6, -1.6), (0.0, -1.3)]
    def upd(t):
        T = START["h10"] + t
        for i, p in enumerate(cast):                                                 # everybody runs in loose circles
            a = t * 1.3 + i * 1.25; x0, y0 = path[i]
            p["root"].location = Vector((x0 + 0.35 * math.cos(a), y0 + 0.25 * math.sin(a), 0.02 * abs(math.sin(a * 4))))
            p["root"].rotation_euler[2] = a + math.pi
            s = math.sin(a * 4); p["LL"].rotation_euler[0] = 0.5 * s; p["LR"].rotation_euler[0] = -0.5 * s
            p["L"].rotation_euler[0] = -0.4 * s; p["R"].rotation_euler[0] = 0.4 * s
        hold_ball(cast[1], b, T); sn.update(t); c.location.y = -6.2 - 0.15 * t
    return upd


SHOTS = {n: (globals()[n], _D[n]) for n in _D}
