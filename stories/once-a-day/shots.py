"""Once a Day (format 4, weird town rule + quirk, round bean characters): in my town each word can be said only once a day;
my words never run out, which seems useless until Biscuit the dog only comes when you call him three times.
Speech bubbles are drawn in edit_config.overlay. Render: STYLE=lowpoly ENGINE=EEVEE PCT=50 ES=12 ... pipeline/anim.py stories/once-a-day OUT all"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
os.environ.setdefault("STYLE", "lowpoly")
import scene                  # noqa
scene.STYLE = os.environ["STYLE"]
from world import *           # noqa
from world import cam as _cam
from characters import bean, dog, stride
import bpy

_D = json.load(open(os.path.join(HERE, "durations.json")))
ME = dict(col=(0.35, 0.65, 0.95), tuft=(0.25, 0.15, 0.1), scarf=(0.95, 0.3, 0.3), name="me")
FOLK = [dict(col=(0.98, 0.62, 0.35), name="f1"), dict(col=(0.6, 0.85, 0.55), style="adult", name="f2", hat=(0.8, 0.2, 0.25)),
        dict(col=(0.95, 0.6, 0.75), bow=(1, 1, 1), name="f3"), dict(col=(0.75, 0.6, 0.9), style="gran", name="f4"),
        dict(col=(0.95, 0.85, 0.4), style="adult", name="f5", scarf=(0.3, 0.5, 0.9)), dict(col=(0.55, 0.75, 0.85), name="f6", hat=(0.3, 0.7, 0.4))]
PELL = dict(col=(0.85, 0.5, 0.55), style="gran", name="pell", scarf=(0.4, 0.6, 0.4))


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


def lantern(loc):
    sphere(loc, 0.04, mat("lantern", (1, 0.8, 0.45), 0.3, emit=(1, 0.75, 0.4), emit_str=12), seg=10)
    light("POINT", loc, 6, col=(1.0, 0.75, 0.45), size=0.05)


def crowd(rng, n=6, y0=0.6, spread=2.4, face=math.pi, lanterns=False):
    out = []
    for i in range(n):
        kw = FOLK[i % len(FOLK)]; x = -spread / 2 + spread * i / max(1, n - 1) + rng.uniform(-0.1, 0.1)
        b = bean((x, y0 + rng.uniform(-0.2, 0.2), 0), rot=face + rng.uniform(-0.3, 0.3), **dict(kw, name=kw["name"] + str(i)))
        if lanterns: lantern((x + 0.18, y0 - 0.1, 0.55))
        out.append(b)
    return out


# ---------------------------------------------------------------- shots
def a1(rng):            # In my town, you can say each word only once a day.: the bright square, folk strolling
    town(rng); folk = crowd(rng, 5, y0=1.4, spread=5.0, face=0.0)
    c = _cam((0.0, -3.2, 1.2), (0, 1.5, 0.7), lens=30, fstop=6)
    def upd(t):
        for i, f in enumerate(folk):
            f["root"].location.x = f["base"].x + 0.25 * t * (1 if i % 2 else -1); f["root"].rotation_euler[2] = (-1.4 if i % 2 else 1.4)
            f["root"].location.z = 0.02 * abs(math.sin(t * 8 + i))
        c.location.y = -3.2 + 0.15 * t
    return upd


def a2(rng):            # Say it twice... and nothing comes out.: a bean opens its mouth, nothing (an empty bubble)
    town(rng); f = bean((0.0, 0.4, 0), mouth="open", **FOLK[0])
    c = _cam((0.1, -0.85, 0.65), (0, 0.4, 0.6), lens=42, fstop=2.4)
    def upd(t): breathe(f, t); f["head"].rotation_euler[0] = 0.08 * math.sin(t * 3)
    return upd


def a3(rng):            # So everyone talks very carefully. "Morning." "Hello." "Greetings." "Hiya.": four greetings in the square
    town(rng); folk = [bean((x, 0.6, 0), rot=r, **FOLK[i]) for i, (x, r) in enumerate([(-0.9, -0.5), (-0.3, 0.4), (0.3, -0.4), (0.9, 0.5)])]
    c = _cam((0.0, -2.2, 0.95), (0, 0.6, 0.6), lens=32, fstop=4)
    starts = [2.6, 3.6, 4.5, 5.5]                                          # local times of each greeting
    def upd(t):
        for i, f in enumerate(folk):
            k = math.sin(math.pi * min(1, max(0, (t - starts[i]) / 0.5))); f["root"].location.z = 0.04 * k
            f["R"].rotation_euler[1] = -1.8 * k
    return upd


def a4(rng):            # Except me. My words never run out.: me, chattering away, a bubble full of words
    town(rng); m = bean((0.0, 0.4, 0), mouth="open", **ME)
    c = _cam((0.0, -1.0, 0.68), (0, 0.4, 0.62), lens=40, fstop=2.4)
    def upd(t):
        m["head"].rotation_euler[0] = 0.06 * math.sin(t * 14); m["R"].rotation_euler[1] = -1.2 - 0.4 * math.sin(t * 6)
        m["L"].rotation_euler[1] = 1.2 + 0.4 * math.sin(t * 6 + 1)
    return upd


def a5(rng):            # I say "sorry" about fifty times a day. People think I'm showing off.: bumping into everyone, side-eye
    town(rng); m = bean((-1.2, 0.5, 0), rot=-1.5, **ME)
    folk = [bean((x, 0.5, 0), rot=math.pi * 0.0, mouth="flat", **dict(FOLK[i], name="s%d" % i)) for i, x in enumerate([-0.3, 0.4, 1.1])]
    c = _cam((0.0, -2.0, 0.85), (0, 0.5, 0.55), lens=30, fstop=5)
    def upd(t):
        x = -1.2 + 0.55 * t; m["root"].location.x = x; m["root"].location.z = 0.02 * abs(math.sin(t * 10))
        for f in folk:
            near = max(0.0, 1 - abs(f["base"].x - x) / 0.25)
            f["root"].location.x = f["base"].x + 0.08 * near; f["head"].rotation_euler[2] = 0.4 * smooth((x - f["base"].x) / 0.3)
    return upd


def a6(rng):            # Then one snowy night, Mrs Pell's dog ran into the woods.: Biscuit bolts for the trees
    woods(rng); d = dog((0.4, -0.2, 0), rot=math.pi); p = bean((-0.6, -0.4, 0), rot=-0.6, mouth="open", **PELL)
    lantern((-0.42, -0.55, 0.55)); sn = Snow((0, 0.5, 0.2), size=(6, 4, 3), n=260, rng=rng)
    c = _cam((0.0, -2.6, 0.8), (0, 1.2, 0.5), lens=30, fstop=5)
    def upd(t):
        sn.update(t); y = -0.2 + 1.2 * t; d["root"].location = Vector((0.4, y, 0.04 * abs(math.sin(t * 14))))
        d["tail"].rotation_euler[1] = 0.6 * math.sin(t * 18); p["R"].rotation_euler[1] = -2.0
    return upd


def a7(rng):            # Biscuit only comes when you call him three times. The whole town stood at the trees. Nobody could do it.
    woods(rng); folk = crowd(rng, 6, y0=0.2, spread=3.0, face=math.pi, lanterns=True)
    sn = Snow((0, 0.5, 0.2), size=(6, 4, 3), n=260, rng=rng)
    c = _cam((0.4, -1.6, 0.8), (0, 2.0, 0.6), lens=28, fstop=5)
    def upd(t):
        sn.update(t); c.location.y = -1.6 + 0.08 * t
        for i, f in enumerate(folk): f["head"].rotation_euler[0] = 0.1 * math.sin(t * 2 + i)
    return upd


def a8(rng):            # So I stepped forward. "Biscuit! Biscuit! BISCUIT!": me in front of the crowd, shouting, the camera shakes
    woods(rng); folk = crowd(rng, 5, y0=-0.6, spread=3.0, face=math.pi, lanterns=True)
    m = bean((0.0, 0.3, 0), rot=math.pi, mouth="open", **ME); sn = Snow((0, 0.5, 0.2), size=(6, 4, 3), n=260, rng=rng)
    c = _cam((0.35, 1.5, 0.65), (0.0, 0.3, 0.62), lens=36, fstop=2.8)          # from the woods side, looking at my face
    shouts = [1.6, 2.6, 3.5]
    def upd(t):
        sn.update(t); m["root"].location.y = 0.3 + 0.25 * smooth(t / 0.8)
        k = max([math.sin(math.pi * min(1, max(0, (t - s) / 0.5))) * (1.3 if i == 2 else 1) for i, s in enumerate(shouts)])
        m["L"].rotation_euler[1] = 1.0 * k; m["R"].rotation_euler[1] = -1.0 * k; m["head"].rotation_euler[0] = -0.15 * k
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


def a10(rng):           # Now the whole town lets me say "good boy" as many times as I like.: the town cheering, me hugging Biscuit
    town(rng, night=True); folk = crowd(rng, 6, y0=0.9, spread=3.4, face=0.0, lanterns=True)
    m = bean((0.0, 0.0, 0), mouth="smile", **ME); d = dog((0.25, -0.1, 0), rot=0.5)
    sn = Snow((0, 0.5, 0.2), size=(6, 4, 3), n=200, rng=rng)
    c = _cam((0.0, -1.9, 0.9), (0.05, 0.3, 0.55), lens=30, fstop=4)
    def upd(t):
        sn.update(t); m["R"].rotation_euler[1] = -1.4; d["tail"].rotation_euler[1] = 0.6 * math.sin(t * 16)
        for i, f in enumerate(folk):
            k = abs(math.sin(t * 6 + i)); f["root"].location.z = 0.03 * k; f["L"].rotation_euler[1] = 2.2 * (i % 2); f["R"].rotation_euler[1] = -2.2 * ((i + 1) % 2)
    return upd


def a11(rng):           # Comment the one word you'd save for the whole day.: the snowy town at night, wide
    town(rng, night=True); folk = crowd(rng, 6, y0=0.9, spread=3.4, face=0.0, lanterns=True)
    m = bean((0.0, 0.0, 0), **ME); d = dog((0.25, -0.1, 0), rot=0.5); sn = Snow((0, 0.5, 0.2), size=(8, 5, 3), n=260, rng=rng)
    c = _cam((0.0, -3.4, 1.4), (0, 1.0, 0.8), lens=30, fstop=6)
    def upd(t): sn.update(t); c.location.y = -3.4 - 0.15 * t; d["tail"].rotation_euler[1] = 0.6 * math.sin(t * 16)
    return upd


SHOTS = {n: (globals()[n], _D[n]) for n in _D}
