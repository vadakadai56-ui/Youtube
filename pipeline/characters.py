"""Dustlight character library. There is no house model: every video picks the design that fits it (channel/formats.md,
"Character model"). Each builder returns the same handles as world.peg() so walk(), breathe() and shot code work unchanged:
{root, head, L, R, cheek, base} plus legs {LL, LR} where the model has legs.

Models
- blocky(): chunky block people (bevelled box head, box torso, hinged block limbs, mitten hands). Comedy, trend, game-like Shorts.
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
