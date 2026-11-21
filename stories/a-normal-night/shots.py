"""A Normal Night: anticlimax POV. Every scare is shot dark (one cold light, creeping camera), every reveal bright and flat.
Render: STYLE=lowpoly ENGINE=EEVEE PCT=50 ES=12 $VENV/bin/python pipeline/anim.py stories/a-normal-night OUT all"""
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
ME = (0.3, 0.55, 0.42)          # the narrator's green hoodie
DAD = (0.35, 0.3, 0.45)
GRAN = (0.7, 0.45, 0.6)


# ---------------------------------------------------------------- props
def cat(loc, rot=0.0, col=(0.85, 0.5, 0.2)):
    x, y, z = loc; m = mat("catfur", col, 0.9, sheen=0.6, noise=0.3); P = []
    P.append(sphere((x, y, z + 0.09), 0.09, m, scale=(1, 1.5, 0.85)))
    P.append(sphere((x, y - 0.14, z + 0.17), 0.065, m))
    for sx in (-1, 1):
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.022, depth=0.05, location=(x + sx * 0.035, y - 0.14, z + 0.235))
        o = bpy.context.object; o.data.materials.append(m); P.append(o)
        P.append(sphere((x + sx * 0.025, y - 0.2, z + 0.18), 0.011, mat("cateye", (0.1, 0.3, 0.05), 0.1, emit=(0.4, 0.9, 0.2), emit_str=0.6)))
    P.append(cyl((x, y + 0.16, z + 0.14), 0.014, 0.18, m, rot=(0.7, 0, 0)))
    g = group("cat", P, loc); g.rotation_euler[2] = rot
    return g


def snowman(loc, smile=True):
    x, y, z = loc; sm = mat("snowbody", (0.96, 0.97, 1.0), 0.6); P = []
    P += [sphere((x, y, z + 0.35), 0.35, sm), sphere((x, y, z + 0.85), 0.25, sm), sphere((x, y, z + 1.22), 0.18, sm)]
    blk = mat("coal", (0.02, 0.02, 0.02), 0.4)
    for sx in (-1, 1): P.append(sphere((x + sx * 0.06, y - 0.16, z + 1.27), 0.022, blk))
    if smile:
        for k in range(5): P.append(sphere((x - 0.06 + k * 0.03, y - 0.165, z + 1.16 - 0.012 * (2 - abs(k - 2))), 0.012, blk))
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.03, depth=0.15, location=(x, y - 0.24, z + 1.22), rotation=(math.pi / 2, 0, 0))
    o = bpy.context.object; o.data.materials.append(mat("carrot", (0.95, 0.45, 0.1), 0.6)); P.append(o)
    P.append(cyl((x, y, z + 1.42), 0.13, 0.14, mat("bucket", (0.75, 0.15, 0.12), 0.4)))
    P.append(torus((x, y, z + 1.02), 0.17, 0.035, mat("sscarf", (0.2, 0.5, 0.8), 0.9, sheen=0.8)))
    return group("snowman", P, loc)


def phone(loc, glow=True):
    x, y, z = loc
    b = cube((x, y, z + 0.006), (0.07, 0.14, 0.012), mat("phone", (0.05, 0.05, 0.06), 0.3, metal=0.5), bevel=0.004)
    s = cube((x, y, z + 0.0125), (0.062, 0.128, 0.001), mat("pscreen", (0.6, 0.8, 1.0), 0.2, emit=(0.6, 0.8, 1.0), emit_str=3 if glow else 0))
    return [b, s]


def xmas_lights(x0, x1, y, z, on=True):
    bulbs = []
    for i in range(int((x1 - x0) / 0.12)):
        x = x0 + i * 0.12; c = [(1, 0.2, 0.2), (0.2, 1, 0.3), (1, 0.85, 0.2), (0.3, 0.5, 1)][i % 4]
        bulbs.append(sphere((x, y, z - 0.04 * abs(math.sin(i * 0.9))), 0.025, mat("xl%d" % (i % 4), c, 0.3, emit=c, emit_str=8 if on else 0), seg=8))
    return bulbs


