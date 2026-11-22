"""Dustlight character library. There is no house model: every video picks the design that fits it (channel/formats.md,
"Character model"). Each builder returns the same handles as world.peg() so walk(), breathe() and shot code work unchanged:
{root, head, L, R, cheek, base} plus legs {LL, LR} where the model has legs.

Models
- blocky(): chunky block people (bevelled box head, box torso, hinged block limbs, mitten hands). Comedy, trend, game-like Shorts.
- clay(): plasticine people (lumpy, matte fingerprint texture, ball nose, button eyes). Warm family and holiday stories; render without STYLE=lowpoly.
- bean(): round one-colour capsule people with big glossy eyes and tiny limbs. Cute, fast comedy, "you" stories, kids logic.
Add new models here (bean, clay, paper...) the first time a video needs one, and list them in channel/formats.md.
"""
import math
from scene import *          # noqa

SKINS = {"light": (0.98, 0.82, 0.66), "tan": (0.85, 0.62, 0.45), "brown": (0.55, 0.36, 0.24), "dark": (0.33, 0.21, 0.14)}


def _pin(objs, piv):
    for o in objs:
        o.parent = piv; o.location = Vector(o.location) - Vector(piv.location)


def blocky(loc, shirt, pants=(0.2, 0.25, 0.4), skin="light", hair=None, style="kid", rot=0.0, h=1.0, name="blk",
           hat=None, glasses=False, shoes=(0.12, 0.1, 0.1), mouth="smile"):
    """Block person about 1 unit tall (same scale as the peg dolls). style: kid | gran | dad | mum (changes hair and build).
    hair: colour (None = default for the style). hat: colour of a knitted beanie. mouth: smile | flat | open. Returns handles incl. legs LL, LR."""
    sk = mat("bskin_" + name, SKINS.get(skin, skin) if isinstance(skin, str) else skin, 0.55, noise=0.05)
    sm = mat("bshirt_" + name, shirt, 0.75, sheen=0.3, noise=0.12)
    pm = mat("bpants_" + name, pants, 0.8, noise=0.12)
    shm = mat("bshoe_" + name, shoes, 0.5)
    blk = mat("beye", (0.02, 0.02, 0.025), 0.15); wht = mat("beyew", (1, 1, 1), 0.1)
    cheek = mat("bcheek_" + name, (0.95, 0.45, 0.45), 0.6)
    wide = {"kid": 0.30, "gran": 0.32, "dad": 0.36, "mum": 0.31}.get(style, 0.32)
    tall = {"kid": 0.28, "gran": 0.30, "dad": 0.34, "mum": 0.32}.get(style, 0.3)
    leg_h = 0.26 if style == "kid" else 0.30
    hz = leg_h + tall                              # top of torso
    hs = 0.30 if style == "kid" else 0.27           # head size (kids get the bigger head)

    torso = [cube((0, 0, leg_h + tall / 2), (wide, 0.18, tall), sm, bevel=0.02)]
    head = empty("head_" + name, (0, 0, hz + 0.02))
    hc = hz + 0.03 + hs / 2
    H = [cube((0, 0, hc), (hs, hs * 0.92, hs), sk, bevel=0.05)]
    ey = -hs * 0.46 - 0.004
    for sx in (-1, 1):                              # big glossy eyes, eyebrows, cheeks
        H += [sphere((sx * hs * 0.2, ey, hc + 0.02), 0.03, blk, scale=(0.8, 0.35, 1.0)),
              sphere((sx * hs * 0.2 + 0.008, ey - 0.008, hc + 0.035), 0.009, wht),
              cube((sx * hs * 0.2, ey, hc + 0.075), (0.05, 0.01, 0.012), blk, rot=(0, sx * 0.18, 0)),
              sphere((sx * hs * 0.32, ey + 0.004, hc - 0.03), 0.025, cheek, scale=(1, 0.3, 0.7))]
    if mouth == "flat":                             # deadpan line
        H.append(cube((0, ey, hc - 0.05), (0.06, 0.01, 0.012), blk))
    elif mouth == "open":                           # surprised "o"
        H.append(sphere((0, ey, hc - 0.055), 0.022, blk, scale=(0.8, 0.3, 1.0)))
    else:
        for k in range(5):                          # little smile
            x = -0.03 + k * 0.015; H.append(sphere((x, ey, hc - 0.05 + 10 * x * x), 0.007, blk, seg=8))
    hcol = hair or {"kid": (0.22, 0.14, 0.08), "gran": (0.93, 0.92, 0.9), "dad": (0.15, 0.1, 0.07), "mum": (0.45, 0.26, 0.12)}[style]
    hm = mat("bhair_" + name, hcol, 0.9, sheen=0.4, noise=0.2)
    top = hc + hs / 2
    if hat:
        km = mat("bhat_" + name, hat, 0.95, sheen=0.9, noise=0.35)
        H += [cube((0, 0.01, top + 0.03), (hs + 0.03, hs * 0.95, 0.12), km, bevel=0.04), sphere((0, 0.01, top + 0.12), 0.04, km)]
    elif style == "kid":                            # messy block fringe
        H += [cube((0, 0.01, top + 0.02), (hs + 0.02, hs * 0.95, 0.06), hm, bevel=0.02),
              cube((-0.06, -hs * 0.44, top - 0.03), (0.12, 0.03, 0.06), hm, rot=(0, 0.2, 0), bevel=0.01),
              cube((0.07, -hs * 0.44, top - 0.02), (0.1, 0.03, 0.05), hm, rot=(0, -0.25, 0), bevel=0.01)]
    elif style == "gran":                           # white hair with a block bun, round glasses
        H += [cube((0, 0.02, top + 0.015), (hs + 0.03, hs * 0.97, 0.05), hm, bevel=0.02),
              cube((0, hs * 0.5, top - 0.02), (0.12, 0.08, 0.12), hm, bevel=0.03)]
        glasses = True
    elif style == "dad":
        H += [cube((0, 0.01, top + 0.012), (hs + 0.015, hs * 0.94, 0.035), hm, bevel=0.01),
              cube((0, ey + 0.012, hc - 0.085), (hs * 0.75, 0.02, 0.05), hm, bevel=0.01)]       # beard line
    elif style == "mum":
        H += [cube((0, 0.03, top - 0.02), (hs + 0.04, hs, 0.1), hm, bevel=0.03),
              cube((0, hs * 0.48, hc - 0.05), (hs + 0.03, 0.05, hs * 0.9), hm, bevel=0.02)]
    if glasses:
        fm = mat("bglass", (0.45, 0.3, 0.2), 0.3, metal=0.6)
        for sx in (-1, 1): H.append(torus((sx * hs * 0.2, ey - 0.006, hc + 0.02), 0.042, 0.005, fm, rot=(math.pi / 2, 0, 0)))
    _pin(H, head)

    arms, legs = {}, {}
    arm_len = tall * 0.95
    for side, sx in (("L", -1), ("R", 1)):          # shoulder pivots: rotate x to swing, y to raise sideways
        px = sx * (wide / 2 + 0.05)
        piv = empty(f"arm{side}_{name}", (px, 0, hz - 0.04))
        _pin([cube((px, 0, hz - 0.04 - arm_len / 2), (0.085, 0.1, arm_len), sm, bevel=0.02),
              cube((px, 0, hz - 0.06 - arm_len), (0.09, 0.1, 0.08), sk, bevel=0.03)], piv)        # mitten hand
        arms[side] = piv
        lp = empty(f"leg{side}_{name}", (sx * wide * 0.25, 0, leg_h))
        _pin([cube((sx * wide * 0.25, 0, leg_h / 2 + 0.03), (wide * 0.44, 0.15, leg_h - 0.04), pm, bevel=0.015),
              cube((sx * wide * 0.25, -0.025, 0.03), (wide * 0.46, 0.2, 0.06), shm, bevel=0.02)], lp)
        legs["L" + side] = lp
    root = empty("root_" + name)
    for o in torso + [head, arms["L"], arms["R"], legs["LL"], legs["LR"]]:
        if o.parent is None: o.parent = root
    root.location = loc; root.rotation_euler[2] = rot; root.scale = (h, h, h)
    return {"root": root, "head": head, "L": arms["L"], "R": arms["R"], "LL": legs["LL"], "LR": legs["LR"],
            "cheek": cheek, "base": Vector(loc), "hand_z": hz - 0.06 - arm_len, "arm_x": wide / 2 + 0.05}


