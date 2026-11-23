"""Dustlight peg-doll world: characters, props, animated effects and sets (kitchen, snowy street, care home, care room).
Built for Eevee animation; every animated thing exposes simple handles that per-frame update functions move."""
import math, random
from scene import *          # noqa

SKIN = (0.97, 0.80, 0.62); WHITE = (0.95, 0.94, 0.92)


# ---------------------------------------------------------------- peg dolls
def peg(loc, body_col, kind="walter", rot=0.0, scarf=None, h=1.0, hair=None):
    """Wooden peg doll (about 1 unit tall). kind: walter | rose | nurse | neighbour1 | neighbour2 | plain | lily | sam | margaret | danny | girl.
    hair: optional hair colour (margaret, danny, girl).
    Returns handles {root, head, L, R, cheek, base} for animation."""
    wood = mat("skin", SKIN, 0.55, noise=0.12); bm = mat("body_" + kind, body_col, 0.7, noise=0.15)
    blk = mat("eyeblk", (0.01, 0.01, 0.01), 0.2); wht = mat("eyewht", (1, 1, 1), 0.2)
    cheek = mat("cheek_" + kind, (0.92, 0.45, 0.45), 0.6)
    P = [cyl((0, 0, 0.30), 0.17, 0.55, bm), sphere((0, 0, 0.04), 0.17, bm, scale=(1, 1, 0.45)),
         sphere((0, 0, 0.575), 0.17, bm, scale=(1, 1, 0.42)), cyl((0, 0, 0.63), 0.06, 0.06, wood)]
    head = empty("head_" + kind, (0, 0, 0.66))
    H = [sphere((0, 0, 0.79), 0.15, wood), sphere((0, -0.15, 0.785), 0.016, wood)]
    for sx in (-1, 1):
        H += [sphere((sx * 0.05, -0.135, 0.805), 0.018, blk), sphere((sx * 0.05 + 0.006, -0.15, 0.812), 0.006, wht),
              sphere((sx * 0.088, -0.118, 0.765), 0.026, cheek, scale=(1, 0.4, 0.8))]
    m0 = len(H)
    for k in range(7):                                                   # painted dotted smile
        x = -0.036 + k * 0.012; H.append(sphere((x, -0.146 + abs(x) * 0.3, 0.748 + 12 * x * x), 0.0065, blk, seg=8))
    H.append(sphere((0, -0.146, 0.75), 0.02, blk, scale=(0.9, 0.3, 0.001)))   # hidden open mouth for characters.say()
    TALK = {"mouth": [(o, tuple(o.scale)) for o in H[m0:-1]], "talk": H[-1]}
    hair_w = mat("whitehair", WHITE, 0.9, sheen=0.5)
    if kind == "walter":
        frame = mat("glasses", (0.15, 0.12, 0.1), 0.3, metal=0.7)
        for sx in (-1, 1):
            H.append(torus((sx * 0.05, -0.148, 0.805), 0.03, 0.004, frame, rot=(math.pi / 2, 0, 0)))
            H.append(sphere((sx * 0.135, 0.0, 0.80), 0.055, hair_w, scale=(0.6, 1.1, 0.9)))
            H.append(sphere((sx * 0.05, -0.135, 0.85), 0.018, hair_w, scale=(1.8, 0.6, 0.5)))
        H.append(cyl((0, -0.15, 0.81), 0.003, 0.04, frame, rot=(0, math.pi / 2, 0)))
    elif kind in ("rose", "neighbour2"):
        hair = mat("hair_" + kind, WHITE if kind == "rose" else (0.45, 0.3, 0.2), 0.9, sheen=0.5)
        H += [sphere((0, 0.035, 0.835), 0.15, hair, scale=(1.06, 0.95, 0.78)), sphere((0, 0.12, 0.93), 0.06, hair)]
    elif kind == "nurse":
        H += [sphere((0, 0.03, 0.84), 0.15, mat("hair_n", (0.25, 0.15, 0.08), 0.9), scale=(1.05, 0.95, 0.76)),
              cyl((0, 0.0, 0.95), 0.08, 0.05, mat("cap", (1, 1, 1), 0.6))]
    elif kind == "lily":                                                   # bald under a yellow knitted beanie
        knit = mat("beanie", (0.98, 0.78, 0.15), 0.95, sheen=0.9, noise=0.35)
        H += [sphere((0, 0.01, 0.845), 0.152, knit, scale=(1.04, 1.02, 0.72)), sphere((0, 0.0, 0.975), 0.035, knit),
              torus((0, 0.005, 0.80), 0.143, 0.018, knit)]
    elif kind == "margaret":                                               # hair in a bun; colour greys with the years
        hm = mat("hair_m_%d" % int(1000 * sum(hair or WHITE)), hair or WHITE, 0.9, sheen=0.5)
        H += [sphere((0, 0.035, 0.84), 0.152, hm, scale=(1.05, 0.98, 0.74)), sphere((0, 0.13, 0.9), 0.065, hm)]
        frame = mat("glasses_m", (0.55, 0.35, 0.2), 0.3, metal=0.6)
        for sx in (-1, 1): H.append(torus((sx * 0.05, -0.148, 0.805), 0.028, 0.0035, frame, rot=(math.pi / 2, 0, 0)))
    elif kind == "danny":                                                  # messy dark hair and a short beard
        hm = mat("hair_d", hair or (0.18, 0.12, 0.08), 0.9, sheen=0.4)
        H += [sphere((0, 0.02, 0.86), 0.155, hm, scale=(1.04, 1.02, 0.6)), sphere((0.06, -0.11, 0.9), 0.035, hm, scale=(1.4, 0.7, 0.6)),
              sphere((0, -0.075, 0.7), 0.105, hm, scale=(0.95, 0.55, 0.3))]
    elif kind == "girl":                                                   # two bunches with red ribbons
        hm = mat("hair_g2", hair or (0.45, 0.28, 0.14), 0.9, sheen=0.5); rb = mat("ribbon", (0.85, 0.15, 0.2), 0.7)
        H += [sphere((0, 0.03, 0.85), 0.153, hm, scale=(1.04, 1.0, 0.66))]
        for sx in (-1, 1): H += [sphere((sx * 0.16, 0.03, 0.82), 0.055, hm, scale=(0.8, 0.8, 1.2)), sphere((sx * 0.14, 0.03, 0.86), 0.02, rb)]
    elif kind == "sam":                                                    # short brown hair
        H += [sphere((0, 0.03, 0.85), 0.152, mat("hair_s", (0.3, 0.2, 0.12), 0.9, sheen=0.4), scale=(1.03, 1.0, 0.62))]
    elif kind == "neighbour1":
        H += [sphere((0, 0.02, 0.86), 0.152, mat("hair_g", (0.5, 0.5, 0.5), 0.9), scale=(1.03, 1, 0.6))]
    for o in H: o.parent = head; o.location = Vector(o.location) - Vector(head.location)
    arms = {}
    for side, sx in (("L", -1), ("R", 1)):
        piv = empty(f"arm{side}_{kind}", (sx * 0.19, 0, 0.56))
        for o in (sphere((sx * 0.19, 0, 0.42), 0.045, bm, scale=(1, 1, 3.3)), sphere((sx * 0.19, 0, 0.27), 0.042, wood)):
            o.parent = piv; o.location = Vector(o.location) - Vector(piv.location)
        arms[side] = piv
    if scarf:
        sm = mat("scarf_" + kind, scarf, 0.95, sheen=0.9, noise=0.3)
        P += [torus((0, 0, 0.62), 0.1, 0.04, sm), cube((0.06, -0.12, 0.5), (0.06, 0.03, 0.2), sm, rot=(0.1, 0.2, 0), bevel=0.01)]
    root = empty("root_" + kind)
    for o in P + [head, arms["L"], arms["R"]]:
        if o.parent is None: o.parent = root
    root.location = loc; root.rotation_euler[2] = rot; root.scale = (h, h, h)
    return {"root": root, "head": head, "L": arms["L"], "R": arms["R"], "cheek": cheek, "base": Vector(loc), **TALK}