def house_front(rng, lights_on=True, xmas=True, snow_on_roof=True):
    """Our house from the front garden: a path, a porch with a lamp, two windows, a snowy roof, a bush."""
    cube((0, 0, -0.05), (30, 30, 0.1), mat("gsnow", (0.82, 0.86, 0.95), 0.7, noise=0.2))
    cube((0, -1.2, 0.003), (0.7, 3.0, 0.006), mat("path", (0.45, 0.42, 0.4), 0.8, noise=0.4))
    wall = mat("hwall", (0.62, 0.42, 0.34), 0.85, noise=0.3)
    cube((0, 0.6, 1.1), (3.2, 1.4, 2.2), wall)
    roof = cube((0, 0.6, 2.45), (3.5, 1.7, 0.5), mat("hroof", (0.3, 0.2, 0.18), 0.8), rot=(0, 0, 0))
    if snow_on_roof: cube((0, 0.6, 2.75), (3.5, 1.7, 0.12), mat("roofsnow2", (0.95, 0.96, 1.0), 0.7))
    cube((0, -0.12, 0.6), (0.6, 0.04, 1.2), mat("fdoor", (0.25, 0.12, 0.08), 0.6, noise=0.5))
    win = mat("fwin", (1, 0.8, 0.5), 0.4, emit=(1, 0.75, 0.4), emit_str=5 if lights_on else 0)
    for x in (-0.95, 0.95): cube((x, -0.11, 1.3), (0.6, 0.02, 0.55), win)
    cube((0, -0.13, 1.45), (0.12, 0.02, 0.06), mat("porchlamp", (1, 0.85, 0.6), 0.3, emit=(1, 0.75, 0.45), emit_str=10 if lights_on else 0))
    if lights_on: light("POINT", (0, -0.5, 1.5), 25, col=(1.0, 0.75, 0.45), size=0.2)
    for _ in range(4): sphere((1.3 + rng.uniform(-0.2, 0.2), -0.6, 0.25), rng.uniform(0.2, 0.3), mat("bush", (0.15, 0.3, 0.18), 0.8))
    bulbs = xmas_lights(-1.6, 1.6, -0.18, 2.18, on=lights_on) if xmas else []
    world_color((0.03, 0.05, 0.12))
    light("SUN", (0, 0, 5), 0.5, col=(0.55, 0.65, 1.0), rot=(0.9, 0.2, 0.4))
    return {"win": win, "bulbs": bulbs}


def room(rng, **kw):
    """The dining room without its chairs (they block the door and the window here)."""
    h = dining_room(rng, outside="snow", food=False, **kw)
    for ch in h["seats"].values():
        ch.location.z = -10
    return h


def scare(target, key=(1.2, -1.5, 2.0), cold=(0.35, 0.45, 1.0)):
    """Horror lighting: dim every light, add one cold key light and darken the world."""
    for ob in bpy.data.objects:
        if ob.type == "LIGHT": ob.data.energy *= 0.12
    light("SPOT", key, 140, col=cold, target=target, spot=0.6)
    world_color((0.005, 0.007, 0.015))


def bright():
    """Reveal lighting: flat, bright, normal."""
    light("AREA", (0.5, -2.0, 2.5), 120, col=(1.0, 0.95, 0.88), size=3, target=(0, 0.5, 0.6))


# ---------------------------------------------------------------- shots
def n1(rng):            # In my town... a normal night is terrifying: the house at night, creeping push
    house_front(rng); scare((0, 0.4, 1.0), key=(-2.5, -3, 3))
    c = _cam((0.4, -5.0, 0.9), (0, 0.3, 1.2), lens=32, fstop=4)
    snow = Snow((0, -1.5, 0.2), size=(5, 4, 3), n=200, rng=rng)
    def upd(t): c.location.y = -5.0 + 0.25 * t; snow.update(t)
    return upd


def n2(rng):            # something scratched at the back door
    h = room(rng, candles=False); scare((-1.68, 1.35, 0.8), key=(-0.6, 0.3, 1.8))
    c = _cam((-0.6, 0.55, 0.9), (-1.68, 1.35, 0.7), lens=34, fstop=2.4)
    def upd(t):
        h["door"].rotation_euler[2] = -0.012 * math.sin(t * 30) * (math.sin(t * 2.2) > 0.3); c.location.x = -0.6 - 0.04 * t
    return upd


