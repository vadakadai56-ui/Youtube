"""Remember November (meme story, 30 Nov 2026): since January Grandpa Stan has said the same six words, "Remember...
November 2026 is coming." On the last night of November he tears the last page off his countdown... "Remember... December."
Cast (Quaternius people, channel/characters.md): Grandpa Stan (old), Maya (kid, the narrator), Mum, Dad.
Render: STYLE=toon TOON_STEP=0.03 TOON_LINES=0 ENGINE=EEVEE PCT=50 ES=8 $VENV/bin/python pipeline/anim.py stories/remember-november OUT all"""
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
scene.LOOK = os.environ.get("LOOK") or "comedy"

_D = json.load(open(os.path.join(HERE, "durations.json")))
H = 0.42                                                       # kitchen() is built small: grown-ups about 0.76 tall
STAN, MAYA, MUM, DAD = ("M_Casual_2", "old", H), ("W_Adventurer", "kid", 0.55), ("W_Casual", "adult", H), ("M_Casual_Hoodie", "adult", H)
FAST = {"r3", "r4", "r6", "r10", "r11"}                        # quick gestures and the torn page: 30 fps
CALM = {"r8"}


def who(c, loc, rot=0.0, action="Idle", offset=0.0):
    return person(c[0], loc, rot=rot, age=c[1], h=c[2], action=action, offset=offset)


def fridge(rng, number="247", night=False):
    """Kitchen with a tall fridge on the left wall and Stan's tear-off countdown pad stuck on its door. Returns the pad's top page."""
    kitchen(rng)
    fm = mat("fridge", (0.93, 0.94, 0.95), 0.3, coat=0.4)
    cube((-1.45, 1.2, 0.85), (0.6, 0.55, 1.7), fm, bevel=0.03); cube((-1.45, 0.92, 1.25), (0.58, 0.01, 0.01), mat("fgap", (0.5, 0.5, 0.52), 0.5))
    cube((-1.2, 0.915, 0.95), (0.02, 0.02, 0.3), mat("fhandle", (0.7, 0.7, 0.72), 0.3, metal=0.8))
    pad = cube((-1.5, 0.92, 1.05), (0.3, 0.012, 0.36), mat("padback", (0.95, 0.95, 0.92), 0.8))
    cube((-1.5, 0.912, 1.24), (0.3, 0.02, 0.04), mat("padtop", (0.8, 0.15, 0.15), 0.6))
    page = cube((-1.5, 0.905, 1.03), (0.29, 0.004, 0.33), mat("page", (1, 1, 0.97), 0.8))
    text(number, (-1.5, 0.899, 1.02), 0.13, mat("pageink", (0.85, 0.1, 0.1), 0.6), rot=(math.pi / 2, 0, 0)).parent = page
    text("DAY" if number == "1" else "DAYS", (-1.5, 0.899, 0.92), 0.045, mat("pageink2", (0.2, 0.2, 0.25), 0.6), rot=(math.pi / 2, 0, 0)).parent = page
    for ch in page.children: ch.location = ch.location - page.location
    if night:
        world_color((0.03, 0.03, 0.06))
        for l in bpy.data.lights: l.energy *= 0.2
        win = bpy.data.materials["morning"]; bsdf(win).inputs["Emission Color"].default_value = (0.05, 0.07, 0.2, 1)   # night outside
        bpy.context.scene["exposure"] = -1.6                              # it is night: scene.render applies this after the toon look
        bsdf(win).inputs["Emission Strength"].default_value = 0.6; bsdf(win).inputs["Base Color"].default_value = (0.04, 0.05, 0.12, 1)
        light("AREA", (-1.0, 0.2, 1.1), 35, col=(0.75, 0.85, 1.0), size=0.6, target=(-1.5, 0.9, 1.0))   # the fridge's cold glow
    return page


# ---------------------------------------------------------------- shots
def r1(rng):            # Since January, Grandpa Stan has said the same six words.: breakfast, the family at the table, push in on Stan
    kitchen(rng); s = who(STAN, (0, 1.0, 0)); pose(s, "sit", seat=0.25)
    m = who(MAYA, (-0.55, 0.45, 0), rot=-math.pi / 2); pose(m, "sit", seat=0.25)
    u = who(MUM, (0.6, 0.5, 0), rot=math.pi / 2); pose(u, "sit", seat=0.25)
    c = _cam((0.1, -1.4, 1.0), (0, 0.8, 0.55), lens=36, fstop=5)
    def upd(t): c.location.y = -1.4 + 0.25 * smooth(t / 4.6)
    return upd


