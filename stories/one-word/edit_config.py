"""Edit settings for One Word (Trend Short, Thanksgiving Day, blocky family).
Each thankful word lands as one huge caption; warm candlelit room tone, cutlery, a soft music box, a single bark-like "boop"
for the dog's silence, and a warm chord on "Your turn"."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
_D = json.load(open(os.path.join(HERE, "durations.json")))
CUTS, _t = [], 0.0
for _n, _d in _D.items():
    CUTS.append((round(_t, 2), _n)); _t += _d
CUTS.append((round(_t, 2), "END"))
T_END = round(_t + 3.2, 2)
XFADE = {}
STEP = {"o2", "o3", "o4", "o5", "o6", "o8"}   # waves and fist pumps: hold frames, no blending
CAPTION = {"words": 2, "y": 1240, "size": 104}
KEY = {'"family."', '"football."', '"dishwasher."', '"wi-fi."', '"huss."', "turkey.", "one", "word."}
END_LINES = [("What's your one word?", 64, 900, (255, 255, 255), True, 0.2),
             ("D U S T L I G H T", 56, 1100, (255, 236, 200), False, 1.0)]
SR = 44100
C = {n: t for t, n in CUTS}


def sound(S):
    S.sample("ambience/room", 0.0, C["END"] + 3, g=0.06, pick=0)
    S.sample("ambience/fire", 0.0, C["END"] + 3, g=0.04, pick=0)
    S.sample("foley/kitchen", 0.3, 4.5, g=0.08, pick=0)                       # cutlery under the opening
    tune = [72, 74, 76, 79, 76, 74, 72, 67]
    for i, m in enumerate(tune * 3): S.add(S.bell(S.note(m), 1.2), 0.3 + i * 0.75, 0.035)
    for sh in ("o2", "o3", "o4", "o5", "o6"): S.add(S.bell(S.note(84), 0.6), C[sh] + 0.05, 0.05)   # a ding for each word
    S.add(S.bell(S.note(60), 0.4), C["o7"] + 1.8, 0.06)                        # the dog's silent "boop"
    S.add(S.pad([261.6, 329.6, 392.0], 3.5, 0.2, 1.8), C["o8"], 0.07)

REHOOK = (dict((n, t) for t, n in CUTS)["o5"] + 0.2, "Wait for the dog…")
HOOK = "Everyone says 'family'. Nobody says this."
