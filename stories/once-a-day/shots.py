"""Once a Day (format 4, weird town rule + quirk): in my town each word can be said only once a day;
my words never run out, which seems useless until Biscuit the dog only comes when you call him three times.
v2 (24 Nov 2026): the townsfolk are the ready-made Quaternius people (owner: human-like people in every video); the old bean
version is shots_v1_bean.py. Speech bubbles are drawn in edit_config.overlay.
Render: STYLE=lowpoly ENGINE=EEVEE PCT=50 ES=8 ... pipeline/anim.py stories/once-a-day OUT all"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
os.environ.setdefault("STYLE", "lowpoly")
import scene                  # noqa
scene.STYLE = os.environ["STYLE"]
from world import *           # noqa
from world import cam as _cam
from characters import dog, person, play
import bpy
scene.LOOK = os.environ.get("LOOK") or "comedy"      # per-video grade (scene.LOOKS)

_D = json.load(open(os.path.join(HERE, "durations.json")))
FAST = {"a1", "a3", "a5", "a8", "a10"}      # walking, waving and calling: 30 fps so limbs never blur into ghosts
# (model, age, h): h sized so the people match the old bean scale (me about 0.7 tall, grown-ups about 0.85)
ME = ("M_Casual_Hoodie", "kid", 0.58)
FOLK = [("W_Casual", "adult", 0.47), ("M_Worker", "adult", 0.47), ("W_Adventurer", "kid", 0.58), ("M_Farmer", "old", 0.47),
        ("W_Suit", "adult", 0.47), ("M_Beach", "kid", 0.58)]
PELL = ("W_Worker", "old", 0.47)                                   # Mrs Pell, Biscuit's owner


def who(c, loc, rot=0.0, action="Idle", offset=0.0):
    return person(c[0], loc, rot=rot, age=c[1], h=c[2], action=action, offset=offset)


def town(rng, night=False):
    """A bright snowy square with toy houses; at night the windows glow and lanterns light the snow."""
    cube((0, 0, -0.05), (40, 40, 0.1), mat("tsnow", (0.92, 0.94, 0.98), 0.75, noise=0.15))
    cols = [(0.95, 0.55, 0.45), (0.55, 0.7, 0.95), (0.98, 0.85, 0.45), (0.6, 0.85, 0.6), (0.9, 0.6, 0.85)]
    win = mat("twin", (1, 0.85, 0.55), 0.4, emit=(1, 0.8, 0.5), emit_str=4 if night else 0.6)
    for i, x in enumerate([-4.2, -2.1, 0.0, 2.1, 4.2]):
        cube((x, 3.0, 0.75), (1.7, 1.4, 1.5), mat("thouse%d" % i, cols[i], 0.7, noise=0.1), bevel=0.05)
        cube((x, 3.0, 1.62), (1.9, 1.6, 0.25), mat("troof", (0.96, 0.97, 1.0), 0.6), bevel=0.08)
        cube((x, 2.29, 0.4), (0.38, 0.03, 0.8), mat("tdoor%d" % i, (0.45, 0.25, 0.15), 0.6))
        for wx in (-0.5, 0.5): cube((x + wx, 2.29, 0.95), (0.35, 0.03, 0.35), win)
    for x in (-6.5, 6.5, -7.5, 7.8): tree((x, 4.0, 0), "snow", rng)
    if night:
        world_color((0.03, 0.04, 0.1))
        light("SUN", (0, 0, 5), 0.4, col=(0.55, 0.65, 1.0), rot=(0.9, 0.2, 0.4))
        light("AREA", (0.5, -3.0, 2.5), 40, col=(1.0, 0.8, 0.6), size=3, target=(0, 1.0, 0.6))
    else:
        world_color((0.42, 0.55, 0.8))
        light("SUN", (0, 0, 5), 1.7, col=(1.0, 0.93, 0.82), rot=(0.75, 0.15, 0.6))
        light("AREA", (0.5, -3.0, 2.5), 45, col=(1.0, 0.95, 0.9), size=3, target=(0, 1.0, 0.6))
    return win


def woods(rng):
    """The edge of the dark woods at night, lanterns held by the crowd."""
    cube((0, 0, -0.05), (40, 40, 0.1), mat("wsnow", (0.85, 0.88, 0.95), 0.75, noise=0.15))
    for k in range(26): tree((rng.uniform(-6, 6), rng.uniform(2.2, 7), 0), "snow", rng)
    for k in range(18):
        x = rng.uniform(-6, 6); y = rng.uniform(2.0, 7); h = rng.uniform(1.2, 2.2)
        bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=0.45, depth=h, location=(x, y, h / 2)); o = bpy.context.object
        o.data.materials.append(mat("pine", (0.12, 0.3, 0.2), 0.8))
    world_color((0.02, 0.03, 0.08))
    light("SUN", (0, 0, 5), 0.35, col=(0.55, 0.65, 1.0), rot=(0.9, 0.2, 0.4))
    light("AREA", (0.3, -2.6, 2.0), 55, col=(1.0, 0.78, 0.55), size=3, target=(0, 0.4, 0.45))   # the crowd's lanterns, from the front
    light("AREA", (0.0, 2.6, 1.6), 25, col=(0.7, 0.8, 1.0), size=3, target=(0, 0.3, 0.45))      # moonlight on faces seen from the woods


def lantern(loc):
    sphere(loc, 0.04, mat("lantern", (1, 0.8, 0.45), 0.3, emit=(1, 0.75, 0.4), emit_str=12), seg=10)
    light("POINT", loc, 6, col=(1.0, 0.75, 0.45), size=0.05)


def crowd(rng, n=6, y0=0.6, spread=2.4, face=math.pi, lanterns=False, action="Idle"):
    out = []
    for i in range(n):
        x = -spread / 2 + spread * i / max(1, n - 1) + rng.uniform(-0.1, 0.1)
        out.append(who(FOLK[i % len(FOLK)], (x, y0 + rng.uniform(-0.2, 0.2), 0), rot=face + rng.uniform(-0.3, 0.3), action=action, offset=i * 0.31))
        if lanterns: lantern((x + 0.18, y0 - 0.1, 0.45))
    return out


# ---------------------------------------------------------------- shots
def a1(rng):            # In my town, you can say each word only once a day.: the bright square, folk strolling
    town(rng); folk = crowd(rng, 5, y0=1.4, spread=5.0, action="Walk")
    for i, f in enumerate(folk): f["root"].rotation_euler[2] = math.pi / 2 if i % 2 else -math.pi / 2   # half walk right, half left
    c = _cam((0.0, -3.2, 1.2), (0, 1.5, 0.7), lens=30, fstop=6)
    def upd(t):
        for i, f in enumerate(folk): f["root"].location.x = f["base"].x + 0.3 * t * (1 if i % 2 else -1)
        c.location.y = -3.2 + 0.15 * t
    return upd


def a2(rng):            # Say it twice... and nothing comes out.: she tries to speak, nothing (an empty bubble)
    town(rng); f = who(FOLK[0], (0.0, 0.4, 0), action="Interact")
    c = _cam((0.1, -0.85, 0.75), (0, 0.4, 0.68), lens=42, fstop=2.4)
    def upd(t): pass
    return upd


def a3(rng):            # So everyone talks very carefully. "Morning." "Hello." "Greetings." "Hiya.": four greetings in the square
    town(rng)
    folk = [who(FOLK[i], (x, 0.6, 0), rot=r, action="Wave", offset=i * 0.45) for i, (x, r) in enumerate([(-0.9, -0.5), (-0.3, 0.4), (0.3, -0.4), (0.9, 0.5)])]
    c = _cam((0.0, -3.0, 0.95), (0, 0.6, 0.5), lens=30, fstop=4)
    def upd(t): pass
    return upd


def a4(rng):            # Except me. My words never run out.: me, chattering away, a bubble full of words
    town(rng); m = who(ME, (0.0, 0.4, 0), action="Interact")
    c = _cam((0.0, -1.0, 0.68), (0, 0.4, 0.6), lens=40, fstop=2.4)
    def upd(t): pass
    return upd


def a5(rng):            # I say "sorry" about fifty times a day. People think I'm showing off.: bumping past everyone, side-eye
    town(rng); m = who(ME, (-1.2, 0.5, 0), rot=math.pi / 2, action="Walk")
    folk = [who(FOLK[i], (x, 0.62, 0)) for i, x in enumerate([-0.3, 0.4, 1.1])]
    c = _cam((0.0, -2.0, 0.85), (0, 0.5, 0.55), lens=30, fstop=5)
    def upd(t):
        x = -1.2 + 0.5 * t; m["root"].location.x = x
        for f in folk:
            near = max(0.0, 1 - abs(f["base"].x - x) / 0.25)
            f["root"].location.y = f["base"].y + 0.08 * near                        # stepping back as I squeeze past
            f["root"].rotation_euler[2] = -0.9 * smooth((x - f["base"].x) / 0.3)     # then turning to stare after me
    return upd


def a6(rng):            # Then one snowy night, Mrs Pell's dog ran into the woods.: Biscuit bolts for the trees
    woods(rng); d = dog((0.4, -0.2, 0), rot=math.pi); p = who(PELL, (-0.35, -0.6, 0), rot=math.pi - 0.6, action="Idle_Gun_Pointing")
    lantern((-0.17, -0.75, 0.45)); sn = Snow((0, 0.5, 0.2), size=(6, 4, 3), n=260, rng=rng)
    c = _cam((0.0, -2.6, 0.8), (0, 1.2, 0.5), lens=30, fstop=5)
    def upd(t):
        sn.update(t); y = -0.2 + 1.2 * t; d["root"].location = Vector((0.4, y, 0.04 * abs(math.sin(t * 14))))
        d["tail"].rotation_euler[1] = 0.6 * math.sin(t * 18)
    return upd


def a7(rng):            # Biscuit only comes when you call him three times. The whole town stood at the trees. Nobody could do it.
    woods(rng); folk = crowd(rng, 6, y0=0.2, spread=3.0, face=math.pi, lanterns=True)
    sn = Snow((0, 0.5, 0.2), size=(6, 4, 3), n=260, rng=rng)
    c = _cam((0.4, -1.6, 0.8), (0, 2.0, 0.6), lens=28, fstop=5)
    def upd(t): sn.update(t); c.location.y = -1.6 + 0.08 * t
    return upd


def a8(rng):            # So I stepped forward. "Biscuit! Biscuit! BISCUIT!": me in front of the crowd, calling, the camera shakes
    woods(rng); folk = crowd(rng, 5, y0=-0.6, spread=3.0, face=math.pi, lanterns=True)
    m = who(ME, (0.0, 0.3, 0), rot=math.pi, action="Wave"); sn = Snow((0, 0.5, 0.2), size=(6, 4, 3), n=260, rng=rng)
    c = _cam((0.35, 1.5, 0.65), (0.0, 0.3, 0.55), lens=36, fstop=2.8)          # from the woods side, looking at my face
    shouts = [1.6, 2.6, 3.5]
    def upd(t):
        sn.update(t); m["root"].location.y = 0.3 + 0.25 * smooth(t / 0.8)
        k = max([math.sin(math.pi * min(1, max(0, (t - s) / 0.5))) * (1.3 if i == 2 else 1) for i, s in enumerate(shouts)])
        c.location.x = 0.35 + 0.02 * math.sin(t * 50) * k
    return upd


def a9(rng):            # Out of the snow... came one very cold dog.: Biscuit bursts out of a snowdrift, snow on his back, shivering
    woods(rng); d = dog((0.0, 1.6, 0), rot=0.0); sn = Snow((0, 0.5, 0.2), size=(6, 4, 3), n=260, rng=rng)
    drift = sphere((0.0, 1.7, 0.0), 0.5, mat("drift", (0.95, 0.96, 1.0), 0.7), scale=(1.4, 1, 0.6))
    snowcap = sphere((0, 0, 0), 0.08, mat("dogsnow", (0.98, 0.98, 1.0), 0.6), scale=(1.4, 1.8, 0.5))
    c = _cam((0.2, -0.9, 0.5), (0, 1.0, 0.35), lens=36, fstop=3)
    def upd(t):
        sn.update(t); k = smooth((t - 0.5) / 0.8)
        d["root"].location = Vector((0.03 * math.sin(t * 40) * (t > 1.8), 1.6 - 1.6 * smooth((t - 1.3) / 2.0), -0.35 + 0.35 * k))
        snowcap.location = d["root"].location + Vector((0, 0.05, 0.28)); d["tail"].rotation_euler[1] = 0.6 * math.sin(t * 16) * (t > 2.4)
    return upd


def a10(rng):           # Now the whole town lets me say "good boy" as many times as I like.: the town cheering, me with Biscuit
    town(rng, night=True); folk = crowd(rng, 6, y0=0.9, spread=3.4, face=0.0, lanterns=True, action="Wave")
    m = who(ME, (0.0, 0.0, 0), action="Interact"); d = dog((0.25, -0.1, 0), rot=0.5)
    sn = Snow((0, 0.5, 0.2), size=(6, 4, 3), n=200, rng=rng)
    c = _cam((0.0, -1.9, 0.9), (0.05, 0.3, 0.55), lens=30, fstop=4)
    def upd(t):
        sn.update(t); d["tail"].rotation_euler[1] = 0.6 * math.sin(t * 16)
        for i, f in enumerate(folk): f["root"].location.z = 0.03 * abs(math.sin(t * 6 + i))   # a little bounce
    return upd


def a11(rng):           # Comment the one word you'd save for the whole day.: the snowy town at night, wide
    town(rng, night=True); folk = crowd(rng, 6, y0=0.9, spread=3.4, face=0.0, lanterns=True)
    m = who(ME, (0.0, 0.0, 0)); d = dog((0.25, -0.1, 0), rot=0.5); sn = Snow((0, 0.5, 0.2), size=(8, 5, 3), n=260, rng=rng)
    c = _cam((0.0, -3.4, 1.4), (0, 1.0, 0.8), lens=30, fstop=6)
    def upd(t): sn.update(t); c.location.y = -3.4 - 0.15 * t; d["tail"].rotation_euler[1] = 0.6 * math.sin(t * 16)
    return upd


SHOTS = {n: (globals()[n], _D[n]) for n in _D}
