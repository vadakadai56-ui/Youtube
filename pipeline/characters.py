"""Dustlight character library. There is no house model: every video picks the design that fits it (channel/formats.md,
"Character model"). Each builder returns the same handles as world.peg() so walk(), breathe() and shot code work unchanged:
{root, head, L, R, cheek, base} plus legs {LL, LR} where the model has legs.

Models
- blocky(): chunky block people (bevelled box head, box torso, hinged block limbs, mitten hands). Comedy, trend, game-like Shorts.
- clay(): plasticine people (lumpy, matte fingerprint texture, ball nose, button eyes). Warm family and holiday stories; render without STYLE=lowpoly.
- bean(): round one-colour capsule people with big glossy eyes and tiny limbs. Cute, fast comedy, "you" stories, kids logic.
- person(): ready-made CC0 people by Quaternius (assets/characters/quaternius, 5 men and 6 women in everyday clothes,
  each with 24 animations: Walk, Run, Idle, Wave, Interact...). The owner's choice for human characters, 23 Nov 2026.
- human(): primitive-built human proportions (neck, elbows, hands, knees, shoes, full face). EXPERIMENT ONLY: the owner rejected
  its look on 23 Nov 2026 ("looks shit"). Do not use in a video; the plan is ready-made CC0 human models (e.g. Quaternius).
Add new models here (bean, clay, paper...) the first time a video needs one, and list them in channel/formats.md.
"""
import math, os
from mathutils import Quaternion
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
    m0 = len(H)
    if mouth == "flat":                             # deadpan line
        H.append(cube((0, ey, hc - 0.05), (0.06, 0.01, 0.012), blk))
    elif mouth == "open":                           # surprised "o"
        H.append(sphere((0, ey, hc - 0.055), 0.022, blk, scale=(0.8, 0.3, 1.0)))
    else:
        for k in range(5):                          # little smile
            x = -0.03 + k * 0.015; H.append(sphere((x, ey, hc - 0.05 + 10 * x * x), 0.007, blk, seg=8))
    TALK = _talk(H, m0, sphere((0, ey, hc - 0.055), 0.024, blk, scale=(0.8, 0.3, 0.001)))
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
            "cheek": cheek, "base": Vector(loc), "hand_z": hz - 0.06 - arm_len, "arm_x": wide / 2 + 0.05, **TALK}


