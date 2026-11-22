"""Edit settings for Same Window (Trend Short, "Same Spot, Years Apart", peg dolls).
Two-word captions, years in yellow. A train rumble and wheel clack for every train, a soft music box that grows warmer each year,
and a full major chord when the whole train waves back."""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
_D = json.load(open(os.path.join(HERE, "durations.json")))
CUTS, _t = [], 0.0
for _n, _d in _D.items():
    CUTS.append((round(_t, 2), _n)); _t += _d
CUTS.append((round(_t, 2), "END"))
T_END = round(_t + 3.4, 2)
XFADE = {"w2": 0.25, "w3": 0.25, "w4": 0.25, "w5": 0.25}
CAPTION = {"words": 2, "y": 1240, "size": 100}
KEY = {"1956.", "1975.", "2001.", "2026.", "seventy", "waves", "back.", "anyway."}
END_LINES = [("Who would you wave at?", 64, 900, (255, 255, 255), True, 0.2),
             ("D U S T L I G H T", 56, 1100, (255, 236, 200), False, 1.0)]
SR = 44100
C = {n: t for t, n in CUTS}


def train_pass(S, t, dur, g=0.12):
    """Low rumble that swells and fades, with a da-dum da-dum wheel clack."""
    n = int(dur * SR); x = np.arange(n) / SR
    S.add(S.noise(dur, 120) * np.sin(np.pi * x / dur) ** 1.5, t, g)
    k = 0.0
    while k < dur - 0.3:
        S.knock(t + k, g * 0.9 * np.sin(np.pi * k / dur) ** 1.2); S.knock(t + k + 0.14, g * 0.7 * np.sin(np.pi * k / dur) ** 1.2)
        k += 0.55


def sound(S):
    S.sample("ambience/wind", 0.0, C["END"] + 3, g=0.04, pick=0)
    S.sample("ambience/rain", C["w4"], _D["w4"], g=0.10, pick=0)
    for sh, off in (("w2", 0.2), ("w3", 0.2), ("w4", 0.2), ("w5", 2.0)):
        train_pass(S, C[sh] + off, min(_D[sh] - off, 4.5))
    train_pass(S, C["w6"], _D["w6"] + 1.0, g=0.08)
    # music box: the same little tune once per year, a bit lower and warmer each time
    tune = [76, 79, 81, 79, 76, 74, 76]
    for i, sh in enumerate(["w1", "w2", "w3", "w4", "w5"]):
        for j, m in enumerate(tune):
            S.add(S.bell(S.note(m - 2 * i), 1.4), C[sh] + 0.4 + j * 0.42, 0.045)
    S.add(S.pad([261.6, 329.6, 392.0, 523.3], 6.0, 0.6, 2.5), C["w6"] + 0.2, 0.08)
    for j, m in enumerate([72, 76, 79, 84, 88]):
        S.add(S.bell(S.note(m), 1.8), C["w6"] + 0.6 + j * 0.3, 0.06)
