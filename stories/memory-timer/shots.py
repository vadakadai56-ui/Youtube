"""Memory Timer (format 6, "What if" + real science, round bean characters): you can see how long anyone will remember this
moment. Timers, fact cards and graphs are drawn in edit_config.overlay; the fact-card shots use plain backdrops (cheap to render).
v2 (24 Nov 2026): the people are the ready-made Quaternius models (owner: human-like people in every video); the old bean
version is shots_v1_bean.py. Render: STYLE=lowpoly ENGINE=EEVEE PCT=50 ES=8 $VENV/bin/python pipeline/anim.py stories/memory-timer OUT all"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
os.environ.setdefault("STYLE", "lowpoly")
import scene                  # noqa
scene.STYLE = os.environ["STYLE"]
from world import *           # noqa
from world import cam as _cam
from characters import person, play, pose
import bpy
scene.LOOK = os.environ.get("LOOK") or "dream"      # per-video grade (scene.LOOKS)

_D = json.load(open(os.path.join(HERE, "durations.json")))
# (model, age, h): sized like the old beans (kids about 0.7 tall, grown-ups about 0.85)
YOU, FRIEND = ("M_Casual_Hoodie", "kid", 0.58), ("W_Adventurer", "kid", 0.58)
GRAN, DAD, HERMANN = ("W_Casual", "old", 0.47), ("M_Casual_2", "adult", 0.47), ("M_Suit", "old", 0.47)
FOLK = [("W_Suit", "adult", 0.47), ("M_Worker", "adult", 0.47), ("W_Casual", "adult", 0.47), ("M_Beach", "kid", 0.58)]
FAST = {"m2", "m3", "m5"}                                   # walking, waving, the pen hand-off: 30 fps, no ghosting


def who(c, loc, rot=0.0, action="Idle", offset=0.0):
    return person(c[0], loc, rot=rot, age=c[1], h=c[2], action=action, offset=offset)


def hand(d, side="R"):
    bpy.context.view_layer.update(); a = d["arm"]
    return a.matrix_world @ a.pose.bones["Wrist." + side].head


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


def phone_at(d):
    """A phone held to d's right ear (the "phone" pose); call ph_follow(d, ph) every frame."""
    pose(d, "phone"); return cube((0, 0, 0), (0.012, 0.05, 0.025), mat("mphone", (0.12, 0.12, 0.14), 0.3))


def ph_follow(d, ph): ph.location = hand(d)


# ---------------------------------------------------------------- shots
def m1(rng):            # What if you could see how long someone will remember this moment?: you on the street, eyes wide
    street_day(rng); y = who(YOU, (0, 0.0, 0))
    c = _cam((0.1, -1.1, 0.66), (0, 0.0, 0.6), lens=40, fstop=2.4)
    def upd(t): c.location.y = -1.1 + 0.05 * t
    return upd


def m2(rng):            # A little timer. Floating over every head.: a crowd crossing the street, a timer above each
    street_day(rng); folk = [who(FOLK[i], (x, 0.9, 0), rot=math.pi / 2 if i % 2 else -math.pi / 2, action="Walk", offset=i * 0.3) for i, x in enumerate((-1.2, -0.4, 0.4, 1.2))]
    c = _cam((0, -2.4, 1.1), (0, 0.9, 0.75), lens=30, fstop=5)
    def upd(t):
        for i, f in enumerate(folk): f["root"].location.x = f["base"].x + 0.3 * t * (1 if i % 2 else -1)
    return upd


def m3(rng):            # You test it on the bus driver. "Morning!" Four minutes.: the driver at the wheel of a little bus
    cube((0, 0, -0.05), (30, 30, 0.1), mat("pave", (0.7, 0.68, 0.66), 0.8, noise=0.3))
    bus = mat("bus", (0.95, 0.75, 0.2), 0.5, coat=0.3)
    cube((0, 1.0, 1.0), (2.0, 2.2, 1.8), bus, bevel=0.06); cube((0, -0.11, 1.25), (1.6, 0.02, 0.7), mat("buswin", (0.75, 0.85, 0.95), 0.2, alpha=0.25))
    cube((-0.3, -0.42, 0.42), (0.8, 0.08, 0.84), bus, bevel=0.03)                     # the dashboard he sits behind
    d = who(FOLK[1], (-0.3, -0.25, 0.32)); y = who(YOU, (0.55, -0.6, 0), rot=0.6, action="Wave")      # the driver, up in his seat
    cyl((-0.3, -0.42, 0.9), 0.12, 0.02, mat("buswheel", (0.1, 0.1, 0.1), 0.5), rot=(1.2, 0, 0))
    day((0, 0.3, 0.9))
    c = _cam((0.9, -2.0, 1.0), (0.0, 0.2, 0.8), lens=32, fstop=4)
    def upd(t): pass
    return upd