def stride(d, t, speed=1.0, direction=(0, -1), amp=0.6, rate=2.0):
    """Walk or run for legged models: legs and arms swing in opposition, small bounce."""
    ph = t * 2 * math.pi * rate
    d["root"].location = d["base"] + Vector((direction[0], direction[1], 0)) * (t * speed)
    d["root"].location.z = d["base"].z + 0.025 * abs(math.sin(ph))
    s = math.sin(ph)
    d["LL"].rotation_euler[0] = amp * s; d["LR"].rotation_euler[0] = -amp * s
    d["L"].rotation_euler[0] = -amp * 0.8 * s; d["R"].rotation_euler[0] = amp * 0.8 * s
    if "LK" in d:                                    # human: the knee bends as the leg swings back, elbows stay soft
        d["LK"].rotation_euler[0] = 1.2 * amp * max(0.0, s); d["RK"].rotation_euler[0] = 1.2 * amp * max(0.0, -s)
        d["LE"].rotation_euler[0] = d["RE"].rotation_euler[0] = -0.35 - 0.3 * amp


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
    body = [capsule((0, 0, feet_h + tall / 2), r, tall - 2 * r, bm)]
    head = empty("head_" + name, (0, 0, feet_h + tall * 0.55))
    ez = feet_h + tall - r * 1.05; ey = -r * 0.93
    H = []
    for sx in (-1, 1):                                            # big glossy eyes with a highlight, cheeks
        H += [sphere((sx * r * 0.38, ey, ez), r * 0.3, wht, scale=(0.9, 0.45, 1.05)),
              sphere((sx * r * 0.36, ey - r * 0.1, ez - r * 0.02), r * 0.18, blk, scale=(0.9, 0.4, 1.1)),
              sphere((sx * r * 0.32, ey - r * 0.17, ez + r * 0.07), r * 0.06, wht),
              sphere((sx * r * 0.62, ey + r * 0.12, ez - r * 0.38), r * 0.13, cheek, scale=(1, 0.35, 0.7))]
    mz = ez - r * 0.5; my = -r - 0.006                          # the mouth sits on the cylinder surface
    m0 = len(H)
    if mouth == "flat": H.append(cube((0, my, mz), (r * 0.35, 0.01, 0.014), blk))
    elif mouth == "open": H.append(sphere((0, my + 0.004, mz - 0.01), r * 0.14, blk, scale=(0.9, 0.3, 1.0)))
    elif mouth == "worried":
        for k in range(5): x = (-2 + k) * r * 0.1; H.append(sphere((x, my, mz - 0.012 * (2 - abs(k - 2))), 0.009, blk, seg=8))
    else:
        for k in range(5): x = (-2 + k) * r * 0.1; H.append(sphere((x, my, mz + 0.03 * (x / (r * 0.2)) ** 2), 0.009, blk, seg=8))
    TALK = _talk(H, m0, sphere((0, my + 0.004, mz - 0.01), r * 0.14, blk, scale=(0.9, 0.3, 0.001)))
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
            "cheek": cheek, "base": Vector(loc), "hand_z": az - 0.18, "arm_x": r * 1.02, **TALK}


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
    my = -hr * 0.9; mz = hz - hr * 0.42; m0 = len(H)
    if mouth == "open": H.append(sphere((0, my, mz), hr * 0.16, blk, scale=(1, 0.4, 0.8)))
    elif mouth == "flat": H.append(cyl((0, my, mz), 0.012, hr * 0.4, blk, rot=(0, math.pi / 2, 0)))
    else: H.append(torus((0, my + 0.01, mz + hr * 0.08), hr * 0.22, 0.011, blk, rot=(math.pi / 2 - 0.25, 0, 0)))
    TALK = _talk(H, m0, sphere((0, my, mz), hr * 0.16, blk, scale=(1, 0.4, 0.001)))
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
            "cheek": cheek, "base": Vector(loc), "hand_z": az - 0.26, "arm_x": 0.2, **TALK}


