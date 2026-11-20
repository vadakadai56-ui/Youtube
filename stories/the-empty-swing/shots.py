"""The Empty Swing: animated shots. Render: ENGINE=EEVEE PCT=50 ES=12 $VENV/bin/python pipeline/anim.py stories/the-empty-swing OUT all"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
from world import *          # noqa

SAM = (0.55, 0.56, 0.6)              # grey hoodie
SAM_COAT = (0.25, 0.3, 0.42)         # winter coat
LILY_GOWN = (0.62, 0.78, 0.92)
LILY_COAT = (0.95, 0.5, 0.55)        # spring coat
PUSH_Y = -0.55                       # where Sam stands behind the swing


def pusher(t, d, piv, amp=0.5, period=2.2):
    """Sam pushes the swing: arms reach forward as the seat comes back towards him."""
    a = swing_angle(t, amp, period); piv.rotation_euler[0] = a
    reach = max(0.0, -math.sin(2 * math.pi * t / period))
    d["L"].rotation_euler[0] = d["R"].rotation_euler[0] = -0.9 - 0.6 * reach
    d["root"].location.y = d["base"].y + 0.05 * reach
    breathe(d, t)


def s1(rng):                                      # dusk, lamps come on, he walks in through the gate
    h = park(rng, "dusk", lamps_on=1.0); lampm = [l for l in h["lamps"] if l.type == "MESH"]; lampl = [l for l in h["lamps"] if l.type == "LIGHT"]
    sam = peg((0.3, -2.6, 0), SAM, "sam", rot=math.pi)
    cam = camera((1.8, -4.2, 1.0), (0.2, -1.5, 0.6), lens=30, dof=3.0, fstop=4)
    def upd(t):
        on = min(1, max(0, (t - 0.4) / 0.6)) * (0.7 + 0.3 * (math.sin(t * 40) > -0.6 or t > 1.4))
        for m in lampm: bsdf(m.data.materials[0]).inputs["Emission Strength"].default_value = 18 * on
        for l in lampl: l.data.energy = 60 * on
        walk(sam, t, direction=(0, 1)); cam.location.x = 1.8 - 0.05 * t
    return upd


def s2(rng):                                      # the same swing, creaking in the wind
    h = park(rng, "dusk"); piv = h["swing"]
    cam = camera((0.35, -1.5, 0.8), (0.0, 0.0, 0.75), lens=36, dof=1.55, fstop=2.2)
    def upd(t):
        piv.rotation_euler[0] = 0.06 * math.sin(t * 1.7); cam.location.x = 0.35 - 0.05 * t
    return upd


def s3(rng):                                      # he pushes it
    h = park(rng, "dusk"); sam = peg((0, PUSH_Y - 0.15, 0), SAM, "sam", rot=math.pi)
    cam = camera((1.6, 0.6, 0.8), (0.0, -0.2, 0.7), lens=34, dof=1.75, fstop=2.8)
    def upd(t): pusher(t, sam, h["swing"], amp=0.35 + 0.05 * t)
    return upd


def s4(rng):                                      # no one on it: push-in on the empty seat
    h = park(rng, "dusk"); sam = peg((0, PUSH_Y - 0.15, 0), SAM, "sam", rot=math.pi)
    cam = camera((0.0, 1.9, 0.62), (0.0, 0.0, 0.6), lens=42, dof=1.9, fstop=2.0)
    def upd(t):
        pusher(t, sam, h["swing"], amp=0.45); cam.location.y = 1.9 - 0.18 * t
    return upd


def s5(rng):                                      # he laughs, talks to the air: 'Higher? Okay... higher!'
    h = park(rng, "dusk"); sam = peg((0, PUSH_Y - 0.15, 0), SAM, "sam", rot=math.pi)
    cam = camera((0.35, 1.3, 0.85), (0.0, PUSH_Y - 0.15, 0.8), lens=40, dof=1.95, fstop=2.2)
    def upd(t):
        pusher(t, sam, h["swing"], amp=0.45 + 0.04 * t); sam["head"].rotation_euler[0] = -0.25 + 0.05 * math.sin(t * 3)
    return upd


def s6(rng):                                      # the other parents pull their children away
    park(rng, "dusk")
    m1 = peg((0.75, -0.5, 0), (0.7, 0.4, 0.45), "neighbour2", rot=-1.2); k1 = peg((1.0, -0.6, 0), (0.95, 0.75, 0.2), "plain", rot=-1.2, h=0.6)
    m2 = peg((-0.8, -0.3, 0), (0.35, 0.45, 0.6), "neighbour1", rot=1.0); k2 = peg((-1.0, -0.45, 0), (0.4, 0.75, 0.5), "plain", rot=1.0, h=0.55)
    camera((0.0, -2.6, 1.0), (0.0, 0.5, 0.5), lens=28, dof=3.0, fstop=4)
    def upd(t):
        k = max(0.0, t - 0.6)
        for d, dx, dy in ((m1, 1, -0.3), (k1, 1, -0.3), (m2, -1, -0.2), (k2, -1, -0.2)):
            walk(d, k, direction=(dx, dy)) if k > 0 else breathe(d, t)
        m1["head"].rotation_euler[2] = 0.6 * math.sin(min(t, 2) * 0.8)
    return upd


def s7(rng):                                      # someone whispers by the gate
    park(rng, "dusk")
    a = peg((-0.25, -2.55, 0), (0.7, 0.4, 0.45), "neighbour2", rot=-0.5); b = peg((0.22, -2.55, 0), (0.35, 0.45, 0.6), "neighbour1", rot=0.5)
    sam = peg((0, PUSH_Y - 0.15, 0), SAM, "sam", rot=math.pi)
    cam = camera((0.0, -3.9, 0.95), (0.0, -1.5, 0.75), lens=34, dof=1.45, fstop=2.2)
    def upd(t):
        lean = 0.22 * smooth(t / 0.8)
        a["root"].rotation_euler[1] = lean; b["root"].rotation_euler[1] = -lean
        a["head"].rotation_euler[2] = -0.4 * smooth(t / 0.8); breathe(sam, t); cam.location.y = -3.9 + 0.06 * t
    return upd


def s8(rng):                                      # he comes when it rains
    h = park(rng, "rain", lamps_on=0.8); rain = Rain((0, -0.3, 0), size=(4, 4, 3), rng=rng)
    sam = peg((0, PUSH_Y - 0.15, 0), (0.35, 0.37, 0.42), "sam", rot=math.pi)
    camera((1.3, -1.9, 0.95), (0.0, -0.3, 0.6), lens=32, dof=2.2, fstop=3)
    def upd(t): pusher(t, sam, h["swing"], amp=0.4); rain.update(t)
    return upd


def s9(rng):                                      # he comes when it snows (snow on the empty seat)
    h = park(rng, "snow", lamps_on=1.0); snow = Snow((0, -0.3, 0), size=(4, 4, 3), rng=rng)
    pile = sphere((0, 0, 0.62), 0.2, mat("seatsnow", (0.96, 0.97, 1.0), 0.7), scale=(1.1, 0.4, 0.18)); pile.parent = h["swing"]; pile.location = (0, 0, 0.62 - 1.78)
    sam = peg((0, PUSH_Y - 0.15, 0), SAM_COAT, "sam", rot=math.pi, scarf=(0.75, 0.12, 0.12))
    camera((-1.2, -1.6, 0.9), (0.0, -0.2, 0.6), lens=34, dof=1.95, fstop=2.8)
    def upd(t):
        brush = smooth(t / 0.5); pile.scale = (1.1 * (1 - brush) + 0.001, 0.4, 0.18 * (1 - brush) + 0.001)
        pusher(max(0, t - 0.5), sam, h["swing"], amp=0.4); snow.update(t)
    return upd


def s10(rng):                                     # every evening, six o'clock: the clock tower
    park(rng, "autumn", lamps_on=0.7); leaves = Flutter((-4.0, 4.4, 0), SEASONS["autumn"][1], size=(3, 2, 4), rng=rng)
    cam = camera((-3.6, 2.6, 2.6), (-4.5, 5.1, 3.3), lens=40, dof=2.6, fstop=3)
    def upd(t): leaves.update(t); cam.location.z = 2.6 + 0.08 * t
    return upd


def s11(rng):                                     # 112 days: autumn leaves round the swing
    h = park(rng, "autumn", lamps_on=0.7); leaves = Flutter((0, -0.2, 0), SEASONS["autumn"][1], size=(4, 3, 3), n=120, rng=rng)
    sam = peg((0, PUSH_Y - 0.15, 0), SAM, "sam", rot=math.pi, scarf=(0.75, 0.12, 0.12))
    camera((1.4, -1.6, 0.8), (0.0, -0.2, 0.65), lens=32, dof=2.15, fstop=2.8)
    def upd(t): pusher(t, sam, h["swing"], amp=0.45); leaves.update(t)
    return upd


def s12(rng):                                     # nobody ever looked across the road: camera rises over the fence
    h = park(rng, "dusk"); hospital(rng, across=9.0)
    sam = peg((0, PUSH_Y - 0.15, 0), SAM, "sam", rot=math.pi)
    cam = camera((0.0, -3.2, 0.5), (0.0, 0.0, 0.6), lens=28, dof=4.0, fstop=8)
    def upd(t):
        pusher(t, sam, h["swing"], amp=0.45)
        k = smooth(t / 1.6); cam.location = Vector((0.0, -3.2 + 0.4 * k, 0.5 + 2.4 * k))
        look_at(cam, Vector((0.0, 0.0 + 9.0 * k, 0.6 + 3.3 * k)))
    return upd


def s13(rng):                                     # the children's hospital, fourth floor, third window: glide in
    park(rng, "dusk"); win = hospital(rng, across=9.0)
    cam = camera((0.0, 2.0, 3.6), win, lens=30, dof=7.0, fstop=8)
    def upd(t):
        k = smooth(t / 3.8); p = Vector((0.0, 2.0, 3.6)).lerp(win + Vector((0, -2.2, 0)), k)
        cam.location = p; look_at(cam, win); cam.data.lens = 30 + 25 * k; cam.data.dof.focus_distance = (win - p).length
    return upd


def lily_room(rng, dusk=True, at_window=True):
    hospital_room(rng, dusk)
    return peg((0.0, 0.95, 0), LILY_GOWN, "lily", rot=math.pi if at_window else 0.4, h=0.7)


def s14(rng):                                     # Lily presses her hand to the glass (behind her, the dusk window)
    l = lily_room(rng)
    cam = camera((-0.45, 0.15, 0.62), (0.0, 1.1, 0.72), lens=36, dof=0.95, fstop=2.0)
    def upd(t):
        breathe(l, t); k = smooth((t - 0.5) / 0.8); l["R"].rotation_euler[0] = -2.3 * k; cam.location.y = 0.15 + 0.05 * t
    return upd


def s15(rng):                                     # she can't go outside. Not yet. (the room, the drip stand)
    l = lily_room(rng)
    cam = camera((-1.3, -1.4, 1.3), (0.0, 0.9, 0.55), lens=28, dof=2.6, fstop=3)
    def upd(t): breathe(l, t); cam.location.x = -1.3 + 0.05 * t
    return upd


def s16(rng):                                     # her view: far below, the tiny swing flying
    h = park(rng, "dusk"); sam = peg((0, PUSH_Y - 0.15, 0), SAM, "sam", rot=math.pi)
    camera((0.0, 7.8, 3.9), (0.0, -0.2, 0.4), lens=55, dof=8.6, fstop=11)
    def upd(t): pusher(t, sam, h["swing"], amp=0.6)
    return upd


def s17(rng):                                     # she laughs: 'Higher, Daddy... higher!'
    l = lily_room(rng); l["root"].rotation_euler[2] = 0.6
    cam = camera((0.5, 0.55, 0.62), (0.0, 0.95, 0.6), lens=44, dof=0.62, fstop=1.8)
    def upd(t):
        breathe(l, t, 2); l["root"].location.z = 0.012 * abs(math.sin(t * 9)); l["R"].rotation_euler[0] = -2.2
        l["head"].rotation_euler[0] = -0.12 + 0.06 * math.sin(t * 9)
    return upd


def s18(rng):                                     # and he pushes harder, as if he heard her
    h = park(rng, "dusk"); sam = peg((0, PUSH_Y - 0.15, 0), SAM, "sam", rot=math.pi)
    camera((0.35, 1.3, 0.85), (0.0, PUSH_Y - 0.15, 0.8), lens=40, dof=1.95, fstop=2.2)
    def upd(t): pusher(t, sam, h["swing"], amp=0.62); sam["head"].rotation_euler[0] = -0.3
    return upd


def s19(rng):                                     # spring... the hospital window is empty (dark)
    park(rng, "spring"); win = hospital(rng, lily_window_lit=False, across=9.0)
    petals = Flutter(win + Vector((0, -2.0, -1.5)), SEASONS["spring"][1], size=(4, 3, 4), rng=rng, flake=0.035)
    cam = camera(win + Vector((0.4, -3.2, -0.3)), win, lens=50, dof=3.25, fstop=4)
    def upd(t): petals.update(t); cam.location.y = win.y - 3.2 + 0.05 * t
    return upd


def s20(rng):                                     # because Lily was finally outside: through the gate, hand in hand
    park(rng, "spring")
    petals = Flutter((0, -1.8, 0), SEASONS["spring"][1], size=(5, 4, 3), rng=rng, flake=0.035)
    sam = peg((-0.15, -3.0, 0), SAM, "sam", rot=math.pi); lily = peg((0.2, -3.0, 0), LILY_COAT, "lily", rot=math.pi, h=0.7)
    cam = camera((0.6, -0.9, 0.7), (0.0, -2.6, 0.55), lens=34, dof=2.0, fstop=2.4)
    def upd(t):
        walk(sam, t, speed=0.8, direction=(0, 1)); walk(lily, t, speed=0.8, direction=(0, 1)); petals.update(t)
        sam["L"].rotation_euler[0] = 0.2; lily["R"].rotation_euler[0] = 0.25
        look_at(cam, sam["root"].location + Vector((0.15, 0, 0.5)))
    return upd


def s21(rng):                                     # she climbs on the swing all by herself
    h = park(rng, "spring"); petals = Flutter((0, -0.3, 0), SEASONS["spring"][1], size=(4, 3, 3), rng=rng, flake=0.035)
    lily = peg((0, -0.3, 0), LILY_COAT, "lily", rot=0.0, h=0.7); sam = peg((-0.65, -0.65, 0), SAM, "sam", rot=math.pi - 0.9)
    camera((1.05, -1.25, 0.8), (0.0, -0.1, 0.55), lens=34, dof=1.65, fstop=2.4)
    def upd(t):
        k = smooth((t - 0.3) / 1.0)
        lily["root"].location = Vector((0, -0.3 + 0.3 * k, 0.55 * k + 0.12 * math.sin(math.pi * k)))
        lily["root"].rotation_euler[2] = math.pi * k
        lily["L"].rotation_euler[0] = lily["R"].rotation_euler[0] = -2.6 * (1 - abs(2 * k - 1))
        breathe(sam, t); petals.update(t)
    return upd


def s22(rng):                                     # 'Higher, Daddy.' She flies up into the pink sky
    h = park(rng, "spring"); petals = Flutter((0, 0.2, 0), SEASONS["spring"][1], size=(5, 4, 3), rng=rng, flake=0.035)
    sam = peg((0, PUSH_Y - 0.15, 0), SAM, "sam", rot=math.pi)
    lily = peg((0, 0, 0), LILY_COAT, "lily", rot=math.pi, h=0.7); lily["root"].parent = h["swing"]; lily["root"].location = (0, 0, 0.6 - 1.78)
    lily["L"].rotation_euler[0] = lily["R"].rotation_euler[0] = -2.9
    cam = camera((0.75, 1.15, 0.42), (0.0, 0.0, 0.95), lens=28, dof=1.4, fstop=2.8)
    def upd(t):
        pusher(t, sam, h["swing"], amp=0.45 + 0.08 * t); petals.update(t)
        lily["head"].rotation_euler[0] = -0.15
    return upd


_D = json.load(open(os.path.join(HERE, "durations.json")))
SHOTS = {n: (globals()[n], _D[n]) for n in _D}
