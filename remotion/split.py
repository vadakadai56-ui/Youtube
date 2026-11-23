"""Split a Remotion --sequence render into per-shot frame folders that pipeline/edit.py reads (with fps.txt = 30).

usage:  python3 remotion/split.py SEQ_DIR STORY_DIR FRAMES_OUT
"""
import json, os, shutil, sys

seq, story, out = sys.argv[1:4]
D = json.load(open(os.path.join(story, "durations.json")))
files = sorted(f for f in os.listdir(seq) if f.endswith(".png"))
t = 0.0
for shot, d in D.items():
    a, b = round(t * 30), round((t + d) * 30); t += d          # same rounding as START in src/index.tsx
    dst = os.path.join(out, shot); os.makedirs(dst, exist_ok=True)
    for i, f in enumerate(files[a:min(b + 1, len(files))]):    # one frame of overlap so edit.py can blend the last one
        shutil.copy(os.path.join(seq, f), os.path.join(dst, f"{i:04d}.png"))
    open(os.path.join(dst, "fps.txt"), "w").write("30")
assert t * 30 <= len(files) + 1, "sequence shorter than the story"
print(f"{len(D)} shots -> {out}")
