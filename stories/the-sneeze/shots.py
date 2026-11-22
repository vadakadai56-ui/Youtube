"""The Sneeze (format 3, "you" + a power, round bean characters): every sneeze rewinds the world ten seconds, which is great
until winter brings a cold, and then Grandma arrives with flowers.
Render: STYLE=lowpoly ENGINE=EEVEE PCT=50 ES=12 $VENV/bin/python pipeline/anim.py stories/the-sneeze OUT all"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
os.environ.setdefault("STYLE", "lowpoly")
import scene                  # noqa
scene.STYLE = os.environ["STYLE"]
from world import *           # noqa
from world import cam as _cam
from characters import bean, ball
import bpy
scene.LOOK = os.environ.get("LOOK") or "comedy"      # per-video grade (scene.LOOKS)

_D = json.load(open(os.path.join(HERE, "durations.json")))
START, _t = {}, 0.0
for _n, _d in _D.items(): START[_n] = _t; _t += _d
YOU = dict(col=(0.35, 0.65, 0.95), tuft=(0.25, 0.15, 0.1), name="you")
FRIEND = dict(col=(0.98, 0.62, 0.35), name="friend")
CRUSH = dict(col=(0.98, 0.6, 0.75), bow=(0.95, 0.95, 0.95), name="crush")
MOM = dict(col=(0.55, 0.8, 0.55), style="adult", name="mom")
GRAN = dict(col=(0.78, 0.6, 0.88), style="gran", name="gran")
BRIGHT = (0.55, 0.6, 0.68)


def lights_day(target=(0, 0.5, 0.6), k=1.0):
    world_color(BRIGHT)
    light("SUN", (0, 0, 5), 2.2 * k, col=(1.0, 0.95, 0.85), rot=(0.8, 0.2, 0.5))
    light("AREA", (0.6, -2.5, 2.2), 90 * k, col=(1.0, 0.95, 0.9), size=3, target=target)


def sneeze(d, t, t0, big=1.0):
    """Wind-up (head back, body stretches), then the snap forward and a squash."""
    if t < t0 - 0.6 or t > t0 + 0.5: return
    if t < t0:
        k = smooth((t - (t0 - 0.6)) / 0.6); d["head"].rotation_euler[0] = 0.35 * k * big; d["root"].scale.z = d["root"].scale.x * (1 + 0.06 * k)
    else:
        k = 1 - smooth((t - t0) / 0.5); d["head"].rotation_euler[0] = -0.45 * k * big; d["root"].scale.z = d["root"].scale.x * (1 - 0.1 * k)


# ---------------------------------------------------------------- sets
def classroom(rng):
    cube((0, 0, -0.05), (10, 10, 0.1), mat("cfloor", (0.45, 0.62, 0.9), 0.6, noise=0.3))
    cube((0, 2.2, 1.5), (8, 0.1, 3), mat("cwall", (0.98, 0.84, 0.42), 0.9, noise=0.1))
    cube((-3.0, 0, 1.5), (0.1, 6, 3), mat("cwall", (0.98, 0.84, 0.42), 0.9, noise=0.1))
    cube((0, 2.14, 1.35), (2.4, 0.03, 1.0), mat("board", (0.12, 0.3, 0.22), 0.8, noise=0.2))
    text("2 + 2 = ?", (-0.4, 2.12, 1.45), 0.18, mat("chalk", (0.95, 0.95, 0.95), 0.9), rot=(math.pi / 2, 0, 0))
    h = clock((1.7, 2.12, 2.1))
    for x in (-0.9, 0.0, 0.9):
        for y in (-0.2, 0.9):
            desk((x, y))
    lights_day()
    return h


def desk(loc):
    x, y = loc; wm = mat("deskwood", (0.7, 0.5, 0.3), 0.6, noise=0.3)
    cube((x, y, 0.5), (0.6, 0.42, 0.04), wm, bevel=0.01)
    for sx in (-0.26, 0.26):
        for sy in (-0.17, 0.17): cube((x + sx, y + sy, 0.25), (0.03, 0.03, 0.5), mat("deskleg", (0.3, 0.3, 0.32), 0.4, metal=0.6))


def clock(loc, r=0.22):
    """Wall clock facing -y. Returns {'min': pivot, 'hr': pivot}: rotate rotation_euler[1] (radians, clockwise = +)."""
    x, y, z = loc
    cyl((x, y, z), r, 0.05, mat("clockrim", (0.85, 0.2, 0.2), 0.4), rot=(math.pi / 2, 0, 0))
    cyl((x, y - 0.03, z), r * 0.88, 0.02, mat("clockface", (0.98, 0.97, 0.93), 0.6), rot=(math.pi / 2, 0, 0))
    hm = mat("hands", (0.05, 0.05, 0.05), 0.4)
    for k in range(12):
        a = k * math.pi / 6; cube((x + r * 0.75 * math.sin(a), y - 0.045, z + r * 0.75 * math.cos(a)), (0.012, 0.005, 0.03), hm, rot=(0, a, 0))
    out = {}
    for name, ln, w in (("min", r * 0.75, 0.012), ("hr", r * 0.5, 0.018)):
        p = empty("clk_" + name, (x, y - 0.05, z)); hnd = cube((x, y - 0.05, z + ln / 2), (w, 0.006, ln), hm)
        hnd.parent = p; hnd.location = Vector(hnd.location) - Vector(p.location); out[name] = p
    return out


def paper(loc, rot=0.0):
    return cube(loc, (0.22, 0.3, 0.003), mat("paper", (0.98, 0.98, 0.95), 0.8), rot=(0, 0, rot))


def pencil(loc):
    p = empty("pencil", loc)
    o = cyl(loc, 0.008, 0.16, mat("pencilwood", (0.98, 0.8, 0.2), 0.5), rot=(0.9, 0, 0)); o.parent = p; o.location = (0, 0, 0)
    return p


def bedroom(rng, snow=True, night=False):
    cube((0, 0, -0.05), (10, 10, 0.1), mat("bfloor", (0.55, 0.38, 0.25), 0.6, noise=0.4))
    wall = mat("bwall", (0.55, 0.78, 0.98), 0.9, noise=0.1)
    cube((-1.0, 2.0, 1.5), (2.0, 0.1, 3), wall); cube((1.6, 2.0, 1.5), (1.2, 0.1, 3), wall); cube((0.5, 2.0, 0.35), (1.0, 0.1, 0.7), wall)
    cube((0.5, 2.0, 2.6), (1.0, 0.1, 0.8), wall); cube((-2.2, 0, 1.5), (0.1, 5, 3), wall)
    cube((0.5, 2.3, 1.45), (1.0, 0.02, 1.4), mat("bsky", (0.75, 0.82, 0.95), 0.5, emit=(0.75, 0.82, 0.95), emit_str=1.2))
    cube((-1.0, 1.1, 0.22), (1.2, 1.7, 0.3), mat("bedframe", (0.6, 0.4, 0.25), 0.6))
    cube((-1.0, 1.1, 0.42), (1.1, 1.6, 0.14), mat("duvet", (0.95, 0.7, 0.3), 0.9, sheen=0.6, noise=0.2), bevel=0.04)
    cube((-1.0, 1.75, 0.53), (0.6, 0.25, 0.1), mat("pillow", (0.98, 0.98, 0.98), 0.9, sheen=0.4), bevel=0.04)
    h = clock((1.6, 1.94, 2.0))
    sn = Snow((0.5, 2.6, 0.5), size=(1.6, 0.5, 2.5), n=120, rng=rng) if snow else None
    lights_day(target=(-0.8, 1.0, 0.5), k=0.7)
    return h, sn


def tissues(rng, n=30, area=((-2, 1.5), (-0.5, 1.8))):
    tm = mat("tissue", (0.98, 0.98, 1.0), 0.95, sheen=0.5)
    for _ in range(n): sphere((rng.uniform(*area[0]), rng.uniform(*area[1]), 0.04), rng.uniform(0.04, 0.07), tm, scale=(1, 1, 0.7), seg=10)


def bouquet(loc, s=1.0, rng=None):
    """An enormous bunch of flowers."""
    x, y, z = loc; g = []; st = mat("stem", (0.2, 0.5, 0.2), 0.7)
    cols = [(0.95, 0.25, 0.35), (0.98, 0.8, 0.2), (0.95, 0.5, 0.8), (0.6, 0.4, 0.95), (1.0, 0.6, 0.2), (0.98, 0.98, 0.98)]
    g.append(sphere((x, y, z), 0.12 * s, mat("wrap", (0.95, 0.9, 0.8), 0.8), scale=(1, 1, 1.6)))
    for k in range(40):
        a = rng.uniform(0, 2 * math.pi); rr = rng.uniform(0, 0.38) * s; hz = z + 0.25 * s + rng.uniform(0, 0.3) * s
        g.append(sphere((x + rr * math.cos(a), y + rr * math.sin(a) * 0.6, hz), rng.uniform(0.05, 0.08) * s, mat("petal%d" % (k % 6), cols[k % 6], 0.6, sheen=0.5), seg=12))
    return group("bouquet", g, loc)


def front_door(rng, open_amt=0.0):
    cube((0, 0, -0.05), (10, 10, 0.1), mat("hall", (0.55, 0.38, 0.25), 0.6, noise=0.4))
    wall = mat("hwall2", (0.98, 0.7, 0.55), 0.9)
    cube((-1.3, 1.0, 1.5), (2.0, 0.1, 3), wall); cube((1.3, 1.0, 1.5), (2.0, 0.1, 3), wall); cube((0, 1.0, 2.55), (0.6, 0.1, 0.9), wall)
    cube((0, 1.6, 1.0), (2, 0.05, 2), mat("outside", (0.85, 0.9, 1.0), 0.5, emit=(0.85, 0.9, 1.0), emit_str=1.0))
    hinge = empty("dhinge2", (-0.3, 1.0, 0))
    d = cube((0, 1.0, 1.05), (0.6, 0.06, 2.1), mat("frontdoor", (0.75, 0.2, 0.2), 0.5), bevel=0.01)
    d.parent = hinge; d.location = Vector(d.location) - Vector(hinge.location); hinge.rotation_euler[2] = 1.7 * open_amt
    lights_day(target=(0, 1.0, 0.8), k=0.8)
    return hinge


# ---------------------------------------------------------------- shots
def s1(rng):            # you discover that every time you sneeze... the world rewinds ten seconds
    h = classroom(rng); y = bean((0, -0.55, 0), **YOU); c = _cam((0.15, -1.75, 0.72), (0, -0.55, 0.62), lens=42, fstop=2.4)
    def upd(t):
        breathe(y, t); sneeze(y, t, 1.9)
        a = -2 * math.pi * 10 / 60 * smooth((t - 1.95) / 0.6)                  # the clock spins back ten seconds' worth, exaggerated
        h["min"].rotation_euler[1] = 1.2 + a * 6; h["hr"].rotation_euler[1] = 0.4 + a
        c.location.y = -1.75 + 0.06 * t
    return upd


def s2(rng):            # it happens in maths class. you write the wrong answer.
    classroom(rng); y = bean((0, -0.55, 0), **YOU); paper((0.0, -0.25, 0.525), 0.1); p = pencil((0.05, -0.28, 0.57))
    c = _cam((0.9, -1.7, 1.3), (0, -0.3, 0.55), lens=34, fstop=3.5)
    def upd(t):
        breathe(y, t); y["R"].rotation_euler[0] = -1.0 + 0.08 * math.sin(t * 14)
        p.location = Vector((0.05 + 0.04 * math.sin(t * 7), -0.28, 0.57))
    return upd


def s3(rng):            # you sneeze. the clock jumps back.: close on the wall clock, hands spinning backwards
    h = classroom(rng); c = _cam((1.55, 1.3, 2.05), (1.7, 2.12, 2.1), lens=40, fstop=2.8)
    def upd(t):
        a = smooth((t - 0.2) / 0.8)
        h["min"].rotation_euler[1] = 1.2 - 2 * math.pi * a; h["hr"].rotation_euler[1] = 0.4 - 0.5 * a
        c.location.x = 1.55 + 0.03 * math.sin(t * 40) * (0.2 < t < 0.6)
    return upd


def s4(rng):            # the answer's gone. the pencil's back in your hand. you write the right one.: the paper, a big green tick
    classroom(rng); paper((0.0, -0.25, 0.525), 0.1); p = pencil((0.05, -0.28, 0.57))
    tick = [cube((0.0, -0.3, 0.53), (0.012, 0.06, 0.003), mat("tick", (0.1, 0.75, 0.25), 0.5, emit=(0.1, 0.75, 0.25), emit_str=0.5), rot=(0, 0, 0.7)),
            cube((0.045, -0.26, 0.53), (0.012, 0.13, 0.003), mat("tick", (0.1, 0.75, 0.25), 0.5, emit=(0.1, 0.75, 0.25), emit_str=0.5), rot=(0, 0, -0.5))]
    c = _cam((0.12, -0.75, 0.95), (0.02, -0.27, 0.53), lens=50, fstop=2.4)
    def upd(t):
        k = smooth((t - 1.6) / 0.4)
        for o in tick: o.scale = (k + 0.001, k + 0.001, 1)
        p.location = Vector((0.06 + 0.03 * math.sin(t * 9) * (t > 1.4), -0.28, 0.57))
    return upd


def s5(rng):            # at lunch, your friend's drink tips over.
    kitchen(rng); lights_day((0, 0.3, 0.6), 0.8)
    f = bean((0.35, 0.6, 0), rot=-0.3, **FRIEND); y = bean((-0.35, 0.3, 0), rot=0.4, **YOU)
    cp, _tea = cup((0.05, 0.25, 0.75))
    c = _cam((0.0, -1.4, 0.95), (0.0, 0.35, 0.7), lens=38, fstop=3)
    def upd(t):
        breathe(f, t); breathe(y, t); f["L"].rotation_euler[0] = -0.9
        cp.rotation_euler[0] = -1.4 * smooth((t - 0.9) / 0.5)
    return upd


def s6(rng):            # you sneeze. you catch the cup before it falls.
    kitchen(rng); lights_day((0, 0.3, 0.6), 0.8)
    f = bean((0.35, 0.6, 0), rot=-0.3, **FRIEND); y = bean((-0.35, 0.3, 0), rot=0.4, **YOU)
    cp, _tea = cup((0.05, 0.25, 0.75))
    c = _cam((-0.8, -0.9, 0.9), (0.0, 0.3, 0.72), lens=40, fstop=2.8)
    def upd(t):
        sneeze(y, t, 0.15); breathe(f, t)
        y["R"].rotation_euler[0] = -1.3 * smooth((t - 0.9) / 0.25)
        cp.rotation_euler[0] = -0.5 * smooth((t - 0.8) / 0.3) * (1 - smooth((t - 1.1) / 0.3))
    return upd


def s7(rng):            # he stares at you. "how did you know?" you don't tell him.
    kitchen(rng); lights_day((0, 0.3, 0.6), 0.8)
    f = bean((0.35, 0.6, 0), rot=-0.5, mouth="open", **FRIEND); y = bean((-0.35, 0.3, 0), rot=0.4, **YOU)
    c = _cam((0.15, -0.7, 0.78), (0.3, 0.6, 0.7), lens=50, fstop=2.2)
    def upd(t):
        breathe(f, t); f["head"].rotation_euler[2] = 0.08 * math.sin(t * 2)
        c.location.x = 0.15 + 0.15 * smooth((t - 2.2) / 1.0)
    return upd


def s8(rng):            # missed shot? sneeze. score.: outside at a hoop
    cube((0, 0, -0.05), (30, 30, 0.1), mat("grass", (0.3, 0.55, 0.25), 0.85, noise=0.3))
    cube((0, 1.2, 0.002), (2.4, 3.0, 0.004), mat("court", (0.75, 0.45, 0.35), 0.8, noise=0.2))
    for x in (-3, -1.6, 1.8, 3.2): tree((x, 4.5, 0), "spring", rng)
    lights_day((0, 1.5, 1.2), 1.0)
    pole = cyl((0, 2.5, 1.2), 0.04, 2.4, mat("pole", (0.3, 0.3, 0.32), 0.4, metal=0.6))
    cube((0, 2.45, 2.35), (0.8, 0.04, 0.55), mat("board2", (0.95, 0.95, 0.95), 0.5))
    torus((0, 2.2, 2.15), 0.16, 0.012, mat("rim", (0.95, 0.4, 0.1), 0.4, metal=0.5))
    y = bean((0, 0.6, 0), rot=math.pi, **YOU); b = ball((0, 0.5, 1.0))
    c = _cam((-1.3, -1.0, 1.0), (-0.2, 1.2, 1.15), lens=28, fstop=5)
    def upd(t):
        sneeze(y, t, 0.85)
        if t < 0.8:                                                       # the first shot clangs off the rim
            k = t / 0.8; b.location = (0.15 * k, 0.5 + 1.75 * k, 1.0 + 1.25 * math.sin(math.pi * k * 0.9))
        else:                                                             # rewound: the second one drops clean through
            k = min(1.0, (t - 0.95) / 0.8); k = max(0.0, k)
            b.location = (0.0, 0.5 + 1.7 * k, 1.0 + 1.4 * math.sin(math.pi * k * 0.85) - 0.35 * max(0, k - 0.9) * 10)
        y["L"].rotation_euler[0] = y["R"].rotation_euler[0] = -2.5 * (t < 0.3 or 0.95 < t < 1.2)
    return upd


def s9(rng):            # said something dumb to your crush? sneeze. say something smooth instead.
    classroom(rng)
    y = bean((-0.3, 0.3, 0), rot=0.6, **YOU); cr = bean((0.3, 0.5, 0), rot=-0.6, **CRUSH)
    c = _cam((0.1, -1.3, 0.8), (0.0, 0.4, 0.62), lens=40, fstop=2.8)
    def upd(t):
        breathe(cr, t); sneeze(y, t, 1.8)
        hot = 1.0 if t < 1.8 else 0.0
        bsdf(y["cheek"]).inputs["Base Color"].default_value = (0.98, 0.5 - 0.35 * hot, 0.5 - 0.35 * hot, 1)
        y["head"].rotation_euler[2] = 0.15 * (t > 2.4); cr["head"].rotation_euler[0] = -0.1 * (t > 2.6)
        y["R"].rotation_euler[1] = -1.2 * smooth((t - 2.6) / 0.4)          # the smooth lean on nothing
    return upd


def s10(rng):           # you start sniffing pepper before every test.
    classroom(rng); y = bean((0, -0.55, 0), **YOU)
    shaker = cyl((0, 0, 0), 0.03, 0.09, mat("shaker", (0.15, 0.15, 0.17), 0.4, metal=0.4))
    c = _cam((0.12, -1.55, 0.72), (0, -0.55, 0.65), lens=48, fstop=2.2)
    def upd(t):
        y["R"].rotation_euler[0] = -2.0; shaker.location = y["root"].location + Vector((0.14, -0.24, 0.5 + 0.02 * math.sin(t * 9)))
        y["head"].rotation_euler[0] = 0.12 * math.sin(t * 6); breathe(y, t)
    return upd


def s11(rng):           # then... winter comes. you wake up with a cold.: in bed, snow outside, red cheeks
    h, sn = bedroom(rng); y = bean((-1.0, 1.15, 0.45), rot=0.0, scarf=(0.9, 0.2, 0.2), mouth="worried", **YOU)
    y["root"].rotation_euler[0] = -1.1                                    # lying back on the pillow
    bsdf(y["cheek"]).inputs["Base Color"].default_value = (1.0, 0.2, 0.2, 1)
    c = _cam((0.6, -1.4, 1.4), (-0.6, 1.2, 0.8), lens=30, fstop=4)
    def upd(t): sn.update(t); c.location.y = -1.4 + 0.08 * t
    return upd


def s12(rng):           # you sneeze. ten seconds back. sneeze again. back. and again. and again.: the same bed shot, looping
    h, sn = bedroom(rng); y = bean((-1.0, 1.15, 0.45), scarf=(0.9, 0.2, 0.2), mouth="worried", **YOU)
    y["root"].rotation_euler[0] = -1.1; bsdf(y["cheek"]).inputs["Base Color"].default_value = (1.0, 0.2, 0.2, 1)
    hits = [x - START["s12"] for x in SNEEZES if START["s12"] <= x < START["s12"] + _D["s12"]]
    c = _cam((-0.2, -0.2, 1.1), (-1.0, 1.2, 0.75), lens=40, fstop=2.8)
    def upd(t):
        sn.update(t % 1.3)                                                # the snow keeps resetting too
        for h0 in hits: sneeze(y, t, h0, big=0.6)
        back = sum(1 for h0 in hits if t > h0)
        h["min"].rotation_euler[1] = 1.0 - 0.6 * back
    return upd


def s13(rng):           # mom walks in with tissues. again. and again. and again.: she enters, rewinds, enters
    h, sn = bedroom(rng); y = bean((-1.0, 1.15, 0.45), scarf=(0.9, 0.2, 0.2), mouth="flat", **YOU)
    y["root"].rotation_euler[0] = -1.1; bsdf(y["cheek"]).inputs["Base Color"].default_value = (1.0, 0.2, 0.2, 1)
    m = bean((1.2, -0.6, 0), rot=2.3, **MOM)
    box = cube((0, 0, 0), (0.14, 0.1, 0.08), mat("tbox", (0.3, 0.6, 0.9), 0.6))
    hits = [x - START["s13"] for x in SNEEZES if START["s13"] <= x < START["s13"] + _D["s13"]]
    c = _cam((0.9, -2.9, 1.6), (-0.4, 0.5, 0.5), lens=26, fstop=6)
    def upd(t):
        last = max([0.0] + [h0 for h0 in hits if t > h0])
        k = min(1.0, (t - last) / 1.0)                                    # she walks in, gets reset, walks in again
        m["root"].location = Vector((0.6 - 0.9 * k, -0.9 + 1.3 * k, 0.02 * abs(math.sin(t * 9))))
        m["R"].rotation_euler[0] = -1.0; box.location = m["root"].location + Vector((-0.18, -0.12, 0.45))
        for h0 in hits: sneeze(y, t, h0, big=0.5)
    return upd


def s14(rng):           # it's been the same ten seconds for what feels like a week.: tissue mountain, exhausted face
    h, sn = bedroom(rng); tissues(rng, 60)
    y = bean((-1.0, 1.15, 0.45), scarf=(0.9, 0.2, 0.2), mouth="flat", **YOU)
    y["root"].rotation_euler[0] = -1.25; bsdf(y["cheek"]).inputs["Base Color"].default_value = (1.0, 0.2, 0.2, 1)
    c = _cam((0.9, -1.8, 1.6), (-0.6, 1.0, 0.4), lens=28, fstop=5)
    def upd(t): c.location.y = -1.8 + 0.05 * t; sn.update(t * 0.2)
    return upd


def s15(rng):           # you hold your breath... and it stops.: cheeks puffed, turning a bit purple
    h, sn = bedroom(rng); y = bean((-1.0, 1.15, 0.45), scarf=(0.9, 0.2, 0.2), mouth="flat", **YOU)
    y["root"].rotation_euler[0] = -0.6
    c = _cam((-0.95, 0.35, 0.95), (-1.0, 1.15, 0.78), lens=46, fstop=2.2)
    body = bsdf(bpy.data.materials["bbody_you"])
    def upd(t):
        k = smooth(t / 1.2) * (1 - smooth((t - 1.6) / 0.4))
        y["head"].scale = (1 + 0.12 * k, 1, 1 - 0.03 * k)
        body.inputs["Base Color"].default_value = (0.35 + 0.3 * k, 0.65 - 0.3 * k, 0.95, 1)
    return upd


def s16(rng):           # the clock finally moves forward. you made it.: the clock ticks on, you flop back, relieved
    h, sn = bedroom(rng, snow=True); y = bean((-1.0, 1.15, 0.45), scarf=(0.9, 0.2, 0.2), **YOU)
    y["root"].rotation_euler[0] = -1.1
    c = _cam((0.4, -0.6, 1.5), (0.6, 1.6, 1.6), lens=30, fstop=4)
    def upd(t):
        tick = int(t * 2); h["min"].rotation_euler[1] = 1.0 + 0.1 * tick; sn.update(t)
        look_at(c, Vector((0.6, 1.6, 1.6)).lerp(Vector((-1.0, 1.15, 0.8)), smooth((t - 1.4) / 0.8)))
    return upd


def s17(rng):           # then the doorbell rings.: the front door, closed, a bell wobbling
    front_door(rng, 0.0); bell = sphere((0.55, 0.93, 1.6), 0.04, mat("bell", (0.95, 0.8, 0.2), 0.3, metal=0.9))
    c = _cam((0.2, -1.4, 1.1), (0, 1.0, 1.0), lens=34, fstop=4)
    def upd(t): bell.location.x = 0.55 + 0.01 * math.sin(t * 60) * (0.2 < t < 1.2); c.location.y = -1.4 + 0.1 * t
    return upd


def s18(rng):           # it's Grandma. holding the biggest bunch of flowers you've ever seen.
    hinge = front_door(rng, 1.0); g = bean((-0.08, 1.35, 0), **GRAN); bq = bouquet((0.32, 1.0, 0.05), s=1.0, rng=rng)
    c = _cam((0.0, -0.7, 0.75), (0.0, 1.1, 0.75), lens=30, fstop=4)
    def upd(t):
        g["root"].location.y = 1.35 - 0.25 * smooth(t / 1.0); bq.location.y = 1.05 - 0.25 * smooth(t / 1.0)
        g["R"].rotation_euler[0] = -1.3; g["L"].rotation_euler[0] = -1.3
        c.location.z = 0.75 + 0.15 * smooth((t - 0.6) / 2.0)
    return upd


def s19(rng):           # "...oh no.": close on your face, nose twitching
    front_door(rng, 1.0); y = bean((0, -0.3, 0), rot=math.pi, mouth="open", **YOU)
    c = _cam((0.05, 0.55, 0.72), (0, -0.3, 0.68), lens=55, fstop=2.0)
    def upd(t):
        y["head"].rotation_euler[0] = 0.12 * smooth(t / 0.8) + 0.02 * math.sin(t * 25)
        y["root"].scale.z = 1 + 0.03 * smooth(t / 0.8)
    return upd


_W = json.load(open(os.path.join(HERE, "words.json")))
SNEEZES = [a for w, a, b in _W if w.lower().strip('."?') in ("sneeze", "sneeze...")] + \
          [a for w, a, b in _W if w.lower().strip('.') == "again" and 37.5 < a < 45]
SHOTS = {n: (globals()[n], _D[n]) for n in _D}