def walk(d, t, speed=1.0, direction=(0, -1)):
    """Peg-doll waddle: bob, sway and swinging arms while moving along direction."""
    ph = t * 2 * math.pi * 1.6
    d["root"].location = d["base"] + Vector((direction[0], direction[1], 0)) * (t * speed * 0.35)
    d["root"].location.z = d["base"].z + 0.03 * abs(math.sin(ph))
    d["root"].rotation_euler[1] = 0.07 * math.sin(ph)
    d["L"].rotation_euler[0] = 0.35 * math.sin(ph); d["R"].rotation_euler[0] = -0.35 * math.sin(ph)


def breathe(d, t, amt=1.0):
    """Idle life so nobody is ever frozen."""
    d["root"].scale.z = d["root"].scale.x * (1 + 0.012 * amt * math.sin(t * 2.4))
    d["head"].rotation_euler[0] = 0.03 * amt * math.sin(t * 1.3)


def smooth(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)


# ---------------------------------------------------------------- props
def cup(loc, col=(0.95, 0.93, 0.88), tea=True):
    m = mat("cup", col, 0.2, coat=0.6)
    P = [cyl((loc[0], loc[1], loc[2] + 0.04), 0.038, 0.08, m), torus((loc[0] + 0.045, loc[1], loc[2] + 0.045), 0.018, 0.006, m, rot=(math.pi / 2, 0, 0)),
         cyl((loc[0], loc[1], loc[2] + 0.002), 0.05, 0.004, m)]
    tea_o = cyl((loc[0], loc[1], loc[2] + 0.075), 0.033, 0.003, mat("tea", (0.35, 0.16, 0.05), 0.1, coat=1)) if tea else None
    if tea_o: P.append(tea_o)
    return group("cup", P, loc), tea_o


def teapot(loc):
    m = mat("pot", (0.55, 0.75, 0.8), 0.25, coat=0.6)
    P = [sphere((loc[0], loc[1], loc[2] + 0.1), 0.1, m, scale=(1.1, 1, 0.85)), sphere((loc[0], loc[1], loc[2] + 0.19), 0.025, m),
         cyl((loc[0] + 0.13, loc[1], loc[2] + 0.13), 0.015, 0.1, m, rot=(0, -0.9, 0)),
         torus((loc[0] - 0.11, loc[1], loc[2] + 0.11), 0.045, 0.012, m, rot=(math.pi / 2, 0, 0))]
    return group("teapot", P, loc)


def flask(loc):
    m = mat("flask", (0.7, 0.12, 0.1), 0.3, metal=0.5)
    return group("flask", [cyl((loc[0], loc[1], loc[2] + 0.1), 0.035, 0.2, m),
                           cyl((loc[0], loc[1], loc[2] + 0.215), 0.03, 0.03, mat("flaskcap", (0.8, 0.8, 0.82), 0.3, metal=1))], loc)


class Steam:
    """Soft rising puffs; update(t, strength) each frame (strength 0 = gone)."""
    def __init__(self, base, n=10, rng=None):
        rng = rng or random.Random(1)
        m = mat("steam", (1, 1, 1), 0.5, emit=(1, 1, 1), emit_str=0.6, alpha=0.22)
        self.base = Vector(base); self.p = [(sphere(base, 0.02, m, seg=12), rng.uniform(0, 2.2), rng.uniform(-1, 1)) for _ in range(n)]
    def update(self, t, strength=1.0):
        for o, off, sw in self.p:
            u = ((t + off) % 2.2) / 2.2
            o.location = self.base + Vector((0.02 * sw * u + 0.012 * math.sin(t * 2 + off * 3), 0, 0.22 * u))
            s = (0.6 + 1.8 * u) * strength * (1 - u) * 1.6
            o.scale = (max(s, 0.001),) * 3


