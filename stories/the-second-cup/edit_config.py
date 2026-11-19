"""Edit settings for The Second Cup (used by pipeline/edit.py)."""
import numpy as np

CUTS = [(0.0, "k1"), (4.4, "k2"), (7.25, "k3"), (9.8, "k4"), (13.2, "k5"), (18.55, "k6"), (23.3, "k7"), (27.2, "k8"), (29.9, "k9"),
        (34.7, "k10"), (39.1, "k11"), (43.15, "k12"), (47.0, "k13"), (49.05, "k14"), (52.8, "k15"), (56.0, "k16"), (59.4, "k17"), (64.9, "END")]
T_END = 68.6
XFADE = {"k14": 0.35, "k16": 0.3}
KEY = {"two cups", "rose", "empty", "goes cold", "poor walter", "coming home", "flask", "two miles", "nobody", "care home",
       "doesn't know", "good morning", "have we met", "not yet", "forgets him", "fall in love", "blushes", "marry him"}
END_LINES = [("Some people are worth", 70, 880, (255, 255, 255), True, 0.2),
             ("remembering twice.", 70, 975, (255, 255, 255), True, 0.2),
             ("D U S T L I G H T", 56, 1160, (255, 236, 200), False, 1.4)]


def sound(S):
    n = S.note
    S.chords([(57, 64, 69, 72), (53, 60, 65, 69), (55, 62, 67, 71), (52, 59, 64, 67)], 0.2, 39.0, step=3.2, bass=0.12, top=0.07)   # sad A minor
    S.add(S.pad([110, 164.8], 39.0, 3, 3), 0.0, 0.06)
    S.ticks(9.9, 10)                                                     # clock ticks while her tea cools
    S.add(S.noise(1.2, 30) * S.env(int(1.2 * 44100), 0.1, 0.8), 18.7, 0.15)   # pouring
    S.steps(23.5, 14); S.wind(23.3, 12.0)                                # walking through the snow
    for k in range(3): S.add(S.piano(n(88 - k * 4), 1.2), 34.6 + k * 0.18, 0.04)   # door chime
    S.chords([(57, 61, 64, 69), (54, 57, 61, 66), (50, 54, 57, 62), (52, 56, 59, 64)], 39.1, 64.9, step=3.0)                    # warm turn: A major
    for i, m in enumerate([76, 78, 81, 80, 78, 76, 73, 76, 78, 76, 74, 73, 71, 73, 76, 81]):
        if 52.6 + i * 0.75 < 64.5: S.add(S.piano(n(m), 2.0), 52.6 + i * 0.75, 0.06)
    S.add(S.pad([220, 277.2, 329.6, 440], 26.0, 3, 3), 39.0, 0.08)
    for i, m in enumerate([69, 73, 76, 81, 85]): S.add(S.piano(n(m), 3.5), 64.9 + i * 0.5, 0.08)   # end card
    S.add(S.pad([220, 277.2, 329.6], 4.0, 0.5, 2.5), 65.0, 0.08)
