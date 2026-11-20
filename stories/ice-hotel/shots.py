"""How a Frozen River Becomes a Hotel: animated shots.
Render: PCT=50 ES=12 $VENV/bin/python pipeline/anim.py stories/ice-hotel OUT all
Look: clean bright 3D. Blue-white ice, warm amber inside light, deep blue night sky.
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
from world import *          # noqa

NIGHT = (0.02, 0.035, 0.09); DAY = (0.55, 0.7, 0.9); MARCH = (0.75, 0.72, 0.8); SUMMER = (0.5, 0.75, 0.95)
HIVIS = (0.95, 0.45, 0.08); PARKA = (0.15, 0.35, 0.75); AMBER = (1.0, 0.62, 0.28)


def ice_m(name="ice", glow=0.35):
    return mat(name, (0.72, 0.86, 1.0), 0.06, coat=1.0, emit=(0.55, 0.78, 1.0), emit_str=glow, alpha=0.9)


def snow_m(name="snowg"):
    return mat(name, (0.9, 0.93, 0.98), 0.85, noise=0.08)


def river(frozen=True, cut=False, water_z=-0.35):
    """Frozen river: a thick ice slab (top at z=0) over dark water, with snowy banks either side.
    cut=True shows the slab's front edge so its thickness reads."""
    cube((0, 0, -0.6), (40, 40, 0.1), mat("riverbed", (0.03, 0.06, 0.1), 0.4))
    water = cube((0, 0, water_z), (12, 40, 0.02), mat("water", (0.05, 0.14, 0.22), 0.05, coat=1.0))
    slab = cube((0, 0, -0.17), (12, 40, 0.34), ice_m("slab", 0.15)) if frozen else None
    top = cube((0, 0, 0.002), (12, 40, 0.004), mat("frost", (0.86, 0.92, 1.0), 0.5, noise=0.1)) if frozen else None
    for sx in (-1, 1): cube((sx * 10.5, 0, 0.15), (9, 40, 0.6), snow_m("bank"))
    return {"water": water, "slab": slab, "top": top}


def hotel(loc=(0, 0, 0), lit=1.0):
    """Ice hotel: five vaulted halls side by side, an entrance arch, warm light inside. Returns the root to melt (scale z)."""
    root = empty("hotel", loc); im = ice_m("hotelice", 0.25); parts = []
    for k in range(5):
        x = (k - 2) * 1.05
        parts.append(cyl((x, 0, 0), 0.5, 3.0, im, rot=(math.pi / 2, 0, 0), verts=40))
        parts.append(cyl((x, -1.52, 0), 0.42, 0.06, mat("glowend", AMBER, 0.4, emit=AMBER, emit_str=2.5 * lit), rot=(math.pi / 2, 0, 0), verts=40))
    parts.append(cyl((0, -1.9, 0), 0.38, 0.8, im, rot=(math.pi / 2, 0, 0), verts=40))           # entrance tunnel
    parts.append(cyl((0, -2.31, 0), 0.26, 0.02, mat("door", AMBER, 0.4, emit=AMBER, emit_str=6 * lit), rot=(math.pi / 2, 0, 0), verts=32))
    for o in parts: o.parent = root; o.location = Vector(o.location)
    light("POINT", (loc[0], loc[1] - 1.0, 0.25), 120 * lit, col=AMBER, size=0.6)
    return root


def worker(loc, rot=0.0, col=HIVIS, kind="neighbour1", h=0.5):
    return peg(loc, col, kind, rot=rot, h=h)


def saw(loc, rot=0.0):
    m = mat("steel", (0.75, 0.77, 0.8), 0.25, metal=1.0)
    root = empty("saw", loc)
    b = cube((0, 0, 0), (0.7, 0.01, 0.12), m); hnd = cube((0.38, 0, 0.08), (0.08, 0.03, 0.12), mat("handle", (0.8, 0.15, 0.1), 0.5))
    for o in (b, hnd): o.parent = root
    root.rotation_euler[2] = rot
    return root


