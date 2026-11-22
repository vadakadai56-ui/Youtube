"""Same Window (Trend Short, "Same Spot, Years Apart", peg dolls): one window by the railway, seventy years. She waves at every
train; nobody waves back; in 2026 every window of the train waves back.
Render: STYLE=lowpoly ENGINE=EEVEE PCT=50 ES=12 $VENV/bin/python pipeline/anim.py stories/same-window OUT all"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
os.environ.setdefault("STYLE", "lowpoly")
import scene                  # noqa
scene.STYLE = os.environ["STYLE"]
from world import *           # noqa
from world import cam as _cam
import bpy

_D = json.load(open(os.path.join(HERE, "durations.json")))
DRESS = (0.75, 0.3, 0.35)
TRACK_Y = -1.6


# ---------------------------------------------------------------- set
def cottage(rng, season="dusk", lit=True):
    """A little brick cottage beside the railway. The window (an opening, no glass) faces the track."""
    ground, foliage, sky = SEASONS[season]
    cube((0, 0, -0.05), (40, 40, 0.1), mat("ground_" + season, ground, 0.85, noise=0.3))
    cube((0, 0.4, 0.06), (8, 3.2, 0.12), mat("bank_" + season, ground, 0.85, noise=0.3))                  # the raised garden
    wall = mat("brick", (0.62, 0.36, 0.28), 0.85, noise=0.45)
    cube((-1.05, 0.0, 1.2), (1.5, 0.15, 2.4), wall); cube((1.05, 0.0, 1.2), (1.5, 0.15, 2.4), wall)          # either side of the window
    cube((0, 0.0, 0.32), (0.6, 0.15, 0.64), wall); cube((0, 0.0, 1.95), (0.6, 0.15, 0.9), wall)               # below and above it
    fm = mat("wframe", (0.95, 0.93, 0.88), 0.5)
    cube((0, -0.09, 0.62), (0.7, 0.12, 0.05), fm); cube((0, -0.09, 1.5), (0.7, 0.06, 0.05), fm)
    for x in (-0.32, 0.32): cube((x, -0.09, 1.06), (0.05, 0.06, 0.9), fm)
    cube((0, 0.0, 2.6), (3.8, 1.6, 0.25), mat("slate", (0.25, 0.22, 0.24), 0.7))
    if season == "snow": cube((0, 0.0, 2.76), (3.8, 1.6, 0.08), mat("roofsnow", (0.95, 0.96, 1.0), 0.7))
    cube((0, 0.9, 1.2), (3.6, 0.1, 2.4), mat("inwall", (0.86, 0.74, 0.55), 0.9, noise=0.2))                  # the room behind her
    cube((0, 0.45, 0.3), (3.6, 1.0, 0.04), mat("infloor", (0.4, 0.26, 0.15), 0.7))
    if lit: light("POINT", (0.3, 0.55, 1.6), 30, col=(1.0, 0.72, 0.42), size=0.3)
    for x in (-2.6, 2.6): tree((x, 0.7, 0.1), season, rng)
    rail = mat("rail", (0.35, 0.33, 0.32), 0.4, metal=0.8); slp = mat("sleeper", (0.3, 0.2, 0.12), 0.9, noise=0.4)
    for dy in (-0.22, 0.22): cube((0, TRACK_Y + dy, 0.03), (40, 0.04, 0.05), rail)
    for k in range(-40, 41): cube((k * 0.5, TRACK_Y, 0.01), (0.12, 0.7, 0.03), slp)
    world_color(sky)
    light("SUN", (0, 0, 5), 1.4 if season != "snow" else 0.9, col=(1.0, 0.85, 0.7) if season in ("dusk", "autumn") else (0.75, 0.82, 1.0), rot=(0.9, 0.2, -0.6))
    light("AREA", (1.2, -4.0, 2.0), 25, col=(1.0, 0.88, 0.75), size=2.5, target=(0, 0, 1.0))


def train(n=4, lit=True, waving=False, rng=None):
    """A little train on the track: an engine and n carriages. Returns (root, passengers)."""
    root = empty("train", (0, 0, 0)); P, people = [], []
    body = mat("carriage", (0.2, 0.32, 0.28), 0.5, coat=0.3); trim = mat("ctrim", (0.85, 0.72, 0.3), 0.4, metal=0.5)
    win = mat("cwin", (1.0, 0.85, 0.55), 0.3, emit=(1.0, 0.8, 0.5), emit_str=3 if lit else 0)
    eng = mat("engine", (0.12, 0.12, 0.14), 0.4, metal=0.4)
    P += [cube((0, 0, 0.42), (1.3, 0.6, 0.6), eng, bevel=0.03), cyl((0.45, 0, 0.82), 0.08, 0.3, eng),
          cyl((-0.2, 0, 0.5), 0.27, 1.0, eng, rot=(0, math.pi / 2, 0))]
    for c in range(n):
        x = -1.5 - c * 1.6
        if waving:                                                        # open-sided carriage: low body, roof on posts, lit inside
            P += [cube((x, 0, 0.27), (1.45, 0.62, 0.26), body, bevel=0.02), cube((x, 0, 0.8), (1.5, 0.66, 0.05), trim)]
            for px in (-0.7, -0.23, 0.23, 0.7):
                for sy in (-1, 1): P.append(cube((x + px, sy * 0.3, 0.6), (0.05, 0.05, 0.4), body))
            P.append(light("POINT", (x, 0, 0.72), 6, col=(1.0, 0.8, 0.5), size=0.1))
        else:
            P += [cube((x, 0, 0.45), (1.45, 0.62, 0.62), body, bevel=0.03), cube((x, 0, 0.78), (1.5, 0.66, 0.05), trim)]
        for wx in (-0.45, 0.0, 0.45):
            if not waving:
                for sy in (-1, 1): P.append(cube((x + wx, sy * 0.312, 0.52), (0.3, 0.01, 0.22), win))
            if waving and rng:                                            # a passenger at each window on the cottage side
                k = peg((x + wx, 0.12, 0.3), rng.choice([(0.3, 0.45, 0.7), (0.8, 0.5, 0.2), (0.5, 0.3, 0.55), (0.3, 0.55, 0.35)]),
                        rng.choice(["sam", "neighbour1", "rose", "girl", "danny"]), rot=math.pi, h=0.42)
                people.append(k); P.append(k["root"])
    root.location = (0, 0, 0)
    for o in P:
        if o.parent is None: o.parent = root
    root.location = (0, TRACK_Y, 0)
    return root, people


def wave(d, t, rate=5.0, side="R"):
    d[side].rotation_euler[1] = (-2.75 if side == "R" else 2.75) + 0.3 * math.sin(t * rate)


def same_spot():
    """The fixed 'same spot' frame across the years: from beyond the track, looking at the window."""
    return _cam((0.55, -3.9, 1.25), (0.0, 0.0, 1.05), lens=52, fstop=5.0)


def her(year, loc=(-0.07, 0.25, 0.32)):
    if year == 1956: return peg((loc[0], loc[1], loc[2] + 0.22), DRESS, "girl", h=0.75, rot=0.0)
    if year == 1975: return peg(loc, (0.3, 0.45, 0.7), "margaret", hair=(0.4, 0.24, 0.12), rot=0.0)
    if year == 2001: return peg(loc, (0.55, 0.35, 0.5), "margaret", hair=(0.6, 0.58, 0.56), rot=0.0)
    return peg(loc, (0.62, 0.45, 0.55), "margaret", hair=(0.96, 0.96, 0.96), rot=0.0, h=0.94)


# ---------------------------------------------------------------- shots
def w1(rng):            # same window. seventy years apart.: slow push from wide to the empty lit window, dusk
    cottage(rng, "dusk"); c = _cam((1.4, -6.5, 1.3), (0, 0, 1.0), lens=36, fstop=6)
    def upd(t): c.location.y = -6.5 + 0.5 * t; c.location.x = 1.4 - 0.1 * t
    return upd


def w2(rng):            # 1956: a little girl waves at every train; the carriages are dark and empty
    cottage(rng, "dusk"); g = her(1956); tr, _ = train(4, lit=False); same_spot()
    sn = Flutter((0, -1, 1.5), [(0.98, 0.9, 0.55)], size=(5, 3, 2), n=30, rng=rng, flake=0.012)   # summer evening dust
    def upd(t):
        tr.location.x = 7 - 3.0 * t; wave(g, t); breathe(g, t); sn.update(t)
        g["root"].location.z = g["base"].z + 0.03 * abs(math.sin(t * 6))                # bouncing on her toes
    return upd


def w3(rng):            # 1975: she still waves, a baby on her hip; autumn leaves
    cottage(rng, "autumn"); m = her(1975); tr, _ = train(4, lit=False); same_spot()
    baby = sphere((0, 0, 0), 0.09, mat("blanket", (0.95, 0.85, 0.6), 0.9, sheen=0.6), scale=(1, 0.9, 1.3))
    bh = sphere((0, 0, 0), 0.06, mat("skin", (0.97, 0.80, 0.62), 0.55, noise=0.12))
    lv = Flutter((0, -0.8, 1.2), SEASONS["autumn"][1], size=(5, 3, 2.5), n=60, rng=rng)
    def upd(t):
        tr.location.x = 7 - 3.0 * t; wave(m, t, rate=4); breathe(m, t); lv.update(t)
        m["L"].rotation_euler[0] = -0.9
        baby.location = m["root"].location + Vector((-0.16, -0.08, 0.45)); bh.location = baby.location + Vector((0, -0.02, 0.12))
    return upd


def w4(rng):            # 2001: grey hair, still waving, in the rain
    cottage(rng, "rain"); m = her(2001); tr, _ = train(4, lit=False); same_spot()
    rn = Rain((0, -1.5, 0), size=(6, 4, 3), n=260, rng=rng)
    def upd(t): tr.location.x = 7 - 3.0 * t; wave(m, t, rate=3.5); breathe(m, t); rn.update(t)
    return upd


def w5(rng):            # 2026: she can barely stand, a stick in one hand; she waves anyway; snow
    cottage(rng, "snow"); m = her(2026); same_spot()
    stick = cyl((0, 0, 0), 0.012, 0.6, mat("stick", (0.35, 0.2, 0.1), 0.6))
    sn = Snow((0, -1.5, 0.2), size=(6, 4, 3), n=260, rng=rng)
    tr, _ = train(4, lit=True)
    def upd(t):
        sn.update(t); tr.location.x = 9 - 2.4 * max(0, t - 2.2)
        m["root"].rotation_euler[1] = 0.12; m["L"].rotation_euler[0] = -0.4
        stick.location = m["root"].location + Vector((-0.2, -0.05, 0.3))
        up = smooth((t - 1.8) / 1.2); m["R"].rotation_euler[1] = -(2.5 * up + 0.2 * math.sin(t * 3) * up)
    return upd


def w6(rng):            # and for the first time... every window on the train waves back: from inside, over her shoulder
    cottage(rng, "snow"); m = her(2026, loc=(-0.3, 0.3, 0.32)); m["root"].rotation_euler[2] = 0.25
    tr, people = train(4, lit=True, waving=True, rng=rng)
    sn = Snow((0, -1.5, 0.2), size=(6, 4, 3), n=200, rng=rng)
    c = _cam((0.12, 0.5, 1.22), (-0.2, TRACK_Y, 0.55), lens=26, fstop=4.0)
    def upd(t):
        sn.update(t); tr.location.x = 5.2 - 0.9 * t                      # the train slows right outside her window
        for i, p in enumerate(people): wave(p, t + i * 0.4, rate=6)
        m["R"].rotation_euler[1] = -(2.5 + 0.2 * math.sin(t * 3))
    return upd


SHOTS = {n: (globals()[n], _D[n]) for n in _D}
