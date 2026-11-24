"""Move each spoken phrase of audio/grown-up.mp3 onto the reference edit's beat times.
Writes audio/grown-up-placed.wav and stories/grown-up/words_placed.json."""
import json, subprocess, numpy as np
SR = 48000
src = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", "audio/grown-up.mp3", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                                   capture_output=True, check=True).stdout, np.float32)
words = json.load(open("stories/grown-up/words.json"))
# (source start, source end, new start): question, don't feel, notice, bills, quiet, worry, until one day, call mum, hear voice
PH = [(0.19, 2.76, 0.60), (3.51, 4.38, 3.85), (4.89, 5.85, 4.95), (6.42, 7.17, 8.20), (7.71, 8.44, 9.90),
      (9.07, 9.68, 11.05), (10.40, 11.30, 12.25), (11.76, 12.61, 13.90), (13.07, 14.26, 14.95)]
END = 20.5
out = np.zeros(int(SR * END), np.float32); placed = []
for s, e, n in PH:
    a, b = int((s - 0.06) * SR), int((e + 0.12) * SR); seg = src[a:b]
    o = int((n - 0.06) * SR); out[o:o + len(seg)] += seg
    placed += [[w, ws - s + n, we - s + n] for w, ws, we in words if s - 0.01 <= ws < e]
assert len(placed) == len(words), (len(placed), len(words))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "audio/grown-up-placed.wav"], input=out.tobytes(), check=True)
json.dump(placed, open("stories/grown-up/words_placed.json", "w"))
print(" ".join(f"{w[1]:.2f}:{w[0]}" for w in placed))