def n3(rng):            # slow. patient. scratch... scratch...: creeping close-up on the bottom of the door
    h = room(rng, candles=False); scare((-1.68, 1.35, 0.2), key=(-1.0, 0.8, 0.9))
    c = _cam((-1.1, 1.05, 0.45), (-1.68, 1.35, 0.2), lens=42, fstop=2.0)
    def upd(t):
        h["door"].rotation_euler[2] = -0.01 * math.sin(t * 34) * (math.sin(t * 1.6) > 0.2); c.location.x = -1.1 - 0.05 * t
    return upd


def n4(rng):            # I opened it: the door swings into darkness
    h = room(rng, candles=False); scare((-1.68, 1.35, 0.8), key=(-0.6, 0.3, 1.8))
    me = peg((-1.2, 1.0, 0), ME, "sam", rot=math.pi / 2 + 0.3)
    c = _cam((-0.5, 0.4, 1.0), (-1.7, 1.35, 0.6), lens=32, fstop=2.4)
    def upd(t): h["door"].rotation_euler[2] = 1.2 * smooth(t / 0.8); me["R"].rotation_euler[0] = -1.2
    return upd


def n5(rng):            # REVEAL: it was the cat. She wanted in. (bright)
    h = room(rng); h["door"].rotation_euler[2] = 1.2; bright()
    k = cat((-1.5, 1.35, 0), rot=-math.pi / 2)
    c = _cam((-0.9, 1.0, 0.45), (-1.5, 1.35, 0.15), lens=40, fstop=3)
    def upd(t):
        k.location.x = -1.5 + 0.18 * min(1, t / 1.5); k.location.z = 0.01 * abs(math.sin(t * 10))
    return upd


def n6(rng):            # at eight, a face in the window: from inside, a pale round shape behind the glass
    h = room(rng, candles=False); scare((0, 2.6, 1.45), key=(0.6, 1.0, 2.2))
    s = snowman((0.05, 2.68, 0.25), smile=False)
    c = _cam((0.3, 0.6, 1.2), (0, 2.6, 1.45), lens=40, fstop=3)
    def upd(t): c.location.y = 0.6 + 0.12 * t
    return upd


def n7(rng):            # pale. round. smiling.: push in close on the face
    h = room(rng, candles=False); scare((0, 2.6, 1.45), key=(0.4, 2.0, 2.0))
    s = snowman((0.05, 2.68, 0.25))
    c = _cam((0.08, 1.45, 1.45), (0.05, 2.6, 1.45), lens=46, fstop=2.2)
    def upd(t): c.location.y = 1.45 + 0.12 * t
    return upd


def n8(rng):            # REVEAL: it was the snowman, outside, cheerful, bright
    house_front(rng); bright()
    s = snowman((-1.1, -1.2, 0)); me = peg((-0.5, -1.4, 0), ME, "sam", rot=0.3)
    c = _cam((-0.6, -3.6, 1.0), (-0.9, -1.2, 0.8), lens=36, fstop=4)
    def upd(t): breathe(me, t); me["R"].rotation_euler[0] = -1.8 + 0.3 * math.sin(t * 6)
    return upd


def n9(rng):            # at nine... footsteps on the roof. heavy ones.: looking up at the dark ceiling, dust falls
    h = room(rng, candles=False); scare((0, 1.0, 2.6), key=(0.5, -0.5, 1.0))
    me = peg((0.3, 0.2, 0), ME, "sam", rot=math.pi)
    dust = [sphere((rng.uniform(-0.6, 0.6), rng.uniform(0.3, 1.5), 2.6), 0.006, mat("cdust", (0.9, 0.9, 1.0), 0.5, emit=(0.6, 0.7, 1.0), emit_str=1), seg=6) for _ in range(40)]
    cube((0, 0.9, 2.62), (4, 4, 0.04), mat("ceil", (0.55, 0.45, 0.4), 0.9))
    c = _cam((0.55, -0.6, 0.6), (0.2, 0.9, 2.4), lens=26, fstop=4)
    def upd(t):
        me["head"].rotation_euler[0] = -0.5
        for i, d in enumerate(dust): d.location.z = 2.6 - ((t * 0.5 + i * 0.07) % 1.0) * 2.4 * (t > 0.6 + (i % 4) * 0.7)
        c.location.z = 0.6 + 0.02 * math.sin(t * 20) * (int(t * 1.3) % 2)
    return upd


