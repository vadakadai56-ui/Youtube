"""Edit settings for How a Frozen River Becomes a Hotel (used by pipeline/edit.py)."""
import json, os
import numpy as np

_D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "durations.json")))
CUTS, _t = [], 0.0
for _n, _d in _D.items():
    CUTS.append((round(_t, 2), _n)); _t += _d
CUTS.append((round(_t, 2), "END"))                      # 46.65
T_END = round(_t + 4.0, 2)
XFADE = {"s3": 0.3, "s16": 0.5, "s20": 0.4}
KEY = {"winter", "hotel", "frozen river", "spring", "melts", "march", "blocks", "fridge", "summer", "freezer",
       "november", "cold", "builders", "snow", "ice", "steel moulds", "artists", "by hand", "bed", "glasses",
       "below freezing", "all night", "drip", "sag", "river", "next march", "all over again"}
END_LINES = [("It melts every spring.", 62, 880, (255, 255, 255), True, 0.2),
             ("It comes back every winter.", 62, 965, (255, 255, 255), True, 0.6),
             ("D U S T L I G H T", 56, 1160, (210, 230, 255), False, 1.4)]
SR = 44100


def saw_strokes(S, start, dur, g=0.05):
    """Rhythmic saw rasp: band of noise pulsing about 4.5 times a second."""
    n = int(dur * SR); x = np.arange(n) / SR
    sig = S.noise(dur, 3) * (0.5 + 0.5 * np.abs(np.sin(np.pi * 4.5 * x))) * S.env(n, 0.05, 0.2)
    S.add(sig, start, g)


def hiss(S, start, dur, g=0.04):
    n = int(dur * SR); S.add(S.noise(dur, 2) * S.env(n, 0.3, 0.6), start, g)


def drip(S, t, g=0.05, f=1800):
    n = int(0.18 * SR); x = np.arange(n) / SR
    S.add(np.sin(2 * np.pi * (f + 1400 * np.exp(-x * 40)) * x) * np.exp(-x * 30), t, g)


def crack(S, t, g=0.2):
    n = int(0.4 * SR); x = np.arange(n) / SR
    S.add((S.noise(0.4, 2) * np.exp(-x * 18) + np.sin(2 * np.pi * 70 * x) * np.exp(-x * 9) * 0.6), t, g)


def sound(S):
    n = S.note
    cut = {name: t for t, name in CUTS}
    end = cut["END"]
    # winter wonder: soft D-major / B-minor piano under the whole build, music-box sparkle on top
    S.add(S.pad([73.4, 110.0, 146.8], end + 3.5, 2.0, 3.0), 0.0, 0.07)
    S.chords([(62, 66, 69, 74), (59, 62, 66, 71), (55, 59, 62, 67), (57, 61, 64, 69)], 0.2, cut["s16"], step=2.4, bass=0.1, top=0.06)
    mel = [74, 78, 81, 78, 76, 74, 76, 78, 81, 83, 81, 78, 76, 74, 73, 74]
    for i, m in enumerate(mel):
        t = 0.3 + i * 1.2
        if t < cut["s15"]: S.add(S.bell(n(m + 12), 1.4), t, 0.035)
    S.wind(0.0, 5.0, 0.05)
    crack(S, cut["s3"] + 0.6, 0.18)                                      # the melt in the opening
    saw_strokes(S, cut["s4"] + 0.1, cut["s5"] - cut["s4"] - 0.1, 0.05)    # March: sawing
    S.knock(cut["s5"] + 0.3, 0.25)                                       # block lifts
    S.add(S.pad([220, 277.2], cut["s8"] - cut["s6"], 0.5, 0.8), cut["s6"], 0.03)   # freezer hum
    S.wind(cut["s8"], 3.0, 0.06)                                         # November wind
    S.steps(cut["s9"] + 0.2, 10, every=0.32, g=0.2)                      # builders on snow
    hiss(S, cut["s10"] + 0.2, cut["s11"] - cut["s10"] - 0.3, 0.05)       # snow cannon spray
    S.ticks(cut["s11"] + 0.1, 5, every=0.25, g=0.35)                     # chisel
    for k in range(3): S.add(S.bell(n(93 + 3 * k), 1.0), cut["s12"] + 0.2 + k * 0.5, 0.03)   # glassy clinks
    for k in range(2): S.add(S.bell(n(96), 0.8), cut["s13"] + 0.3 + k * 0.45, 0.04)
    S.wind(cut["s14"], cut["s16"] - cut["s14"], 0.04)                    # cold night
    # spring: the chords turn, drips, the melt
    S.chords([(55, 59, 62, 67), (57, 61, 64, 69), (62, 66, 69, 74), (59, 62, 66, 71)], cut["s16"], end + 0.5, step=2.0, bass=0.12, top=0.07)
    for k in range(14): drip(S, cut["s17"] + 0.15 + k * 0.28 + 0.05 * (k % 3), 0.04, 1500 + 200 * (k % 4))
    crack(S, cut["s18"] + 0.4, 0.15)
    S.add(S.noise(cut["s20"] - cut["s19"] + 0.4, 60) * 3 * S.env(int((cut["s20"] - cut["s19"] + 0.4) * SR), 0.2, 0.3), cut["s19"], 0.08)  # rushing water
    saw_strokes(S, cut["s20"] + 1.0, 0.6, 0.06)                          # and it starts again
    S.add(S.bell(n(86), 2.5), end + 0.1, 0.06); S.add(S.bell(n(90), 2.5), end + 0.5, 0.05); S.add(S.bell(n(93), 3.0), end + 0.9, 0.05)