def human(loc, col, rot=0.0, h=1.0, name="human", style="adult", hair=None, skin=(0.96, 0.78, 0.62), mouth="smile",
          glasses=False, scarf=None, hat=None, apron=None, pants=None, shoes=(0.15, 0.12, 0.11)):
    """Human-proportioned person, about 1 unit tall as an adult (kid 0.78, old 0.94 and a little stooped): capsule torso and
    limbs, a neck, shoulders, elbows (LE, RE) and knees (LK, RK) that bend, round hands, shoes, and a face with eyes, brows,
    nose, ears and a mouth. Same arguments as clay() (col = top colour) and the same handles, plus LE/RE/LK/RK and hip_z."""
    H_ = {"kid": 0.78, "adult": 1.0, "old": 0.94}.get(style, 1.0)
    hr = {"kid": 0.1, "adult": 0.092, "old": 0.09}.get(style, 0.092)                 # kids: bigger head for their size
    sk = mat("huskin_" + name, skin, 0.55); top = mat("hutop_" + name, col, 0.7)
    low = mat("hupants_" + name, pants or tuple(c * 0.45 for c in col), 0.75); sh = mat("hushoe_" + name, shoes, 0.5)
    blk = mat("hueye", (0.03, 0.03, 0.04), 0.2); wht = mat("huwht", (0.98, 0.98, 0.97), 0.3)
    cheek = mat("hucheek_" + name, (0.97, 0.6, 0.55), 0.6)
    hip_z = 0.46 * H_; sho_z = 0.78 * H_ - (0.02 if style == "old" else 0)
    leg_r, arm_r = 0.038 * H_ ** 0.5, 0.025 * H_ ** 0.5
    torso = [capsule((0, 0, (hip_z + sho_z) / 2), 0.078 * H_ ** 0.5, sho_z - hip_z - 0.06, top),
             cyl((0, 0, sho_z + 0.025), 0.03, 0.06, sk)]                                # neck
    torso[0].scale = (1.08, 0.7, 1.0)
    if apron:
        ap = capsule((0, -0.05, hip_z + 0.06), 0.06, 0.12, mat("huapron_" + name, apron, 0.8)); ap.scale = (1.0, 0.25, 1.0); torso.append(ap)
    if scarf: torso.append(torus((0, 0, sho_z + 0.01), 0.045, 0.022, mat("huscarf_" + name, scarf, 0.9)))
    hz = sho_z + 0.055 + hr
    head = empty("head_" + name, (0, 0, sho_z + 0.05))
    F = [sphere((0, 0, hz), hr, sk, scale=(0.95, 0.95, 1.05)), sphere((0, -hr * 0.97, hz - hr * 0.12), hr * 0.13, sk)]   # head, nose
    ey, ez = -hr * 0.86, hz + hr * 0.12
    for sx in (-1, 1):
        F += [sphere((sx * hr * 0.38, ey, ez), hr * 0.27, wht, scale=(0.85, 0.45, 1.1)),            # eye white
              sphere((sx * hr * 0.37, ey - hr * 0.09, ez - hr * 0.03), hr * 0.17, blk, scale=(0.85, 0.4, 1.05)),
              capsule((sx * hr * 0.42, ey - 0.004, ez + hr * 0.36), hr * 0.045, hr * 0.22, blk),    # brow
              sphere((sx * hr * 0.98, 0, hz - hr * 0.02), hr * 0.2, sk, scale=(0.45, 0.7, 1.0)),     # ear
              sphere((sx * hr * 0.6, ey + hr * 0.12, hz - hr * 0.32), hr * 0.15, cheek, scale=(1, 0.3, 0.7))]
        F[-3].rotation_euler = (0, math.pi / 2 + sx * 0.1, 0)
    my, mz = -hr * 0.9, hz - hr * 0.45; m0 = len(F)
    if mouth == "open": F.append(sphere((0, my, mz), hr * 0.14, blk, scale=(1, 0.4, 0.8)))
    elif mouth == "flat": F.append(capsule((0, my, mz), 0.006, hr * 0.3, blk)); F[-1].rotation_euler = (0, math.pi / 2, 0)
    else: F.append(torus((0, my + 0.006, mz + hr * 0.05), hr * 0.15, 0.0045, blk, rot=(math.pi / 2 - 0.45, 0, 0)))
    TALK = _talk(F, m0, sphere((0, my, mz), hr * 0.15, blk, scale=(1, 0.4, 0.001)))
    hcol = hair or {"kid": (0.35, 0.22, 0.12), "adult": (0.22, 0.15, 0.1), "old": (0.93, 0.92, 0.9)}[style]
    hm = mat("huhair_" + name, hcol, 0.85, sheen=0.3)
    if hat:
        km = mat("huhat_" + name, hat, 0.9)
        F += [sphere((0, 0.005, hz + hr * 0.45), hr * 1.06, km, scale=(1, 1, 0.62)), sphere((0, 0, hz + hr * 1.1), hr * 0.25, km)]
    elif style == "old":
        F += [sphere((sx * hr * 0.82, hr * 0.15, hz + hr * 0.1), hr * 0.35, hm, scale=(0.6, 1, 0.8)) for sx in (-1, 1)]
    else:
        F += [sphere((0, hr * 0.12, hz + hr * 0.3), hr * 1.04, hm, scale=(1.02, 0.98, 0.78))]
        if style == "kid": F.append(sphere((-hr * 0.35, -hr * 0.62, hz + hr * 0.62), hr * 0.32, hm, scale=(1.4, 0.7, 0.55)))   # fringe
    if glasses:
        fm = mat("huglass", (0.25, 0.18, 0.14), 0.3, metal=0.5)
        for sx in (-1, 1):
            F.append(torus((sx * hr * 0.38, -hr * 0.98, ez), hr * 0.3, 0.004, fm, rot=(math.pi / 2, 0, 0))); F[-1]["noline"] = 1
    _pin(F, head)
    joints = {}
    for side, sx in (("L", -1), ("R", 1)):
        ax = sx * 0.11 * H_ ** 0.5
        sp = empty(f"arm{side}_{name}", (ax, 0, sho_z - 0.02)); ua = 0.17 * H_; fa = 0.15 * H_
        ep = empty(f"elbow{side}_{name}", (ax, 0, sho_z - 0.02 - ua))
        _pin([capsule((ax, 0, sho_z - 0.02 - ua / 2), arm_r, ua - 2 * arm_r, top)], sp)
        _pin([capsule((ax, 0, sho_z - 0.02 - ua - fa / 2), arm_r * 0.9, fa - 2 * arm_r, sk if style == "kid" else top),
              sphere((ax, 0, sho_z - 0.02 - ua - fa - 0.01), arm_r * 1.25, sk)], ep)          # forearm, hand
        ep.parent = sp; ep.location = Vector(ep.location) - Vector(sp.location)
        lx = sx * 0.045 * H_ ** 0.5; th = hip_z * 0.5; shn = hip_z * 0.5 - 0.03
        lp = empty(f"leg{side}_{name}", (lx, 0, hip_z)); kp = empty(f"knee{side}_{name}", (lx, 0, hip_z - th))
        _pin([capsule((lx, 0, hip_z - th / 2), leg_r, th - leg_r, low)], lp)
        shoe = capsule((lx, -0.025, 0.022), 0.024, 0.05, sh); shoe.rotation_euler = (math.pi / 2, 0, 0)   # lying along the foot
        _pin([capsule((lx, 0, hip_z - th - shn / 2), leg_r * 0.85, shn - leg_r, low), shoe], kp)
        kp.parent = lp; kp.location = Vector(kp.location) - Vector(lp.location)
        joints.update({side: sp, "E" + side: ep, "L" + side: lp, "K" + side: kp})
    root = empty("root_" + name)
    for o in torso + [head, joints["L"], joints["R"], joints["LL"], joints["LR"]]:
        if o.parent is None: o.parent = root
    root.location = loc; root.rotation_euler[2] = rot; root.scale = (h, h, h)
    if style == "old": head.rotation_euler[0] = 0.12; root.rotation_euler[0] = 0.05      # a little stooped
    return {"root": root, "head": head, "L": joints["L"], "R": joints["R"], "LL": joints["LL"], "LR": joints["LR"],
            "LE": joints["EL"], "RE": joints["ER"], "LK": joints["KL"], "RK": joints["KR"], "cheek": cheek,
            "base": Vector(loc), "hand_z": sho_z - 0.02 - 0.32 * H_, "arm_x": 0.11 * H_ ** 0.5, "hip_z": hip_z, **TALK}


QDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "characters", "quaternius")
PEOPLE = sorted(f[:-6] for f in os.listdir(QDIR) if f.endswith(".blend")) if os.path.isdir(QDIR) else []


HAIR_MATS = {"W_Formal": ("Red",), "W_Worker": ("DarkBrown",), "W_Adventurer": ("Hair_Brown",),
             "M_Farmer": ("Eyebrows",), "M_Worker": ("Eyebrows", "Moustache")}   # the material that is hair, where it is not named so


def person(name, loc=(0, 0, 0), rot=0.0, h=0.55, action="Idle", speed=1.0, offset=0.0, age="adult", hair=None):
    """A Quaternius person (see PEOPLE, e.g. "W_Casual", "M_Suit") standing at loc, facing -y like the other models.
    h scales the 1.8 m model to the sets' size (0.55 gives an adult about 1 unit tall, like clay()). action is one of the
    model's own clips (Idle, Walk, Run, Wave, Interact, ...); speed and offset (seconds) keep two people out of step.
    age: "adult" | "kid" (smaller, bigger head, quicker) | "old" (white hair, a stoop, slower). hair: an RGB to recolour.
    The stoop shows best from the side or three-quarter view; straight on, an old person mostly reads as shorter.
    Returns {root, arm, base, clips}; change the clip later with play()."""
    with bpy.data.libraries.load(os.path.join(QDIR, name + ".blend"), link=False) as (src, dst):
        dst.objects = list(src.objects); dst.actions = [a for a in src.actions if a not in bpy.data.actions]
    arm = None
    for o in dst.objects:
        bpy.context.scene.collection.objects.link(o)
        weapon = any(w in o.name for w in ("Pistol", "Sword", "Gun", "Knife"))   # the packs ship props for games: never shown
        o.hide_render = o.hide_viewport = weapon
        if o.type == "ARMATURE": arm = o
    if age == "kid": h *= 0.66; speed *= 1.15; arm.pose.bones["Head"].scale = (1.45, 1.45, 1.45)   # scale is never keyed
    if age == "old": speed *= 0.8; hair = hair or (0.86, 0.86, 0.88)
    if hair:
        for o in dst.objects:
            if o.type != "MESH": continue
            for i, m in enumerate(o.data.materials):
                if m and m.name.split(".")[0] in HAIR_MATS.get(name, ("Hair", "Hair_Brown", "Hair_Blond", "Eyebrows", "Moustache")):
                    m = o.data.materials[i] = m.copy(); bsdf(m).inputs["Base Color"].default_value = (*hair, 1)
    arm.location = loc; arm.rotation_euler[2] = rot; arm.scale = (h, h, h)               # the models already face -y
    d = {"root": arm, "arm": arm, "base": Vector(loc), "clips": sorted(a.name.split(".")[0] for a in dst.actions), "age": age}
    play(d, action, speed, offset)
    return d