def night_sky(stars=60, rng=None):
    world_color(NIGHT); rng = rng or random.Random(4); sm = mat("star", (1, 1, 1), 0.5, emit=(1, 1, 1), emit_str=6)
    for _ in range(stars):
        a = rng.uniform(-1.3, 1.3); e = rng.uniform(0.15, 0.9)
        sphere((25 * math.sin(a), 25 * math.cos(a), 25 * math.sin(e)), rng.uniform(0.02, 0.05), sm, seg=6)
    light("SUN", (0, 0, 10), 0.35, col=(0.6, 0.7, 1.0), rot=(0.9, 0.1, 0.4))


def lerp3(a, b, k): return tuple(a[i] + (b[i] - a[i]) * k for i in range(3))


# ---------------------------------------------------------------- shots
def s1(rng):                       # night, the glowing hotel on the frozen river, snow; slow push-in
    river(); hotel(); night_sky(rng=rng); snow = Snow((0, -2, 0), size=(8, 8, 4), rng=rng)
    cam = camera((3.4, -6.5, 1.3), (0, 0, 0.3), lens=32)
    def upd(t): cam.location = Vector((3.4 - 0.3 * t, -6.5 + 0.5 * t, 1.3)); look_at(cam, Vector((0, 0, 0.3))); snow.update(t)
    return upd


def s2(rng):                       # the camera sinks to the ice edge: the hotel stands on the river
    river(cut=True); hotel((0, 2.0, 0)); night_sky(rng=rng); snow = Snow((0, -2, 0), size=(8, 8, 4), rng=rng)
    cut = cube((0, -1.0, -0.17), (12, 0.02, 0.34), ice_m("edge", 0.9))
    cube((0, -1.5, -0.17), (12, 1.0, 0.36), mat("hole", NIGHT, 0.2))           # open water in front of the edge
    cam = camera((0, -4.0, 0.9), (0, 0, 0.0), lens=30)
    def upd(t):
        k = smooth(t / 2.2); cam.location = Vector((0.0, -4.0 + 0.6 * k, 0.9 - 0.85 * k)); look_at(cam, Vector((0, 0.5, -0.05 + 0.2 * k))); snow.update(t)
    return upd


def s3(rng):                       # every spring it melts: same wide shot, daylight, it slumps into water
    r = river(); h = hotel(lit=0.0); world_color(DAY)
    light("SUN", (0, 0, 10), 3.0, col=(1.0, 0.95, 0.85), rot=(0.8, 0.2, 0.5))
    cam = camera((3.0, -6.0, 1.3), (0, 0, 0.3), lens=32)
    def upd(t):
        k = smooth((t - 0.5) / 1.8); h.scale = (1.0, 1.0, max(0.02, 1.0 - 0.97 * k)); h.location.z = -0.1 * k
        r["top"].scale = (1, 1, max(0.01, 1 - k)); r["slab"].location.z = -0.17 - 0.4 * k
    return upd


def s4(rng):                       # March: white river, low sun, workers saw a grid into the ice
    river(); world_color(MARCH); light("SUN", (0, 0, 10), 2.4, col=(1.0, 0.82, 0.65), rot=(1.25, 0.0, -0.9))
    gm = mat("grid", (0.4, 0.55, 0.75), 0.3)
    for k in range(-3, 4):
        cube((k * 0.45, 0, 0.004), (0.012, 3.2, 0.004), gm); cube((0, k * 0.45, 0.004), (3.2, 0.012, 0.004), gm)
    w1 = worker((-0.3, -0.25, 0), rot=0.3); w2 = worker((0.6, 0.4, 0), rot=-2.2, col=PARKA, kind="sam")
    s = saw((-0.1, -0.05, 0.06), rot=0.3)
    cam = camera((1.6, -2.6, 1.6), (0, 0, 0), lens=30)
    def upd(t):
        s.location.x = -0.1 + 0.12 * math.sin(t * 9); w1["R"].rotation_euler[0] = -1.0 + 0.3 * math.sin(t * 9)
        breathe(w1, t); breathe(w2, t); cam.location.x = 1.6 - 0.1 * t
    return upd


