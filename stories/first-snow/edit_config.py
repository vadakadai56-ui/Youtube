"""Edit settings for First Snow (Trend Short, clay characters).
Two-word captions; snowy wind, a sleigh-bell tune, a whoosh down the hill, a ding for the tea-tray reveal."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
_D = json.load(open(os.path.join(HERE, "durations.json")))
CUTS, _t = [], 0.0
for _n, _d in _D.items():
    CUTS.append((round(_t, 2), _n)); _t += _d
CUTS.append((round(_t, 2), "END"))
T_END = round(_t + 3.2, 2)
XFADE = {}
CAPTION = {"words": 2, "y": 1240, "size": 100}
KEY = {"snow", "sledge", "race.", "grandma", "wins.", "tea", "tray."}
END_LINES = [("What's your first-snow tradition?", 56, 900, (255, 255, 255), True, 0.2),
             ("D U S T L I G H T", 56, 1100, (255, 236, 200), False, 1.0)]
SR = 44100
C = {n: t for t, n in CUTS}


def sound(S):
    S.sample("ambience/wind", 0.0, C["END"] + 3, g=0.06, pick=1)
    tune = [76, 76, 76, 76, 76, 76, 76, 79, 72, 74, 76, 77, 77, 77, 77, 77, 76, 76]
    for i, m in enumerate(tune): S.add(S.bell(S.note(m), 0.6), 0.2 + i * 0.3, 0.035)
    S.sample("transitions/whoosh", C["f4"] + 0.3, 1.5, g=0.35, pick=0); S.sample("transitions/whoosh", C["f4"] + 1.2, 1.2, g=0.3, pick=2)
    S.sample("foley/kitchen", C["f5"] + 0.3, 0.6, g=0.2, pick=0)                  # a teacup clink
    S.add(S.pad([220, 261.6, 329.6], C["f7"] - C["f6"], 0.3, 0.5), C["f6"], 0.04)   # spying
    for j, m in enumerate([84, 88, 91]): S.add(S.bell(S.note(m), 0.8), C["f8"] + 0.05 + j * 0.1, 0.07)
    S.sample("transitions/whoosh", C["f8"] + 0.6, 1.2, g=0.35, pick=1)
    S.add(S.pad([261.6, 329.6, 392.0, 523.3], 3.5, 0.2, 2.0), C["END"] - 0.5, 0.06)
HOOK = "Grandma wins this race every year. Nobody knows how."
