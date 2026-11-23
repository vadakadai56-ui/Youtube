"""The Last Door (format 1, emotional twist, clay characters, advent): Grandad's handmade advent calendar has 25 doors; for 11
years he never opened the last one. This year he gives it to me: inside is a key to the shed, and a new box with my name on it.
Render (no low-poly for clay): ENGINE=EEVEE PCT=50 ES=12 $VENV/bin/python pipeline/anim.py stories/the-last-door OUT all"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
import scene                  # noqa
scene.STYLE = "clay"
from world import *           # noqa
from world import cam as _cam
from characters import clay, clay_mat, say, spans
import bpy
scene.LOOK = os.environ.get("LOOK") or "story"      # per-video grade (scene.LOOKS)

_D = json.load(open(os.path.join(HERE, "durations.json")))
_W = json.load(open(os.path.join(HERE, "words.json")))
_S = {n: sum(list(_D.values())[:i]) for i, n in enumerate(_D)}      # shot start, global seconds
GRANDAD = dict(col=(0.45, 0.35, 0.3), style="old", glasses=True, name="grandad")
ME = dict(col=(0.3, 0.45, 0.7), style="kid", hair=(0.45, 0.28, 0.12), scarf=(0.9, 0.75, 0.3), name="me")
AUNT = dict(col=(0.75, 0.45, 0.55), style="adult", hair=(0.25, 0.15, 0.1), name="aunt")
COUSIN = dict(col=(0.4, 0.65, 0.45), style="kid", hat=(0.9, 0.3, 0.3), name="cousin")
NAME = "MILO"


def advent(loc, painted=True, opened=(), scale=1.0, name=None):
    """The cigar-box advent calendar, front facing -y: 25 little doors (5 x 5), door 25 bigger and red.
    Returns {'doors': {n: hinge}, 'root': empty, 'items': {n: obj}}."""
    root = empty("advent", (0, 0, 0)); P = []
    wood = clay_mat("cigar" if painted else "rawwood", (0.55, 0.32, 0.18) if painted else (0.85, 0.72, 0.52))
    P.append(cube((0, 0.06, 0.2), (0.5, 0.12, 0.42), wood))
    P.append(cube((0, 0.06, 0.425), (0.52, 0.14, 0.03), clay_mat("lid" if painted else "rawlid", (0.45, 0.25, 0.14) if painted else (0.8, 0.68, 0.48))))
    if name: P.append(text(name, (0, 0.06, 0.442), 0.06, clay_mat("carve", (0.45, 0.3, 0.18)), rot=(0, 0, 0)))
    cols = [(0.85, 0.25, 0.2), (0.2, 0.5, 0.3), (0.95, 0.8, 0.3), (0.3, 0.45, 0.75), (0.95, 0.95, 0.9)]
    doors, items = {}, {}
    for n in range(1, 26):
        r, cidx = (n - 1) // 5, (n - 1) % 5
        x = -0.18 + cidx * 0.09; z = 0.36 - r * 0.075
        big = n == 25
        w, hgt = (0.075, 0.065)
        col = (0.75, 0.12, 0.12) if big else (cols[(n * 3) % 5] if painted else (0.88, 0.76, 0.56))
        hinge = empty("door%d" % n, (x - w / 2, -0.002, z)); P.append(hinge)
        d = cube((x, -0.004, z), (w, 0.008, hgt), clay_mat("adoor%d_%d" % (n, painted), col))
        d.parent = hinge; d.location = Vector(d.location) - Vector(hinge.location)
        if painted:
            t = text(str(n), (x, -0.009, z - 0.012), 0.028, clay_mat("num", (0.98, 0.96, 0.9)), rot=(math.pi / 2, 0, 0))
            t.parent = hinge; t.location = Vector(t.location) - Vector(hinge.location)
        if n in opened: hinge.rotation_euler[2] = -1.9
        doors[n] = hinge
    for o in P:
        if o.parent is None: o.parent = root
    root.location = loc; root.scale = (scale,) * 3
    return {"doors": doors, "root": root}


def room(rng, warm=True, dim=False):
    cube((0, 0, -0.05), (10, 10, 0.1), clay_mat("lfloor", (0.5, 0.36, 0.24)))
    w = clay_mat("lwall", (0.86, 0.72, 0.55))
    cube((0, 1.6, 1.5), (6, 0.1, 3), w); cube((-2.0, 0, 1.5), (0.1, 6, 3), w); cube((2.0, 0, 1.5), (0.1, 6, 3), w)
    cube((0.8, 1.54, 1.4), (0.7, 0.02, 0.8), mat("lwin", (0.15, 0.2, 0.4), 0.5, emit=(0.2, 0.25, 0.45), emit_str=1.0))
    world_color((0.05, 0.04, 0.05))
    light("POINT", (-0.4, 0.2, 1.3), 40 if not dim else 15, col=(1.0, 0.68, 0.38), size=0.3)
    light("AREA", (0.3, -2.2, 1.8), 30 if not dim else 12, col=(1.0, 0.85, 0.7), size=2.5, target=(0, 0.5, 0.6))


def table(loc=(0, 0.4, 0)):
    x, y, z = loc; tm = clay_mat("ltable", (0.55, 0.35, 0.2))
    cube((x, y, 0.55), (1.0, 0.6, 0.05), tm)
    for sx in (-0.45, 0.45):
        for sy in (-0.25, 0.25): cube((x + sx, y + sy, 0.27), (0.05, 0.05, 0.55), tm)


def sit(d):
    for l in ("LL", "LR"): d[l].rotation_euler[0] = -math.pi / 2


# ---------------------------------------------------------------- shots
def d1(rng):            # Grandad's advent calendar has twenty-five little doors.: close on the box in candlelight, slow push
    room(rng); table(); a = advent((0, 0.4, 0.575)); candle((0.4, 0.45, 0.575))
    c = _cam((0.12, -0.25, 0.8), (0, 0.4, 0.8), lens=46, fstop=2.2)
    def upd(t): c.location.y = -0.25 + 0.05 * t
    return upd


def d2(rng):            # He made it himself, out of an old cigar box.: years ago, Grandad at his workbench, painting a door
    room(rng); table(); a = advent((0, 0.45, 0.575), painted=False); g = clay((0, 1.0, 0), rot=math.pi, mouth="smile", **GRANDAD)
    brush = cyl((0, 0, 0), 0.008, 0.12, clay_mat("brush", (0.6, 0.4, 0.2)))
    c = _cam((0.55, -0.35, 0.95), (0, 0.6, 0.7), lens=40, fstop=2.4)
    def upd(t):
        g["R"].rotation_euler[0] = -1.4; brush.location = g["root"].location + Vector((0.12, -0.42, 0.55 + 0.01 * math.sin(t * 9)))
        brush.rotation_euler = (1.0, 0, 0)
    return upd


def d3(rng):            # Every December, he opens one door a day. A chocolate. A button. A tiny paper star.
    room(rng); table(); a = advent((0, 0.4, 0.575), opened=())
    ch = cube((0, 0, 0), (0.03, 0.012, 0.03), clay_mat("choc", (0.35, 0.2, 0.1)))
    bt = cyl((0, 0, 0), 0.016, 0.006, clay_mat("button", (0.85, 0.2, 0.3)), rot=(math.pi / 2, 0, 0))
    star = cyl((0, 0, 0), 0.018, 0.004, clay_mat("star", (1.0, 0.85, 0.25)), verts=5, rot=(math.pi / 2, 0, 0))
    c = _cam((0.02, -0.12, 0.88), (0, 0.4, 0.86), lens=50, fstop=2.0)
    seq = [(1, 3.1, ch), (2, 4.2, bt), (3, 5.2, star)]                     # door, local open time, the treasure inside
    def upd(t):
        for n, t0, item in seq:
            k = smooth((t - t0) / 0.35); a["doors"][n].rotation_euler[2] = -1.9 * k
            r, cidx = (n - 1) // 5, (n - 1) % 5
            item.location = (-0.18 + cidx * 0.09, 0.38, 0.575 + 0.36 - r * 0.075)
            item.scale = (k + 0.001,) * 3
    return upd


def d4(rng):            # But for eleven years... he never opened the last one. "Not yet," he says. "Not this year.": Grandad taps door 25
    room(rng); table(); a = advent((-0.14, 0.35, 0.575), opened=tuple(range(1, 25)), scale=0.65)
    g = clay((0.24, 0.8, 0), rot=0.25, **GRANDAD); k = clay((-0.22, -0.15, 0), rot=math.pi * 0.9, **ME)
    c = _cam((0.0, -1.2, 0.95), (0.05, 0.3, 0.72), lens=32, fstop=3.2)
    lines = spans(_W, 18.5, 19.1, _S["d4"]) + spans(_W, 20.7, 21.5, _S["d4"])     # "Not yet," ... "Not this year."
    def upd(t):
        say(g, t, lines)
        tap = abs(math.sin(t * 5)) * (3.6 < t < 5.0); g["L"].rotation_euler[0] = -1.0 - 0.15 * tap
        g["head"].rotation_euler[2] = 0.25 * math.sin(t * 1.1) * (t > 5.5); breathe(k, t)
        c.location.y = -1.2 + 0.04 * t
    return upd


def d5(rng):            # My cousins think it's empty. My aunt thinks it's stuck.: a cousin shakes the box, the aunt tugs the little door
    room(rng); table(); a = advent((0, 0.4, 0.575), opened=tuple(range(1, 25)))
    cz = clay((-0.4, 0.15, 0), rot=-0.5, mouth="open", **COUSIN); au = clay((0.45, 0.15, 0), rot=0.5, mouth="flat", **AUNT)
    c = _cam((0.0, -1.0, 0.95), (0, 0.4, 0.7), lens=34, fstop=3)
    def upd(t):
        a["root"].location.x = 0.01 * math.sin(t * 30) * (t < 1.8); cz["R"].rotation_euler[0] = -1.2 * (t < 1.9)
        au["L"].rotation_euler[0] = -1.3 * (t > 2.0); a["doors"][25].rotation_euler[2] = -0.06 * abs(math.sin(t * 20)) * (t > 2.2)
    return upd


def d6(rng):            # I asked him once. He just tapped the little door and smiled.: close two-shot by the fire
    room(rng); table(); a = advent((-0.12, 0.35, 0.575), opened=tuple(range(1, 25)), scale=0.65)
    g = clay((0.22, 0.8, 0), rot=0.2, mouth="smile", **GRANDAD); k = clay((-0.2, -0.05, 0), rot=math.pi * 0.92, mouth="open", **ME)
    c = _cam((0.05, -0.75, 0.85), (0.1, 0.6, 0.78), lens=40, fstop=2.6)
    def upd(t):
        tap = abs(math.sin(t * 5)) * (1.4 < t < 2.6); g["L"].rotation_euler[0] = -1.0 - 0.15 * tap
        g["head"].rotation_euler[0] = -0.05 * smooth((t - 2.6) / 0.6)
    return upd


def d7(rng):            # This year, Grandad couldn't come down the stairs.: the empty armchair at the foot of the stairs
    room(rng, dim=True); chm = clay_mat("armchair", (0.55, 0.25, 0.2))
    cube((0.4, 0.8, 0.25), (0.6, 0.55, 0.4), chm); cube((0.4, 1.05, 0.6), (0.6, 0.12, 0.6), chm)
    for sx in (0.12, 0.68): cube((sx, 0.8, 0.5), (0.1, 0.55, 0.3), chm)
    st = clay_mat("stairs", (0.6, 0.42, 0.28))
    for k in range(8): cube((-1.2, 0.5 + k * 0.25, 0.1 + k * 0.2), (0.8, 0.3, 0.2), st)
    c = _cam((0.2, -1.4, 1.0), (-0.3, 0.8, 0.8), lens=30, fstop=3.5)
    def upd(t): c.location.y = -1.4 + 0.04 * t
    return upd


def d8(rng):            # So I carried the calendar up to him. Door twenty-five.: climbing the stairs with the box held out in front
    room(rng, dim=True); st = clay_mat("stairs", (0.6, 0.42, 0.28))
    for k in range(8): cube((-0.2, 0.1 + k * 0.25, 0.1 + k * 0.2), (0.8, 0.3, 0.2), st)
    k_ = clay((-0.2, 0.0, 0.0), rot=math.pi, **ME); a = advent((0, 0, 0), opened=tuple(range(1, 25)), scale=0.8)
    a["root"].rotation_euler[2] = math.pi
    c = _cam((0.8, -0.8, 0.8), (-0.2, 0.6, 0.9), lens=30, fstop=3)
    def upd(t):
        y = 0.0 + 0.32 * t; z = max(0.0, (y - 0.0) / 0.25 * 0.2); k_["root"].location = Vector((-0.2, y, z))
        k_["L"].rotation_euler[0] = k_["R"].rotation_euler[0] = -1.4
        a["root"].location = k_["root"].location + Vector((0, 0.22, 0.32))
        s = math.sin(t * 7); k_["LL"].rotation_euler[0] = 0.4 * s; k_["LR"].rotation_euler[0] = -0.4 * s
        look_at(c, k_["root"].location + Vector((0, 0, 0.5)))
    return upd


def bedroom(rng):
    room(rng, dim=True); bm = clay_mat("bedc", (0.85, 0.8, 0.7))
    cube((0.3, 0.9, 0.22), (0.9, 1.4, 0.35), clay_mat("bedframe", (0.5, 0.32, 0.18))); cube((0.3, 0.9, 0.42), (0.85, 1.3, 0.12), bm)
    cube((0.3, 1.45, 0.52), (0.6, 0.25, 0.12), clay_mat("pillow", (0.96, 0.95, 0.92)))


def d9(rng):            # He put it in my hands. "It was always yours.": Grandad in bed, handing the box over
    bedroom(rng); g = clay((0.3, 1.2, 0.3), mouth="smile", **GRANDAD); g["root"].rotation_euler[0] = -0.2; sit(g)
    k = clay((0.05, 0.3, 0), rot=math.pi, **ME); a = advent((0, 0, 0), opened=tuple(range(1, 25)), scale=0.8)
    c = _cam((0.2, -0.75, 1.05), (0.22, 0.9, 0.7), lens=32, fstop=3.0)
    def upd(t):
        p_ = smooth((t - 0.4) / 1.4); src = Vector((0.15, 0.8, 0.62)); dst = k["root"].location + Vector((0.0, 0.2, 0.42))
        a["root"].location = src.lerp(dst, p_); a["root"].rotation_euler[2] = math.pi * p_
        k["L"].rotation_euler[0] = k["R"].rotation_euler[0] = -1.3 * p_; g["R"].rotation_euler[0] = -1.2 * (1 - p_)
    return upd


def d10(rng):           # Inside was a tiny key. And a note in his wobbly writing.: door 25 swings open
    room(rng); table(); a = advent((0, 0.4, 0.575), opened=tuple(range(1, 25)))
    key = group("key", [torus((0, 0, 0.012), 0.008, 0.003, mat("brasskey", (0.95, 0.75, 0.3), 0.3, metal=1.0)),
                        cube((0, 0, -0.004), (0.003, 0.003, 0.022), mat("brasskey", (0.95, 0.75, 0.3), 0.3, metal=1.0))], (0, 0, 0))
    note = cube((0, 0, 0), (0.035, 0.002, 0.025), clay_mat("note", (0.96, 0.94, 0.86)))
    c = _cam((0.12, -0.12, 0.7), (0.18, 0.4, 0.64), lens=50, fstop=3.0)
    def upd(t):
        k = smooth((t - 0.3) / 0.6); a["doors"][25].rotation_euler[2] = -1.9 * k
        key.location = (0.18, 0.385, 0.64); note.location = (0.2, 0.39, 0.625); note.rotation_euler = (0, 0.2, 0)
        c.location.y = -0.12 + 0.02 * t
    return upd


def d11(rng):           # "For the shed.": the note, close, in shaky handwriting
    cube((0, 0, 0), (0.6, 0.4, 0.002), clay_mat("notebig", (0.96, 0.94, 0.86)))
    text("For the shed.", (0, 0, 0.003), 0.07, mat("ink", (0.15, 0.15, 0.3), 0.6), rot=(0, 0, 0.03))
    world_color((0.1, 0.08, 0.06)); light("POINT", (0.2, -0.2, 0.6), 20, col=(1.0, 0.75, 0.45), size=0.2)
    c = camera((0, -0.02, 0.8), (0, 0.0, 0.0), lens=45)
    def upd(t): pass
    return upd


def shed(rng):
    cube((0, 0, -0.05), (10, 10, 0.1), clay_mat("shedfloor", (0.45, 0.38, 0.3)))
    pl = clay_mat("planks", (0.55, 0.4, 0.26))
    cube((0, 1.4, 1.2), (4, 0.1, 2.4), pl); cube((-1.6, 0, 1.2), (0.1, 4, 2.4), pl); cube((1.6, 0, 1.2), (0.1, 4, 2.4), pl)
    cube((0, 1.0, 0.45), (1.6, 0.6, 0.06), clay_mat("bench", (0.6, 0.45, 0.28)))
    for k in range(5): cyl((-0.9 + k * 0.4, 1.33, 1.3), 0.03, 0.3, clay_mat("tool%d" % k, [(0.5, 0.5, 0.55), (0.6, 0.35, 0.2)][k % 2]))
    world_color((0.2, 0.22, 0.3))
    light("SPOT", (0, -0.5, 2.2), 120, col=(0.9, 0.92, 1.0), target=(0, 1.0, 0.5), spot=0.9)
    light("POINT", (0.4, 0.6, 1.5), 15, col=(1.0, 0.75, 0.45), size=0.3)


def d12(rng):           # In the shed... a brand new box. Twenty-five little doors. Unpainted.: the door creaks open on the workbench
    shed(rng); a = advent((0, 1.0, 0.48), painted=False, name=None)
    door = empty("sheddoor", (-0.5, -0.6, 0)); dd = cube((0, -0.6, 1.0), (1.0, 0.06, 2.0), clay_mat("sdoor", (0.45, 0.3, 0.2)))
    dd.parent = door; dd.location = Vector(dd.location) - Vector(door.location)
    c = _cam((0.1, -1.4, 1.0), (0, 1.0, 0.6), lens=30, fstop=3)
    def upd(t):
        door.rotation_euler[2] = -1.8 * smooth(t / 1.2)
        c.location.y = -1.4 + 0.25 * smooth((t - 1.0) / 4.0); look_at(c, Vector((0, 1.0, 0.6)))
    return upd


def d13(rng):           # And my name, carved on the lid.: top-down on the lid, the name carved in
    shed(rng); a = advent((0, 1.0, 0.48), painted=False, name=NAME)
    c = camera((0.0, 0.85, 1.25), (0.0, 1.06, 0.92), lens=50, dof=0.42, fstop=2.2)
    def upd(t): c.location.z = 1.25 - 0.04 * t
    return upd


def d14(rng):           # The note said... "Your turn. Make one for someone you love.": me at the bench with a brush, the first door painted
    shed(rng); a = advent((0, 1.0, 0.48), painted=False, name=NAME)
    k = clay((0.0, 0.5, 0), rot=math.pi, **ME); brush = cyl((0, 0, 0), 0.008, 0.12, clay_mat("brush", (0.6, 0.4, 0.2)))
    first = cube((0, 0, 0), (0.075, 0.009, 0.065), clay_mat("firstred", (0.85, 0.25, 0.2)))
    c = _cam((0.75, 0.55, 0.95), (0.0, 1.0, 0.75), lens=34, fstop=2.8)
    def upd(t):
        k["R"].rotation_euler[0] = -1.4; brush.location = k["root"].location + Vector((0.14, 0.4, 0.58 + 0.01 * math.sin(t * 9)))
        p_ = smooth((t - 1.0) / 2.0); first.location = (-0.18, 0.993, 0.48 + 0.36); first.scale = (p_ + 0.001, 1, 1)
        c.location.x = 0.75 - 0.04 * t
    return upd


SHOTS = {n: (globals()[n], _D[n]) for n in _D}

CALM = {"d1", "d4", "d6", "d7", "d9", "d11", "d12", "d13", "d14"}   # slow shots rendered at 6 fps (edit.py blends to 30)