class Snow:
    """Falling snow in a box around center; update(t) each frame."""
    def __init__(self, center, size=(6, 5, 4), n=380, rng=None):
        rng = rng or random.Random(2); self.c = Vector(center); self.size = size
        m = mat("snowflake", (1, 1, 1), 0.5, emit=(1, 1, 1), emit_str=0.8)
        self.f = [(sphere((0, 0, 0), rng.uniform(0.006, 0.014), m, seg=6),
                   Vector((rng.uniform(-.5, .5) * size[0], rng.uniform(-.5, .5) * size[1], rng.uniform(0, 1) * size[2])),
                   rng.uniform(0.25, 0.5), rng.uniform(0, 6)) for _ in range(n)]
    def update(self, t):
        for o, p, v, ph in self.f:
            o.location = self.c + Vector((p.x + 0.08 * math.sin(t * 0.9 + ph), p.y, (p.z - v * t) % self.size[2]))


# ---------------------------------------------------------------- sets
def kitchen(rng):
    """Walter's kitchen: table for two, two chairs (Rose's with her lilac cardigan), morning window, wall clock. Returns the clock's second-hand pivot."""
    cube((0, 0, -0.05), (8, 8, 0.1), mat("kfloor", (0.45, 0.3, 0.18), 0.6, noise=0.5))
    wall = mat("kwall", (0.88, 0.8, 0.64), 0.9, noise=0.15)
    cube((-1.2, 1.6, 1.5), (2.4, 0.1, 3), wall); cube((2.0, 1.6, 1.5), (2.4, 0.1, 3), wall); cube((0.4, 1.6, 2.4), (0.8, 0.1, 1.2), wall); cube((0.4, 1.6, 0.35), (0.8, 0.1, 0.7), wall)
    cube((-2.0, 0, 1.5), (0.1, 8, 3), wall); cube((2.6, 0, 1.5), (0.1, 8, 3), wall)
    cube((0.4, 1.7, 1.25), (0.8, 0.02, 1.1), mat("morning", (0.95, 0.92, 0.85), 0.5, emit=(1.0, 0.93, 0.8), emit_str=3))
    fm = mat("wframe", (0.95, 0.95, 0.93), 0.5)
    for dx in (-0.4, 0, 0.4): cube((0.4 + dx, 1.62, 1.25), (0.04, 0.06, 1.12), fm)
    for dz in (-0.55, 0, 0.55): cube((0.4, 1.62, 1.25 + dz), (0.84, 0.06, 0.04), fm)
    light("AREA", (0.4, 1.4, 1.3), 90, col=(1.0, 0.92, 0.78), size=1.0, rot=(math.pi / 2, 0, 0))
    light("POINT", (-0.6, -0.8, 1.9), 35, col=(1.0, 0.75, 0.5), size=0.4)
    light("AREA", (0.0, -1.0, 1.3), 45, col=(1.0, 0.85, 0.7), size=1.2, target=(0, 0.8, 0.75))     # soft face light
    tm = mat("table", (0.55, 0.35, 0.2), 0.5, noise=0.5)
    cube((0, 0.55, 0.43), (1.1, 0.7, 0.04), tm, bevel=0.01)
    for sx in (-0.5, 0.5):
        for sy in (0.25, 0.85): cube((sx, sy, 0.21), (0.04, 0.04, 0.42), tm)
    cube((0, 0.55, 0.452), (0.9, 0.5, 0.004), mat("cloth", (0.85, 0.3, 0.3), 0.9, sheen=0.5, noise=0.2))
    for x in (-0.32, 0.32):
        cube((x, 1.0, 0.25), (0.34, 0.32, 0.04), tm, bevel=0.01); cube((x, 1.15, 0.5), (0.34, 0.03, 0.5), tm, bevel=0.01)
        for sx in (-0.15, 0.15):
            for sy in (0.86, 1.14): cube((x + sx, sy, 0.12), (0.03, 0.03, 0.24), tm)
    cm = mat("cardigan", (0.62, 0.5, 0.75), 0.95, sheen=0.9, noise=0.3)
    cube((0.32, 1.17, 0.62), (0.36, 0.06, 0.3), cm, bevel=0.03); cube((0.16, 1.12, 0.48), (0.07, 0.05, 0.32), cm, rot=(0, 0.25, 0), bevel=0.02)
    clk = empty("clockhand", (1.2, 1.54, 1.85))
    cyl((1.2, 1.55, 1.85), 0.16, 0.03, mat("clockrim", (0.3, 0.18, 0.1), 0.5), rot=(math.pi / 2, 0, 0))
    cyl((1.2, 1.535, 1.85), 0.14, 0.005, mat("clockface", (0.95, 0.93, 0.86), 0.7), rot=(math.pi / 2, 0, 0))
    ink = mat("clockink", (0.05, 0.04, 0.03), 0.6)
    cube((1.2, 1.53, 1.89), (0.01, 0.004, 0.08), ink); cube((1.23, 1.53, 1.85), (0.06, 0.004, 0.012), ink)
    sec = cube((1.2, 1.528, 1.90), (0.004, 0.003, 0.11), mat("sechand", (0.8, 0.1, 0.1), 0.5)); sec.parent = clk; sec.location = (0, -0.012, 0.05)
    cyl((0.75, 1.55, 0.72), 0.06, 0.09, mat("plantpot", (0.7, 0.35, 0.2), 0.7))
    for _ in range(6): sphere((0.75 + rng.uniform(-.05, .05), 1.55 + rng.uniform(-.03, .03), 0.8 + rng.uniform(0, 0.08)), 0.04, mat("leaf", (0.2, 0.5, 0.2), 0.6))
    return clk


