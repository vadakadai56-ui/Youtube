"""Edit settings for The Last Door (format 1, emotional twist, clay characters, advent).
Warm candlelit room tone and a crackling fire, a slow music box that moves from minor to major at "It was always yours",
a little wooden click for every door, a key jingle, the shed door creak. 1 to 3 word captions, yellow keywords."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
_D = json.load(open(os.path.join(HERE, "durations.json")))
CUTS, _t = [], 0.0
for _n, _d in _D.items():
    CUTS.append((round(_t, 2), _n)); _t += _d
CUTS.append((round(_t, 2), "END"))
T_END = round(_t + 3.6, 2)
XFADE = {"d2": 0.4, "d7": 0.5, "d12": 0.5}
CAPTION = {"words": 3, "y": 1240, "size": 92}
KEY = {"twenty-five", "last", "eleven", '"not', 'yet,"', "yours.\"", "key.", "shed.\"", "name,", '"your', 'turn.'}
END_LINES = [("Who would you make one for?", 60, 900, (255, 255, 255), True, 0.2),
             ("D U S T L I G H T", 56, 1100, (255, 236, 200), False, 1.0)]
SR = 44100
C = {n: t for t, n in CUTS}


def sound(S):
    S.sample("ambience/fire", 0.0, C["d7"], g=0.07, pick=0)
    S.sample("ambience/room", 0.0, C["END"] + 3, g=0.04, pick=0)
    S.sample("ambience/wind", C["d12"], C["END"] + 3 - C["d12"], g=0.05, pick=0)
    minor = [69, 72, 76, 74, 72, 71, 72, 69]; major = [72, 76, 79, 77, 76, 74, 76, 72]
    t, k = 0.4, 0
    while t < C["END"]:
        tune = minor if t < C["d9"] + 1.7 else major
        S.add(S.bell(S.note(tune[k % 8]), 1.6), t, 0.04); t += 0.8; k += 1
    S.add(S.pad([220, 261.6, 329.6], C["d9"] + 1.7, 2.0, 2.0), 0.0, 0.035)
    S.add(S.pad([261.6, 329.6, 392.0], C["END"] - C["d9"] - 1.7 + 3, 2.0, 2.5), C["d9"] + 1.7, 0.05)
    for off in (3.16, 4.26, 5.3): S.knock(C["d3"] + off, 0.18)                       # the little doors
    for off in (3.8, 4.1, 4.4): S.knock(C["d4"] + off, 0.12)                          # tap tap tap
    S.knock(C["d10"] + 0.4, 0.2)
    for j in range(4): S.add(S.bell(S.note(98 + j % 2), 0.2), C["d10"] + 1.3 + j * 0.09, 0.04)   # key jingle
    S.sample("foley/door", C["d12"] + 0.05, 1.5, g=0.35, pick=1, fade=0.02)
    S.sample("foley/footsteps", C["d8"], _D["d8"], g=0.2, pick=0)