POSES = {   # one-frame offsets layered on top of any clip: a number bends the bone (radians), a tuple moves it
    "stoop": (("Abdomen", 0.22), ("Chest", 0.16), ("Neck", 0.2)),
    # sit: the legs are IK (feet and knee targets drive them), so move the hips down and back and the feet forward;
    # offsets are metres in the 1.8 m model's own space (x right, y back, z up), sized for chair() at h=0.55
    "sit": (("Body", (0, 0.12, -0.38)), ("Foot.L", (0, -0.32, 0)), ("Foot.R", (0, -0.32, 0)),
            ("PT.L", (0, -0.6, 0.1)), ("PT.R", (0, -0.6, 0.1))),
}


def _pose_action(arm, name):
    """The POSES[name] offsets as a one-frame action, keyed on arm and then detached (made once per scene)."""
    act = bpy.data.actions.get("pose_" + name)
    if act: return act
    ad = arm.animation_data or arm.animation_data_create(); act = bpy.data.actions.new("pose_" + name); ad.action = act
    for bone, v in POSES[name]:
        pb = arm.pose.bones[bone]
        if isinstance(v, tuple):                               # a move in model space, turned into the bone's own axes
            pb.location = pb.bone.matrix_local.to_3x3().inverted() @ Vector(v); pb.keyframe_insert("location", frame=0)
        else:                                                  # a bend (radians) about the bone's own x axis
            pb.rotation_mode = "QUATERNION"; pb.rotation_quaternion = Quaternion((1, 0, 0), v)
            pb.keyframe_insert("rotation_quaternion", frame=0)
    ad.action = None
    return act


def pose(d, name, seat=0.32):
    """Add a held pose layer ("sit", "stoop") to a person; it combines with whatever clip play() gives them.
    sit: seat is the seat height (chair() is 0.32); smaller people are lifted so they sit on it, not in it."""
    if name == "sit": d["root"].location.z = d["base"].z = seat - 0.58 * d["root"].scale.z   # 0.58: the sit pose's seat in model metres
    d.setdefault("layers", [])
    if name not in d["layers"]: d["layers"].append(name)
    play(d, d.get("clip", "Idle"), d.get("speed", 1.0), d.get("offset", 0.0))


def play(d, action, speed=1.0, offset=0.0):
    """Loop one of the person's clips from shot time 0 (anim.py moves the scene clock for every frame it renders)."""
    act = bpy.data.actions.get(action) or next(a for a in bpy.data.actions if a.name.split(".")[0] == action)
    ad = d["arm"].animation_data or d["arm"].animation_data_create(); ad.action = None
    for tr in list(ad.nla_tracks): ad.nla_tracks.remove(tr)
    fs, fe = act.frame_range
    st = ad.nla_tracks.new().strips.new(action, int(-offset * 24 * speed), act)
    st.scale = 1.0 / speed; st.repeat = 200; st.extrapolation = "HOLD"
    d["clip"], d["speed"], d["offset"] = action, speed, offset
    for name in (["stoop"] if d.get("age") == "old" else []) + d.get("layers", []):   # pose layers above the clip, combined
        s2 = ad.nla_tracks.new().strips.new(name, 0, _pose_action(d["arm"], name)); s2.blend_type = "COMBINE"
        s2.action_frame_start, s2.action_frame_end = 0, 1; s2.repeat = 100000; s2.extrapolation = "HOLD_FORWARD"   # a 1-frame strip, held for the whole shot


