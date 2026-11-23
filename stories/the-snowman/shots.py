"""The Snowman Nobody Builds (emotional twist, 1 Dec 2026): every December 1st a snowman appears outside Mrs Kowalski's
window. At 4 a.m. Ava sees Danny the bin man build it: her late husband built one for him when he was a kid with no dad.
Cast (Quaternius people, channel/characters.md): Ava (kid, narrator), Oscar (her brother), Danny (bin man), Mrs Kowalski,
Mr Kowalski (flashback). Night street, toon look without outlines, warm windows against blue snow.
Render: STYLE=toon TOON_STEP=0.03 TOON_LINES=0 ENGINE=EEVEE PCT=50 ES=8 $VENV/bin/python pipeline/anim.py stories/the-snowman OUT all"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
os.environ.setdefault("STYLE", "toon")
import scene                  # noqa
scene.STYLE = os.environ["STYLE"]
from world import *           # noqa
from world import cam as _cam
from characters import person, play, pose
import bpy
scene.LOOK = os.environ.get("LOOK") or "story"

_D = json.load(open(os.path.join(HERE, "durations.json")))
AVA, OSCAR = ("W_Adventurer", "kid"), ("M_Casual_Hoodie", "kid")
DANNY, MRSK, MRK = ("M_Worker", "adult"), ("W_Formal", "old"), ("M_Suit", "adult")
POST = ("M_Casual_2", "adult")
FAST = {"s9", "s10", "s15", "s17"}                       # jumping down, building, the two waves: 30 fps
CALM = {"s3", "s7", "s14"}
SNOWMAN = Vector((1.15, 0.4, 0))                          # in Mrs Kowalski's front garden, under her window
WINDOW = Vector((1.62, 0.4, 1.0))                         # her front window (the facade is the plane x = 1.6)


def who(c, loc, rot=0.0, action="Idle", offset=0.0):
    return person(c[0], loc, rot=rot, age=c[1], action=action, offset=offset)


def street_night(rng, dawn=False, lit=True):
    """The road (along y), Mrs Kowalski's house on the right with a lit front window, Ava's house across the road, lamps, snow."""
    snow = mat("ssnow", (0.86, 0.9, 0.98), 0.7, noise=0.15)
    cube((0, 0, -0.05), (40, 40, 0.1), snow); cube((0, 0, 0.003), (2.0, 40, 0.006), mat("sroad", (0.45, 0.48, 0.55), 0.8, noise=0.3))
    wall = mat("kwall2", (0.72, 0.5, 0.42), 0.8, noise=0.2); trim = mat("ktrim", (0.95, 0.95, 0.92), 0.6)
    # her facade (x = 1.6), with a window hole at y 0.1..0.7, z 0.7..1.3 and a door at y -0.9
    for y0, y1, z0, z1 in ((-3, 0.1, 0, 2.4), (0.7, 3, 0, 2.4), (0.1, 0.7, 0, 0.7), (0.1, 0.7, 1.3, 2.4)):
        cube((1.65, (y0 + y1) / 2, (z0 + z1) / 2), (0.1, y1 - y0, z1 - z0), wall)
    cube((1.6, 0.4, 0.68), (0.14, 0.7, 0.05), trim); cube((1.6, -0.9, 0.5), (0.04, 0.45, 1.0), mat("kdoor", (0.25, 0.35, 0.3), 0.6))
    cube((2.5, 0.4, 2.6), (1.9, 6.2, 0.4), mat("kroof", (0.95, 0.96, 1.0), 0.7))
    room = mat("kroom", (1.0, 0.82, 0.6), 0.8, emit=(1.0, 0.78, 0.5), emit_str=1.4 if lit else 0.1)
    cube((3.2, 0.4, 1.2), (0.1, 3, 2.4), room); cube((2.4, 1.9, 1.2), (1.6, 0.1, 2.4), room); cube((2.4, -1.1, 1.2), (1.6, 0.1, 2.4), room)
    if lit: light("POINT", (2.5, 0.4, 1.4), 30, col=(1.0, 0.75, 0.45), size=0.3)
    # Ava's house across the road, with her upstairs window
    cube((-2.6, 0.0, 1.4), (1.9, 6.0, 2.8), mat("awall", (0.45, 0.55, 0.7), 0.8, noise=0.2))
    cube((-1.64, 0.4, 1.9), (0.02, 0.5, 0.45), mat("awin", (1, 0.85, 0.6), 0.5, emit=(1, 0.8, 0.5), emit_str=2.5 if lit else 0.3))
    for y in (-3.0, 4.0):
        cyl((1.25, y, 1.0), 0.035, 2.0, mat("lampm", (0.08, 0.08, 0.09), 0.4, metal=0.8))
        sphere((1.25, y, 2.05), 0.1, mat("lampglow", (1, 0.85, 0.6), 0.2, emit=(1, 0.78, 0.45), emit_str=14))
        light("POINT", (1.2, y, 1.9), 35, col=(1.0, 0.72, 0.42), size=0.15)
    if dawn:
        world_color((0.45, 0.5, 0.65)); light("SUN", (0, 0, 5), 1.2, col=(1.0, 0.85, 0.75), rot=(1.1, 0.2, -0.6))
    else:
        world_color((0.05, 0.07, 0.15)); light("SUN", (0, 0, 5), 0.5, col=(0.55, 0.65, 1.0), rot=(0.9, 0.2, 0.4))
        bpy.context.scene["exposure"] = -1.3                              # night (scene.render applies it after the toon look)
    light("AREA", (-0.8, -1.5, 2.0), 40, col=(0.75, 0.82, 1.0), size=3, target=(1.0, 0.4, 0.7))      # moonlight on the garden
    return Snow((0.5, 0.4, 0.3), size=(5, 6, 3), n=260, rng=rng)


def snowman(parts=3, scarf=True, loc=SNOWMAN):
    """Three snowballs, coal eyes, a carrot nose and the red scarf. Returns the balls (bottom first) and the scarf."""
    sm = mat("snowball", (0.96, 0.97, 1.0), 0.6); out = []
    for i, (r, z) in enumerate(((0.22, 0.2), (0.16, 0.52), (0.11, 0.76))[:parts]):
        out.append(sphere(loc + Vector((0, 0, z)), r, sm))
    sc = None
    if scarf:
        sc = torus(loc + Vector((0, 0, 0.66)), 0.12, 0.035, mat("redscarf", (0.85, 0.12, 0.12), 0.8))
        cube(loc + Vector((-0.07, -0.08, 0.55)), (0.06, 0.03, 0.2), mat("redscarf", (0.85, 0.12, 0.12), 0.8)).parent = sc
    if parts == 3:
        coal = mat("coal", (0.05, 0.05, 0.05), 0.6)
        for dy in (-0.04, 0.04): sphere(loc + Vector((-0.1, dy, 0.8)), 0.014, coal)
        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.018, depth=0.09, location=loc + Vector((-0.14, 0, 0.76)), rotation=(0, -math.pi / 2, 0))
        bpy.context.object.data.materials.append(mat("carrot", (0.95, 0.45, 0.1), 0.6))
    return out, sc


def lorry(loc, rot=0.0):
    """The council bin lorry: green body, white cab, black wheels, one orange beacon. Returns its root empty."""
    root = empty("lorry", loc); body = mat("lorrybody", (0.2, 0.45, 0.28), 0.5); cab = mat("lorrycab", (0.92, 0.93, 0.9), 0.4)
    P = [cube((0, 0.55, 0.85), (1.05, 2.0, 1.5), body, bevel=0.03),
         cube((0, -0.85, 0.45), (1.0, 0.8, 0.5), cab, bevel=0.03), cube((0, -0.85, 1.45), (1.0, 0.8, 0.1), cab, bevel=0.02),   # an open
         sphere((0, -0.85, 1.55), 0.06, mat("beacon", (1, 0.55, 0.1), 0.3, emit=(1, 0.5, 0.1), emit_str=12))]                     # window band
    for x in (-0.47, 0.47):
        for y in (-1.22, -0.48): P.append(cube((x, y, 1.05), (0.06, 0.06, 0.7), cab))
    for y in (-0.85, 0.2, 1.1):
        for x in (-0.5, 0.5): P.append(cyl((x, y, 0.17), 0.17, 0.1, mat("tyre", (0.05, 0.05, 0.06), 0.8), rot=(0, math.pi / 2, 0)))
    for p in P: p.parent = root; p.location = p.location
    root.rotation_euler[2] = rot
    return root


# ---------------------------------------------------------------- shots
def s1(rng):            # Every December first, a snowman appears outside Mrs Kowalski's window.: dawn, the snowman, her at the window
    sn = street_night(rng, dawn=True); snowman(); k = who(MRSK, (1.9, 0.4, 0.3), rot=math.pi / 2)
    c = _cam((-0.6, -1.6, 1.0), (1.3, 0.4, 0.75), lens=32, fstop=5)
    def upd(t): sn.update(t * 0.5); c.location.x = -0.6 + 0.25 * smooth(t / 5.4)
    return upd


def s2(rng):            # Nobody has ever seen who builds it.: neighbours on doorsteps, peering at it
    sn = street_night(rng, dawn=True); snowman()
    a = who(POST, (-0.75, -0.3, 0), rot=-math.pi / 2 - 0.3); b = who(OSCAR, (-0.55, 0.6, 0), rot=-math.pi / 2 + 0.2)
    c = _cam((0.0, -3.3, 1.0), (0.15, 0.3, 0.6), lens=26, fstop=6)
    def upd(t):
        sn.update(t * 0.5); a["root"].rotation_euler[1] = 0.1 * math.sin(t * 2); b["root"].location.x = -0.55 + 0.05 * math.sin(t * 3)   # craning
    return upd


def s3(rng):            # Twelve years. Same spot. Same red scarf.: close on the scarf, snow drifting past
    sn = street_night(rng, dawn=True); snowman()
    c = _cam((0.55, 0.05, 0.75), SNOWMAN + Vector((0, 0, 0.66)), lens=40, fstop=4)
    def upd(t):
        sn.update(t * 0.4); a = 0.25 * t / 4.1                                  # a slow arc round the scarf
        c.location = SNOWMAN + Vector((-0.85 * math.cos(a), -0.45 + 0.85 * math.sin(a), 0.78)); look_at(c, SNOWMAN + Vector((0, 0, 0.66)))
    return upd


def s4(rng):            # The neighbours have theories. The postman. A ghost. Mrs Kowalski herself.: each suspect appears by the snowman
    sn = street_night(rng, dawn=True); snowman()
    p = who(POST, (0.8, 0.0, 0), rot=-0.6, action="Interact")
    gm = mat("ghost", (0.95, 0.97, 1.0), 0.5, emit=(0.8, 0.9, 1.0), emit_str=0.6)
    ghost = [sphere((0.8, 0.0, 0.85), 0.16, gm)]; bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=0.28, depth=0.8, location=(0.8, 0.0, 0.45))
    ghost.append(bpy.context.object); ghost[-1].data.materials.append(gm)
    for ey in (-0.05, 0.05): ghost.append(sphere((0.66, ey, 0.88), 0.025, mat("ghosteye", (0.05, 0.05, 0.08), 0.5)))
    k = who(MRSK, (0.8, 0.0, 0), rot=-0.6, action="Interact")
    c = _cam((-0.6, -1.4, 0.85), (0.95, 0.25, 0.55), lens=34, fstop=4)
    t_g, t_k = 2.8, 3.9                                                         # "A ghost." and "Mrs Kowalski herself." (shot time)
    def upd(t):
        sn.update(t * 0.5)
        p["root"].hide_render = not (1.76 < t < t_g)
        for o in ghost: o.hide_render = not (t_g <= t < t_k); o.location.z = o.location.z if t < t_g else o.location.z
        k["root"].hide_render = not (t >= t_k)
        for o in p["root"].children_recursive: o.hide_render = p["root"].hide_render
        for o in k["root"].children_recursive: o.hide_render = k["root"].hide_render
    return upd


def s5(rng):            # My brother Oscar set up a camera.: Oscar at Ava's window with a little camera on a tripod
    sn = street_night(rng); o = who(OSCAR, (-1.25, 0.15, 0), rot=-math.pi / 2, action="Interact")
    cm = mat("camblk", (0.08, 0.08, 0.09), 0.4)
    camb = cube((-1.05, 0.45, 0.62), (0.1, 0.07, 0.06), cm)
    for a in (0, 2.1, 4.2): cyl((-1.05 + 0.08 * math.cos(a), 0.45 + 0.08 * math.sin(a), 0.3), 0.008, 0.62, cm, rot=(0.25 * math.sin(a), -0.25 * math.cos(a), 0))
    c = _cam((-0.2, -0.5, 0.85), (-1.1, 0.35, 0.6), lens=36, fstop=2.8)
    def upd(t): sn.update(t)
    return upd


def s6(rng):            # By morning, snow had covered the lens.: through the camera, the view whiting out
    sn = street_night(rng); snowman()
    c = _cam((-1.0, 0.45, 0.62), (1.15, 0.4, 0.6), lens=34, fstop=6)
    lens_snow = cube((0, 0, 0), (0.2, 0.002, 0.35), mat("lenssnow", (0.95, 0.96, 1.0), 0.6, alpha=0.0))
    lens_snow.parent = c; lens_snow.location = (0, 0, -0.1); lens_snow.rotation_euler = (math.pi / 2, 0, 0)
    m = lens_snow.data.materials[0]
    def upd(t):
        sn.update(t); bsdf(m).inputs["Alpha"].default_value = min(1.0, 0.15 + 0.85 * smooth((t - 0.4) / 2.2))
    return upd


def s7(rng):            # So this year... I didn't sleep.: Ava's dark bedroom, her at the window, the clock at 3:59
    cube((0, 0, -0.05), (6, 6, 0.1), mat("bfloor", (0.35, 0.28, 0.25), 0.7)); w = mat("bwall", (0.35, 0.4, 0.6), 0.8)
    for y0, y1, z0, z1 in ((-3, -0.35, 0, 2.4), (0.35, 3, 0, 2.4), (-0.35, 0.35, 0, 0.8), (-0.35, 0.35, 1.5, 2.4)):
        cube((1.0, (y0 + y1) / 2, (z0 + z1) / 2), (0.1, y1 - y0, z1 - z0), w)          # the wall with her window
    cube((1.2, 0, 1.15), (0.02, 0.7, 0.7), mat("bnight", (0.05, 0.08, 0.2), 0.5, emit=(0.08, 0.12, 0.3), emit_str=1.5))
    cube((0.95, 0, 0.78), (0.2, 0.8, 0.04), mat("sill", (0.9, 0.9, 0.88), 0.6))
    cube((0.3, 0.75, 0.25), (0.3, 0.3, 0.5), mat("bside", (0.5, 0.35, 0.22), 0.6))
    text("3:59", (0.3, 0.6, 0.55), 0.06, mat("clockled", (1, 0.25, 0.2), 0.3, emit=(1, 0.2, 0.15), emit_str=6), rot=(math.pi / 2, 0, 0))
    a = who(AVA, (0.72, 0.0, 0), rot=-math.pi / 2)                                     # facing the window (+x)
    world_color((0.02, 0.02, 0.05)); light("AREA", (1.15, 0, 1.2), 25, col=(0.6, 0.7, 1.0), size=0.6, target=(0.5, 0, 0.8))   # cold window light
    light("POINT", (0.3, 0.6, 0.7), 3, col=(1, 0.3, 0.2), size=0.05)
    c = _cam((-0.45, -0.75, 0.85), (0.75, 0.05, 0.7), lens=34, fstop=2.8)
    def upd(t): c.location.x = -0.45 + 0.04 * t
    return upd


def s8(rng):            # At four a.m., the bin lorry stopped outside her house.: the lorry rolls up and stops, beacon turning
    sn = street_night(rng); snowman(); L = lorry((0.3, -6.0, 0))
    c = _cam((-0.9, 2.6, 1.3), (0.5, -0.5, 0.7), lens=30, fstop=5)
    def upd(t): sn.update(t); L.location.y = -6.0 + 6.2 * smooth(t / 2.6)
    return upd


def s9(rng):            # Danny the bin man jumped down.: from the cab, a hop into the snow
    sn = street_night(rng); snowman(); L = lorry((0.3, 0.2, 0)); d = who(DANNY, (0.95, -0.65, 0.7), rot=math.pi / 2)
    c = _cam((1.0, -2.6, 0.8), (0.9, -0.6, 0.6), lens=34, fstop=3.5)
    def upd(t):
        sn.update(t); k = smooth((t - 0.4) / 0.35); d["root"].location = Vector((0.95 + 0.25 * k, -0.65, 0.7 * (1 - k) + 0.08 * math.sin(math.pi * k)))
    return upd


def s10(rng):           # Three balls of snow. One red scarf. Three minutes.: Danny builds it at speed, ball by ball
    sn = street_night(rng); L = lorry((0.3, 2.6, 0)); d = who(DANNY, (0.8, 0.0, 0), rot=-0.9, action="Interact")
    balls, sc = snowman()
    c = _cam((-0.4, -1.2, 0.85), (1.1, 0.35, 0.5), lens=32, fstop=4)
    times = (0.3, 0.9, 1.4)                                                    # each ball appears as he packs it
    def upd(t):
        sn.update(t)
        for b, t0 in zip(balls, times): b.scale = (smooth((t - t0) / 0.3) + 0.001,) * 3
        sc.scale = (smooth((t - 1.6) / 0.25) + 0.001,) * 3
    return upd


def s11(rng):           # Then he was gone.: the lorry pulls away, the snowman alone under the window
    sn = street_night(rng); snowman(); L = lorry((0.3, 0.2, 0))
    c = _cam((-0.7, -2.0, 1.0), (1.1, 0.4, 0.6), lens=30, fstop=5)
    def upd(t): sn.update(t); L.location.y = 0.2 + 5.0 * smooth(t / 1.6) ** 2
    return upd


def s12(rng):           # The next morning, I asked him why.: Ava and Danny by the bins at the kerb, morning
    sn = street_night(rng, dawn=True, lit=False); snowman()
    d = who(DANNY, (0.4, -0.5, 0), rot=-2.4); a = who(AVA, (0.0, -0.95, 0), rot=0.8, action="Interact")
    for x in (0.75, 0.95): cube((x, -0.9, 0.25), (0.18, 0.18, 0.5), mat("wheeliebin", (0.15, 0.3, 0.2), 0.6))
    c = _cam((-0.8, -2.0, 0.8), (0.25, -0.65, 0.55), lens=34, fstop=3.5)
    def upd(t): sn.update(t * 0.3)
    return upd


def s13(rng):           # "When I was eight, her husband built one for me. I was the kid whose dad never came home.": warm flashback
    sn = street_night(rng, dawn=True, lit=True); balls, sc = snowman()
    mk = who(MRK, (1.0, -0.15, 0), rot=-0.4, action="Interact"); yd = person("M_Casual_Hoodie", (0.72, 0.3, 0), rot=-1.2, age="kid", action="Wave", hair=(0.85, 0.65, 0.3))   # young Danny, blond
    bpy.context.scene["exposure"] = 0.3                                         # memories run warm and bright
    c = _cam((-0.7, -1.1, 0.85), (0.9, 0.45, 0.5), lens=32, fstop=4)
    def upd(t):
        sn.update(t * 0.4); c.location.x = -0.5 + 0.08 * t
        for b, t0 in zip(balls, (0.3, 1.5, 2.6)): b.scale = (smooth((t - t0) / 0.6) + 0.001,) * 3
        sc.scale = (smooth((t - 4.2) / 0.5) + 0.001,) * 3
    return upd


def s14(rng):           # "He made me promise. One every year. For her.": Danny now, at night, in the cab, looking at the window
    sn = street_night(rng); L = lorry((0.3, 0.2, 0)); d = who(DANNY, (0.3, -0.75, 0)); pose(d, "sit", seat=0.62)
    c = _cam((0.05, -1.75, 1.05), (0.3, -0.75, 1.0), lens=44, fstop=2.4)
    def upd(t): sn.update(t); c.location.y = -1.75 + 0.05 * t
    return upd


def s15(rng):           # At the window, Mrs Kowalski waved.: from the lorry, her in the warm window, a small wave
    sn = street_night(rng); snowman(); k = who(MRSK, (1.9, 0.4, 0.3), rot=math.pi / 2, action="Wave")
    c = _cam((0.4, -0.3, 1.15), (1.85, 0.4, 1.0), lens=44, fstop=3)
    def upd(t): sn.update(t)
    return upd


def s16(rng):           # And Danny, in the bin lorry...: wide, the lorry idling beside her window, beacon turning
    sn = street_night(rng); snowman(); L = lorry((0.3, 0.2, 0)); k = who(MRSK, (1.9, 0.4, 0.3), rot=math.pi / 2)
    c = _cam((-1.0, -3.2, 1.6), (0.8, 0.3, 0.8), lens=30, fstop=6)
    def upd(t): sn.update(t)
    return upd


def s17(rng):           # waved back. Who would you build one for?: Danny waves from the cab, the lorry pulls away
    sn = street_night(rng); snowman(); L = lorry((0.3, 0.2, 0)); d = who(DANNY, (0.3, -0.75, 0), rot=math.pi / 2, action="Wave"); pose(d, "sit", seat=0.62)
    c = _cam((1.15, -1.8, 1.05), (0.4, -0.7, 1.0), lens=38, fstop=4)
    def upd(t):
        sn.update(t); dy = 3.0 * smooth((t - 1.6) / 2.0) ** 2; L.location.y = 0.2 + dy; d["root"].location.y = -0.75 + dy
        look_at(c, Vector((0.4, -0.7 + dy, 1.0)))
    return upd


SHOTS = {n: (globals()[n], _D[n]) for n in _D}
