"""One Word (Trend Short, Thanksgiving Day): everyone says what they are thankful for in one word; the dog just looks at
the turkey. v2 (23 Nov 2026): the family are the ready-made Quaternius people (owner: human-like people in every video), toon look.
Render: STYLE=toon TOON_STEP=0.03 TOON_LINES=0 ENGINE=EEVEE PCT=50 ES=8 $VENV/bin/python pipeline/anim.py stories/one-word OUT all"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
os.environ.setdefault("STYLE", "toon")
import scene                  # noqa
scene.STYLE = os.environ["STYLE"]
from world import *           # noqa
from world import cam as _cam
from characters import ball, dog, person, pose, play
import bpy
scene.LOOK = os.environ.get("LOOK") or "comedy"      # per-video grade (scene.LOOKS)

_D = json.load(open(os.path.join(HERE, "durations.json")))
CAST = {"gran": ("W_Formal", "old"), "dad": ("M_Casual_2", "adult"), "mum": ("W_Casual", "adult"),
        "sis": ("W_Adventurer", "kid"), "kid": ("M_Casual_Hoodie", "kid")}
SEAT = {"gran": ("HEAD", 0.0), "dad": ("L1", math.pi / 2), "mum": ("R1", -math.pi / 2), "sis": ("L2", math.pi / 2), "kid": ("R2", -math.pi / 2)}


def dinner(rng):
    """The Thanksgiving table with the family seated (each on a chair, facing the table). Returns {name: person}."""
    dining_room(rng, outside="snow", card=False, food=True)
    light("AREA", (0, 0.9, 2.2), 260, col=(1.0, 0.86, 0.7), size=1.8, target=(0, 0.9, 0.6))      # warm lamp over the table:
    light("AREA", (0, -1.6, 1.4), 90, col=(0.85, 0.9, 1.0), size=2.5, target=(0, 0.6, 0.7))    # the room is candle-dark
    fam = {}
    for i, (nm, (model, age)) in enumerate(CAST.items()):
        seat, rot = SEAT[nm]; x, y = SEATS[seat]
        x += -0.12 if x < 0 else 0.12 if x > 0 else 0; y += 0.12 if seat == "HEAD" else 0      # where dining_room put the chair
        f = person(model, (x, y, 0), rot=rot, age=age, action="Idle", offset=i * 0.37, h=0.66); pose(f, "sit")   # 0.66: heads well above the table
        fam[nm] = f
    return fam


def hand(f, side="R"):
    """World position of a person's hand right now (props follow it)."""
    bpy.context.view_layer.update(); a = f["arm"]
    return a.matrix_world @ a.pose.bones["Wrist." + side].head


# ---------------------------------------------------------------- shots
def o1(rng):            # Thanksgiving rule in our house. Say what you're thankful for. One word only.: the whole table, push in
    fam = dinner(rng); c = _cam((0.0, -1.7, 1.45), (0, 0.95, 0.6), lens=28, fstop=5)
    def upd(t): c.location.y = -1.7 + 0.12 * t
    return upd


def close(name, look, clip, lens=46):
    """Close on one person, who plays clip (their gesture) for the whole shot."""
    def shot(rng):
        fam = dinner(rng); f = fam[name]; play(f, clip); x, y = f["root"].location.x, f["root"].location.y
        c = _cam(look, (x, y, 0.8), lens=lens, fstop=2.2)
        def upd(t): c.location.y = look[1] + 0.03 * t
        return upd
    return shot


o2 = close("gran", (0.55, 0.95, 0.95), "Wave")                               # to the side, past the candles                                 # "Family."
o3 = close("dad", (0.25, -0.45, 1.05), "Punch_Right")                         # "Football." (a fist pump)
o4 = close("mum", (-0.25, -0.45, 1.05), "Interact")                           # "Dishwasher."


def o5(rng):            # My sister. "Wi-Fi.": she holds up her phone, glowing
    fam = dinner(rng); f = fam["sis"]; play(f, "Idle_Gun_Pointing"); x, y = f["root"].location.x, f["root"].location.y
    ph = cube((0, 0, 0), (0.05, 0.008, 0.09), mat("sisphone", (0.6, 0.8, 1.0), 0.2, emit=(0.6, 0.8, 1.0), emit_str=2.5))
    c = _cam((0.2, 0.25, 1.05), (x, y, 0.75), lens=46, fstop=2.2)
    def upd(t): ph.location = hand(f); ph.rotation_euler = (0, 0, -math.pi / 2)
    return upd


def o6(rng):            # Me? "Huss.": deadpan, the ball under one arm
    fam = dinner(rng); f = fam["kid"]; b = ball((0, 0, 0), r=0.06)
    c = _cam((-0.2, 0.25, 1.05), (f["root"].location.x, f["root"].location.y, 0.75), lens=46, fstop=2.2)
    def upd(t): b.location = hand(f, "L") + Vector((0, 0, 0.05))
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
    c = _cam((0.0, -1.4, 1.25), (0, 0.9, 0.75), lens=30, fstop=4)
    for i, f in enumerate(fam.values()): play(f, "Wave", offset=i * 0.2)        # everyone waves at you
    def upd(t): d["tail"].rotation_euler[1] = 0.6 * math.sin(t * 14)
    return upd


SHOTS = {n: (globals()[n], _D[n]) for n in _D}