def street(rng, houses=True):
    """Snowy evening street: road, lamp posts, little houses with lit windows."""
    cube((0, 0, -0.05), (40, 40, 0.1), mat("snowground", (0.85, 0.88, 0.95), 0.7, noise=0.2))
    cube((0, 0, 0.002), (2.0, 40, 0.004), mat("road", (0.55, 0.57, 0.62), 0.8, noise=0.3))
    lamp_m = mat("lampm", (0.08, 0.08, 0.09), 0.4, metal=0.8)
    for y in range(-6, 30, 4):
        for x in (-1.4, 1.4):
            cyl((x, y, 1.0), 0.035, 2.0, lamp_m); sphere((x, y, 2.05), 0.1, mat("lampglow", (1, 0.85, 0.6), 0.2, emit=(1, 0.78, 0.45), emit_str=18))
            light("POINT", (x, y, 1.95), 40, col=(1.0, 0.75, 0.45), size=0.15)
    if houses:
        for y in range(-6, 30, 3):
            for x in (-3.2, 3.2):
                c = rng.choice([(0.7, 0.35, 0.3), (0.4, 0.5, 0.65), (0.8, 0.75, 0.6), (0.45, 0.6, 0.45)])
                cube((x, y, 1.0), (2.0, 2.4, 2.0), mat("house", c, 0.8, noise=0.3))
                cube((x, y, 2.25), (2.2, 2.6, 0.5), mat("roofsnow", (0.95, 0.96, 1.0), 0.7))
                for wy in (-0.6, 0.6):
                    cube((x - math.copysign(1.0, x) * 1.0, y + wy, 1.2), (0.02, 0.45, 0.5), mat("hwin", (1, 0.8, 0.5), 0.5, emit=(1, 0.78, 0.45), emit_str=4))
    world_color((0.12, 0.15, 0.25))
    light("SUN", (0, 0, 5), 0.8, col=(0.7, 0.78, 1.0), rot=(0.9, 0.2, 0.5))


def care_home(rng, sign="SUNNY MEADOWS CARE HOME"):
    street(rng, houses=False)
    snow_m = mat("roofsnow", (0.95, 0.96, 1.0), 0.7)
    cube((0, 8, 1.6), (7, 2.5, 3.2), mat("carebrick", (0.78, 0.62, 0.48), 0.85, noise=0.4)); cube((0, 8, 3.4), (7.4, 2.9, 0.5), snow_m)
    wm = mat("carewin", (1, 0.82, 0.55), 0.5, emit=(1, 0.8, 0.5), emit_str=5)
    for x in (-2.6, -1.3, 1.3, 2.6):
        for z in (1.0, 2.3): cube((x, 6.73, z), (0.6, 0.02, 0.7), wm)
    cube((0, 6.72, 0.75), (0.9, 0.02, 1.5), mat("caredoor", (0.4, 0.25, 0.15), 0.6))
    cube((0, 6.68, 1.75), (2.6, 0.04, 0.32), mat("caresign", (0.95, 0.93, 0.85), 0.7))
    text(sign, (0, 6.65, 1.75), 0.15, mat("signink2", (0.25, 0.4, 0.25), 0.6))
    for x in (-1.1, 1.1): cube((x, 3.5, 0.6), (0.25, 0.25, 1.2), mat("pillar", (0.7, 0.68, 0.66), 0.8)); sphere((x, 3.5, 1.3), 0.14, snow_m)
    for k in range(-6, 7):
        if abs(k) > 3: cyl((k * 0.3, 3.5, 0.45), 0.015, 0.9, mat("lampm", (0.08, 0.08, 0.09), 0.4, metal=0.8))
    for x in (-3.0, -2.2, 2.2, 3.0):
        sphere((x, 5.0, 0.3), 0.4, mat("bush", (0.15, 0.35, 0.18), 0.8)); sphere((x, 5.0, 0.55), 0.3, snow_m, scale=(1.1, 1.1, 0.5))


def care_room(rng, sun=1.0):
    """Rose's room: armchair by a big bright window, small round table, visitor's chair, plant. Returns (sun_light, window)."""
    cube((0, 0, -0.05), (8, 8, 0.1), mat("crfloor", (0.55, 0.4, 0.28), 0.6, noise=0.4))
    cube((0, 0.0, 0.003), (1.8, 1.4, 0.006), mat("rug", (0.6, 0.25, 0.25), 0.95, sheen=0.5, noise=0.3))
    wall = mat("crwall", (0.93, 0.86, 0.68), 0.9, noise=0.12)
    cube((-1.4, 1.5, 1.5), (1.6, 0.1, 3), wall); cube((1.9, 1.5, 1.5), (1.4, 0.1, 3), wall); cube((0.35, 1.5, 2.45), (1.5, 0.1, 1.1), wall); cube((0.35, 1.5, 0.3), (1.5, 0.1, 0.6), wall)
    cube((-2.2, 0, 1.5), (0.1, 8, 3), wall)
    win = cube((0.35, 1.6, 1.25), (1.5, 0.02, 1.3), mat("daylight", (0.85, 0.92, 1.0), 0.5, emit=(0.9, 0.95, 1.0), emit_str=3 * sun))
    fm = mat("crframe", (0.97, 0.97, 0.95), 0.5)
    for dx in (-0.75, 0, 0.75): cube((0.35 + dx, 1.52, 1.25), (0.05, 0.06, 1.32), fm)
    for dz in (-0.65, 0.65): cube((0.35, 1.52, 1.25 + dz), (1.55, 0.06, 0.05), fm)
    sunl = light("AREA", (0.35, 1.3, 1.3), 140 * sun, col=(1.0, 0.95, 0.85), size=1.4, rot=(math.pi / 2, 0, 0))
    light("POINT", (-1.2, -1.2, 2.0), 25, col=(1.0, 0.78, 0.55), size=0.4)
    light("AREA", (0.0, -1.0, 1.3), 55, col=(1.0, 0.85, 0.7), size=1.4, target=(0.1, 0.8, 0.8))
    am = mat("armchair", (0.45, 0.55, 0.45), 0.9, sheen=0.6, noise=0.2)
    cube((0.55, 0.95, 0.2), (0.6, 0.55, 0.4), am, bevel=0.06); cube((0.55, 1.2, 0.55), (0.6, 0.12, 0.6), am, bevel=0.06)
    for sx in (-0.3, 0.3): cube((0.55 + sx, 0.95, 0.38), (0.1, 0.55, 0.22), am, bevel=0.04)
    tm = mat("ctable", (0.55, 0.36, 0.22), 0.5, noise=0.5)
    cyl((0.05, 0.55, 0.38), 0.22, 0.03, tm); cyl((0.05, 0.55, 0.19), 0.03, 0.38, tm)
    ch = mat("vchair", (0.5, 0.32, 0.2), 0.5, noise=0.4)
    cube((-0.5, 0.75, 0.25), (0.34, 0.32, 0.04), ch, bevel=0.01); cube((-0.66, 0.75, 0.5), (0.03, 0.34, 0.5), ch, bevel=0.01)
    for sx in (-0.14, 0.14):
        for sy in (0.61, 0.89): cube((-0.5 + sx, sy, 0.12), (0.03, 0.03, 0.24), ch)
    cyl((-1.0, 1.35, 0.22), 0.12, 0.25, mat("bigpot", (0.75, 0.45, 0.3), 0.7))
    for _ in range(9): sphere((-1.0 + rng.uniform(-.12, .12), 1.35 + rng.uniform(-.1, .1), 0.4 + rng.uniform(0, 0.35)), 0.07, mat("leaf", (0.2, 0.5, 0.2), 0.6))
    return sunl, win


