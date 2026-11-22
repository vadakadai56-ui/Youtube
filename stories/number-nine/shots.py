"""Number Nine (Trend Short, Christmas kickoff, clay characters): the whole street turns its Christmas lights on at the same
minute every year, except number nine, where Mr Abel lives alone. This year the kids climb his ladder for him.
Render (no low-poly for clay): STYLE=none ENGINE=EEVEE PCT=50 ES=12 $VENV/bin/python pipeline/anim.py stories/number-nine OUT all"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
import scene                  # noqa
scene.STYLE = "clay"          # anything but "lowpoly": clay stays smooth
from world import *           # noqa
from world import cam as _cam
from characters import clay, clay_mat
import bpy
scene.LOOK = os.environ.get("LOOK") or "dream"      # per-video grade (scene.LOOKS)

_D = json.load(open(os.path.join(HERE, "durations.json")))
HOUSES = [-6.0, -3.0, 0.0, 3.0, 6.0]                                   # number nine is the one at x = 0
COLS = [(0.75, 0.45, 0.4), (0.5, 0.6, 0.75), (0.8, 0.72, 0.55), (0.55, 0.7, 0.55), (0.78, 0.55, 0.65)]
BULB_COLS = [(1, 0.25, 0.2), (0.25, 1, 0.35), (1, 0.85, 0.25), (0.35, 0.55, 1)]
KID = dict(col=(0.85, 0.3, 0.25), style="kid", hat=(0.25, 0.5, 0.85), scarf=(0.95, 0.85, 0.3), name="kid")
SIS = dict(col=(0.4, 0.7, 0.85), style="kid", hair=(0.35, 0.2, 0.1), scarf=(0.9, 0.4, 0.6), name="sis")
ABEL = dict(col=(0.35, 0.45, 0.6), style="old", glasses=True, name="abel")


def street_of(rng, lit_others=False, lit_nine=False, ladder=True):
    """Five clay houses in a row facing the camera, snow, one lamp. Returns {'others': mats, 'nine': mats, 'win9': mat}."""
    cube((0, 0, -0.05), (40, 40, 0.1), clay_mat("snowground", (0.9, 0.92, 0.97), 0.8))
    cube((0, -0.9, 0.003), (40, 0.9, 0.006), clay_mat("pavement", (0.7, 0.72, 0.78)))
    on_o = mat("bulbs_others", (1, 0.85, 0.5), 0.3, emit=(1, 0.8, 0.45), emit_str=6 if lit_others else 0)
    on_n = mat("bulbs_nine", (1, 0.85, 0.5), 0.3, emit=(1, 0.8, 0.45), emit_str=6 if lit_nine else 0)
    win = mat("win9", (1, 0.8, 0.5), 0.4, emit=(1, 0.75, 0.4), emit_str=2.5)
    bulb_mats = {"others": [], "nine": []}
    for i, x in enumerate(HOUSES):
        nine = x == 0.0; key = "nine" if nine else "others"
        cube((x, 1.0, 0.8), (2.2, 1.6, 1.6), clay_mat("house%d" % i, COLS[i]))
        cube((x, 1.0, 1.6), (2.4, 1.2, 1.2), clay_mat("roofsnow", (0.95, 0.96, 1.0)), rot=(math.pi / 4, 0, 0))   # snowy gable roof
        cube((x, 0.19, 0.5), (0.45, 0.04, 1.0), clay_mat("door%d" % i, (0.45, 0.2, 0.12)))
        for wx in (-0.65, 0.65): cube((x + wx, 0.19, 1.05), (0.45, 0.03, 0.4), win if nine else mat("winlit", (1, 0.8, 0.5), 0.4, emit=(1, 0.75, 0.4), emit_str=2.5))
        if nine: text("9", (x, 0.16, 1.15), 0.18, clay_mat("brass", (0.95, 0.75, 0.3)), rot=(math.pi / 2, 0, 0))
        for k in range(22):                                              # a string of bulbs along the roof edge
            bx = x - 1.05 + k * 0.1; c = BULB_COLS[k % 4]
            m = mat("bulb_%s_%d" % (key, k % 4), c, 0.3, emit=c, emit_str=8 if (lit_nine if nine else lit_others) else 0)
            sphere((bx, 0.16, 1.62 - 0.03 * abs(math.sin(k * 0.8))), 0.03, m, seg=8)
            if m not in bulb_mats[key]: bulb_mats[key].append(m)
    if ladder:
        lm = clay_mat("ladder", (0.6, 0.4, 0.22))
        for sx in (-0.15, 0.15): cube((0.9 + sx, 0.05, 1.0), (0.04, 0.04, 2.1), lm, rot=(-0.2, 0, 0))
        for k in range(8): cube((0.9, 0.05 + 0.03 * k - 0.12, 0.25 + k * 0.24), (0.32, 0.03, 0.03), lm, rot=(-0.2, 0, 0))
    cyl((-1.6, -1.2, 1.0), 0.035, 2.0, mat("lampm", (0.08, 0.08, 0.09), 0.4, metal=0.8))
    sphere((-1.6, -1.2, 2.05), 0.1, mat("lampglow", (1, 0.85, 0.6), 0.2, emit=(1, 0.78, 0.45), emit_str=18))
    light("POINT", (-1.6, -1.2, 1.95), 60, col=(1.0, 0.75, 0.45), size=0.15)
    world_color((0.04, 0.05, 0.12))
    light("SUN", (0, 0, 5), 0.5, col=(0.55, 0.65, 1.0), rot=(0.9, 0.2, 0.4))
    light("AREA", (0.5, -4.0, 2.5), 45, col=(1.0, 0.85, 0.7), size=3, target=(0, 0.5, 0.8))
    return bulb_mats


def set_lights(mats, k):
    for m in mats: bsdf(m).inputs["Emission Strength"].default_value = 8.0 * k


# ---------------------------------------------------------------- shots
def n1(rng):            # The day after Thanksgiving, my whole street turns its Christmas lights on.: the dark street, push in
    street_of(rng); sn = Snow((0, -0.5, 0.2), size=(10, 4, 3), n=260, rng=rng)
    c = _cam((0.0, -9.0, 1.6), (0, 1.0, 1.0), lens=34, fstop=8)
    def upd(t): sn.update(t); c.location.y = -9.0 + 0.4 * t
    return upd


def n2(rng):            # Same minute. Every year.: the houses flick on one after another, fast
    m = street_of(rng); sn = Snow((0, -0.5, 0.2), size=(10, 4, 3), n=260, rng=rng)
    c = _cam((0.0, -7.2, 1.5), (0, 1.0, 1.0), lens=34, fstop=8)
    def upd(t): sn.update(t); set_lights(m["others"], 1.0 if t > 0.5 else 0.0); set_lights(m["nine"], 0.0)
    return upd


def n3(rng):            # Except number nine.: close on the one dark house between the lit ones
    m = street_of(rng, lit_others=True); sn = Snow((0, -0.5, 0.2), size=(6, 3, 3), n=200, rng=rng)
    c = _cam((0.3, -3.2, 1.2), (0, 0.5, 1.2), lens=38, fstop=5)
    def upd(t): sn.update(t); c.location.y = -3.2 + 0.15 * t
    return upd


def n4(rng):            # Mr Abel lives alone. His ladder's too tall for him now.: at his window, looking at the ladder
    street_of(rng, lit_others=True); a = clay((-0.35, -0.25, 0), rot=0.2, mouth="flat", **ABEL)
    sn = Snow((0, -0.5, 0.2), size=(5, 3, 3), n=160, rng=rng)
    c = _cam((-0.55, -1.7, 0.75), (-0.35, -0.25, 0.6), lens=40, fstop=2.8)
    def upd(t):
        sn.update(t); breathe(a, t, 0.5); a["head"].rotation_euler[2] = -0.6 * smooth((t - 1.6) / 0.8)   # he looks over at the ladder
        look_at(c, Vector((-0.35, -0.25, 0.6)).lerp(Vector((0.9, 0.1, 1.4)), smooth((t - 1.8) / 1.2)))
    return upd


def n5(rng):            # So this year, at 5:59... we climbed it for him.: the kids on the ladder, hanging the bulbs
    m = street_of(rng, lit_others=False); sn = Snow((0, -0.5, 0.2), size=(5, 3, 3), n=160, rng=rng)
    k = clay((0.9, -0.05, 0.9), rot=math.pi, **KID); s = clay((0.35, -0.5, 0), rot=-0.3, **SIS)
    c = _cam((2.0, -2.4, 1.2), (0.6, 0.2, 1.2), lens=32, fstop=4)
    def upd(t):
        sn.update(t); k["root"].location.z = 0.9 + 0.12 * smooth(t / 2.0)
        k["L"].rotation_euler[0] = -2.6 + 0.2 * math.sin(t * 5); k["R"].rotation_euler[0] = -2.4 + 0.2 * math.sin(t * 5 + 1.5)
        s["R"].rotation_euler[1] = -2.0; breathe(s, t)
    return upd


def n6(rng):            # 6:00.: close on a little mitten pressing the plug into the socket
    street_of(rng); cube((-0.3, 0.17, 0.3), (0.12, 0.03, 0.16), clay_mat("socket", (0.95, 0.95, 0.93)))
    plug = cube((0, 0, 0), (0.07, 0.06, 0.08), clay_mat("plug", (0.2, 0.55, 0.25)))
    mit = sphere((0, 0, 0), 0.05, clay_mat("mitten", (0.95, 0.85, 0.3)), scale=(1, 0.8, 1.2))
    c = _cam((-0.1, -0.45, 0.4), (-0.3, 0.17, 0.3), lens=50, fstop=2.0)
    def upd(t):
        y = 0.0 + 0.12 * (1 - smooth((t - 0.2) / 0.4)); plug.location = (-0.3, 0.12 - y, 0.3); mit.location = (-0.3, 0.06 - y, 0.3)
    return upd


def n7(rng):            # The whole street lit up.: wide, every house blazes on together
    m = street_of(rng); sn = Snow((0, -0.5, 0.2), size=(10, 4, 3), n=260, rng=rng)
    c = _cam((0.0, -8.0, 1.5), (0, 1.0, 1.1), lens=32, fstop=8)
    def upd(t):
        sn.update(t); set_lights(m["nine"], 1.0 if t > 0.05 else 0.0); set_lights(m["others"], 1.0 if t > 0.35 else 0.0)
        c.location.y = -8.0 - 0.3 * t
    return upd


def n8(rng):            # Number nine first.: Mr Abel at his open door under his lights, the kids waving
    m = street_of(rng, lit_others=True, lit_nine=True); sn = Snow((0, -0.5, 0.2), size=(5, 3, 3), n=160, rng=rng)
    a = clay((0.0, 0.0, 0), mouth="smile", **ABEL); k = clay((0.6, -0.9, 0), rot=2.6, **KID); s = clay((-0.6, -0.9, 0), rot=-2.6, **SIS)
    c = _cam((0.2, -2.6, 0.9), (0, 0.0, 0.75), lens=36, fstop=3.5)
    def upd(t):
        sn.update(t); a["R"].rotation_euler[1] = -2.3 + 0.3 * math.sin(t * 5)
        for d in (k, s): d["R"].rotation_euler[1] = -2.4 + 0.3 * math.sin(t * 6); d["root"].location.z = 0.02 * abs(math.sin(t * 7))
    return upd


SHOTS = {n: (globals()[n], _D[n]) for n in _D}
