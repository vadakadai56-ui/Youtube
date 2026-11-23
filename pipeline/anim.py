"""Render a story's animated shots with Eevee, frame by frame (resumable).

usage (with the bpy venv python):
  ENGINE=EEVEE python pipeline/anim.py STORY_DIR OUT_DIR [shot ...|all]
  PREVIEW=1 PCT=30 ES=8 ... renders only frame 0 of each shot, for a fast framing check.
  STILLS="w2:4.0,w3:2.5" PCT=100 ... renders single stills at those shot times (carousels).

STORY_DIR/shots.py must define SHOTS = {"name": (setup_fn, duration_seconds)}.
setup_fn(rng) builds the scene and returns update(t) that poses everything at time t (seconds).
Frames land in OUT_DIR/<shot>/0000.png ... at FPSA frames per second (default 12), or 6 for shots listed in the story's CALM set; edit.py blends them to 30 fps.
"""
import importlib.util, math, os, random, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("ENGINE", "EEVEE")
import bpy
import scene
try:
    from characters import animate_all as _life
except Exception:
    _life = None

FPSA = int(os.environ.get("FPSA", "12"))


def load_story(story_dir):
    spec = importlib.util.spec_from_file_location("story_shots", os.path.join(story_dir, "shots.py"))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def run(mod, name, out_root, preview=False):
    fn, dur = mod.SHOTS[name]
    scene.reset(); upd = fn(random.Random(11))
    out = os.path.join(out_root, name); os.makedirs(out, exist_ok=True)
    fpsf = os.path.join(out, "fps.txt")                     # the frames' own rate, read back by edit.py
    if not preview and not os.path.exists(fpsf):
        started = any(f.endswith(".png") for f in os.listdir(out))   # never change the rate of a half-rendered shot
        open(fpsf, "w").write(str(FPSA if started or name not in getattr(mod, "CALM", ()) else 6))
    fps = int(open(fpsf).read()) if os.path.exists(fpsf) else FPSA
    n = 1 if preview else int(math.ceil(dur * fps)) + 1
    t0 = time.time()
    for f in range(n):
        p = os.path.join(out, f"{f:04d}.png")
        if os.path.exists(p) and not preview: continue
        bpy.context.scene.frame_set(int(f / fps * 24), subframe=(f / fps * 24) % 1)   # clock for ready-made clips (24 fps)
        upd(f / fps)
        if _life: _life(f / fps)                          # blinks and glances for every character
        scene.render(p)
    print(f"SHOT_DONE {name} frames={n} secs={time.time() - t0:.0f}", flush=True)


if __name__ == "__main__":
    story_dir, out_root = sys.argv[1], sys.argv[2]
    names = sys.argv[3:] or ["all"]
    mod = load_story(story_dir)
    if os.environ.get("STILLS"):                            # STILLS="w2:4.0,w3:2.5" renders single stills (for carousels) to OUT_DIR/<shot>_<t>.png
        os.makedirs(out_root, exist_ok=True)
        for item in os.environ["STILLS"].split(","):
            nm, t = item.split(":"); t = float(t)
            scene.reset(); upd = mod.SHOTS[nm][0](random.Random(11))
            for k in range(0, int(t * FPSA) + 1): upd(k / FPSA)   # step up to t so stateful shots end in the right place
            bpy.context.scene.frame_set(int(t * 24), subframe=(t * 24) % 1); upd(t)   # then land on t itself, clips too
            if _life: _life(t)
            scene.render(os.path.join(out_root, f"{nm}_{t:g}.png")); print("STILL", nm, t, flush=True)
        sys.exit(0)
    for nm in (list(mod.SHOTS) if names == ["all"] else names):
        run(mod, nm, out_root, preview=os.environ.get("PREVIEW") == "1")