# ---------------------------------------------------------------- weather and seasons
class Rain:
    """Falling rain streaks; update(t) each frame."""
    def __init__(self, center, size=(5, 4, 3), n=260, rng=None):
        rng = rng or random.Random(3); self.c = Vector(center); self.size = size
        m = mat("rain", (0.8, 0.85, 1.0), 0.1, emit=(0.8, 0.85, 1.0), emit_str=0.5, alpha=0.35)
        self.f = [(cyl((0, 0, 0), 0.0025, 0.12, m, verts=6), Vector((rng.uniform(-.5, .5) * size[0], rng.uniform(-.5, .5) * size[1], rng.uniform(0, 1) * size[2])), rng.uniform(5, 7)) for _ in range(n)]
    def update(self, t):
        for o, p, v in self.f:
            o.location = self.c + Vector((p.x, p.y, (p.z - v * t) % self.size[2]))


class Flutter:
    """Falling, tumbling flakes for autumn leaves or spring petals; update(t)."""
    def __init__(self, center, colors, size=(4, 3, 3), n=90, rng=None, flake=0.03):
        rng = rng or random.Random(4); self.c = Vector(center); self.size = size
        ms = [mat("flutter%d" % i, c, 0.7, sheen=0.4) for i, c in enumerate(colors)]
        self.f = [(sphere((0, 0, 0), flake * rng.uniform(0.6, 1.2), rng.choice(ms), scale=(1, 0.6, 0.15), seg=10),
                   Vector((rng.uniform(-.5, .5) * size[0], rng.uniform(-.5, .5) * size[1], rng.uniform(0, 1) * size[2])),
                   rng.uniform(0.25, 0.45), rng.uniform(0, 6)) for _ in range(n)]
    def update(self, t):
        for o, p, v, ph in self.f:
            o.location = self.c + Vector((p.x + 0.25 * math.sin(t * 1.3 + ph), p.y + 0.1 * math.cos(t + ph), (p.z - v * t) % self.size[2]))
            o.rotation_euler = (t * 2 + ph, t * 1.5, ph)


SEASONS = {   # ground, foliage colours, sky (world colour)
    "dusk":   ((0.16, 0.28, 0.14), [(0.2, 0.42, 0.18), (0.25, 0.48, 0.2)], (0.10, 0.09, 0.17)),
    "autumn": ((0.3, 0.3, 0.14), [(0.85, 0.42, 0.1), (0.75, 0.25, 0.08), (0.9, 0.62, 0.15)], (0.22, 0.15, 0.16)),
    "rain":   ((0.15, 0.25, 0.14), [(0.18, 0.34, 0.18)], (0.08, 0.09, 0.12)),
    "snow":   ((0.85, 0.88, 0.95), [], (0.09, 0.1, 0.17)),
    "spring": ((0.25, 0.48, 0.2), [(0.98, 0.72, 0.8), (1.0, 0.82, 0.88)], (0.42, 0.28, 0.34)),
}


def tree(loc, season, rng):
    x, y, z = loc
    cyl((x, y, z + 0.7), 0.08, 1.4, mat("bark", (0.3, 0.2, 0.12), 0.9, noise=0.5))
    cols = SEASONS[season][1]
    if not cols:                                                       # bare winter branches with snow
        for k in range(5):
            cyl((x + 0.15 * math.cos(k), y + 0.15 * math.sin(k), z + 1.5), 0.025, 0.6, mat("bark", (0.3, 0.2, 0.12), 0.9, noise=0.5), rot=(0.6 * math.sin(k * 2), 0.6 * math.cos(k * 2), 0))
        return
    for _ in range(9):
        sphere((x + rng.uniform(-.35, .35), y + rng.uniform(-.35, .35), z + 1.5 + rng.uniform(-0.1, 0.45)), rng.uniform(0.25, 0.38),
               mat("foliage", rng.choice(cols), 0.8, sheen=0.3), seg=16)


def swing_set(loc):
    """Child's swing. Returns (pivot, seat): rotate pivot.rotation_euler[0] to swing (forward = +y)."""
    x, y, z = loc
    frame = mat("swingframe", (0.75, 0.2, 0.2), 0.35, metal=0.6); chain = mat("chain", (0.6, 0.6, 0.62), 0.3, metal=1)
    for sx in (-0.7, 0.7):
        for sy in (-0.35, 0.35): cyl((x + sx, y + sy * 0.6, z + 0.9), 0.03, 1.9, frame, rot=(sy * 0.5, 0, 0))
    cyl((x, y, z + 1.8), 0.035, 1.5, frame, rot=(0, math.pi / 2, 0))
    piv = empty("swingpivot", (x, y, z + 1.78))
    parts = [cyl((x + sx, y, z + 1.18), 0.006, 1.2, chain, verts=6) for sx in (-0.2, 0.2)]
    seat = cube((x, y, z + 0.58), (0.48, 0.18, 0.035), mat("seat", (0.25, 0.25, 0.28), 0.6), bevel=0.01)
    for o in parts + [seat]: o.parent = piv; o.location = Vector(o.location) - Vector(piv.location)
    return piv, seat


