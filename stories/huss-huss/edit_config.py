"""Edit settings for Huss Huss (Trend Short, blocky characters).
One huge word at a time in the top third, "HUSS" in yellow. A real thud on every bounce, a quiet snowy night under everything,
warm table chatter in the window shot, a door creak, then a bouncy little tune for the payoff."""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
_D = json.load(open(os.path.join(HERE, "durations.json")))
CUTS, _t = [], 0.0
for _n, _d in _D.items():
    CUTS.append((round(_t, 2), _n)); _t += _d
CUTS.append((round(_t, 2), "END"))
T_END = round(_t + 3.2, 2)
XFADE = {}
CAPTION = {"words": 1, "y": 560, "size": 150}
KEY = {"huss", "thanksgiving", "except", "grandma", "slippers", "ball", "nobody"}
END_LINES = [("Who's your huss huss person?", 60, 900, (255, 255, 255), True, 0.2),
             ("D U S T L I G H T", 56, 1100, (255, 236, 200), False, 1.0)]
SR = 44100
C = {n: t for t, n in CUTS}
_W = json.load(open(os.path.join(HERE, "words.json")))
HITS = [a + 0.08 for w, a, b in _W if w.lower().startswith("huss")]


def bounce(S, t, g=0.55):
    """Basketball on packed snow: a low thud plus a short rubbery ring."""
    S.knock(t, g)
    n = int(0.12 * SR); x = np.arange(n) / SR
    S.add(np.sin(2 * np.pi * 210 * x) * np.exp(-x * 45), t, g * 0.35)


def sound(S):
    S.sample("ambience/wind", 0.0, C["END"] + 3, g=0.05, pick=1)
    S.sample("ambience/night", 0.0, C["END"] + 3, g=0.04, pick=0)
    for h in HITS: bounce(S, h)
    for k in range(3): bounce(S, C["h1"] + 0.4 + k * 0.9, g=0.18)            # far away, in the first wide shot
    S.sample("ambience/room", C["h4"], _D["h4"], g=0.12, pick=0)              # warm room tone at the table
    S.sample("foley/kitchen", C["h4"], _D["h4"], g=0.10, pick=0)              # plates and cutlery
    S.sample("foley/door", C["h6"] + 0.15, 1.4, g=0.4, pick=0, fade=0.02)
    S.sample("foley/footsteps", C["h7"], _D["h7"], g=0.25, pick=1)            # slippers on snow
    S.sample("transitions/whoosh", C["h8"] + 0.45, 0.5, g=0.35, pick=0, fade=0.02)   # the steal
    S.sample("transitions/hit", C["h9"] + 1.65, 0.8, g=0.35, pick=1, fade=0.01)      # the big HUSS
    # the payoff: a bouncy little tune on top of the family game
    for i, m in enumerate([67, 71, 74, 79, 74, 79, 83]):
        S.add(S.bell(S.note(m), 0.9), C["h10"] + 0.2 + i * 0.32, 0.06)
    S.add(S.pad([196, 246.9, 293.7], 4.0, 0.4, 2.0), C["h10"], 0.05)
