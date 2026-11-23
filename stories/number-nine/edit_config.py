"""Edit settings for Number Nine (Trend Short, Christmas kickoff, clay characters).
Two-word captions, the times in yellow. Snowy night wind, a soft sleigh-bell music bed that goes quiet at "Except number nine",
a switch click at 6:00 and a big warm chord with sparkles as the whole street lights up."""
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
KEY = {"christmas", "lights", "nine.", "alone.", "5:59...", "6:00.", "first.", "ladder's"}
END_LINES = [("Who's your number nine?", 64, 900, (255, 255, 255), True, 0.2),
             ("D U S T L I G H T", 56, 1100, (255, 236, 200), False, 1.0)]
SR = 44100
C = {n: t for t, n in CUTS}


def sound(S):
    S.sample("ambience/wind", 0.0, C["END"] + 3, g=0.06, pick=1)
    tune = [76, 76, 76, 76, 76, 76, 76, 79, 72, 74, 76]                   # a little sleigh-bell figure
    for i, m in enumerate(tune * 2):
        t = 0.3 + i * 0.32
        if t < C["n3"]: S.add(S.bell(S.note(m), 0.6), t, 0.035)
    S.add(S.pad([220, 261.6, 329.6], C["n6"] - C["n3"], 0.8, 1.2), C["n3"], 0.04)   # quiet, a bit sad
    S.knock(C["n6"] + 0.55, 0.35)                                               # the plug clicks in
    S.add(S.pad([261.6, 329.6, 392.0, 523.3], 5.0, 0.05, 2.5), C["n7"], 0.09)
    for j, m in enumerate([84, 88, 91, 96, 91, 96, 100]): S.add(S.bell(S.note(m), 1.0), C["n7"] + 0.05 + j * 0.12, 0.05)
    for i, m in enumerate([72, 76, 79, 84]): S.add(S.bell(S.note(m), 1.4), C["n8"] + 0.2 + i * 0.25, 0.05)

REHOOK = (dict((n, t) for t, n in CUTS)["n3"] + 0.2, "Wait for six o'clock…")
HOOK = "Is it possible to light a whole street in one minute?"
