"""Edit settings for The Empty Swing (used by pipeline/edit.py)."""
import json, os
import numpy as np

_D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "durations.json")))
CUTS, _t = [], 0.0
for _n, _d in _D.items():
    CUTS.append((round(_t, 2), _n)); _t += _d
CUTS.append((round(_t, 2), "END"))                     # 67.5
T_END = round(_t + 4.2, 2)
XFADE = {"s13": 0.4, "s19": 0.5}
KEY = {"six", "same swing", "no one", "higher", "pull their children", "before", "rains", "snows", "six o'clock",
       "one hundred and twelve days", "across the road", "children's hospital", "third window", "lily", "glass",
       "not yet", "swing fly", "daddy", "spring", "empty", "finally outside", "all by herself"}
END_LINES = [("Some people keep your seat warm", 62, 880, (255, 255, 255), True, 0.2),
             ("until you come back.", 62, 965, (255, 255, 255), True, 0.2),
             ("D U S T L I G H T", 56, 1160, (255, 236, 200), False, 1.4)]
SR = 44100


def creak(S, t, g=0.05):
    """The swing's chain squeaking at the top of each push."""
    n = int(0.28 * SR); x = np.arange(n) / SR
    f = 820 + 260 * np.sin(x * 22)
    sig = np.sin(2 * np.pi * np.cumsum(f) / SR) * S.env(n, 0.02, 0.15) * (0.6 + 0.4 * np.sin(x * 90))
    S.add(sig, t, g)


def birds(S, start, dur, g=0.03):
    for k in range(int(dur / 0.7)):
        t = start + k * 0.7 + S.rng.uniform(0, 0.4); n = int(0.12 * SR); x = np.arange(n) / SR
        f0 = S.rng.uniform(2600, 3800)
        S.add(np.sin(2 * np.pi * np.cumsum(f0 + 900 * np.sin(x * 60)) / SR) * S.env(n, 0.005, 0.05), t, g)


def sound(S):
    n = S.note
    cut = {name: t for t, name in CUTS}
    # sad A-minor piano through the empty-swing half
    S.chords([(57, 64, 69, 72), (53, 60, 65, 69), (50, 57, 62, 65), (52, 59, 64, 68)], 0.3, 31.4, step=3.4, bass=0.12, top=0.065)
    S.add(S.pad([110, 164.8], 31.6, 3, 2), 0.0, 0.06)
    for t in np.arange(cut["s3"] + 0.55, cut["s12"] + 2.5, 2.2): creak(S, t)           # squeak on every push
    S.add(S.noise(cut["s9"] - cut["s8"] + 0.5, 3) * 0.6 * S.env(int((cut["s9"] - cut["s8"] + 0.5) * SR), 0.2, 0.3), cut["s8"], 0.12)   # rain
    S.wind(cut["s9"], 2.6, 0.07); S.wind(cut["s11"], 3.0, 0.05)                         # snow wind, autumn wind
    for k in range(6): S.add(S.bell(n(84 + (k % 2) * 3), 2.0), cut["s10"] + 0.5 + k * 0.55, 0.018)   # distant clock chimes
    S.add(S.piano(n(76), 4.0), cut["s12"] + 0.1, 0.11)                                  # the turn: one held note
    S.add(S.pad([220, 329.6], 4.5, 1.0, 1.5), cut["s12"], 0.07)
    # hope: music box over soft major chords while we meet Lily
    S.chords([(57, 61, 64, 69), (54, 57, 61, 66), (50, 54, 57, 62), (52, 56, 59, 64)], cut["s13"], cut["s19"], step=3.0, bass=0.1, top=0.06)
    mel = [69, 73, 76, 73, 74, 71, 69, 71, 73, 69, 66, 69, 71, 73, 76, 81]
    for i, m in enumerate(mel):
        t = cut["s14"] + i * 0.7
        if t < cut["s19"] - 0.3: S.add(S.bell(n(m + 12), 1.6), t, 0.05)
    for t in np.arange(cut["s16"] + 0.4, cut["s19"], 2.2): creak(S, t, 0.03)            # her swing, far below
    # the empty window: almost silence
    S.add(S.pad([55, 82.4], cut["s20"] - cut["s19"] + 0.3, 1.0, 0.6), cut["s19"], 0.1)
    # she's outside: warm swell, birdsong, the swing again
    S.chords([(57, 64, 69, 73), (54, 61, 66, 69), (50, 57, 62, 66), (52, 59, 64, 68)], cut["s20"], cut["END"] + 0.5, step=2.6, bass=0.14, top=0.085)
    S.add(S.pad([220, 277.2, 329.6, 440], cut["END"] - cut["s20"] + 1.5, 0.8, 1.5), cut["s20"], 0.1)
    birds(S, cut["s20"], cut["END"] - cut["s20"])
    for t in np.arange(cut["s22"] + 0.55, cut["END"], 2.2): creak(S, t, 0.04)
    for i, m in enumerate([69, 73, 76, 81, 85]): S.add(S.piano(n(m), 3.5), cut["END"] + 0.1 + i * 0.5, 0.08)
    S.add(S.pad([220, 277.2, 329.6], 4.0, 0.5, 2.5), cut["END"] + 0.1, 0.08)