def m4(rng):            # Your teacher. Two hours.: the teacher at the board
    room_of((0.95, 0.88, 0.72)); cube((0, 1.54, 1.4), (2.0, 0.03, 0.9), mat("mboard", (0.12, 0.3, 0.22), 0.8))
    t_ = who(FOLK[2], (-0.2, 0.9, 0), rot=0.2, action="Interact")
    c = _cam((0.15, -1.0, 0.8), (-0.2, 0.9, 0.7), lens=38, fstop=3)
    def upd(t): pass
    return upd


def m5(rng):            # Your best friend, when you lend her a pen? Eleven seconds.
    room_of((0.95, 0.88, 0.72)); f = who(FRIEND, (0.3, 0.5, 0), rot=-0.5, action="Interact", offset=0.6); y = who(YOU, (-0.3, 0.4, 0), rot=0.5, action="Interact")
    pen = cyl((0, 0, 0), 0.01, 0.15, mat("pen", (0.2, 0.4, 0.9), 0.4), rot=(0, math.pi / 2, 0))
    c = _cam((0.0, -1.2, 0.75), (0.0, 0.45, 0.6), lens=36, fstop=3)
    def upd(t):
        k = smooth((t - 0.8) / 0.6); pen.location = hand(y).lerp(hand(f, "L"), k)          # from my hand to hers
    return upd


def m6(rng):            # In 1885, Hermann Ebbinghaus tested his own memory with nonsense words.: an old scientist at a desk, candlelight
    room_of((0.75, 0.62, 0.45), night=True)
    cube((0, 0.7, 0.45), (1.2, 0.6, 0.05), mat("mdesk", (0.4, 0.25, 0.12), 0.6, noise=0.4))
    h = who(HERMANN, (0, 1.05, 0))
    cube((0, 0.65, 0.48), (0.3, 0.22, 0.01), mat("notebook", (0.95, 0.92, 0.8), 0.8)); candle((0.4, 0.75, 0.475))
    light("POINT", (0.4, 0.75, 0.7), 12, col=(1.0, 0.7, 0.4), size=0.05)
    c = _cam((0.2, -0.5, 1.05), (0, 0.9, 0.78), lens=38, fstop=2.6)
    def upd(t): c.location.y = -0.5 + 0.03 * t
    return upd


def m7(rng):            # Within an hour, more than half of them were gone. Our brains throw away almost everything.: the curve card
    backdrop((0.12, 0.14, 0.22))
    def upd(t): pass
    return upd


def m8(rng):            # So you start trying. Big gifts. Loud jokes. A surprise party.: you with a huge gift, confetti
    room_of((0.92, 0.82, 0.9)); f = who(FRIEND, (0.35, 0.6, 0), rot=-0.4); y = who(YOU, (-0.35, 0.4, 0), rot=0.5)
    gift = cube((0, 0, 0), (0.35, 0.3, 0.3), mat("gift", (0.9, 0.2, 0.3), 0.5), bevel=0.02)
    cube((0, 0, 0), (0.36, 0.06, 0.31), mat("ribbon2", (1.0, 0.85, 0.2), 0.4)).parent = gift
    conf = [cube((rng.uniform(-1, 1), rng.uniform(0, 1), rng.uniform(1.2, 2.2)), (0.03, 0.03, 0.005),
                 mat("conf%d" % (k % 4), [(1, 0.3, 0.3), (0.3, 0.6, 1), (1, 0.85, 0.2), (0.4, 0.9, 0.4)][k % 4], 0.5), rot=(k, k * 2, 0)) for k in range(70)]
    base = [Vector(o.location) for o in conf]
    c = _cam((0.0, -1.5, 0.9), (0.0, 0.5, 0.6), lens=32, fstop=4)
    def upd(t):
        gift.location = y["root"].location + Vector((0.12, -0.2, 0.36 + 0.02 * math.sin(t * 6)))            # held out in front
        for o, b in zip(conf, base): o.location = b - Vector((0, 0, ((t * 0.6 + b.x) % 1.6) * (t > 3.3)))
    return upd


def m9(rng):            # The timers barely move. Three days. Two days. One.: you sag on a bench, the friend walks off
    street_day(rng); y = who(YOU, (0, 0.3, 0.0)); pose(y, "sit", seat=0.28)
    cube((0, 0.35, 0.25), (1.0, 0.3, 0.06), mat("bench", (0.5, 0.32, 0.18), 0.6)); f = who(FRIEND, (0.6, 1.2, 0), rot=math.pi / 2, action="Walk")
    c = _cam((0.1, -1.4, 0.75), (0, 0.4, 0.55), lens=36, fstop=3)
    def upd(t):
        f["root"].location.x = 0.6 + 0.3 * t                                         # she walks off; I stay on the bench
    return upd