def s5(rng):                       # a block lifts out: bigger than a fridge (a fridge beside it for scale)
    river(); world_color(MARCH); light("SUN", (0, 0, 10), 2.4, col=(1.0, 0.82, 0.65), rot=(1.25, 0.0, -0.9))
    cube((0, 0, -0.17), (0.9, 0.9, 0.36), mat("holew", (0.05, 0.14, 0.22), 0.05, coat=1.0))
    blk = cube((0, 0, -0.17), (0.86, 0.86, 0.62), ice_m("block", 0.5), bevel=0.02)
    chain = cyl((0, 0, 1.6), 0.01, 2.6, mat("chain", (0.2, 0.2, 0.22), 0.4, metal=1.0))
    fr = cube((1.0, 0.2, 0.32), (0.32, 0.3, 0.64), mat("fridge", (0.96, 0.96, 0.97), 0.3), bevel=0.03)
    cube((0.83, 0.2, 0.42), (0.01, 0.03, 0.18), mat("fhandle", (0.5, 0.5, 0.55), 0.3, metal=1.0))
    w = worker((-0.9, -0.3, 0), rot=0.8)
    cam = camera((0.6, -3.0, 0.7), (0.3, 0, 0.45), lens=34)
    def upd(t):
        k = smooth(t / 2.2); blk.location.z = -0.17 + 0.62 * k + 0.01 * math.sin(t * 5); chain.location.z = 1.6 + 0.62 * k; breathe(w, t)
    return upd