def stride(d, t, speed=1.0, direction=(0, -1), amp=0.6, rate=2.0):
    """Walk or run for legged models: legs and arms swing in opposition, small bounce."""
    ph = t * 2 * math.pi * rate
    d["root"].location = d["base"] + Vector((direction[0], direction[1], 0)) * (t * speed)
    d["root"].location.z = d["base"].z + 0.025 * abs(math.sin(ph))
    s = math.sin(ph)
    d["LL"].rotation_euler[0] = amp * s; d["LR"].rotation_euler[0] = -amp * s
    d["L"].rotation_euler[0] = -amp * 0.8 * s; d["R"].rotation_euler[0] = amp * 0.8 * s


def ball(loc, r=0.09, col=(0.92, 0.42, 0.12)):
    """Basketball with dark seams."""
    m = mat("bball", col, 0.55, noise=0.25); sm = mat("bseam", (0.08, 0.05, 0.04), 0.6)
    b = sphere(loc, r, m)
    seams = [torus(loc, r * 1.005, r * 0.05, sm), torus(loc, r * 1.005, r * 0.05, sm, rot=(math.pi / 2, 0, 0)),
             torus(loc, r * 1.005, r * 0.05, sm, rot=(0, math.pi / 2, 0))]
    for s in seams: s.parent = b; s.location = (0, 0, 0)
    b["r"] = r
    return b