def dog(loc, rot=0.0, col=(0.96, 0.92, 0.84)):
    """A blocky dog sitting up: box body, head with floppy ears, a wagging tail. Returns {root, head, tail}."""
    m = mat("dogfur", col, 0.85, sheen=0.5, noise=0.25); dk = mat("dogdark", (0.35, 0.22, 0.12), 0.8)
    blk = mat("dogeye", (0.02, 0.02, 0.02), 0.15, coat=0.8); wht = mat("dogwht", (1, 1, 1), 0.2)
    P = [cube((0, 0.05, 0.16), (0.2, 0.32, 0.2), m, bevel=0.04), cube((0, -0.06, 0.3), (0.18, 0.16, 0.22), m, bevel=0.04)]
    for sx in (-1, 1): P.append(cube((sx * 0.06, -0.12, 0.05), (0.06, 0.08, 0.1), m, bevel=0.02))
    head = empty("doghead", (0, -0.08, 0.42))
    H = [cube((0, -0.1, 0.48), (0.2, 0.18, 0.17), m, bevel=0.05), cube((0, -0.21, 0.45), (0.1, 0.08, 0.08), m, bevel=0.03),
         sphere((0, -0.255, 0.47), 0.022, blk)]
    for sx in (-1, 1):
        H += [sphere((sx * 0.05, -0.19, 0.52), 0.022, blk), sphere((sx * 0.05 + 0.006, -0.205, 0.528), 0.007, wht),
              cube((sx * 0.11, -0.08, 0.46), (0.04, 0.08, 0.14), dk, rot=(0, sx * 0.2, 0), bevel=0.015)]
    _pin(H, head)
    tail = empty("dogtail", (0, 0.2, 0.18)); _pin([cube((0, 0.28, 0.24), (0.04, 0.04, 0.16), m, rot=(0.6, 0, 0), bevel=0.015)], tail)
    root = empty("dogroot")
    for o in P + [head, tail]:
        if o.parent is None: o.parent = root
    root.location = loc; root.rotation_euler[2] = rot
    return {"root": root, "head": head, "tail": tail}


def _talk(H, m0, talk):
    """Remember a head's mouth parts (H[m0:]) and add the hidden open mouth say() uses."""
    H.append(talk)
    return {"mouth": [(o, tuple(o.scale)) for o in H[m0:-1]], "talk": talk}


def say(d, t, words):
    """Lip flap: d's mouth opens and closes about once per syllable during each spoken word.
    words = [(start, end), ...] in shot seconds, e.g. from words.json minus the shot's start. Clay characters only for now.
    shortcut: syllables are guessed from word length (0.16 s each), not phonemes; upgrade if close-ups need real visemes."""
    o = 0.0
    for a, b in words:
        if a <= t <= b:
            n = max(1, round((b - a) / 0.16)); o = abs(math.sin(math.pi * n * (t - a) / max(b - a, 0.05)))
    d["talk"].scale.z = 0.001 + 0.8 * o
    d["talk"].scale.x = 0.8 + 0.2 * o
    for m, sc in d["mouth"]: m.scale = (0.001,) * 3 if o > 0.15 else sc


def spans(words, t0, t1, shot_start):
    """Word spans from a words.json list between global times t0 and t1, shifted into shot time."""
    return [(a - shot_start, b - shot_start) for _, a, b in words if t0 <= a < t1]


# ---------------------------------------------------------------- life: automatic blinks and glances for every character
EYE_MATS = {"beye", "beaneye", "clayeye", "dogeye", "eyeblk", "hueye"}                       # pupils (move on a glance)
LID_MATS = EYE_MATS | {"beyew", "beanwht", "claywht", "clay_claywht", "dogwht", "eyewht", "huwht"}          # everything that closes on a blink
_LIFE = {}


def _life_index():
    """Group eye parts by their head (parent) once per shot."""
    groups = {}
    for o in bpy.data.objects:
        if o.type != "MESH" or not o.material_slots or o.parent is None: continue
        mname = (o.material_slots[0].material.name if o.material_slots[0].material else "").split(".")[0]
        if mname not in LID_MATS: continue
        g = groups.setdefault(o.parent.name, {"white": [], "black": []})
        g["black" if mname in EYE_MATS else "white"].append(o)
    heads = {}
    for name, g in groups.items():
        if not g["white"]: continue
        h = heads.setdefault(name, {"parts": [(o, o.scale.z) for o in g["white"]], "pupils": []})
        for o in g["black"]:                                   # a pupil sits right by an eye white; brows and mouths do not
            d = min((Vector(o.location) - Vector(w.location)).length for w in g["white"])
            if d < 0.8 * max(o.dimensions):
                h["parts"].append((o, o.scale.z)); h["pupils"].append((o, Vector(o.location), max(o.dimensions.x, 0.004)))
    return heads