def park(rng, season="dusk", lamps_on=1.0):
    """The park: swing, fence and gate, lamps, trees, bench, clock tower. Returns dict of handles."""
    g, _, sky = SEASONS[season]
    cube((0, 0, -0.05), (30, 30, 0.1), mat("ground_" + season, g, 0.9, noise=0.3))
    cube((0, -0.6, 0.003), (1.2, 30, 0.006), mat("parkpath", (0.6, 0.55, 0.48) if season != "snow" else (0.9, 0.92, 0.96), 0.85, noise=0.3), rot=(0, 0, 0.3))
    piv, seat = swing_set((0, 0, 0))
    fm = mat("parkfence", (0.15, 0.17, 0.15), 0.4, metal=0.7)
    for k in range(-20, 21):
        if abs(k) > 1: cyl((k * 0.15, -2.2, 0.4), 0.012, 0.8, fm, verts=6)
    cube((0, -2.2, 0.78), (6.2, 0.03, 0.03), fm)
    lamps = []
    for lx, ly in ((-1.6, -1.6), (1.7, -1.5), (-2.2, 1.2)):
        cyl((lx, ly, 1.1), 0.035, 2.2, mat("lampm", (0.08, 0.08, 0.09), 0.4, metal=0.8))
        lamps.append(sphere((lx, ly, 2.25), 0.1, mat("plamp%.1f" % lx, (1, 0.85, 0.6), 0.2, emit=(1, 0.78, 0.45), emit_str=18 * lamps_on)))
        lamps.append(light("POINT", (lx, ly, 2.1), 60 * lamps_on, col=(1.0, 0.75, 0.45), size=0.2))
    for tx, ty in ((-2.6, 2.4), (2.4, 2.0), (3.2, -0.5), (-3.4, -0.2)): tree((tx, ty, 0), season, rng)
    cube((1.6, 0.9, 0.22), (0.9, 0.3, 0.05), mat("bench", (0.45, 0.28, 0.15), 0.6, noise=0.5))
    cube((1.6, 1.05, 0.42), (0.9, 0.04, 0.3), mat("bench", (0.45, 0.28, 0.15), 0.6, noise=0.5))
    tw = mat("tower", (0.7, 0.62, 0.55), 0.85, noise=0.3)
    cube((-4.5, 5.5, 2.0), (0.8, 0.8, 4.0), tw); cube((-4.5, 5.5, 4.2), (0.95, 0.95, 0.4), tw)
    face = cyl((-4.5, 5.08, 3.3), 0.3, 0.03, mat("towerface", (0.95, 0.93, 0.85), 0.6, emit=(1, 0.95, 0.8), emit_str=1.2), rot=(math.pi / 2, 0, 0))
    ink = mat("clockink", (0.05, 0.04, 0.03), 0.6)
    cube((-4.5, 5.05, 3.42), (0.025, 0.01, 0.22), ink); cube((-4.5, 5.05, 3.18), (0.03, 0.01, 0.22), ink)   # 6 o'clock
    world_color(sky)
    light("SUN", (0, 0, 6), 1.2 if season in ("spring", "autumn") else 0.6, col=(1.0, 0.75, 0.6) if season != "snow" else (0.75, 0.8, 1.0), rot=(1.1, 0.2, -0.6))
    return {"swing": piv, "seat": seat, "lamps": lamps}


def swing_angle(t, amp=0.5, period=2.2):
    return amp * math.sin(2 * math.pi * t / period)


def hospital(rng, lily_window_lit=True, across=9.0):
    """The children's hospital across the road (front face at y=across-1). Window (floor 4, col 3) is Lily's."""
    y = across
    cube((0, y + 1.5, 3.0), (7.5, 3.0, 6.0), mat("hosp", (0.88, 0.88, 0.85), 0.8, noise=0.15))
    cube((0, y, 0.002), (12, 2.2, 0.004), mat("road", (0.35, 0.36, 0.4), 0.8, noise=0.3))
    cube((0, y + 0.0, 5.7), (2.6, 0.05, 0.45), mat("hsign", (0.25, 0.45, 0.7), 0.6))
    text("CHILDREN'S HOSPITAL", (0, y - 0.03, 5.7), 0.22, mat("hsignink", (1, 1, 1), 0.5, emit=(1, 1, 1), emit_str=2))
    lit = mat("hwinlit", (1, 0.85, 0.6), 0.5, emit=(1, 0.82, 0.55), emit_str=3); dark = mat("hwindark", (0.15, 0.18, 0.25), 0.3)
    target = None
    for fl in range(5):
        for col in range(6):
            x = -2.75 + col * 1.1; z = 0.8 + fl * 1.05
            is_lily = fl == 3 and col == 2
            m = (lit if lily_window_lit else dark) if is_lily else (lit if rng.random() < 0.55 else dark)
            w = cube((x, y - 0.01, z), (0.6, 0.02, 0.7), m)
            if is_lily: target = Vector((x, y, z))
    return target


def hospital_room(rng, dusk=True):
    """Lily's room: a window wall at y=1.2 looking out to the park, bed, drip stand."""
    cube((0, 0, -0.05), (6, 6, 0.1), mat("hfloor", (0.75, 0.78, 0.8), 0.5, noise=0.1))
    wall = mat("hwall", (0.82, 0.88, 0.9), 0.9, noise=0.1)
    cube((-1.35, 1.2, 1.5), (1.9, 0.1, 3), wall); cube((1.35, 1.2, 1.5), (1.9, 0.1, 3), wall)
    cube((0, 1.2, 2.45), (0.8, 0.1, 1.1), wall); cube((0, 1.2, 0.35), (0.8, 0.1, 0.7), wall)
    cube((0, 1.35, 1.3), (0.8, 0.02, 1.2), mat("dusksky", (0.9, 0.6, 0.5), 0.5, emit=(1.0, 0.62, 0.45) if dusk else (0.8, 0.9, 1.0), emit_str=1.3))
    cube((-2.0, 0, 1.5), (0.1, 6, 3), wall)
    bm = mat("hbed", (0.95, 0.95, 0.97), 0.8)
    cube((-1.2, 0.2, 0.32), (0.8, 1.6, 0.18), bm, bevel=0.05); cube((-1.2, 0.85, 0.5), (0.8, 0.08, 0.5), mat("hbedframe", (0.7, 0.72, 0.75), 0.4, metal=0.6))
    cyl((0.6, 0.6, 0.75), 0.015, 1.5, mat("drip", (0.7, 0.72, 0.75), 0.3, metal=0.8))
    sphere((0.6, 0.6, 1.4), 0.06, mat("dripbag", (0.85, 0.9, 1.0), 0.2, alpha=0.6), scale=(0.8, 0.5, 1.3))
    light("AREA", (0, 1.0, 1.4), 45, col=(1.0, 0.7, 0.5) if dusk else (0.9, 0.95, 1.0), size=0.8, rot=(math.pi / 2, 0, 0))
    light("POINT", (-0.5, -1.2, 2.0), 30, col=(1.0, 0.85, 0.7), size=0.6)
    light("AREA", (-0.8, -0.2, 1.6), 18, col=(1.0, 0.8, 0.65), size=1.0, target=(0, 1.0, 0.6))