def n10(rng):           # then a crash, right outside my window: a mass of snow falls past the glass
    h = room(rng, candles=False); scare((0, 2.6, 1.45), key=(0.6, 1.0, 2.2))
    lumps = [sphere((rng.uniform(-0.3, 0.3), 3.0 + rng.uniform(0, 0.3), 2.6), rng.uniform(0.1, 0.22), mat("slump", (0.95, 0.96, 1.0), 0.7)) for _ in range(9)]
    c = _cam((0.25, 0.9, 1.1), (0, 2.6, 1.4), lens=34, fstop=3)
    def upd(t):
        for i, l in enumerate(lumps): l.location.z = 2.6 - 9.8 * max(0, t - 0.4 - i * 0.03) ** 2 / 2
        c.location.x = 0.25 + 0.03 * math.sin(t * 40) * (0.4 < t < 0.9)
    return upd


def n11(rng):           # REVEAL: it was snow, sliding off the roof (outside, calm, a pile on the bush)
    house_front(rng, snow_on_roof=False); bright()
    for _ in range(10): sphere((1.2 + rng.uniform(-0.5, 0.5), -0.5, 0.35 + rng.uniform(0, 0.25)), rng.uniform(0.15, 0.3), mat("pile", (0.95, 0.96, 1.0), 0.7))
    c = _cam((2.6, -3.2, 1.1), (0.9, -0.3, 0.8), lens=34, fstop=4)
    def upd(t): c.location.x = 2.6 - 0.05 * t
    return upd


def n12(rng):           # at ten, every light on our street went out: the street, then darkness
    street(rng); c = _cam((0.0, -6.0, 1.4), (0, 8, 1.0), lens=30, fstop=5)
    lamps = [o for o in bpy.data.objects if o.type == "LIGHT" and o.data.type == "POINT"]
    mats = [bpy.data.materials.get("lampglow"), bpy.data.materials.get("hwin")]
    base = {o.name: o.data.energy for o in lamps}
    def upd(t):
        k = 0.0 if t > 1.6 else 1.0
        for o in lamps: o.data.energy = base[o.name] * k
        for m in mats:
            if m: bsdf(m).inputs["Emission Strength"].default_value = (18 if m.name == "lampglow" else 4) * k
        world_color((0.12, 0.15, 0.25) if k else (0.01, 0.012, 0.03)); c.location.y = -6.0 + 0.1 * t
    return upd


def n13(rng):           # a dark figure came up the path: backlit silhouette walking towards us
    house_front(rng, lights_on=False); scare((0, -1.5, 1.0), key=(0, 3, 2.5))
    f = figure((0, -3.5, 0), 1.25)
    light("POINT", (0.4, -6.5, 1.8), 220, col=(1.0, 0.75, 0.45), size=0.3)            # a street lamp behind him: a black shape against warm light
    sphere((0.4, -6.5, 1.9), 0.1, mat("slamp", (1, 0.85, 0.6), 0.2, emit=(1, 0.78, 0.45), emit_str=25)); cyl((0.4, -6.5, 0.95), 0.03, 1.9, mat("spole", (0.05, 0.05, 0.05), 0.5))
    world_color((0.02, 0.03, 0.07))
    c = _cam((0.25, -0.6, 0.95), (0, -3.5, 0.8), lens=40, fstop=2.8)
    def upd(t): f.location.y = -3.5 + 0.45 * t; f.rotation_euler[1] = 0.04 * math.sin(t * 9)
    return upd


def n14(rng):           # REVEAL: it was my dad, holding the plug: "too bright"
    h = house_front(rng, lights_on=False); bright()
    dad = peg((0.3, -1.0, 0), DAD, "neighbour1", rot=0.2)
    plug = cube((0.12, -1.12, 0.45), (0.05, 0.03, 0.06), mat("plug", (0.9, 0.9, 0.9), 0.4))
    cyl((0.05, -0.6, 0.5), 0.006, 1.0, mat("cable", (0.1, 0.4, 0.1), 0.6), rot=(1.2, 0, 0))
    c = _cam((0.6, -2.3, 0.95), (0.25, -1.0, 0.75), lens=40, fstop=3)
    def upd(t): breathe(dad, t); dad["L"].rotation_euler[0] = -0.7; dad["head"].rotation_euler[2] = 0.2 * math.sin(t * 1.5)
    return upd