def r2(rng):            # "Remember... November 2026 is coming.": close on Stan, dead serious
    kitchen(rng); s = who(STAN, (0, 1.0, 0)); pose(s, "sit", seat=0.25)
    c = _cam((0.05, 0.25, 0.62), (0, 1.0, 0.62), lens=48, fstop=5)
    def upd(t): c.location.y = 0.25 + 0.08 * t                                  # a slow, solemn push
    return upd


def r3(rng):            # At breakfast.: Stan leans across to Maya over her cereal
    kitchen(rng); s = who(STAN, (0.2, 0.95, 0), rot=0.5, action="Interact"); m = who(MAYA, (-0.3, 0.08, 0), rot=-0.6)
    bowl = cyl((-0.15, 0.55, 0.47), 0.06, 0.04, mat("bowl", (0.95, 0.85, 0.3), 0.4))
    c = _cam((-0.6, -0.4, 0.75), (-0.05, 0.75, 0.55), lens=36, fstop=3)
    def upd(t): pass
    return upd


def r4(rng):            # At my birthday.: a cake with candles, Maya in a party hat, Stan right behind her
    kitchen(rng); m = who(MAYA, (0, 0.2, 0)); s = who(STAN, (0.25, 0.0, 0), rot=-0.4, action="Interact")
    cyl((0, 0.55, 0.5), 0.12, 0.08, mat("cake", (0.95, 0.75, 0.8), 0.6))
    for k in range(5): candle((-0.06 + k * 0.03, 0.55, 0.54), h=0.05)
    hat = bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.035, depth=0.09); hat = bpy.context.object
    hat.data.materials.append(mat("partyhat", (0.3, 0.6, 1.0), 0.5))
    c = _cam((0.05, -0.75, 0.62), (0.1, 0.2, 0.5), lens=36, fstop=3)
    def upd(t):
        bpy.context.view_layer.update(); a = m["arm"]; hat.location = a.matrix_world @ a.pose.bones["Head"].tail + Vector((0, 0, 0.03))
    return upd


def r5(rng):            # At the dentist.: Maya in the dentist's chair, Stan leaning in from the doorway
    cube((0, 0, -0.05), (8, 8, 0.1), mat("dfloor", (0.85, 0.88, 0.9), 0.4)); w = mat("dwall", (0.75, 0.9, 0.92), 0.8)
    cube((0, 1.6, 1.5), (6, 0.1, 3), w); cube((1.2, 0, 1.5), (0.1, 6, 3), w)
    cube((0, 0.6, 0.2), (0.4, 0.9, 0.12), mat("dchair", (0.2, 0.55, 0.6), 0.4), rot=(0.25, 0, 0))
    light("AREA", (0, -1.2, 1.8), 60, col=(1, 1, 1), size=2, target=(0, 0.6, 0.4)); sphere((0.0, 0.3, 0.9), 0.06, mat("dlamp", (1, 1, 0.95), 0.2, emit=(1, 1, 0.9), emit_str=10))
    world_color((0.6, 0.7, 0.75))
    m = who(MAYA, (0, 0.55, 0)); pose(m, "sit", seat=0.28); s = who(STAN, (0.75, 0.9, 0), rot=-0.9, action="Interact")
    c = _cam((-0.5, -0.9, 0.75), (0.25, 0.65, 0.45), lens=32, fstop=4)
    def upd(t): s["root"].location.x = 0.85 - 0.12 * smooth(t / 0.5)               # popping round the door
    return upd


def r6(rng):            # In March, he put a countdown on the fridge.: Stan slaps the pad onto the fridge door
    page = fridge(rng, "247"); s = who(STAN, (-1.1, 0.45, 0), rot=-2.2, action="Interact")
    c = _cam((-0.55, -0.35, 0.95), (-1.4, 0.9, 0.9), lens=36, fstop=3)
    def upd(t): look_at(c, Vector((-1.35, 0.85, 0.85)).lerp(Vector((-1.5, 0.9, 1.0)), smooth((t - 2.0) / 1.2)))   # then onto the number
    return upd


def r7(rng):            # Nobody knew why.: Mum, Dad and Maya swap looks at the table
    kitchen(rng); u = who(MUM, (-0.5, 0.55, 0), rot=-math.pi / 2); d = who(DAD, (0.5, 0.55, 0), rot=math.pi / 2); m = who(MAYA, (0, 0.1, 0))
    c = _cam((0.0, -1.1, 0.85), (0, 0.5, 0.5), lens=32, fstop=4)
    def upd(t):
        u["root"].rotation_euler[2] = -math.pi / 2 + 0.5 * math.sin(t * 2.5); d["root"].rotation_euler[2] = math.pi / 2 - 0.5 * math.sin(t * 2.5 + 1)
        m["root"].rotation_euler[2] = 0.6 * math.sin(t * 3)                    # looking from one to the other
    return upd