# ---------------------------------------------------------------- The Extra Plate: dining room and Thanksgiving props
SEATS = {"L1": (-0.62, 0.15), "L2": (-0.62, 0.7), "L3": (-0.62, 1.25), "R1": (0.62, 0.15), "R2": (0.62, 0.7),
         "R3": (0.62, 1.25), "HEAD": (0.0, 1.85)}                          # R2 is Danny's chair, R3 gets the tiny chair
TABLE_Z = 0.5


def plate(loc, food=False):
    x, y, z = loc; pm = mat("plate", (0.96, 0.95, 0.9), 0.25, coat=0.5)
    P = [cyl((x, y, z + 0.005), 0.12, 0.01, pm, verts=24), cyl((x, y, z + 0.012), 0.08, 0.004, mat("plate_in", (0.93, 0.92, 0.86), 0.3), verts=24)]
    sm = mat("silver", (0.8, 0.8, 0.82), 0.25, metal=1.0)
    P += [cube((x - 0.15, y, z + 0.006), (0.012, 0.16, 0.006), sm), cube((x + 0.15, y, z + 0.006), (0.012, 0.16, 0.006), sm)]
    if food: P += [sphere((x - 0.03, y, z + 0.025), 0.04, mat("food1", (0.75, 0.45, 0.2), 0.6), scale=(1.2, 1, 0.5)),
                   sphere((x + 0.04, y + 0.02, z + 0.025), 0.03, mat("food2", (0.3, 0.55, 0.2), 0.6), scale=(1, 1, 0.5))]
    return P


def name_card(loc, name="Danny", rot=0.0):
    x, y, z = loc; cm = mat("card", (0.97, 0.94, 0.86), 0.7)
    a = cube((x, y, z + 0.035), (0.13, 0.004, 0.07), cm, rot=(-0.35, 0, rot))
    t = text(name, (x, y - 0.012, z + 0.04), 0.035, mat("cardink", (0.45, 0.12, 0.08), 0.6), rot=(math.pi / 2 - 0.35, 0, rot))
    return [a, t]


def turkey(loc):
    x, y, z = loc; tm = mat("turkey", (0.62, 0.32, 0.12), 0.45, coat=0.4, noise=0.4)
    P = [cyl((x, y, z + 0.01), 0.2, 0.02, mat("platter", (0.9, 0.88, 0.82), 0.3, coat=0.4), verts=24),
         sphere((x, y, z + 0.09), 0.12, tm, scale=(1.25, 1, 0.7))]
    for sx in (-1, 1): P += [sphere((x + sx * 0.1, y - 0.07, z + 0.07), 0.04, tm, scale=(1, 1.4, 0.8)),
                             sphere((x + sx * 0.13, y - 0.13, z + 0.07), 0.018, mat("bone", (0.95, 0.92, 0.85), 0.5))]
    return P


def pie(loc):
    x, y, z = loc
    return [cyl((x, y, z + 0.02), 0.1, 0.04, mat("crust", (0.8, 0.55, 0.28), 0.6, noise=0.4), verts=20),
            cyl((x, y, z + 0.041), 0.085, 0.004, mat("filling", (0.75, 0.38, 0.1), 0.5), verts=20)]


def candle(loc, h=0.16, lit=True):
    x, y, z = loc; P = [cyl((x, y, z + h / 2), 0.018, h, mat("wax", (0.96, 0.92, 0.82), 0.5)),
                        cyl((x, y, z), 0.035, 0.012, mat("brass_c", (0.75, 0.55, 0.2), 0.3, metal=1.0))]
    if lit:
        f = sphere((x, y, z + h + 0.022), 0.011, mat("cflame", (1, 0.7, 0.3), 0.3, emit=(1.0, 0.5, 0.12), emit_str=12), scale=(0.7, 0.7, 1.8))
        f.visible_shadow = False; P.append(f)
        light("POINT", (x, y, z + h + 0.06), 6, col=(1.0, 0.55, 0.2), size=0.02)
    return P


def chair(loc, rot=0.0, s=1.0, col=(0.42, 0.25, 0.13)):
    x, y, z = loc; m = mat("chair_%d" % int(s * 100), col, 0.55, noise=0.5); P = []
    P.append(cube((0, 0, 0.3 * s), (0.34 * s, 0.32 * s, 0.04 * s), m, bevel=0.01))
    P.append(cube((0, 0.15 * s, 0.6 * s), (0.34 * s, 0.03 * s, 0.6 * s), m, bevel=0.01))
    for sx in (-0.14, 0.14):
        for sy in (-0.13, 0.13): P.append(cube((sx * s, sy * s, 0.15 * s), (0.03 * s, 0.03 * s, 0.3 * s), m))
    g = group("chair", P, (0, 0, 0)); g.location = (x, y, z); g.rotation_euler[2] = rot
    return g