def dribble(d, b, t, rate=2.2, side="R", floor=0.0):
    """Bounce ball b under the hand on `side` of block person d; the arm pumps in time. Returns the ball height 0..1."""
    ph = (t * rate) % 1.0
    up = 1 - abs(1 - 2 * ph)                          # 0 at the floor, 1 at the hand
    root = d["root"]; s = root.scale.x
    sx = 1 if side == "R" else -1
    a = root.rotation_euler[2]; lx, ly = sx * d["arm_x"] * s, -0.12 * s
    off = root.location + Vector((lx * math.cos(a) - ly * math.sin(a), lx * math.sin(a) + ly * math.cos(a), 0))
    r = b.get("r", 0.09)
    b.location = (off.x, off.y, floor + r + (d["hand_z"] * s - r) * (1 - (1 - up) ** 2))
    d[side].rotation_euler[0] = -0.55 + 0.35 * up
    return up


def bean(loc, col, rot=0.0, h=1.0, name="bean", style="kid", mouth="smile", glasses=False, tuft=None, bow=None, hat=None,
         scarf=None):
    """Round bean person about 1 unit tall: one soft capsule body in a single colour, big glossy eyes, tiny arms and feet.
    style: kid | adult | gran (changes proportions). tuft: hair colour for a little curl on top. bow: ribbon colour. hat: beanie
    colour. Returns the same handles as blocky() (legs LL/LR are the feet)."""
    bm = mat("bbody_" + name, col, 0.45, sheen=0.4, noise=0.05, coat=0.25)
    blk = mat("beaneye", (0.02, 0.02, 0.03), 0.1, coat=0.8); wht = mat("beanwht", (1, 1, 1), 0.2)
    cheek = mat("bcheek_" + name, (0.98, 0.5, 0.5), 0.6)
    r = {"kid": 0.21, "adult": 0.23, "gran": 0.24}.get(style, 0.22)
    tall = {"kid": 0.78, "adult": 0.95, "gran": 0.88}.get(style, 0.85)
    feet_h = 0.06
    body = [cyl((0, 0, feet_h + tall / 2), r, tall - 2 * r, bm, verts=40),
            sphere((0, 0, feet_h + r), r, bm), sphere((0, 0, feet_h + tall - r), r, bm)]
    head = empty("head_" + name, (0, 0, feet_h + tall * 0.55))
    ez = feet_h + tall - r * 1.05; ey = -r * 0.93
    H = []
    for sx in (-1, 1):                                            # big glossy eyes with a highlight, cheeks
        H += [sphere((sx * r * 0.38, ey, ez), r * 0.3, wht, scale=(0.9, 0.45, 1.05)),
              sphere((sx * r * 0.36, ey - r * 0.1, ez - r * 0.02), r * 0.18, blk, scale=(0.9, 0.4, 1.1)),
              sphere((sx * r * 0.32, ey - r * 0.17, ez + r * 0.07), r * 0.06, wht),
              sphere((sx * r * 0.62, ey + r * 0.12, ez - r * 0.38), r * 0.13, cheek, scale=(1, 0.35, 0.7))]
    mz = ez - r * 0.5; my = -r - 0.006                          # the mouth sits on the cylinder surface
    if mouth == "flat": H.append(cube((0, my, mz), (r * 0.35, 0.01, 0.014), blk))
    elif mouth == "open": H.append(sphere((0, my + 0.004, mz - 0.01), r * 0.14, blk, scale=(0.9, 0.3, 1.0)))
    elif mouth == "worried":
        for k in range(5): x = (-2 + k) * r * 0.1; H.append(sphere((x, my, mz - 0.012 * (2 - abs(k - 2))), 0.009, blk, seg=8))
    else:
        for k in range(5): x = (-2 + k) * r * 0.1; H.append(sphere((x, my, mz + 0.03 * (x / (r * 0.2)) ** 2), 0.009, blk, seg=8))
    top = feet_h + tall
    if glasses or style == "gran":
        fm = mat("beanglass", (0.5, 0.33, 0.22), 0.3, metal=0.6)
        for sx in (-1, 1): H.append(torus((sx * r * 0.38, ey - 0.012, ez), r * 0.33, 0.006, fm, rot=(math.pi / 2, 0, 0)))
    if style == "gran":
        hm = mat("beangran_" + name, (0.95, 0.94, 0.92), 0.9, sheen=0.5)
        H += [sphere((0, r * 0.15, top - r * 0.25), r * 0.9, hm, scale=(1.08, 1.0, 0.45)), sphere((0, r * 0.55, top + 0.01), r * 0.38, hm)]
    if tuft:
        tm = mat("beantuft_" + name, tuft, 0.8, sheen=0.4)
        H += [sphere((dx, 0.0, top - 0.005 + 0.02 * k), r * 0.16, tm) for k, dx in enumerate((-0.03, 0.0, 0.035))]
    if bow:
        bwm = mat("beanbow_" + name, bow, 0.6)
        for sx in (-1, 1): H.append(sphere((sx * r * 0.18 + r * 0.5, 0, top - r * 0.2), r * 0.17, bwm, scale=(1.2, 0.5, 0.8)))
    if hat:
        km = mat("beanhat_" + name, hat, 0.95, sheen=0.9, noise=0.35)
        H += [sphere((0, 0, top - r * 0.35), r * 1.02, km, scale=(1, 1, 0.62)), sphere((0, 0, top + r * 0.3), r * 0.25, km),
              torus((0, 0, top - r * 0.62), r * 0.98, r * 0.12, km)]
    _pin(H, head)
    if scarf:
        sm = mat("beanscarf_" + name, scarf, 0.95, sheen=0.9, noise=0.3)
        body.append(torus((0, 0, ez - r * 0.9), r * 1.0, r * 0.16, sm))
    arms, legs = {}, {}
    az = feet_h + tall * 0.52
    for side, sx in (("L", -1), ("R", 1)):
        piv = empty(f"arm{side}_{name}", (sx * r * 0.95, 0, az))
        _pin([sphere((sx * r * 1.02, 0, az - 0.09), 0.045, bm, scale=(0.85, 0.85, 2.2)), sphere((sx * r * 1.02, 0, az - 0.18), 0.05, bm)], piv)
        arms[side] = piv
        lp = empty(f"leg{side}_{name}", (sx * r * 0.45, 0, feet_h + 0.04))
        _pin([sphere((sx * r * 0.45, -0.03, feet_h * 0.6), 0.065, bm, scale=(0.9, 1.3, 0.6))], lp)
        legs["L" + side] = lp
    root = empty("root_" + name)
    for o in body + [head, arms["L"], arms["R"], legs["LL"], legs["LR"]]:
        if o.parent is None: o.parent = root
    root.location = loc; root.rotation_euler[2] = rot; root.scale = (h, h, h)
    return {"root": root, "head": head, "L": arms["L"], "R": arms["R"], "LL": legs["LL"], "LR": legs["LR"],
            "cheek": cheek, "base": Vector(loc), "hand_z": az - 0.18, "arm_x": r * 1.02}


