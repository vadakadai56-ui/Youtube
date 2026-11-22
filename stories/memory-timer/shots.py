"""Memory Timer (format 6, "What if" + real science, round bean characters): you can see how long anyone will remember this
moment. Timers, fact cards and graphs are drawn in edit_config.overlay; the fact-card shots use plain backdrops (cheap to render).
Render: STYLE=lowpoly ENGINE=EEVEE PCT=50 ES=12 $VENV/bin/python pipeline/anim.py stories/memory-timer OUT all"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
os.environ.setdefault("STYLE", "lowpoly")
import scene                  # noqa
scene.STYLE = os.environ["STYLE"]
from world import *           # noqa
from world import cam as _cam
from characters import bean
import bpy
scene.LOOK = os.environ.get("LOOK") or "dream"      # per-video grade (scene.LOOKS)

_D = json.load(open(os.path.join(HERE, "durations.json")))
YOU = dict(col=(0.35, 0.65, 0.95), tuft=(0.25, 0.15, 0.1), name="you")
FRIEND = dict(col=(0.95, 0.6, 0.75), bow=(1, 1, 1), name="friend")
GRAN = dict(col=(0.78, 0.6, 0.88), style="gran", name="gran")
DAD = dict(col=(0.55, 0.75, 0.55), style="adult", name="dad", glasses=True)
FOLK = [dict(col=(0.98, 0.62, 0.35), name="f1"), dict(col=(0.6, 0.85, 0.55), style="adult", name="f2", hat=(0.8, 0.2, 0.25)),
        dict(col=(0.95, 0.85, 0.4), style="adult", name="f3"), dict(col=(0.55, 0.75, 0.85), name="f4", hat=(0.3, 0.7, 0.4))]


def day(target=(0, 0.5, 0.6), k=1.0):
    world_color((0.45, 0.52, 0.62)); light("SUN", (0, 0, 5), 1.8 * k, col=(1.0, 0.95, 0.85), rot=(0.8, 0.2, 0.5))
    light("AREA", (0.6, -2.5, 2.2), 70 * k, col=(1.0, 0.95, 0.9), size=3, target=target)


def street_day(rng):
    cube((0, 0, -0.05), (30, 30, 0.1), mat("pave", (0.7, 0.68, 0.66), 0.8, noise=0.3))
    for i, x in enumerate((-3, -1, 1, 3)):
        cube((x, 3.0, 1.2), (1.8, 1.2, 2.4), mat("shop%d" % i, [(0.85, 0.55, 0.45), (0.55, 0.7, 0.85), (0.9, 0.8, 0.5), (0.6, 0.8, 0.6)][i], 0.8, noise=0.2))
        cube((x, 2.38, 0.8), (1.2, 0.03, 0.9), mat("shopwin", (0.75, 0.85, 0.95), 0.2, emit=(0.8, 0.9, 1.0), emit_str=0.5))
    day((0, 1.0, 0.7))


def room_of(col=(0.9, 0.85, 0.75), night=False):
    cube((0, 0, -0.05), (10, 10, 0.1), mat("mfloor", (0.55, 0.42, 0.3), 0.6, noise=0.4))
    w = mat("mwall_%d" % int(col[1] * 100), col, 0.9, noise=0.1)
    cube((0, 1.6, 1.5), (6, 0.1, 3), w); cube((-2.0, 0, 1.5), (0.1, 6, 3), w); cube((2.0, 0, 1.5), (0.1, 6, 3), w)
    sky = (0.08, 0.1, 0.2) if night else (0.85, 0.9, 1.0)
    cube((0.6, 1.54, 1.4), (0.8, 0.02, 0.8), mat("mwin_%d" % night, sky, 0.5, emit=sky, emit_str=1.5))
    if night:
        world_color((0.05, 0.05, 0.08)); light("POINT", (-0.6, 0.6, 1.4), 30, col=(1.0, 0.7, 0.4), size=0.3)
        light("AREA", (0.3, -2.0, 1.8), 25, col=(0.8, 0.85, 1.0), size=2, target=(0, 0.5, 0.6))
    else: day((0, 0.6, 0.6), 0.9)


def backdrop(col):
    """A plain soft-lit card behind the fact graphics (cheap frames)."""
    cube((0, 2.0, 1.0), (8, 0.1, 6), mat("card_%d" % int(col[0] * 100), col, 0.9, emit=col, emit_str=0.6))
    world_color(col); camera((0, -1.0, 1.0), (0, 2.0, 1.0), lens=35)


def phone_at(d, side="R"):
    ph = cube((0, 0, 0), (0.05, 0.02, 0.1), mat("mphone", (0.12, 0.12, 0.14), 0.3))
    d[side].rotation_euler[0] = -2.6
    return ph


# ---------------------------------------------------------------- shots
def m1(rng):            # What if you could see how long someone will remember this moment?: you on the street, eyes wide
    street_day(rng); y = bean((0, 0.0, 0), mouth="open", **YOU)
    c = _cam((0.1, -1.1, 0.66), (0, 0.0, 0.62), lens=40, fstop=2.4)
    def upd(t): breathe(y, t); c.location.y = -1.1 + 0.05 * t
    return upd


def m2(rng):            # A little timer. Floating over every head.: a crowd crossing the street, a timer above each
    street_day(rng); folk = [bean((x, 0.9, 0), rot=1.5 if i % 2 else -1.5, **FOLK[i]) for i, x in enumerate((-1.2, -0.4, 0.4, 1.2))]
    c = _cam((0, -2.4, 1.1), (0, 0.9, 0.75), lens=30, fstop=5)
    def upd(t):
        for i, f in enumerate(folk):
            f["root"].location.x = f["base"].x + 0.25 * t * (1 if i % 2 else -1); f["root"].location.z = 0.02 * abs(math.sin(t * 8 + i))
    return upd


def m3(rng):            # You test it on the bus driver. "Morning!" Four minutes.: the driver at the wheel of a little bus
    cube((0, 0, -0.05), (30, 30, 0.1), mat("pave", (0.7, 0.68, 0.66), 0.8, noise=0.3))
    bus = mat("bus", (0.95, 0.75, 0.2), 0.5, coat=0.3)
    cube((0, 1.0, 1.0), (2.0, 2.2, 1.8), bus, bevel=0.06); cube((0, -0.11, 1.25), (1.6, 0.02, 0.7), mat("buswin", (0.75, 0.85, 0.95), 0.2, alpha=0.25))
    d = bean((-0.3, 0.3, 0.35), **FOLK[1]); y = bean((0.55, -0.6, 0), rot=0.6, **YOU)
    cube((-0.3, -0.05, 0.85), (0.3, 0.05, 0.3), mat("buswheel", (0.1, 0.1, 0.1), 0.5))
    day((0, 0.3, 0.9))
    c = _cam((0.9, -2.0, 1.0), (0.0, 0.2, 0.8), lens=32, fstop=4)
    def upd(t): y["R"].rotation_euler[1] = -2.2 * smooth((t - 1.6) / 0.3); d["head"].rotation_euler[2] = 0.2
    return upd


def m4(rng):            # Your teacher. Two hours.: the teacher at the board
    room_of((0.95, 0.88, 0.72)); cube((0, 1.54, 1.4), (2.0, 0.03, 0.9), mat("mboard", (0.12, 0.3, 0.22), 0.8))
    t_ = bean((-0.2, 0.9, 0), rot=0.2, **dict(FOLK[2], glasses=True))
    c = _cam((0.15, -1.0, 0.8), (-0.2, 0.9, 0.7), lens=38, fstop=3)
    def upd(t): t_["R"].rotation_euler[1] = -1.5 + 0.2 * math.sin(t * 4); breathe(t_, t)
    return upd


def m5(rng):            # Your best friend, when you lend her a pen? Eleven seconds.
    room_of((0.95, 0.88, 0.72)); f = bean((0.3, 0.5, 0), rot=-0.5, **FRIEND); y = bean((-0.3, 0.4, 0), rot=0.5, **YOU)
    pen = cyl((0, 0, 0), 0.01, 0.15, mat("pen", (0.2, 0.4, 0.9), 0.4), rot=(0, math.pi / 2, 0))
    c = _cam((0.0, -1.2, 0.75), (0.0, 0.45, 0.6), lens=36, fstop=3)
    def upd(t):
        k = smooth((t - 0.8) / 0.6); y["R"].rotation_euler[0] = -1.2 * (1 - k * 0.5); f["L"].rotation_euler[0] = -1.2 * k
        pen.location = Vector((-0.1 + 0.25 * k, 0.25, 0.48))
    return upd


def m6(rng):            # In 1885, Hermann Ebbinghaus tested his own memory with nonsense words.: an old scientist at a desk, candlelight
    room_of((0.75, 0.62, 0.45), night=True)
    cube((0, 0.7, 0.45), (1.2, 0.6, 0.05), mat("mdesk", (0.4, 0.25, 0.12), 0.6, noise=0.4))
    h = bean((0, 1.05, 0), style="adult", glasses=True, tuft=(0.3, 0.2, 0.12), col=(0.4, 0.35, 0.45), name="hermann")
    cube((0, 0.65, 0.48), (0.3, 0.22, 0.01), mat("notebook", (0.95, 0.92, 0.8), 0.8)); candle((0.4, 0.75, 0.475))
    light("POINT", (0.4, 0.75, 0.7), 12, col=(1.0, 0.7, 0.4), size=0.05)
    c = _cam((0.2, -0.5, 0.95), (0, 0.9, 0.65), lens=38, fstop=2.6)
    def upd(t): h["R"].rotation_euler[0] = -0.9 + 0.05 * math.sin(t * 10); h["head"].rotation_euler[0] = 0.15; c.location.y = -0.5 + 0.03 * t
    return upd


def m7(rng):            # Within an hour, more than half of them were gone. Our brains throw away almost everything.: the curve card
    backdrop((0.12, 0.14, 0.22))
    def upd(t): pass
    return upd


def m8(rng):            # So you start trying. Big gifts. Loud jokes. A surprise party.: you with a huge gift, confetti
    room_of((0.92, 0.82, 0.9)); f = bean((0.35, 0.6, 0), rot=-0.4, **FRIEND); y = bean((-0.35, 0.4, 0), rot=0.5, mouth="open", **YOU)
    gift = cube((0, 0, 0), (0.35, 0.3, 0.3), mat("gift", (0.9, 0.2, 0.3), 0.5), bevel=0.02)
    cube((0, 0, 0), (0.36, 0.06, 0.31), mat("ribbon2", (1.0, 0.85, 0.2), 0.4)).parent = gift
    conf = [cube((rng.uniform(-1, 1), rng.uniform(0, 1), rng.uniform(1.2, 2.2)), (0.03, 0.03, 0.005),
                 mat("conf%d" % (k % 4), [(1, 0.3, 0.3), (0.3, 0.6, 1), (1, 0.85, 0.2), (0.4, 0.9, 0.4)][k % 4], 0.5), rot=(k, k * 2, 0)) for k in range(70)]
    base = [Vector(o.location) for o in conf]
    c = _cam((0.0, -1.5, 0.9), (0.0, 0.5, 0.6), lens=32, fstop=4)
    def upd(t):
        gift.location = y["root"].location + Vector((0.2, -0.15, 0.45 + 0.02 * math.sin(t * 6))); y["R"].rotation_euler[0] = y["L"].rotation_euler[0] = -1.3
        for o, b in zip(conf, base): o.location = b - Vector((0, 0, ((t * 0.6 + b.x) % 1.6) * (t > 3.3)))
    return upd


def m9(rng):            # The timers barely move. Three days. Two days. One.: you sag on a bench, the friend walks off
    street_day(rng); y = bean((0, 0.3, 0.0), mouth="worried", **YOU)
    cube((0, 0.35, 0.25), (1.0, 0.3, 0.06), mat("bench", (0.5, 0.32, 0.18), 0.6)); f = bean((0.6, 1.2, 0), rot=-1.6, **FRIEND)
    c = _cam((0.1, -1.4, 0.75), (0, 0.4, 0.55), lens=36, fstop=3)
    def upd(t):
        y["root"].scale.z = 1 - 0.08 * smooth(t / 3.0); f["root"].location.x = 0.6 + 0.35 * t
    return upd


def m10(rng):           # Then on Sunday, you burn the pancakes at Grandma's. Black. Smoking. You both laugh so hard you cry.
    room_of((0.98, 0.85, 0.7)); cube((-0.4, 0.95, 0.42), (1.6, 0.6, 0.84), mat("mcounter", (0.85, 0.85, 0.82), 0.4))
    pan = cyl((-0.4, 0.85, 0.88), 0.14, 0.03, mat("pan", (0.15, 0.15, 0.16), 0.4, metal=0.6))
    cake = cyl((-0.4, 0.85, 0.9), 0.1, 0.02, mat("burntcake", (0.08, 0.06, 0.05), 0.9, noise=0.4))
    sm = Steam((-0.4, 0.85, 0.95), n=16, rng=rng)
    g = bean((0.2, 0.5, 0), rot=-0.5, mouth="open", **GRAN); y = bean((-0.45, 0.35, 0), rot=0.4, mouth="open", **YOU)
    c = _cam((0.0, -1.2, 0.95), (-0.1, 0.6, 0.7), lens=32, fstop=3.5)
    def upd(t):
        sm.update(t, strength=3.0)
        for i, d in enumerate((g, y)):                                    # the laughing fit
            k = smooth((t - 4.8) / 0.5); d["root"].location.z = 0.03 * abs(math.sin(t * 11 + i)) * k
            d["head"].rotation_euler[0] = -0.25 * k; d["L"].rotation_euler[1] = 1.0 * k; d["R"].rotation_euler[1] = -1.0 * k
    return upd


def m11(rng):           # Her timer flips. Forty years.: close on Grandma, tears of laughter
    room_of((0.98, 0.85, 0.7)); g = bean((0.0, 0.5, 0), mouth="smile", **GRAN)
    c = _cam((0.05, -0.45, 0.7), (0.0, 0.5, 0.68), lens=44, fstop=2.2)
    def upd(t): g["head"].rotation_euler[0] = -0.1 + 0.03 * math.sin(t * 8); breathe(g, t)
    return upd


def m12(rng):           # Psychologists have a name for this. The peak-end rule.: the two of you at the table, warm and still
    room_of((0.98, 0.85, 0.7)); cube((0, 0.6, 0.45), (1.0, 0.6, 0.05), mat("mtable", (0.55, 0.35, 0.2), 0.5))
    g = bean((0.35, 0.75, 0), rot=-1.6, **GRAN); y = bean((-0.35, 0.75, 0), rot=1.6, **YOU)
    c = _cam((0.0, -1.0, 0.9), (0, 0.7, 0.6), lens=34, fstop=3)
    def upd(t): breathe(g, t); breathe(y, t); c.location.y = -1.0 + 0.05 * t
    return upd


def m13(rng):           # In a 1993 study, Daniel Kahneman found... not by how long it lasts.: the peak-end card
    backdrop((0.14, 0.12, 0.2))
    def upd(t): pass
    return upd


def m14(rng):           # So that night, you call Dad. And at the end, you say something you never say.: your room at night, phone
    room_of((0.6, 0.7, 0.9), night=True); y = bean((0, 0.6, 0), mouth="flat", **YOU); ph = phone_at(y)
    c = _cam((0.25, -0.6, 0.85), (0, 0.6, 0.65), lens=40, fstop=2.4)
    def upd(t): ph.location = y["root"].location + Vector((0.18, -0.08, 0.62)); breathe(y, t, 0.5); c.location.y = -0.6 + 0.04 * t
    return upd


def m15(rng):           # "Love you." The line goes quiet. His timer goes blank. Then it reads one word.: Dad in his kitchen, still
    room_of((0.85, 0.9, 0.8), night=True); d = bean((0, 0.6, 0), mouth="flat", **DAD); ph = phone_at(d)
    c = _cam((-0.2, -0.55, 0.85), (0, 0.6, 0.68), lens=42, fstop=2.4)
    def upd(t):
        ph.location = d["root"].location + Vector((0.18, -0.08, 0.66))
        d["head"].rotation_euler[0] = 0.12 * smooth((t - 1.2) / 1.0)      # he looks down, moved
    return upd


def m16(rng):           # Forever.: close on Dad, a small smile
    room_of((0.85, 0.9, 0.8), night=True); d = bean((0, 0.6, 0), mouth="smile", **DAD); ph = phone_at(d)
    c = _cam((-0.05, -0.15, 0.82), (0, 0.6, 0.78), lens=50, fstop=2.0)
    def upd(t): ph.location = d["root"].location + Vector((0.18, -0.08, 0.66))
    return upd


def m17(rng):           # What moment will you never forget? Tell me in the comments.: you at the window, snow starting
    room_of((0.6, 0.7, 0.9), night=True); y = bean((0.5, 1.2, 0), rot=math.pi, **YOU)
    sn = Snow((0.6, 2.2, 0.5), size=(1.4, 0.6, 2.5), n=100, rng=rng)
    c = _cam((-0.3, -0.8, 1.0), (0.5, 1.4, 0.9), lens=32, fstop=3.5)
    def upd(t): sn.update(t); c.location.y = -0.8 - 0.1 * t
    return upd


SHOTS = {n: (globals()[n], _D[n]) for n in _D}