def dining_room(rng, outside="autumn", night=True, candles=True, tiny_chair=False, danny_plate=True, card=True, food=True):
    """Margaret's dining room. Long table along y, seats in SEATS, a window behind the head seat showing the season,
    a doorway on the left wall. outside: autumn | snow | rain | dusk. Returns handles."""
    cube((0, 0, -0.05), (10, 10, 0.1), mat("dfloor", (0.36, 0.22, 0.12), 0.6, noise=0.5))
    wall = mat("dwall", (0.55, 0.36, 0.26), 0.9, noise=0.2)
    cube((-1.0, 2.5, 1.5), (1.4, 0.1, 3), wall); cube((1.0, 2.5, 1.5), (1.4, 0.1, 3), wall)
    cube((0, 2.5, 2.55), (0.6, 0.1, 0.9), wall); cube((0, 2.5, 0.35), (0.6, 0.1, 0.7), wall)
    cube((-1.7, -0.6, 1.5), (0.1, 3.2, 3), wall); cube((-1.7, 2.1, 1.5), (0.1, 0.8, 3), wall); cube((-1.7, 1.35, 2.6), (0.1, 0.7, 0.8), wall)
    cube((1.7, 0.5, 1.5), (0.1, 6, 3), wall)
    sky = {"autumn": (0.10, 0.08, 0.22), "snow": (0.06, 0.09, 0.2), "rain": (0.05, 0.06, 0.1), "dusk": (0.35, 0.18, 0.25)}[outside]
    cube((0, 2.8, 1.45), (0.62, 0.02, 1.2), mat("dsky_" + outside, sky, 0.5, emit=sky, emit_str=1.0))
    fm = mat("dframe", (0.9, 0.88, 0.82), 0.5)
    cube((0, 2.46, 1.45), (0.04, 0.06, 1.22), fm); cube((0, 2.46, 1.45), (0.64, 0.06, 0.04), fm)
    if outside == "autumn":
        for _ in range(5): sphere((rng.uniform(-0.3, 0.3), 3.3, rng.uniform(1.0, 1.9)), rng.uniform(0.15, 0.3), mat("dtree", (0.55, 0.25, 0.08), 0.8))
    light("AREA", (0, 2.3, 1.4), 12, col=(0.45, 0.55, 1.0), size=0.8, rot=(math.pi / 2, 0, 0))        # cool window light
    tm = mat("dtable", (0.5, 0.3, 0.15), 0.5, noise=0.5)
    cube((0, 0.95, TABLE_Z), (0.9, 2.2, 0.05), tm, bevel=0.01)
    for sx in (-0.38, 0.38):
        for sy in (0.0, 1.9): cube((sx, sy, TABLE_Z / 2), (0.05, 0.05, TABLE_Z), tm)
    cube((0, 0.95, TABLE_Z + 0.03), (0.7, 2.0, 0.004), mat("dcloth", (0.92, 0.88, 0.78), 0.9, sheen=0.4, noise=0.2))
    cube((0, 0.95, TABLE_Z + 0.034), (0.25, 2.0, 0.003), mat("drunner", (0.65, 0.2, 0.12), 0.9, sheen=0.5))
    seats = {}
    for k, (x, y) in SEATS.items():
        rot = (math.pi / 2 if x < 0 else -math.pi / 2) if k != "HEAD" else 0.0          # chair back away from the table
        seats[k] = chair((x + (-0.12 if x < 0 else 0.12 if x > 0 else 0), y + (0.12 if k == "HEAD" else 0), 0), rot)
        if k == "R2" and not danny_plate: continue
        px = x * 0.55; py = y if k != "HEAD" else y - 0.15
        plate((px, py, TABLE_Z + 0.036), food=food and k != "R2")
    tiny = chair((0.82, SEATS["R3"][1], 0), -math.pi / 2, s=0.62, col=(0.85, 0.55, 0.4)) if tiny_chair else None
    hc = name_card((SEATS["R2"][0] * 0.55 - 0.02, SEATS["R2"][1] + 0.12, TABLE_Z + 0.036), "Danny", rot=math.pi / 2) if card else None
    if food:
        turkey((0, 0.75, TABLE_Z + 0.036)); pie((0, 1.35, TABLE_Z + 0.036))
    if candles:
        for y in (0.35, 1.1, 1.55): candle((0, y, TABLE_Z + 0.036))
    light("POINT", (0, 0.95, 1.75), 55, col=(1.0, 0.62, 0.3), size=0.4)                                   # warm pendant (out of frame)
    light("AREA", (0, -1.2, 1.6), 9, col=(1.0, 0.75, 0.55), size=1.5, target=(0, 1.0, 0.7))               # soft fill from the camera side
    hall = cube((-2.5, 1.35, 1.1), (0.05, 1.2, 2.2), mat("dhall", (1, 0.85, 0.6), 0.5, emit=(1.0, 0.78, 0.5), emit_str=0.0))
    cube((-1.64, 1.35, 0.015), (0.03, 0.66, 0.03), mat("dgap", (1, 0.8, 0.5), 0.5, emit=(1.0, 0.75, 0.45), emit_str=25))   # light under the door
    door = empty("dhinge", (-1.68, 1.0, 0))
    d = cube((-1.68, 1.35, 1.1), (0.06, 0.66, 2.18), mat("ddoor", (0.32, 0.17, 0.08), 0.55, noise=0.6), bevel=0.01)
    d.parent = door; d.location = Vector(d.location) - Vector(door.location)
    return {"seats": seats, "tiny": tiny, "card": hc, "door": door, "hall": hall}


def spot_camera(push=0.0):
    """The 'same spot' camera: the same frame of the table every year."""
    return camera((0.0, -1.05 + push, 1.12), (0.0, 1.05, 0.62), lens=26, dof=2.0, fstop=4.0)


def cam(loc, target, lens=45, fstop=2.2):
    """Camera focused exactly on its target."""
    return camera(loc, target, lens=lens, dof=(Vector(target) - Vector(loc)).length, fstop=fstop)


def postcard(loc, text_body="Your plate\nis still warm.", rot=(0, 0, 0)):
    x, y, z = loc
    c = cube((x, y, z), (0.3, 0.2, 0.004), mat("postcard", (0.96, 0.92, 0.8), 0.7), rot=rot)
    t = text(text_body, (x, y, z + 0.004), 0.03, mat("pcink", (0.15, 0.15, 0.35), 0.6), rot=rot)
    return [c, t]