def m10(rng):           # Then on Sunday, you burn the pancakes at Grandma's. Black. Smoking. You both laugh so hard you cry.
    room_of((0.98, 0.85, 0.7)); cube((-0.4, 0.95, 0.42), (1.6, 0.6, 0.84), mat("mcounter", (0.85, 0.85, 0.82), 0.4))
    pan = cyl((-0.4, 0.85, 0.88), 0.14, 0.03, mat("pan", (0.15, 0.15, 0.16), 0.4, metal=0.6))
    cake = cyl((-0.4, 0.85, 0.9), 0.1, 0.02, mat("burntcake", (0.08, 0.06, 0.05), 0.9, noise=0.4))
    sm = Steam((-0.4, 0.85, 0.95), n=16, rng=rng)
    g = who(GRAN, (0.2, 0.5, 0), rot=-0.5); y = who(YOU, (-0.45, 0.35, 0), rot=0.4)
    c = _cam((0.0, -1.2, 0.95), (-0.1, 0.6, 0.7), lens=32, fstop=3.5)
    def upd(t):
        sm.update(t, strength=3.0)
        for i, d in enumerate((g, y)):                                    # the laughing fit
            k = smooth((t - 4.8) / 0.5); d["root"].location.z = 0.025 * abs(math.sin(t * 11 + i)) * k
            d["root"].rotation_euler[0] = 0.18 * k * (0.6 + 0.4 * abs(math.sin(t * 5 + i)))     # doubled over laughing
    return upd


def m11(rng):           # Her timer flips. Forty years.: close on Grandma, tears of laughter
    room_of((0.98, 0.85, 0.7)); g = who(GRAN, (0.0, 0.5, 0))
    c = _cam((0.05, -0.45, 0.76), (0.0, 0.5, 0.74), lens=44, fstop=2.2)
    def upd(t): pass
    return upd


def m12(rng):           # Psychologists have a name for this. The peak-end rule.: the two of you at the table, warm and still
    room_of((0.98, 0.85, 0.7)); cube((0, 0.6, 0.45), (1.0, 0.6, 0.05), mat("mtable", (0.55, 0.35, 0.2), 0.5))
    g = who(GRAN, (0.35, 0.75, 0), rot=-1.6); y = who(YOU, (-0.35, 0.75, 0), rot=1.6)
    c = _cam((0.0, -1.0, 0.9), (0, 0.7, 0.6), lens=34, fstop=3)
    def upd(t): c.location.y = -1.0 + 0.05 * t
    return upd


def m13(rng):           # In a 1993 study, Daniel Kahneman found... not by how long it lasts.: the peak-end card
    backdrop((0.14, 0.12, 0.2))
    def upd(t): pass
    return upd


def m14(rng):           # So that night, you call Dad. And at the end, you say something you never say.: your room at night, phone
    room_of((0.6, 0.7, 0.9), night=True); y = who(YOU, (0, 0.6, 0)); ph = phone_at(y)
    c = _cam((-0.3, -0.55, 0.8), (0, 0.6, 0.62), lens=40, fstop=2.4)               # from my right, so the phone shows
    def upd(t): ph_follow(y, ph); c.location.y = -0.6 + 0.04 * t
    return upd


def m15(rng):           # "Love you." The line goes quiet. His timer goes blank. Then it reads one word.: Dad in his kitchen, still
    room_of((0.85, 0.9, 0.8), night=True); d = who(DAD, (0, 0.6, 0)); ph = phone_at(d)
    c = _cam((-0.2, -0.55, 0.85), (0, 0.6, 0.76), lens=42, fstop=2.4)
    def upd(t): ph_follow(d, ph); c.location.z = 0.85 - 0.03 * smooth((t - 1.2) / 1.0)    # the camera settles as he takes it in
    return upd


def m16(rng):           # Forever.: close on Dad, a small smile
    room_of((0.85, 0.9, 0.8), night=True); d = who(DAD, (0, 0.6, 0)); ph = phone_at(d)
    c = _cam((-0.05, -0.15, 0.84), (0, 0.6, 0.8), lens=50, fstop=2.0)
    def upd(t): ph_follow(d, ph)
    return upd


def m17(rng):           # What moment will you never forget? Tell me in the comments.: you at the window, snow starting
    room_of((0.6, 0.7, 0.9), night=True); y = who(YOU, (0.5, 1.2, 0), rot=math.pi)
    sn = Snow((0.6, 2.2, 0.5), size=(1.4, 0.6, 2.5), n=100, rng=rng)
    c = _cam((-0.3, -0.8, 1.0), (0.5, 1.4, 0.9), lens=32, fstop=3.5)
    def upd(t): sn.update(t); c.location.y = -0.8 - 0.1 * t
    return upd


SHOTS = {n: (globals()[n], _D[n]) for n in _D}

CALM = {"m6", "m7", "m11", "m12", "m13", "m14", "m15", "m16", "m17"}   # slow shots rendered at 6 fps (edit.py blends to 30)