def r8(rng):            # Tonight is the last night of November.: the dark kitchen, the pad says 1
    fridge(rng, "1", night=True); c = _cam((-1.2, 0.2, 1.0), (-1.5, 0.9, 1.0), lens=44, fstop=2.2)
    def upd(t): c.location.y = 0.2 + 0.06 * t
    return upd


def r9(rng):            # Grandpa Stan stands up. "Remember... November 2026...": low angle, Stan rising in the dark kitchen
    fridge(rng, "1", night=True); s = who(STAN, (-0.8, 0.55, 0), rot=-0.5)
    m = who(MAYA, (-0.2, -0.05, 0), rot=math.pi * 0.85); light("AREA", (0, -0.8, 0.4), 18, col=(0.9, 0.7, 0.5), size=0.8, target=(-0.8, 0.55, 0.7))
    c = _cam((-0.55, -0.25, 0.3), (-0.8, 0.55, 0.7), lens=30, fstop=3)          # from below: the big moment
    def upd(t): s["root"].location.z = -0.25 * (1 - smooth(t / 1.0)); c.location.y = -0.25 + 0.06 * t   # rising up from his chair
    return upd


def r10(rng):           # "Grandpa. It's here. It's over.": Maya points at the pad, Stan does not blink
    fridge(rng, "1", night=True); s = who(STAN, (-0.8, 0.55, 0), rot=-0.5); m = who(MAYA, (-0.25, 0.1, 0), rot=math.pi * 0.8, action="Interact")
    light("AREA", (0, -0.8, 1.0), 20, col=(0.9, 0.75, 0.6), size=1.0, target=(-0.5, 0.4, 0.5))
    c = _cam((0.25, -0.6, 0.75), (-0.55, 0.45, 0.5), lens=32, fstop=3.5)
    def upd(t): pass
    return upd


def r11(rng):           # He tears the last page off the countdown.: the page rips off and flutters away
    page = fridge(rng, "1", night=True)
    text("365", (-1.5, 0.9035, 1.02), 0.13, mat("pageink", (0.85, 0.1, 0.1), 0.6), rot=(math.pi / 2, 0, 0))      # the page underneath
    text("DAYS", (-1.5, 0.9035, 0.92), 0.045, mat("pageink2", (0.2, 0.2, 0.25), 0.6), rot=(math.pi / 2, 0, 0))
    cube((-1.5, 0.906, 1.03), (0.29, 0.002, 0.33), mat("page2", (1, 1, 0.97), 0.8))
    c = _cam((-1.42, 0.35, 1.02), (-1.5, 0.9, 1.0), lens=50, fstop=2.4)
    def upd(t):
        k = smooth((t - 0.25) / 0.4); page.location = Vector((-1.5 + 0.5 * k, 0.905 - 0.25 * k, 1.03 + 0.15 * k - 0.4 * k * k))
        page.rotation_euler = (0.9 * k, 0.6 * k, 1.8 * k)
    return upd


def r12(rng):           # "Remember... December 2026 is coming.": Stan, triumphant; pull back to the whole family groaning
    fridge(rng, "365", night=True); s = who(STAN, (-0.8, 0.55, 0), rot=-0.5)
    m = who(MAYA, (-0.2, 0.05, 0), rot=math.pi * 0.85); u = who(MUM, (0.35, 0.4, 0), rot=1.9); d = who(DAD, (0.55, 0.0, 0), rot=2.2)
    light("AREA", (0, -0.8, 1.0), 22, col=(0.9, 0.75, 0.6), size=1.2, target=(-0.3, 0.3, 0.5))
    c = _cam((-0.65, 0.1, 0.72), (-0.8, 0.55, 0.68), lens=44, fstop=6); c.data.dof.use_dof = False   # the camera travels: keep it all sharp
    def upd(t):
        k = smooth((t - 2.6) / 2.0)                                            # after the line: pull back to the groans
        c.location = Vector((-0.65, 0.1, 0.72)).lerp(Vector((0.1, -1.4, 1.0)), k); look_at(c, Vector((-0.8, 0.55, 0.68)).lerp(Vector((-0.2, 0.3, 0.5)), k))
        for i, f in enumerate((m, u, d)): f["root"].rotation_euler[0] = 0.15 * k * (0.7 + 0.3 * math.sin(t * 3 + i))   # heads drop
    return upd


SHOTS = {n: (globals()[n], _D[n]) for n in _D}
