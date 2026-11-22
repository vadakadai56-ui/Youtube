"""One Word (Trend Short, Thanksgiving Day, blocky family from Huss Huss): everyone says what they are thankful for in one word;
the dog just looks at the turkey.
Render: STYLE=lowpoly ENGINE=EEVEE PCT=50 ES=12 $VENV/bin/python pipeline/anim.py stories/one-word OUT all"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
os.environ.setdefault("STYLE", "lowpoly")
import scene                  # noqa
scene.STYLE = os.environ["STYLE"]
from world import *           # noqa
from world import cam as _cam
from characters import blocky, ball, dog
import bpy

_D = json.load(open(os.path.join(HERE, "durations.json")))
KID = dict(shirt=(0.85, 0.2, 0.2), pants=(0.15, 0.2, 0.35), style="kid", hat=(0.2, 0.55, 0.85), name="kid", mouth="flat")
GRAN = dict(shirt=(0.62, 0.38, 0.6), pants=(0.3, 0.28, 0.35), style="gran", skin="tan", shoes=(0.98, 0.62, 0.78), name="gran")
DAD = dict(shirt=(0.3, 0.5, 0.35), pants=(0.25, 0.22, 0.2), style="dad", skin="brown", name="dad")
MUM = dict(shirt=(0.95, 0.75, 0.3), pants=(0.3, 0.3, 0.45), style="mum", skin="tan", name="mum")
SIS = dict(shirt=(0.4, 0.7, 0.85), pants=(0.5, 0.3, 0.45), style="kid", skin="tan", hair=(0.35, 0.2, 0.1), name="sis")
SEAT = {"gran": ("HEAD", 0.0), "dad": ("L1", math.pi / 2), "mum": ("R1", -math.pi / 2), "sis": ("L2", math.pi / 2), "kid": ("R2", -math.pi / 2)}


def dinner(rng):
    """The Thanksgiving table with the family seated. Returns {name: handles}."""
    dining_room(rng, outside="snow", card=False, food=True)
    fam = {}
    for nm, kw in (("gran", GRAN), ("dad", DAD), ("mum", MUM), ("sis", SIS), ("kid", KID)):
        seat, rot = SEAT[nm]; x, y = SEATS[seat]
        f = blocky((x, y + (0.12 if seat == "HEAD" else 0), 0.05), rot=rot, **kw)
        for k in ("LL", "LR"): f[k].rotation_euler[0] = -math.pi / 2
        f["L"].rotation_euler[0] = f["R"].rotation_euler[0] = -0.8
        fam[nm] = f
    return fam


def speak(f, t, t0, dur=0.6):
    """A little bounce and head tilt while saying the word."""
    k = math.sin(math.pi * min(1, max(0, (t - t0) / dur)))
    f["root"].location.z = 0.05 + 0.02 * k; f["head"].rotation_euler[0] = -0.12 * k


# ---------------------------------------------------------------- shots
def o1(rng):            # Thanksgiving rule in our house. Say what you're thankful for. One word only.: the whole table, push in
    fam = dinner(rng); c = _cam((0.0, -1.7, 1.45), (0, 0.95, 0.6), lens=28, fstop=5)
    def upd(t):
        for i, f in enumerate(fam.values()): f["head"].rotation_euler[2] = 0.08 * math.sin(t * 1.2 + i)
        c.location.y = -1.7 + 0.12 * t
    return upd


def close(name, look, word_t, lens=46, extra=None):
    def shot(rng):
        fam = dinner(rng); f = fam[name]; x, y = f["root"].location.x, f["root"].location.y
        c = _cam(look, (x, y, 0.75), lens=lens, fstop=2.2)
        def upd(t):
            speak(f, t, word_t)
            if extra: extra(f, t)
            c.location.y = look[1] + 0.03 * t
        return upd
    return shot


def _fist(f, t): f["R"].rotation_euler[1] = -2.4 * smooth((t - 0.8) / 0.2) - 0.2 * math.sin(t * 10) * (t > 1.0)
def _bliss(f, t): f["head"].rotation_euler[0] = -0.2; f["L"].rotation_euler[0] = f["R"].rotation_euler[0] = -1.3


o2 = close("gran", (0.0, 0.85, 0.95), 0.9)                                    # "Family."
o3 = close("dad", (0.15, -0.55, 0.9), 0.75, extra=_fist)                    # "Football."
o4 = close("mum", (-0.15, -0.55, 0.9), 0.8, extra=_bliss)                   # "Dishwasher."


def o5(rng):            # My sister. "Wi-Fi.": she holds up her phone, glowing
    fam = dinner(rng); f = fam["sis"]; x, y = f["root"].location.x, f["root"].location.y
    ph = cube((0, 0, 0), (0.07, 0.012, 0.13), mat("sisphone", (0.6, 0.8, 1.0), 0.2, emit=(0.6, 0.8, 1.0), emit_str=2.5))
    c = _cam((0.2, 0.15, 0.95), (x, y, 0.75), lens=46, fstop=2.2)
    def upd(t):
        speak(f, t, 1.0); f["R"].rotation_euler[0] = -1.9
        ph.location = f["root"].location + Vector((0.14, 0.1, 0.78)); ph.rotation_euler = (0, 0, math.pi / 2)
    return upd


def o6(rng):            # Me? "Huss.": deadpan, the ball under one arm
    fam = dinner(rng); f = fam["kid"]; b = ball((0, 0, 0))
    c = _cam((-0.2, 0.15, 0.95), (f["root"].location.x, f["root"].location.y, 0.75), lens=46, fstop=2.2)
    def upd(t):
        speak(f, t, 0.75); b.location = f["root"].location + Vector((-0.05, 0.25, 0.45))
    return upd


def o7(rng):            # The dog didn't say anything. He just looked at the turkey.: the dog on the empty chair, eyes on the turkey
    fam = dinner(rng); x, y = SEATS["L3"]; d = dog((x + 0.05, y, 0.3), rot=math.pi / 2)
    c = _cam((0.25, 0.95, 0.9), (x, y, 0.72), lens=46, fstop=2.2)
    def upd(t):
        d["tail"].rotation_euler[1] = 0.6 * math.sin(t * 14)
        d["head"].rotation_euler[0] = 0.25 * smooth((t - 1.2) / 0.6)              # head tilts down to the turkey
        look_at(c, Vector((x, y, 0.72)).lerp(Vector((0.0, 0.75, 0.6)), smooth((t - 2.2) / 0.8)))
    return upd


def o8(rng):            # Your turn. One word.: everyone turns to look at the camera
    fam = dinner(rng); d = dog((SEATS["L3"][0] + 0.05, SEATS["L3"][1], 0.3), rot=math.pi / 2)
    c = _cam((0.0, -1.3, 1.0), (0, 0.9, 0.75), lens=30, fstop=4)
    def upd(t):
        k = smooth(t / 0.5)
        for nm, f in fam.items():
            base = SEAT[nm][1]; f["head"].rotation_euler[2] = -base * 0.45 * k
        d["tail"].rotation_euler[1] = 0.6 * math.sin(t * 14)
    return upd


SHOTS = {n: (globals()[n], _D[n]) for n in _D}