def n15(rng):           # at midnight, the phone rang. no caller ID.: phone glowing on a dark table, buzzing
    h = room(rng, candles=False, card=False); scare((0.2, 0.6, 0.55), key=(0.8, 0.0, 1.6))
    ph = phone((0.2, 0.6, TABLE_Z + 0.036)); g = group("phone", ph, (0.2, 0.6, TABLE_Z + 0.036))
    light("POINT", (0.2, 0.6, TABLE_Z + 0.12), 4, col=(0.6, 0.8, 1.0), size=0.05)
    c = _cam((0.45, 0.25, 0.78), (0.2, 0.6, TABLE_Z + 0.04), lens=44, fstop=2.0)
    def upd(t): g.location.x = 0.2 + 0.006 * math.sin(t * 90) * (int(t * 2) % 2 == 0); c.location.y = 0.25 + 0.03 * t
    return upd


def n16(rng):           # I picked up. breathing. then a voice.: the narrator in the dark, phone to ear
    h = room(rng, candles=False); scare((0.4, 0.9, 0.8), key=(1.1, 0.4, 1.2), cold=(0.5, 0.65, 1.0))
    me = peg((0.4, 0.9, 0), ME, "sam", rot=-0.5); ph = group("phone", phone((0, 0, 0)), (0, 0, 0))
    c = _cam((1.2, 0.1, 0.9), (0.4, 0.9, 0.75), lens=40, fstop=2.2)
    def upd(t):
        breathe(me, t, 0.3); me["R"].rotation_euler[0] = -2.3
        ph.location = Vector((0.27, 0.85, 0.8)); ph.rotation_euler = (1.4, 0, -0.5); c.location.x = 1.2 - 0.05 * t
    return upd


def n17(rng):           # "did you take my good scissors?": extreme close on the ear and the phone, red tint
    h = room(rng, candles=False); scare((0.4, 0.9, 0.8), key=(1.0, 0.6, 1.1), cold=(1.0, 0.25, 0.2))
    me = peg((0.4, 0.9, 0), ME, "sam", rot=-0.5); ph = group("phone", phone((0, 0, 0)), (0, 0, 0))
    c = _cam((1.1, 0.5, 0.88), (0.33, 0.87, 0.8), lens=70, fstop=1.8)
    def upd(t):
        me["R"].rotation_euler[0] = -2.3; ph.location = Vector((0.27, 0.85, 0.8)); ph.rotation_euler = (1.4, 0, -0.5)
        c.location.x = 1.1 - 0.04 * t
    return upd


def n18(rng):           # REVEAL: it was Grandma, in her bright kitchen, on the phone, looking in a drawer
    kitchen(rng); bright()
    g = peg((-0.3, 0.3, 0), GRAN, "rose", rot=0.3); ph = group("phone", phone((0, 0, 0)), (0, 0, 0))
    c = _cam((0.4, -1.0, 0.95), (-0.25, 0.3, 0.8), lens=38, fstop=3)
    def upd(t):
        breathe(g, t); g["R"].rotation_euler[0] = -2.3; ph.location = Vector((-0.42, 0.25, 0.8)); ph.rotation_euler = (1.4, 0, 0.3)
        g["head"].rotation_euler[2] = 0.3 * math.sin(t * 3)
    return upd


def n19(rng):           # so yeah. another normal night in Dustlight.: the house, lights back on, snow, calm
    h = house_front(rng); bright()
    snow = Snow((0, -1.5, 0.2), size=(5, 4, 3), n=200, rng=rng)
    c = _cam((0.4, -3.8, 1.0), (0, 0.3, 1.2), lens=32, fstop=4)
    def upd(t): snow.update(t); c.location.y = -3.8 - 0.15 * t
    return upd


SHOTS = {n: (globals()[n], _D[n]) for n in _D}
