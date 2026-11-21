"""The Extra Plate: animated shots, "Same Spot, Years Apart" (one fixed table camera across the years).
Render: STYLE=lowpoly ENGINE=EEVEE PCT=50 ES=12 $VENV/bin/python pipeline/anim.py stories/the-extra-plate OUT all"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
os.environ.setdefault("STYLE", "lowpoly")
import scene                  # noqa
scene.STYLE = os.environ["STYLE"]
from world import *           # noqa
from world import cam as _cam

_D = json.load(open(os.path.join(HERE, "durations.json")))
MARGARET = (0.55, 0.3, 0.45)      # plum cardigan
DANNY = (0.25, 0.32, 0.42)        # blue-grey coat
GIRL = (0.95, 0.72, 0.3)          # mustard dress
FAMILY = [("L1", "neighbour1", (0.3, 0.35, 0.5), 1.0), ("L2", "neighbour2", (0.7, 0.4, 0.45), 0.95),
          ("L3", "plain", (0.4, 0.7, 0.5), 0.6), ("R1", "sam", (0.5, 0.45, 0.3), 1.0)]


def hair(year):
    """Margaret greys over the decade: brown-grey in 2017, white by 2026."""
    k = min(1, max(0, (year - 2016) / 10))
    return tuple(a + (b - a) * k for a, b in zip((0.48, 0.38, 0.3), (0.93, 0.91, 0.89)))


def seat_rot(key):
    x = SEATS[key][0]
    return 0.0 if key == "HEAD" else (math.pi / 2 if x < 0 else -math.pi / 2)


def sit(key, col, kind, h=1.0, z=0.0, **kw):
    x, y = SEATS[key]
    return peg((x, y + (0.05 if key == "HEAD" else 0), z), col, kind, rot=seat_rot(key), h=h, **kw)


def table(rng, year, outside="autumn", family=True, margaret_seated=True, steam=True, **kw):
    h = dining_room(rng, outside=outside, **kw); people = []
    if family:
        for key, kind, col, hh in FAMILY: people.append(sit(key, col, kind, h=hh, z=0.27 if hh < 0.8 else 0.0))
    m = sit("HEAD", MARGARET, "margaret", hair=hair(year)) if margaret_seated else None
    st = Steam((0, 0.75, TABLE_Z + 0.15), n=8, rng=rng) if steam else None
    snow = Snow((0, 3.2, 0.6), size=(1.6, 0.6, 2.2), n=90, rng=rng) if outside == "snow" else None
    return h, people, m, st, snow


def life(t, people, m=None, st=None, snow=None, eat=True):
    for i, d in enumerate(people):
        breathe(d, t + i)
        if eat: d["R"].rotation_euler[0] = -0.6 - 0.25 * max(0, math.sin(t * 2.2 + i * 1.7))
    if m: breathe(m, t)
    if st: st.update(t)
    if snow: snow.update(t)


def s1(rng):              # hook: from above, the extra plate and the little name card
    h, people, m, st, _ = table(rng, 2017)
    cam = _cam((0.34, 0.7, 1.35), (0.34, 0.76, 0.53), lens=50, fstop=3.5); cam.rotation_euler[2] += math.pi / 2
    def upd(t):
        life(t, people, m, st); cam.location.z = 1.35 - 0.04 * t
    return upd


def s2(rng):              # same table, same chair: the fixed camera
    h, people, m, st, _ = table(rng, 2017); cam = spot_camera()
    def upd(t): life(t, people, m, st); cam.location.y = -1.05 + 0.03 * t
    return upd


def s3(rng):              # the name card: "Danny"
    h, people, m, st, _ = table(rng, 2017)
    cam = _cam((0.6, 0.72, 0.66), (0.32, 0.82, 0.57), lens=50, fstop=1.8)
    def upd(t): life(t, people, m, st); cam.location.x = 0.6 - 0.02 * t
    return upd


def s4(rng):              # the first year, they asked who it was for: heads turn to the empty chair
    h, people, m, st, _ = table(rng, 2017); cam = spot_camera()
    def upd(t):
        life(t, people, m, st, eat=False); k = smooth((t - 0.4) / 0.8)
        for d, a in zip(people, (0.5, 0.45, 0.6, -0.5)): d["head"].rotation_euler[2] = a * k
        m["head"].rotation_euler[0] = 0.25 * k
    return upd


def s5(rng):              # the second year... they stopped asking: snow outside, everyone eats
    h, people, m, st, snow = table(rng, 2018, outside="snow"); cam = spot_camera()
    def upd(t): life(t, people, m, st, snow); m["head"].rotation_euler[0] = 0.2; cam.location.y = -1.05 + 0.03 * t
    return upd


def s6(rng):              # the fight: cold blue room, Danny walks out, the door slams
    h = dining_room(rng, outside="rain", candles=False, food=False)
    bsdf(h["hall"].data.materials[0]).inputs["Emission Strength"].default_value = 3.0
    dan = peg((-1.05, 0.45, 0), DANNY, "danny", rot=math.pi)
    mar = peg((-0.1, 0.25, 0), MARGARET, "margaret", rot=math.pi / 2 + 0.6, hair=hair(2016))
    light("AREA", (0.5, -0.5, 2.0), 40, col=(0.4, 0.5, 1.0), size=2, target=(-0.8, 1.2, 0.8))
    cam = _cam((-0.55, -1.05, 1.0), (-1.45, 1.1, 0.85), lens=32, fstop=2.8)
    def upd(t):
        k = min(1, t / 2.6)
        dan["root"].location = Vector((-1.05 - 0.85 * k, 0.45 + 0.9 * k, 0.03 * abs(math.sin(t * 9))))
        dan["root"].rotation_euler[2] = math.pi - 0.6                           # walking to the door, away from us
        h["door"].rotation_euler[2] = -1.3 * (1 - smooth((t - 2.9) / 0.35))   # open, then slams at ~3.1 s
        bsdf(h["hall"].data.materials[0]).inputs["Emission Strength"].default_value = 3.0 * (1 - smooth((t - 2.9) / 0.35))
        mar["R"].rotation_euler[0] = -0.9 * smooth(t / 1.2); breathe(mar, t)
        if t > 3.0: dan["root"].location.z = -5
    return upd


def s7(rng):              # every November, a postcard: Margaret at the window, snow outside
    h = dining_room(rng, outside="snow", food=False)
    mar = peg((0.45, 2.15, 0), MARGARET, "margaret", rot=1.75, hair=hair(2018))
    pc = postcard((0.6, 2.12, 0.58), rot=(0.9, 0, 1.75))
    light("AREA", (1.0, 1.7, 1.0), 14, col=(1.0, 0.7, 0.45), size=0.5, target=(0.45, 2.15, 0.78))
    snow = Snow((0, 3.2, 0.6), size=(1.6, 0.6, 2.2), n=90, rng=rng)
    cam = _cam((1.2, 2.38, 0.9), (0.45, 2.15, 0.74), lens=42, fstop=2.0)
    def upd(t):
        breathe(mar, t); snow.update(t); mar["R"].rotation_euler[0] = -1.2 + 0.08 * math.sin(t * 6)
        mar["head"].rotation_euler[0] = 0.3; cam.location.x = 1.2 - 0.03 * t
    return upd


def s8(rng):              # the five words, close up
    h = dining_room(rng, outside="snow", food=False, card=False)
    postcard((0.15, 0.6, TABLE_Z + 0.04)); cyl((0.32, 0.55, TABLE_Z + 0.045), 0.006, 0.16, mat("pen", (0.1, 0.1, 0.3), 0.3), rot=(0, math.pi / 2, 0.4))
    cam = camera((0.15, 0.52, 0.95), (0.15, 0.6, TABLE_Z), lens=50, dof=0.42, fstop=2.5)
    def upd(t): cam.location.z = 0.95 - 0.03 * t
    return upd


def s9(rng):              # he never writes back: the empty plate, the same frame, years ticking
    h, people, m, st, _ = table(rng, 2020); cam = spot_camera()
    def upd(t): life(t, people, m, st); m["head"].rotation_euler[0] = 0.3; cam.location.y = -1.05 + 0.08 * t
    return upd


def s10(rng):             # year six: she hears he has a little girl; a photo in her hands
    h = dining_room(rng, outside="autumn", food=False)
    mar = peg((0.3, 1.9, 0), MARGARET, "margaret", rot=0.45, hair=hair(2022))
    fr = cube((0.37, 1.76, 0.56), (0.12, 0.012, 0.15), mat("pframe", (0.6, 0.45, 0.2), 0.4, metal=0.5), rot=(1.2, 0, 0.35))
    cube((0.368, 1.765, 0.56), (0.09, 0.004, 0.12), mat("photo", (0.9, 0.75, 0.6), 0.5, emit=(1, 0.8, 0.6), emit_str=0.6), rot=(1.2, 0, 0.35))
    cam = _cam((0.55, 0.95, 0.85), (0.3, 1.88, 0.75), lens=50, fstop=1.9)
    def upd(t):
        breathe(mar, t); mar["R"].rotation_euler[0] = -1.1; mar["L"].rotation_euler[0] = -1.1
        mar["head"].rotation_euler[0] = 0.35; cam.location.y = 0.95 + 0.04 * t
    return upd


def s11(rng):             # year eight: a tiny chair, just in case
    h, people, m, st, _ = table(rng, 2024, tiny_chair=True); cam = spot_camera()
    tiny = h["tiny"]
    def upd(t):
        life(t, people, m, st); k = smooth(t / 1.8); tiny.location.x = 1.35 - 0.53 * k
    return upd


def s12(rng):             # year nine: the turkey goes cold, the candles burn low
    h, people, m, st, _ = table(rng, 2025, outside="rain", steam=False, candles=False, tiny_chair=True)
    for y in (0.35, 1.1, 1.55): candle((0, y, TABLE_Z + 0.036), h=0.05)
    cam = _cam((0.42, 0.18, 0.78), (0.05, 0.78, 0.6), lens=42, fstop=2.0)
    def upd(t): life(t, people, m, None, eat=False); cam.location.y = 0.18 + 0.05 * t
    return upd


def s13(rng):             # year ten: she almost doesn't set it
    h, people, m, st, _ = table(rng, 2026, danny_plate=False, card=False, margaret_seated=False, tiny_chair=True)
    mar = peg((0.95, 0.75, 0), MARGARET, "margaret", rot=-math.pi / 2 - 0.3, hair=hair(2026))
    held = plate((0.78, 0.68, 0.55))
    cam = _cam((0.15, 0.0, 0.92), (0.88, 0.73, 0.7), lens=38, fstop=2.4)
    def upd(t):
        life(t, people, None, st); breathe(mar, t); mar["head"].rotation_euler[0] = 0.35
        mar["L"].rotation_euler[0] = mar["R"].rotation_euler[0] = -1.0 + 0.05 * math.sin(t * 1.5)
    return upd


def s14(rng):             # then... a knock: the door, warm light under it, shaking
    h = dining_room(rng, outside="snow")
    bsdf(h["hall"].data.materials[0]).inputs["Emission Strength"].default_value = 2.0
    light("POINT", (-1.2, 1.35, 0.4), 6, col=(1.0, 0.6, 0.3), size=0.2)
    cam = _cam((-0.95, 0.95, 1.35), (-1.68, 1.35, 0.55), lens=32, fstop=2.4)
    def upd(t):
        knock = sum(math.exp(-((t - a) / 0.05) ** 2) for a in (0.25, 0.55, 0.85))
        h["door"].rotation_euler[2] = -0.04 * knock; cam.location.x = -0.95 - 0.04 * t
    return upd


def s15(rng):             # a little girl walks past everyone, straight to the tiny chair
    h, people, m, st, _ = table(rng, 2026, tiny_chair=True); cam = spot_camera()
    g = peg((-0.4, 2.2, 0), GIRL, "girl", rot=-math.pi / 2, h=0.6)
    path = [(-0.4, 2.2), (0.95, 2.15), (0.95, 1.25)]
    def upd(t):
        life(t, people, m, st, eat=False); k = smooth(t / 3.4) * 2
        i = min(1, int(k)); u = k - i; (x0, y0), (x1, y1) = path[i], path[i + 1]
        g["root"].location = Vector((x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, 0.025 * abs(math.sin(t * 11)) + (0.19 * smooth((t - 3.4) / 0.4))))
        g["root"].rotation_euler[2] = -math.pi / 2 if i == 0 else (math.pi if t < 3.4 else -math.pi / 2)
        g["L"].rotation_euler[0] = 0.4 * math.sin(t * 11); g["R"].rotation_euler[0] = -0.4 * math.sin(t * 11)
        for d, a in zip(people, (0.6, 0.5, 0.7, -0.4)): d["head"].rotation_euler[2] = a * smooth(t / 1.0)
    return upd


def s16(rng):             # she picks up the card: "Danny... that's my daddy."
    h, people, m, st, _ = table(rng, 2026, tiny_chair=True, card=False)
    g = peg((0.95, 1.25, 0.19), GIRL, "girl", rot=-math.pi / 2 - 0.3, h=0.6)
    card = name_card((0.84, 1.2, 0.47), "Danny", rot=-math.pi / 2 - 0.3)
    cam = _cam((0.22, 0.95, 0.72), (0.9, 1.22, 0.58), lens=46, fstop=1.8)
    def upd(t):
        life(t, people, m, st, eat=False); breathe(g, t); g["head"].rotation_euler[0] = 0.25
        g["L"].rotation_euler[0] = g["R"].rotation_euler[0] = -1.1; cam.location.x = 0.22 + 0.03 * t
    return upd


def s17(rng):             # in the doorway, holding nine postcards, stands her son
    h = dining_room(rng, outside="snow")
    h["door"].rotation_euler[2] = -1.35
    bsdf(h["hall"].data.materials[0]).inputs["Emission Strength"].default_value = 3.5
    dan = peg((-1.95, 1.35, 0), DANNY, "danny", rot=math.pi / 2)
    cards = [cube((-1.8, 1.35, 0.42 + i * 0.006), (0.12, 0.17, 0.004), mat("pc%d" % (i % 3), [(0.96, 0.92, 0.8), (0.9, 0.85, 0.7), (0.95, 0.88, 0.75)][i % 3], 0.7),
                  rot=(0, 0, 0.05 * i)) for i in range(9)]
    light("AREA", (-1.3, 1.35, 1.2), 25, col=(1.0, 0.7, 0.45), size=0.6, target=(-1.95, 1.35, 0.75))
    cam = _cam((-0.35, 1.38, 1.3), (-1.95, 1.35, 0.62), lens=38, fstop=2.8)
    def upd(t):
        breathe(dan, t); dan["L"].rotation_euler[0] = dan["R"].rotation_euler[0] = -0.7
        cam.location.x = -0.35 - 0.05 * t
    return upd


def s18(rng):             # "Mom... is my plate still warm?"
    h = dining_room(rng, outside="snow")
    h["door"].rotation_euler[2] = -1.35
    bsdf(h["hall"].data.materials[0]).inputs["Emission Strength"].default_value = 3.5
    dan = peg((-1.95, 1.35, 0), DANNY, "danny", rot=math.pi / 2 + 0.25)
    light("AREA", (-1.2, 1.1, 1.1), 35, col=(1.0, 0.65, 0.4), size=0.6, target=(-1.95, 1.35, 0.8))
    cam = _cam((-1.15, 1.2, 0.86), (-1.95, 1.37, 0.8), lens=50, fstop=1.8)
    def upd(t):
        breathe(dan, t); dan["head"].rotation_euler[0] = -0.08 + 0.03 * math.sin(t * 2)
        cam.location.x = -1.15 - 0.04 * t
    return upd


def s19(rng):             # she doesn't say a word; she sets one more plate
    h, people, m, st, _ = table(rng, 2026, danny_plate=False, card=False, margaret_seated=False, tiny_chair=True)
    mar = peg((0.98, 0.75, 0), MARGARET, "margaret", rot=-math.pi / 2, hair=hair(2026))
    pl = group("newplate", plate((0, 0, 0)), (0, 0, 0))
    cam = _cam((0.05, 0.3, 0.86), (0.45, 0.72, 0.56), lens=38, fstop=2.2)
    def upd(t):
        life(t, people, None, st, eat=False); breathe(mar, t); k = smooth(t / 2.0)
        pl.location = Vector((0.75 - 0.41 * k, 0.72, 0.62 - (0.62 - TABLE_Z - 0.036) * k))
        mar["L"].rotation_euler[0] = mar["R"].rotation_euler[0] = -1.1 + 0.3 * k
    return upd


def s20(rng):             # every chair is full: the same frame, warm, slowly pulling back
    h, people, m, st, _ = table(rng, 2026, outside="snow", tiny_chair=True)
    dan = sit("R2", DANNY, "danny"); g = peg((0.82, 1.25, 0.19), GIRL, "girl", rot=-math.pi / 2, h=0.6)
    snow = Snow((0, 3.2, 0.6), size=(1.6, 0.6, 2.2), n=90, rng=rng)
    cam = spot_camera(push=0.15)
    def upd(t):
        life(t, people + [dan, g], m, st, snow); cam.location.y = -0.9 - 0.06 * t; cam.location.z = 1.12 + 0.02 * t
        m["head"].rotation_euler[0] = 0.05 * math.sin(t)
    return upd


SHOTS = {n: (globals()[n], _D[n]) for n in _D}
