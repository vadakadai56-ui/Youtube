"""Render a story's animated shots with Eevee, frame by frame (resumable).

usage (with the bpy venv python):
  ENGINE=EEVEE python pipeline/anim.py STORY_DIR OUT_DIR [shot ...|all]
  PREVIEW=1 PCT=30 ES=8 ... renders only frame 0 of each shot, for a fast framing check.

STORY_DIR/shots.py must define SHOTS = {"name": (setup_fn, duration_seconds)}.
setup_fn(rng) builds the scene and returns update(t) that poses everything at time t (seconds).
Frames land in OUT_DIR/<shot>/0000.png ... at FPSA frames per second (default 12); edit.py blends them to 30 fps.
"""
import importlib.util, math, os, random, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("ENGINE", "EEVEE")
import bpy
import scene

FPSA = int(os.environ.get("FPSA", "12"))


def load_story(story_dir):
    spec = importlib.util.spec_from_file_location("story_shots", os.path.join(story_dir, "shots.py"))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def run(mod, name, out_root, preview=False):
    fn, dur = mod.SHOTS[name]
    scene.reset(); upd = fn(random.Random(11))
    out = os.path.join(out_root, name); os.makedirs(out, exist_ok=True)
    n = 1 if preview else int(math.ceil(dur * FPSA)) + 1
    t0 = time.time()
    for f in range(n):
        p = os.path.join(out, f"{f:04d}.png")
        if os.path.exists(p) and not preview: continue
        upd(f / FPSA); scene.render(p)
    print(f"SHOT_DONE {name} frames={n} secs={time.time() - t0:.0f}", flush=True)


if __name__ == "__main__":
    story_dir, out_root = sys.argv[1], sys.argv[2]
    names = sys.argv[3:] or ["all"]
    mod = load_story(story_dir)
    for nm in (list(mod.SHOTS) if names == ["all"] else names):
        run(mod, nm, out_root, preview=os.environ.get("PREVIEW") == "1")
