"""The Second Cup: animated shots. Render: ENGINE=EEVEE PCT=50 ES=12 $VENV/bin/python pipeline/anim.py stories/the-second-cup OUT all"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from world import *          # noqa

WALTER_HOME = (0.45, 0.35, 0.25)        # brown cardigan
WALTER_COAT = (0.2, 0.32, 0.25)         # green coat
SCARF = (0.75, 0.12, 0.12)
ROSE_C = (0.62, 0.5, 0.75)


def k1(rng):                                        # two cups, steam, pouring
    kitchen(rng); w = peg((-0.05, 0.92, 0), WALTER_HOME, "walter")
    tp = teapot((0, 0, 0)); tp.parent = w["R"]; tp.location = (0.03, -0.12, -0.32); tp.rotation_euler = (0, 0, -math.pi / 2)
    cup((-0.2, 0.55, 0.455)); cup((0.22, 0.55, 0.455))
    s1 = Steam((-0.2, 0.55, 0.53), rng=rng); s2 = Steam((0.22, 0.55, 0.53), rng=rng)
    cam = camera((0.05, -1.25, 0.95), (0.0, 0.6, 0.6), lens=34, dof=1.8, fstop=2.8)
    def upd(t):
        breathe(w, t); w["R"].rotation_euler[0] = -0.9 - 0.25 * math.sin(t * 1.4); w["R"].rotation_euler[1] = 0.25
        s1.update(t); s2.update(t); cam.location.y = -1.25 + 0.08 * t
    return upd


def k2(rng):                                        # the second cup slides to the empty chair
    kitchen(rng); w = peg((-0.32, 0.92, 0), WALTER_HOME, "walter")
    cup((-0.25, 0.55, 0.455)); c2, _ = cup((0.0, 0.55, 0.455)); s2 = Steam((0, 0.55, 0.53), rng=rng)
    cam = camera((0.6, -0.6, 0.8), (0.1, 0.7, 0.5), lens=36, dof=1.5, fstop=2.4)
    def upd(t):
        k = smooth((t - 0.4) / 1.6)
        c2.location.x = 0.3 * k; c2.location.y = 0.55 + 0.1 * k; s2.base = Vector((c2.location.x, c2.location.y, 0.53))
        w["R"].rotation_euler[0] = -0.7 * (1 - abs(2 * k - 1)); w["R"].rotation_euler[1] = 0.4 * (1 - abs(2 * k - 1))
        breathe(w, t); s2.update(t); cam.location.x = 0.6 - 0.04 * t
    return upd


def k3(rng):                                        # the empty chair
    kitchen(rng)
    cam = camera((0.38, -0.5, 0.72), (0.32, 1.0, 0.5), lens=40, dof=1.5, fstop=2.0)
    def upd(t):
        cam.location.y = -0.5 + 0.17 * t; cam.location.z = 0.72 - 0.03 * t
    return upd


def k4(rng):                                        # her tea goes cold
    clk = kitchen(rng); cup((0.3, 0.6, 0.455)); s2 = Steam((0.3, 0.6, 0.53), n=12, rng=rng)
    cam = camera((0.18, 0.18, 0.62), (0.3, 0.6, 0.5), lens=48, dof=0.48, fstop=2.0)
    def upd(t):
        s2.update(t, strength=max(0.0, 1 - t / 2.8)); clk.rotation_euler[1] = int(t) * (2 * math.pi / 60) * 6
        cam.location.y = 0.18 + 0.03 * t
    return upd


def k5(rng):                                        # the neighbours whisper over the fence
    street(rng, houses=False); snow = Snow((0, 0, 0), size=(5, 4, 3), rng=rng)
    cube((0, 3.0, 1.2), (6, 0.2, 2.4), mat("whouse", (0.72, 0.42, 0.35), 0.85, noise=0.3))
    cube((0, 2.88, 1.3), (0.9, 0.02, 0.8), mat("kwinlit", (1, 0.85, 0.6), 0.5, emit=(1, 0.82, 0.55), emit_str=4))
    fm = mat("fence", (0.95, 0.95, 0.95), 0.7)
    for k in range(-12, 13): cube((k * 0.16, 0.0, 0.35), (0.09, 0.03, 0.7), fm, bevel=0.01)
    cube((0, 0.02, 0.5), (4, 0.03, 0.06), fm)
    n1 = peg((-0.3, 0.25, -0.35), (0.3, 0.3, 0.55), "neighbour1", rot=0.15); n2 = peg((0.3, 0.25, -0.38), (0.6, 0.35, 0.3), "neighbour2", rot=-0.15)
    camera((0.0, -1.6, 0.85), (0.0, 0.3, 0.8), lens=38, dof=1.85, fstop=2.4)
    def upd(t):
        k = smooth(t / 0.8)
        n1["root"].location.z = -0.35 + 0.47 * k; n2["root"].location.z = -0.38 + 0.50 * k
        lean = 0.25 * min(1, max(0, (t - 1.5) / 0.6))
        n1["root"].rotation_euler[2] = 0.15 - lean; n2["root"].rotation_euler[2] = -0.15 + lean
        n1["head"].rotation_euler[1] = 0.6 * lean; n2["head"].rotation_euler[1] = -0.6 * lean
        snow.update(t)
    return upd


def k6(rng):                                        # pouring her tea into a flask
    kitchen(rng); tp = teapot((0.1, 0.55, 0.47)); flask((-0.05, 0.55, 0.455))
    stream = cyl((0.0, 0.55, 0.58), 0.006, 0.12, mat("teastream", (0.4, 0.2, 0.07), 0.1, coat=1))
    cam = camera((0.2, 0.05, 0.62), (0.02, 0.55, 0.6), lens=45, dof=0.56, fstop=2.0)
    def upd(t):
        k = smooth((t - 0.3) / 0.8); tp.rotation_euler[1] = -0.75 * k; tp.location = (0.1 - 0.02 * k, 0.55, 0.47 + 0.12 * k)
        stream.scale.z = 1.0 if k > 0.95 else 0.001; cam.location.x = 0.2 - 0.02 * t
    return upd


def k7(rng):                                        # coat on, out into the snow
    street(rng); snow = Snow((0, 1.5, 0), size=(5, 6, 3), rng=rng)
    w = peg((0.6, 2.2, 0), WALTER_COAT, "walter", scarf=SCARF)
    fl = flask((0, 0, 0)); fl.parent = w["R"]; fl.location = (0.0, -0.05, -0.34); fl.scale = (1.2, 1.2, 1.2)
    cam = camera((-0.3, -0.6, 0.6), (0.6, 1.6, 0.45), lens=32, dof=2.3, fstop=3)
    def upd(t):
        walk(w, t, direction=(0, -1)); w["R"].rotation_euler[0] = -0.2
        snow.update(t); cam.location.y = -0.6 - 0.2 * t; look_at(cam, w["root"].location + Vector((0, -0.2, 0.45)))
    return upd


def k8(rng):                                        # two miles in the cold
    street(rng); snow = Snow((0, 4, 0), size=(8, 10, 5), n=500, rng=rng)
    w = peg((0.4, 6.0, 0), WALTER_COAT, "walter", rot=math.pi, scarf=SCARF)
    cam = camera((0.0, -1.5, 3.2), (0.3, 9.0, 0.0), lens=28, dof=7.5, fstop=8)
    def upd(t):
        walk(w, t, direction=(0, 1)); snow.update(t); cam.location.y = -1.5 + 0.1 * t
    return upd


def k9(rng):                                        # Sunny Meadows Care Home
    care_home(rng); snow = Snow((0, 2, 0), size=(8, 8, 4), n=450, rng=rng)
    w = peg((0.0, 1.8, 0), WALTER_COAT, "walter", rot=math.pi, scarf=SCARF)
    cam = camera((0.6, -2.2, 1.1), (0.0, 6.5, 1.5), lens=28, dof=6.0, fstop=6)
    def upd(t):
        walk(w, t, direction=(0, 1)); snow.update(t); cam.location.y = -2.2 + 0.25 * t
    return upd


def room_people(rng, walter=True, nurse=False, sun=1.0):
    sunl, win = care_room(rng, sun)
    r = peg((0.55, 0.92, 0.12), ROSE_C, "rose", rot=-0.35)
    w = peg((-0.48, 0.72, 0.1), WALTER_HOME, "walter", rot=0.6) if walter else None
    n = peg((0.95, 0.4, 0), (0.45, 0.65, 0.85), "nurse", rot=0.9) if nurse else None
    return r, w, n, sunl, win


def k10(rng):                                       # Rose by the window
    r, *_ = room_people(rng, walter=False)
    cam = camera((0.0, -0.9, 0.9), (0.5, 0.9, 0.75), lens=36, dof=1.95, fstop=2.4)
    def upd(t):
        breathe(r, t); r["head"].rotation_euler[2] = -0.3 + 0.25 * min(1, t / 2.5); cam.location.x = 0.03 * t
    return upd


def k11(rng):                                       # 'Good morning. I brought you some tea.'
    r, w, *_ = room_people(rng)
    cup((0.12, 0.6, 0.395)); fl = flask((0, 0, 0)); fl.parent = w["R"]; fl.location = (0.0, -0.06, -0.33)
    st = Steam((0.12, 0.6, 0.47), rng=rng)
    cam = camera((-0.1, -0.95, 0.88), (0.0, 0.75, 0.58), lens=28, dof=1.75, fstop=2.4)
    def upd(t):
        breathe(w, t); breathe(r, t)
        k = smooth((t - 0.8) / 0.9); w["R"].rotation_euler[0] = -1.1 * k; w["R"].rotation_euler[2] = 0.3 * k
        st.update(t, strength=min(1, max(0, (t - 1.6) / 0.6))); cam.location.x = -0.1 + 0.03 * t
    return upd


def k12(rng):                                       # 'You're very kind. Have we met?'
    r, w, *_ = room_people(rng)
    cam = camera((0.25, 0.1, 0.94), (0.55, 0.92, 0.88), lens=44, dof=0.88, fstop=1.8)
    def upd(t):
        breathe(r, t); r["head"].rotation_euler[1] = 0.12 * math.sin(min(t, 2.2) * 1.4); cam.location.y = 0.1 + 0.02 * t
    return upd


def k13(rng):                                       # 'Not yet,' he says. (a tear)
    r, w, *_ = room_people(rng)
    tear = sphere((-0.5, 0.6, 0.86), 0.008, mat("tear", (0.8, 0.9, 1.0), 0.05, coat=1))
    camera((-0.15, 0.05, 0.92), (-0.48, 0.72, 0.84), lens=46, dof=0.76, fstop=1.8)
    w["root"].rotation_euler[2] = 0.9
    def upd(t):
        breathe(w, t); w["head"].rotation_euler[0] = 0.08 * math.sin(min(t, 1.2) * 2.6)
        tear.location.z = 0.83 - 0.06 * max(0, t - 0.6)
    return upd


def k14(rng):                                       # every day she forgets: days pass in the window
    r, w, _, sunl, win = room_people(rng)
    camera((-0.1, -1.1, 1.05), (0.1, 0.8, 0.6), lens=30, dof=2.0, fstop=3)
    wm = bsdf(win.data.materials[0])
    def upd(t):
        b = 0.25 + 0.75 * math.sin(((t / 1.25) % 1.0) * math.pi)
        sunl.data.energy = 160 * b; sunl.data.color = (1.0, 0.75 + 0.2 * b, 0.55 + 0.4 * b)
        wm.inputs["Emission Strength"].default_value = 0.6 + 3 * b
        breathe(r, t); breathe(w, t); r["head"].rotation_euler[2] = 0.25 * math.sin(t * 1.1)
    return upd


def k15(rng):                                       # falling in love again: her hand on his
    r, w, *_ = room_people(rng)
    cam = camera((0.02, -1.05, 0.98), (0.05, 0.8, 0.62), lens=30, dof=1.75, fstop=2.4)
    def upd(t):
        breathe(r, t); breathe(w, t)
        k = smooth((t - 0.4) / 1.2)
        w["R"].rotation_euler[0] = -0.9; r["L"].rotation_euler[0] = -1.0 * k; r["L"].rotation_euler[2] = -0.5 * k
        r["head"].rotation_euler[0] = 0.1 * math.sin(t * 3) * k; cam.location.y = -1.05 + 0.05 * t
    return upd


def k16(rng):                                       # the nurse asks about her visitor
    r, _, n, _, _ = room_people(rng, walter=False, nurse=True)
    cup((0.12, 0.6, 0.395), tea=False)
    camera((-0.3, -0.95, 0.95), (0.7, 0.72, 0.65), lens=28, dof=1.9, fstop=2.4)
    def upd(t):
        breathe(r, t); k = min(1, t / 1.5); n["root"].rotation_euler[0] = 0.25 * k; n["head"].rotation_euler[0] = 0.15 * k
        r["head"].rotation_euler[2] = -0.4 * k
    return upd


def k17(rng):                                       # Rose blushes; reveal the empty chair and the empty cup
    r, *_ = room_people(rng, walter=False)
    cup((0.12, 0.6, 0.395), tea=False)
    cb = bsdf(r["cheek"])
    cam = camera((0.25, 0.1, 0.94), (0.55, 0.92, 0.88), lens=44, dof=0.88, fstop=1.8)
    def upd(t):
        breathe(r, t)
        k = min(1, t / 2.0); cb.inputs["Base Color"].default_value = (0.92 + 0.08 * k, 0.45 - 0.2 * k, 0.45 - 0.2 * k, 1)
        cb.inputs["Emission Color"].default_value = (1, 0.3, 0.3, 1); cb.inputs["Emission Strength"].default_value = 0.6 * k
        r["head"].rotation_euler[2] = 0.35 * min(1, max(0, (t - 1.5) / 1.5))
        pull = smooth((t - 2.5) / 2.5)
        cam.location = Vector((0.25 - 0.45 * pull, 0.1 - 0.75 * pull, 0.94 + 0.05 * pull))
        look_at(cam, Vector((0.55 - 0.6 * pull, 0.92 - 0.25 * pull, 0.88 - 0.3 * pull)))
        cam.data.dof.focus_distance = 0.88 + 0.6 * pull
    return upd


SHOTS = {"k1": (k1, 4.4), "k2": (k2, 2.85), "k3": (k3, 2.55), "k4": (k4, 3.4), "k5": (k5, 5.35), "k6": (k6, 4.75),
         "k7": (k7, 3.9), "k8": (k8, 2.7), "k9": (k9, 4.8), "k10": (k10, 4.4), "k11": (k11, 4.05), "k12": (k12, 3.85),
         "k13": (k13, 2.05), "k14": (k14, 3.75), "k15": (k15, 3.2), "k16": (k16, 3.4), "k17": (k17, 5.5)}