def s6(rng):                       # the blocks wait out the summer, stacked in a giant freezer
    world_color((0.05, 0.07, 0.1)); cube((0, 0, -0.05), (12, 12, 0.1), mat("wfloor", (0.35, 0.37, 0.4), 0.6))
    wm = mat("wwall", (0.55, 0.6, 0.66), 0.7)
    cube((0, 3.0, 2.0), (12, 0.1, 4), wm); cube((-3.5, 0, 2.0), (0.1, 12, 4), wm); cube((3.5, 0, 2.0), (0.1, 12, 4), wm)
    bm = ice_m("stack", 0.4)
    for ix in range(-3, 4):
        for iy in range(0, 4):
            for iz in range(3 - abs(ix) // 2):
                cube((ix * 0.92, iy * 0.92, 0.32 + iz * 0.64), (0.86, 0.86, 0.62), bm, bevel=0.02)
    for x in (-2, 0, 2): light("AREA", (x, 1.0, 3.8), 120, col=(0.7, 0.85, 1.0), size=1.2, rot=(0, 0, 0))
    mist = Steam((0, -0.8, 0.2), n=16, rng=rng)
    cam = camera((0.5, -4.5, 1.2), (0, 1.0, 0.9), lens=28)
    def upd(t): cam.location.x = 0.5 - 0.25 * t; look_at(cam, Vector((0, 1.0, 0.9))); mist.update(t, 0.8)
    return upd


def s7(rng):                       # outside it's summer: green trees, the freezer door breathes cold
    world_color(SUMMER); cube((0, 0, -0.05), (30, 30, 0.1), mat("grass", (0.3, 0.55, 0.22), 0.9, noise=0.3))
    light("SUN", (0, 0, 10), 3.0, col=(1.0, 0.95, 0.85), rot=(0.7, 0.2, 0.6))
    cube((0, 2.0, 1.4), (5, 3, 2.8), mat("shed", (0.75, 0.78, 0.82), 0.5, metal=0.3))
    cube((0, 0.49, 0.8), (1.2, 0.02, 1.6), mat("dooropen", (0.6, 0.8, 1.0), 0.3, emit=(0.6, 0.8, 1.0), emit_str=2.5))
    for tx, ty in ((-3.6, 1.0), (3.4, 1.4), (-2.6, -1.8), (4.2, -1.0)): tree((tx, ty, 0), "dusk", rng)
    mist = Steam((0, 0.3, 0.1), n=18, rng=rng)
    cam = camera((1.8, -5.0, 1.1), (0, 1.0, 0.9), lens=30)
    def upd(t): mist.update(t, 1.4); cam.location.y = -5.0 + 0.3 * t
    return upd


def s8(rng):                       # November: the riverbank turns white, snow begins
    g = cube((0, 0, -0.05), (30, 30, 0.1), mat("bankg", (0.3, 0.35, 0.2), 0.9, noise=0.2))
    for tx, ty in ((-1.6, 1.0), (1.2, 1.8), (2.6, 0.2), (-2.8, 2.6), (0.0, 3.2)): tree((tx, ty, 0), "snow", rng)
    sun = light("SUN", (0, 0, 10), 1.2, col=(0.8, 0.85, 1.0), rot=(1.0, 0.1, 0.4))
    snow = Snow((0, 0.5, 0), size=(8, 8, 4), n=420, rng=rng)
    cam = camera((0.4, -4.2, 1.2), (0, 1.0, 1.0), lens=30)
    def upd(t):
        k = smooth(t / 2.6); bsdf(g.data.materials[0]).inputs["Base Color"].default_value = (*lerp3((0.3, 0.35, 0.2), (0.88, 0.9, 0.96), k), 1)
        world_color(lerp3((0.35, 0.4, 0.5), (0.12, 0.15, 0.28), k)); snow.update(t)
    return upd


def s9(rng):                       # and so do the builders: a line of workers walks in across the snow
    river(); world_color((0.12, 0.15, 0.28)); light("SUN", (0, 0, 10), 1.2, col=(0.8, 0.85, 1.0), rot=(1.0, 0.1, 0.4))
    snow = Snow((0, 0, 0), size=(8, 8, 4), rng=rng)
    ws = [worker((-1.6 + 0.5 * k, -1.2 - 0.35 * k, 0), rot=math.pi, col=HIVIS if k % 2 else PARKA, kind="sam" if k % 2 else "neighbour1") for k in range(5)]
    cam = camera((2.4, 2.4, 0.6), (-0.6, -1.4, 0.3), lens=34)
    def upd(t):
        for w in ws: walk(w, t, speed=1.2, direction=(0.35, 1))
        snow.update(t)
    return upd


def s10(rng):                      # snow and ice are sprayed over steel moulds, layer by layer
    river(); world_color((0.12, 0.15, 0.28)); light("SUN", (0, 0, 10), 1.4, col=(0.85, 0.9, 1.0), rot=(1.0, 0.1, 0.4))
    steel = mat("mould", (0.7, 0.72, 0.76), 0.3, metal=1.0)
    for k in range(3): cyl(((k - 1) * 1.1, 0, 0), 0.5, 2.4, steel, rot=(math.pi / 2, 0, 0), verts=40)
    layer = cyl((-1.1, 0, 0), 0.5, 2.4, snow_m("sprayed"), rot=(math.pi / 2, 0, 0), verts=40)
    w = worker((-1.1, -1.7, 0), rot=0.2)
    nozzle = cyl((-1.0, -1.45, 0.55), 0.03, 0.4, mat("hose", (0.15, 0.15, 0.15), 0.5), rot=(-0.9, 0, 0))
    spray = [sphere((0, 0, 0), 0.02, snow_m("spray"), seg=6) for _ in range(40)]
    cam = camera((2.6, -3.2, 1.3), (-0.4, 0, 0.3), lens=32)
    def upd(t):
        k = smooth(t / 3.2); r = 0.5 + 0.06 * k; layer.scale = (r / 0.5, r / 0.5, 1.0 * (0.3 + 0.7 * k)); breathe(w, t)
        for i, p in enumerate(spray):
            u = ((t * 2.5 + i / 40) % 1.0)
            p.location = Vector((-1.0 + 0.3 * math.sin(i * 1.7), -1.3 + 1.2 * u, 0.6 + 0.2 * u - 0.3 * u * u))
    return upd


def s11(rng):                      # then artists carve every room by hand
    world_color((0.03, 0.05, 0.1)); cube((0, 0, -0.05), (10, 10, 0.1), snow_m("floor"))
    cyl((0, 0.6, 0), 1.6, 4, ice_m("vault", 0.2), rot=(0, math.pi / 2, 0), verts=48)
    sc = cube((0, 0.2, 0.45), (0.5, 0.5, 0.9), ice_m("sculpt", 0.6), bevel=0.06)
    head = sphere((0, 0.2, 1.02), 0.22, ice_m("sculpt", 0.6))
    a = worker((-0.55, -0.1, 0), rot=-1.2, col=PARKA, kind="sam", h=0.9)
    chips = [sphere((0, 0, 0), 0.012, ice_m("chip", 1.0), seg=6) for _ in range(24)]
    light("POINT", (0.6, -0.8, 1.4), 80, col=(0.6, 0.8, 1.0), size=0.4); light("POINT", (-0.8, 0.9, 0.6), 40, col=AMBER, size=0.4)
    cam = camera((0.9, -1.9, 0.9), (-0.1, 0.1, 0.7), lens=36)
    def upd(t):
        a["R"].rotation_euler[0] = -1.4 + 0.35 * math.sin(t * 12); breathe(a, t)
        for i, c in enumerate(chips):
            u = ((t * 1.6 + i / 24) % 1.0)
            c.location = Vector((-0.25 + 0.4 * u * math.cos(i), 0.0 - 0.3 * u * math.sin(i * 2), 0.8 + 0.4 * u - 1.2 * u * u))
        head.rotation_euler[2] = 0.05 * t
    return upd


def room_set():
    world_color((0.02, 0.03, 0.06)); cube((0, 0, -0.05), (10, 10, 0.1), snow_m("rfloor"))
    cyl((0, 0.5, 0), 1.8, 4, ice_m("rvault", 0.18), rot=(0, math.pi / 2, 0), verts=48)
    light("POINT", (0.0, -0.4, 1.4), 70, col=AMBER, size=0.5); light("POINT", (0.9, 1.2, 0.5), 50, col=(0.5, 0.75, 1.0), size=0.5)


def s12(rng):                      # the bed is ice (with reindeer-skin blanket)
    room_set()
    cube((0, 0.5, 0.25), (1.2, 1.9, 0.5), ice_m("bed", 0.5), bevel=0.05)
    cube((0, 0.45, 0.53), (1.0, 1.6, 0.06), mat("fur", (0.55, 0.4, 0.28), 0.95, sheen=1.0, noise=0.5), bevel=0.02)
    cube((0, 1.3, 0.62), (0.5, 0.2, 0.12), mat("pillow", (0.92, 0.9, 0.86), 0.9, sheen=0.6), bevel=0.04)
    cam = camera((1.5, -1.3, 1.1), (0, 0.5, 0.4), lens=34)
    def upd(t): cam.location.x = 1.5 - 0.15 * t; look_at(cam, Vector((0, 0.5, 0.4)))
    return upd


def s13(rng):                      # the glasses are ice
    room_set()
    cube((0, 0.3, 0.45), (1.6, 0.5, 0.9), ice_m("bar", 0.4), bevel=0.04)
    gm = ice_m("glass", 1.0); gl = []
    for k in range(4):
        gl.append(cube((-0.45 + 0.3 * k, 0.25, 0.98), (0.12, 0.12, 0.16), gm, bevel=0.01))
    drink = cube((0.15, 0.25, 0.96), (0.09, 0.09, 0.09), mat("drink", (0.9, 0.3, 0.4), 0.2, emit=(0.9, 0.3, 0.4), emit_str=1.0))
    cam = camera((0.5, -0.9, 1.15), (0, 0.25, 0.98), lens=45, dof=1.2, fstop=2.0)
    def upd(t): cam.location.x = 0.5 - 0.2 * t; look_at(cam, Vector((0, 0.25, 0.98)))
    return upd


def s14(rng):                      # inside, it stays below freezing: a thermometer at -5 °C, breath in the air
    room_set()
    cyl((0, 1.6, 0.9), 0.05, 0.9, mat("thermo", (0.95, 0.95, 0.97), 0.2), verts=24)
    bar = cyl((0, 1.55, 0.7), 0.025, 0.5, mat("red", (0.9, 0.08, 0.06), 0.3, emit=(0.9, 0.08, 0.06), emit_str=1.5), verts=16)
    sphere((0, 1.55, 0.45), 0.06, mat("red", (0.9, 0.08, 0.06), 0.3, emit=(0.9, 0.08, 0.06), emit_str=1.5))
    text("-5 °C", (0.35, 1.55, 0.9), 0.16, mat("label", (1, 1, 1), 0.5, emit=(1, 1, 1), emit_str=2.0), rot=(math.pi / 2, 0, 0))
    breath = Steam((-0.15, 0.6, 0.85), n=14, rng=rng)
    cam = camera((0.2, -0.4, 0.95), (0.05, 1.55, 0.85), lens=38)
    def upd(t):
        k = smooth(t / 1.5); bar.scale = (1, 1, 1.0 - 0.6 * k); bar.location.z = 0.7 - 0.15 * k; breath.update(t, 1.2)
    return upd


def s15(rng):                      # ...all night: wide of the lit hotel under the stars
    river(); hotel(); night_sky(stars=120, rng=rng); snow = Snow((0, -2, 0), size=(8, 8, 4), n=200, rng=rng)
    cam = camera((-4.5, -5.0, 0.9), (0, 0, 0.35), lens=30)
    def upd(t): cam.location.x = -4.5 + 0.35 * t; look_at(cam, Vector((0, 0, 0.35))); snow.update(t)
    return upd


def s16(rng):                      # then spring comes: the sun rises over the hotel
    river(); h = hotel(lit=0.3)
    sun = light("SUN", (0, 0, 10), 0.5, col=(1.0, 0.7, 0.45), rot=(1.4, 0.0, 0.3))
    cam = camera((3.2, -5.6, 1.0), (0, 0, 0.4), lens=32)
    def upd(t):
        k = smooth(t / 2.2); world_color(lerp3(NIGHT, DAY, k)); sun.data.energy = 0.5 + 2.8 * k; sun.rotation_euler[0] = 1.4 - 0.5 * k
    return upd


def s17(rng):                      # the walls drip: close-up of a vault edge, drops falling
    world_color(DAY); light("SUN", (0, 0, 10), 3.0, col=(1.0, 0.95, 0.85), rot=(0.8, 0.2, 0.5))
    cube((0, 0, -0.05), (10, 10, 0.1), mat("slush", (0.6, 0.7, 0.8), 0.2, coat=1.0))
    cyl((0, 0.5, 0), 0.9, 3, ice_m("wet", 0.2), rot=(math.pi / 2, 0, 0), verts=48)
    drops = [sphere((0, 0, 0), 0.025, ice_m("drop", 0.8), scale=(1, 1, 1.4), seg=10) for _ in range(9)]
    cam = camera((0.3, -1.4, 0.35), (0, -1.0, 0.55), lens=42, dof=0.55, fstop=2.0)
    def upd(t):
        for i, d in enumerate(drops):
            u = ((t * 0.9 + i / 9) % 1.0); x = -0.6 + 0.15 * i
            zt = math.sqrt(max(0.0, 0.81 - x * x)); d.location = Vector((x, -1.0, max(0.02, zt - 1.4 * u * u)))
    return upd


def s18(rng):                      # the arches sag
    r = river(); h = hotel(lit=0.0); world_color(DAY); light("SUN", (0, 0, 10), 3.0, col=(1.0, 0.95, 0.85), rot=(0.8, 0.2, 0.5))
    cam = camera((1.6, -3.6, 0.6), (0, 0, 0.3), lens=34)
    def upd(t):
        k = smooth(t / 2.0); h.scale = (1.0 + 0.1 * k, 1.0, 1.0 - 0.55 * k); h.location.z = -0.05 * k
    return upd


def s19(rng):                      # the whole hotel flows back into the river
    r = river(); h = hotel(lit=0.0); world_color(DAY); light("SUN", (0, 0, 10), 3.0, col=(1.0, 0.95, 0.85), rot=(0.8, 0.2, 0.5))
    h.scale = (1.1, 1.0, 0.45)
    cam = camera((3.0, -5.0, 1.6), (0, 0, 0.0), lens=30)
    def upd(t):
        k = smooth(t / 1.3); h.scale = (1.1, 1.0, max(0.01, 0.45 * (1 - k))); h.location.z = -0.3 * k
        r["top"].scale = (1, 1, max(0.01, 1 - k)); r["slab"].location.z = -0.17 - 0.3 * k; r["water"].location.z = -0.35 + 0.33 * k
    return upd


def s20(rng):                      # next March: the saw touches fresh ice again
    river(); world_color(MARCH); light("SUN", (0, 0, 10), 2.4, col=(1.0, 0.82, 0.65), rot=(1.25, 0.0, -0.9))
    s = saw((0, 0, 0.1), rot=0.0); w = worker((0.2, 0.35, 0), rot=math.pi, h=0.6)
    cam = camera((0.0, -1.1, 0.35), (0, 0, 0.05), lens=40, dof=1.1, fstop=2.2)
    def upd(t):
        k = smooth(t / 1.0); s.location.z = 0.1 - 0.06 * k; s.location.x = 0.05 * math.sin(t * 9) * (t > 1.0) * (t < 1.6); breathe(w, t)
    return upd


DUR = json.load(open(os.path.join(HERE, "durations.json")))
SHOTS = {k: (globals()[k], DUR[k]) for k in DUR}