def clay_mat(name, col, rough=0.75):
    """Plasticine: matte, a little sheen, fine fingerprint-like bumps."""
    m = mat("clay_" + name, col, rough, sheen=0.25, noise=0.0)
    nt = m.node_tree; b = bsdf(m)
    tex = nt.nodes.new("ShaderNodeTexNoise"); tex.inputs["Scale"].default_value = 140.0; tex.inputs["Detail"].default_value = 6.0
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.18
    nt.links.new(tex.outputs["Fac"], bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    return m


def lumpy(objs, strength=0.012, seed=0):
    """Hand-pressed unevenness: a soft noise displacement on every part (needs smooth shading, so no low-poly pass)."""
    tex = bpy.data.textures.get("claylump") or bpy.data.textures.new("claylump", "CLOUDS")
    tex.noise_scale = 0.08
    for o in objs:
        if o.type != "MESH": continue
        o["lowpoly"] = 1                                           # keep the low-poly pass away from clay
        for p in o.data.polygons: p.use_smooth = True
        d = o.modifiers.new("lump", "DISPLACE"); d.texture = tex; d.strength = strength; d.mid_level = 0.5
        d.texture_coords = "GLOBAL"


def clay(loc, col, rot=0.0, h=1.0, name="clay", style="kid", hair=None, skin=(0.96, 0.78, 0.62), mouth="smile", glasses=False,
         scarf=None, hat=None, apron=None):
    """Plasticine person about 1 unit tall: pear body, round head with a ball nose, button eyes, sausage arms, stubby legs.
    style: kid | adult | old (old = stooped, white hair). Returns the same handles as blocky()."""
    sk = clay_mat("skin_" + name, skin); bm = clay_mat("body_" + name, col)
    blk = mat("clayeye", (0.02, 0.02, 0.02), 0.25); wht = clay_mat("claywht", (0.97, 0.96, 0.93), 0.6)
    cheek = clay_mat("cheek_" + name, (0.95, 0.55, 0.5))
    tall = {"kid": 0.42, "adult": 0.52, "old": 0.48}.get(style, 0.5); hr = {"kid": 0.17, "adult": 0.15, "old": 0.15}.get(style, 0.15)
    leg_h = 0.14 if style == "kid" else 0.18
    parts = []
    body = [sphere((0, 0, leg_h + tall * 0.42), 0.2, bm, scale=(1.0, 0.85, 1.25)),
            sphere((0, 0, leg_h + tall * 0.85), 0.14, bm, scale=(1.05, 0.9, 0.8))]
    if apron: body.append(sphere((0, -0.08, leg_h + tall * 0.4), 0.17, clay_mat("apron_" + name, apron), scale=(0.95, 0.5, 1.1)))
    if scarf: body.append(torus((0, 0, leg_h + tall * 0.98), 0.1, 0.045, clay_mat("scarf_" + name, scarf)))
    hz = leg_h + tall + hr * 0.85
    head = empty("head_" + name, (0, 0, leg_h + tall))
    H = [sphere((0, 0, hz), hr, sk, scale=(1, 0.95, 1.02)), sphere((0, -hr * 0.98, hz - hr * 0.08), hr * 0.24, sk)]
    for sx in (-1, 1):
        H += [sphere((sx * hr * 0.38, -hr * 0.86, hz + hr * 0.12), hr * 0.2, wht, scale=(1, 0.5, 1.15)),
              sphere((sx * hr * 0.38, -hr * 0.95, hz + hr * 0.1), hr * 0.11, blk, scale=(1, 0.5, 1.1)),
              sphere((sx * hr * 0.62, -hr * 0.75, hz - hr * 0.22), hr * 0.16, cheek, scale=(1, 0.4, 0.75))]
    my = -hr * 0.9; mz = hz - hr * 0.42
    if mouth == "open": H.append(sphere((0, my, mz), hr * 0.16, blk, scale=(1, 0.4, 0.8)))
    elif mouth == "flat": H.append(cyl((0, my, mz), 0.012, hr * 0.4, blk, rot=(0, math.pi / 2, 0)))
    else: H.append(torus((0, my + 0.01, mz + hr * 0.08), hr * 0.22, 0.011, blk, rot=(math.pi / 2 - 0.25, 0, 0)))
    hcol = hair or {"kid": (0.4, 0.25, 0.12), "adult": (0.3, 0.2, 0.12), "old": (0.95, 0.94, 0.92)}[style]
    hm = clay_mat("hair_" + name, hcol)
    if hat:
        km = clay_mat("hat_" + name, hat)
        H += [sphere((0, 0.01, hz + hr * 0.5), hr * 1.02, km, scale=(1, 1, 0.6)), sphere((0, 0, hz + hr * 1.15), hr * 0.28, km)]
    elif style == "old":
        H += [sphere((sx * hr * 0.85, 0.02, hz + hr * 0.05), hr * 0.38, hm, scale=(0.7, 1, 0.9)) for sx in (-1, 1)]
        H += [sphere((0, hr * 0.1, hz + hr * 0.75), hr * 0.5, hm, scale=(1.3, 1, 0.35))]
    else:
        H += [sphere((0, hr * 0.12, hz + hr * 0.42), hr * 0.98, hm, scale=(1.05, 1, 0.72)),
              sphere((-hr * 0.3, -hr * 0.6, hz + hr * 0.65), hr * 0.3, hm, scale=(1.2, 0.8, 0.6))]
    if glasses:
        fm = mat("clayglass", (0.3, 0.2, 0.15), 0.3, metal=0.5)
        for sx in (-1, 1): H.append(torus((sx * hr * 0.38, -hr * 0.98, hz + hr * 0.12), hr * 0.26, 0.008, fm, rot=(math.pi / 2, 0, 0)))
    _pin(H, head)
    arms, legs = {}, {}
    az = leg_h + tall * 0.85
    for side, sx in (("L", -1), ("R", 1)):
        piv = empty(f"arm{side}_{name}", (sx * 0.17, 0, az))
        _pin([sphere((sx * 0.2, 0, az - 0.12), 0.05, bm, scale=(0.9, 0.9, 2.6)), sphere((sx * 0.2, 0, az - 0.26), 0.05, sk)], piv)
        arms[side] = piv
        lp = empty(f"leg{side}_{name}", (sx * 0.08, 0, leg_h))
        _pin([sphere((sx * 0.08, 0, leg_h * 0.55), 0.06, clay_mat("legs_" + name, (0.3, 0.28, 0.35)), scale=(1, 1, 1.4)),
              sphere((sx * 0.08, -0.03, 0.03), 0.065, clay_mat("shoe_" + name, (0.2, 0.15, 0.12)), scale=(1, 1.4, 0.6))], lp)
        legs["L" + side] = lp
    root = empty("root_" + name)
    for o in body + [head, arms["L"], arms["R"], legs["LL"], legs["LR"]]:
        if o.parent is None: o.parent = root
    lumpy([o for o in body + H] + [c for a in list(arms.values()) + list(legs.values()) for c in a.children])
    root.location = loc; root.rotation_euler[2] = rot; root.scale = (h, h, h)
    if style == "old": root.rotation_euler[0] = 0.08
    return {"root": root, "head": head, "L": arms["L"], "R": arms["R"], "LL": legs["LL"], "LR": legs["LR"],
            "cheek": cheek, "base": Vector(loc), "hand_z": az - 0.26, "arm_x": 0.2}