def animate_all(t):
    """Called by anim.py after every update(t): each head blinks every 2.5 to 5 s and glances left or right now and then."""
    key = id(bpy.context.scene), bpy.data.objects.__len__()
    if _LIFE.get("key") != key: _LIFE["key"] = key; _LIFE["heads"] = _life_index()
    for name, h in _LIFE["heads"].items():
        seed = sum(ord(c) for c in name)
        period = 2.5 + (seed % 25) / 10.0; ph = (t + seed * 0.37) % period
        close = 1.0 - max(0.0, 1.0 - abs(ph - 0.08) / 0.08) * 0.9                    # a 0.16 s blink
        for o, z in h["parts"]: o.scale.z = z * close
        g = math.sin((t + seed) * 0.6) ; look = (1 if g > 0.55 else -1 if g < -0.55 else 0)
        for o, base, w in h["pupils"]:
            o.location = base + Vector((0.22 * w * look, 0, 0))
    _weight(t)


# ---------------------------------------------------------------- weight: lean into moves, head trails a beat behind
def _add(obj, axis, key, off):
    """Add off to obj.rotation_euler[axis] on top of whatever the shot set this frame (never accumulates)."""
    st = _LIFE.setdefault("applied", {}); k = (obj.name, axis, key); cur = obj.rotation_euler[axis]
    last_val, last_off = st.get(k, (None, 0.0))
    base = cur - last_off if last_val is not None and abs(cur - last_val) < 1e-6 else cur   # the shot rewrote it: new base
    obj.rotation_euler[axis] = base + off; st[k] = (base + off, off)


def _weight(t):
    """Each character root: smoothed world velocity -> body lean toward the move; head lag = fast minus slow velocity,
    so the head tips back when a move starts and nods forward when it stops."""
    W = _LIFE.setdefault("w", {})
    for name in _LIFE["heads"]:
        head = bpy.data.objects.get(name)
        if head is None or head.parent is None: continue
        root = head.parent                                   # every character model parents its head straight to its root
        pos = root.location.copy()                           # in the parent's space: riding in a moving car is not a lean
        s = W.get(root.name)
        dt = t - s["t"] if s else 0.0
        if not s or dt <= 0 or dt > 0.5:                      # first frame, a resumed render or a jump in time: start at rest
            s = W[root.name] = {"t": t, "p": pos, "f": Vector((0, 0, 0)), "s": Vector((0, 0, 0))}; continue
        v = (pos - s["p"]) / dt
        if v.length > 5: v = Vector((0, 0, 0))                 # the shot teleported the character: no lean for that
        s["f"] += (v - s["f"]) * min(1.0, dt / 0.12); s["s"] += (v - s["s"]) * min(1.0, dt / 0.35)
        s["t"], s["p"] = t, pos
        rz = root.rotation_euler[2]; c, sn = math.cos(-rz), math.sin(-rz)
        loc_v = lambda w: (w.x * c - w.y * sn, w.x * sn + w.y * c)     # world velocity -> the root's own x, y
        fx, fy = loc_v(s["f"]); lx, ly = loc_v(s["f"] - s["s"])
        clamp = lambda a, m: max(-m, min(m, a))
        _add(root, 0, "lean", clamp(-0.18 * fy, 0.12)); _add(root, 1, "lean", clamp(0.18 * fx, 0.12))
        _add(head, 0, "lag", clamp(0.5 * ly, 0.15)); _add(head, 1, "lag", clamp(-0.5 * lx, 0.15))


def _selfcheck():
    """Assert-based check of the math pieces that need no Blender scene."""
    assert spans([["Not", 18.54, 18.8], ["x", 30, 31]], 18, 22, 14.72) == [(18.54 - 14.72, 18.8 - 14.72)]
    a = Vector((0, -1.0, 0)); c, sn = math.cos(0), math.sin(0)
    assert (a.x * c - a.y * sn, a.x * sn + a.y * c) == (0.0, -1.0)
    assert max(-0.12, min(0.12, -0.18 * -1.0)) == 0.12          # moving toward -y leans the top toward -y (positive x rotation)
