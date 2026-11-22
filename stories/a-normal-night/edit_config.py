"""Edit settings for A Normal Night (format 2, anticlimax POV).
One huge caption word at a time in the top third. Each scare: a low drone and a horror sting. Each reveal: silence, then a dry
comic "deflate". Real CC0 sounds from the Dustlight library for the door, the cat's world, the snow, the street and the phone room."""
import json, os
import numpy as np

_D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "durations.json")))
CUTS, _t = [], 0.0
for _n, _d in _D.items():
    CUTS.append((round(_t, 2), _n)); _t += _d
CUTS.append((round(_t, 2), "END"))                     # 56.0
T_END = round(_t + 3.6, 2)
XFADE = {}
CAPTION = {"words": 1, "y": 560, "size": 150}
KEY = {"terrifying", "cat", "snowman", "snow", "dad", "grandma", "scissors", "normal"}
END_LINES = [("Just another normal night.", 64, 900, (255, 255, 255), True, 0.2),
             ("D U S T L I G H T", 56, 1100, (255, 236, 200), False, 1.0)]
SR = 44100
C = {n: t for t, n in CUTS}
SCARES = ["n1", "n2", "n6", "n9", "n12", "n13", "n15"]
REVEALS = ["n5", "n8", "n11", "n14", "n18"]


def sting(S, t, g=0.16):
    """Horror sting: a rising dissonant cluster that cuts off."""
    n = int(0.9 * SR); x = np.arange(n) / SR
    sig = sum(np.sin(2 * np.pi * f * (1 + 0.15 * x) * x) for f in (311, 330, 466, 494)) / 4
    S.add(sig * np.linspace(0.2, 1, n) * S.env(n, 0.05, 0.02), t, g)


def drone(S, t, dur, g=0.07):
    S.add(S.pad([55, 58.3], dur, 0.6, 0.3), t, g)


def deflate(S, t, g=0.18):
    """A dry comic 'wah': a soft tone sliding down."""
    n = int(0.45 * SR); x = np.arange(n) / SR
    f = 520 * np.exp(-x * 2.2)
    S.add(np.sin(2 * np.pi * np.cumsum(f) / SR) * S.env(n, 0.01, 0.12), t, g)


def ring(S, t, n=3, g=0.12):
    for k in range(n):
        m = int(1.0 * SR); x = np.arange(m) / SR
        tone = (np.sin(2 * np.pi * 440 * x) + np.sin(2 * np.pi * 480 * x)) * (np.sin(2 * np.pi * 20 * x) > 0)
        S.add(tone * S.env(m, 0.01, 0.05), t + k * 1.6, g)


def sound(S):
    # the house at night: wind and a clock under everything
    S.sample("ambience/wind", 0.0, C["END"], g=0.06, pick=0)
    S.sample("ambience/room", 0.0, C["END"], g=0.05, pick=0)
    for sh in SCARES:
        drone(S, C[sh], _D[sh] + 0.2)
        sting(S, C[sh] + 0.15)
    for sh in REVEALS:
        deflate(S, C[sh] + 0.35)
    # story sounds
    for k in range(6): S.add(S.noise(0.18, 900) * S.env(int(0.18 * SR), 0.01, 0.1), C["n2"] + 0.6 + k * 0.45, 0.08)   # scratching
    for k in range(8): S.add(S.noise(0.16, 900) * S.env(int(0.16 * SR), 0.01, 0.1), C["n3"] + 0.4 + k * 0.5, 0.08)
    S.sample("foley/door", C["n4"], 1.2, g=0.35, pick=1, fade=0.02)                       # the creak as it opens
    S.sample("foley/footsteps", C["n9"] + 0.5, 3.2, g=0.4, pick=2)                         # heavy steps above
    S.sample("transitions/hit", C["n10"] + 0.4, 1.0, g=0.6, pick=0, fade=0.01)             # the crash
    S.sample("foley/footsteps", C["n13"], _D["n13"], g=0.25, pick=1)                       # steps in the snow
    ring(S, C["n15"] + 0.2)
    S.sample("human/breath", C["n16"] + 1.0, 2.0, g=0.3, pick=1)
    # the deadpan sign-off: a tiny cheerful tune
    for i, m in enumerate([72, 76, 79, 84]): S.add(S.bell(S.note(m), 1.2), C["n19"] + 0.6 + i * 0.25, 0.05)
    S.add(S.pad([261.6, 329.6, 392], 3.0, 0.3, 1.5), C["END"], 0.05)
