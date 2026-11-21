"""Edit an animated Dustlight story into a finished Short.

usage:  python3 pipeline/edit.py STORY_DIR FRAMES_DIR NARRATION.mp3 OUT.mp4
STORY_DIR/edit_config.py defines:
  CUTS   = [(start_seconds, "shot_name"), ..., (t, "END")]       # "END" = end card
  T_END  = total length in seconds
  KEY    = {"phrase", ...}                                         # caption words shown in yellow
  XFADE  = {"shot": seconds}                                       # optional dissolves into a shot
  CAPTION = {"words": 1, "y": 520, "size": 140}                    # optional caption style (default 3 words, y 1240, size 92)
  END_LINES = [(text, font_size, y, rgb, italic, delay)]           # end card text
  def sound(S): ...                                                # music and effects using the S toolkit below
  def overlay(img, t): ...                                         # optional on-screen graphics (typed headline, year counter), drawn under the captions
Real recordings: S.sample("ambience/fire", at, dur, g) plays a sound from the Dustlight library (~/dustlight-sfx, see pipeline/sfx_library.py).
STORY_DIR/words.json = [[word, start, end], ...]  (make it with pipeline/align.py)
Loudness: loudnorm to -14 LUFS, then a measured gain trim so the result lands at about -14.
"""
import importlib.util, json, math, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, SR = 1080, 1920, 30, 44100
FPSA = int(os.environ.get("FPSA", "12"))
FONT_BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FONT_ITAL = "/usr/share/fonts/opentype/inter/Inter-Italic.otf"
YELLOW = (255, 214, 64)


# ---------------------------------------------------------------- sound toolkit
class Sound:
    def __init__(self, seconds, seed=5):
        self.A = np.zeros(int((seconds + 0.5) * SR)); self.rng = np.random.default_rng(seed)
    def add(self, sig, at, g=1.0):
        i = int(at * SR); j = min(len(self.A), i + len(sig))
        if 0 <= i < len(self.A): self.A[i:j] += sig[: j - i] * g
    def env(self, n, att, rel):
        e = np.ones(n); a = min(n, int(att * SR)); r = min(n, int(rel * SR))
        if a: e[:a] = np.linspace(0, 1, a)
        if r: e[-r:] *= np.linspace(1, 0, r)
        return e
    @staticmethod
    def note(m): return 440 * 2 ** ((m - 69) / 12)
    def piano(self, f, dur=2.5):
        n = int(dur * SR); x = np.arange(n) / SR
        return sum(np.sin(2 * np.pi * f * k * x) * np.exp(-x * (1.5 + k)) / k for k in (1, 2, 3, 4)) * self.env(n, 0.004, 0.2)
    def bell(self, f, dur=1.6):
        n = int(dur * SR); x = np.arange(n) / SR
        s = np.sin(2 * np.pi * f * x) + 0.4 * np.sin(2 * np.pi * f * 2.01 * x) * np.exp(-x * 3) + 0.25 * np.sin(2 * np.pi * f * 3.98 * x) * np.exp(-x * 6)
        return s * np.exp(-x * 2.2) * self.env(n, 0.003, 0.05)
    def pad(self, fs, dur, att=1.5, rel=1.5):
        n = int(dur * SR); x = np.arange(n) / SR; s = np.zeros(n)
        for f in fs:
            for det in (-0.5, 0.5): s += np.sin(2 * np.pi * (f + det) * x + self.rng.uniform(0, 6))
        return np.convolve(s, np.ones(20) / 20, "same") / (2 * len(fs)) * self.env(n, att, rel)
    def noise(self, dur, k=40):
        n = int(dur * SR); return np.convolve(self.rng.standard_normal(n), np.ones(k) / k, "same")
    def chords(self, prog, start, end, step=3.0, bass=0.13, top=0.075):
        """prog: list of (bass_midi, n1, n2, n3); arpeggiated piano chords from start to end."""
        for i, tt in enumerate(np.arange(start, end, step)):
            ch = prog[i % len(prog)]; self.add(self.piano(self.note(ch[0] - 12), step + 0.2), tt, bass)
            for k, m in enumerate(ch[1:]): self.add(self.piano(self.note(m), step - 0.2), tt + 0.35 + k * 0.4, top)
    def steps(self, start, n, every=0.31, g=0.25):                    # footsteps crunching in snow
        for k in range(n): self.add(self.noise(0.12, 6) * self.env(int(0.12 * SR), 0.01, 0.08), start + k * every, g)
    def ticks(self, start, n, every=0.33, g=0.25):                    # clock ticks
        for k in range(n): self.add(self.noise(0.015, 2) * self.env(int(0.015 * SR), 0.001, 0.01), start + k * every, g)
    def wind(self, start, dur, g=0.06):
        self.add(self.noise(dur, 400) * self.env(int(dur * SR), 1.5, 2) * 5, start, g)
    def sample(self, cat, at, dur=None, g=0.3, pick=0, fade=0.4, offset=0.0):
        """A real recording from the sound library: the pick-th file in LIB/cat, trimmed to dur seconds, faded in and out."""
        lib = os.path.expanduser(os.environ.get("SFX_LIB", "~/dustlight-sfx")); d = os.path.join(lib, cat)
        fs = sorted(f for f in os.listdir(d) if not f.startswith(".")) if os.path.isdir(d) else []
        if not fs: print(f"! no sound in {d}, skipped"); return
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(offset), "-i", os.path.join(d, fs[pick % len(fs)])] + (["-t", str(dur)] if dur else []) +
                             ["-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
        x = np.frombuffer(raw, np.float32).astype(np.float64)
        if not len(x): return
        x = x / max(1e-9, np.max(np.abs(x))); self.add(x * self.env(len(x), fade, fade), at, g)
    def knock(self, t, g=0.7):
        n = int(0.25 * SR); x = np.arange(n) / SR
        self.add(np.sin(2 * np.pi * 95 * x) * np.exp(-x * 28) + self.noise(0.25, 8) * np.exp(-x * 50) * 0.6, t, g)


# ---------------------------------------------------------------- video
def load_config(story_dir):
    spec = importlib.util.spec_from_file_location("edit_config", os.path.join(story_dir, "edit_config.py"))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod


def main(story_dir, frames_dir, narration, outf):
    C = load_config(story_dir); words = json.load(open(os.path.join(story_dir, "words.json")))
    xfade = getattr(C, "XFADE", {}); key = {k.lower() for k in C.KEY}
    cache = {}
    def frame(shot, idx):
        d = os.path.join(frames_dir, shot); n = len([f for f in os.listdir(d) if f.endswith(".png")])
        idx = max(0, min(n - 1, idx)); k = (shot, idx)
        if k not in cache:
            if len(cache) > 12: cache.pop(next(iter(cache)))
            cache[k] = Image.open(os.path.join(d, f"{idx:04d}.png")).convert("RGB").resize((W, H), Image.LANCZOS)
        return cache[k]
    def shot_image(shot, local):
        x = local * FPSA; i = int(x); a = x - i; A = frame(shot, i)
        return Image.blend(A, frame(shot, i + 1), a) if a > 0.02 else A

    capc = getattr(C, "CAPTION", {}); CAP_W = capc.get("words", 3); CAP_Y = capc.get("y", 1240); CAP_SIZE = capc.get("size", 92)
    chunks, cur = [], []                                           # captions: 1-3 words (CAPTION["words"]), broken on punctuation
    for w, a, b in words:
        cur.append((w, a, b))
        if w[-1] in ".,?!" or w.endswith("...") or len(cur) == CAP_W or w.endswith('"'): chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    def is_key(ci, j):
        ws = [c[0].strip('".,?!').lower().rstrip(".") for c in chunks[ci]]
        for k in key:
            ks = k.split()
            for s in range(len(ws) - len(ks) + 1):
                if ws[s:s + len(ks)] == ks and s <= j < s + len(ks): return True
        return False
    FONT = {s: ImageFont.truetype(FONT_BLACK, s) for s in range(40, 170, 2)}
    def caption(img, t):
        for ci, ch in enumerate(chunks):
            st = ch[0][1]; en = min(chunks[ci + 1][0][1] if ci + 1 < len(chunks) else ch[-1][2] + 0.6, ch[-1][2] + 0.7)
            if not (st - 0.05 <= t < en): continue
            shown = [(w, j) for j, (w, a, b) in enumerate(ch) if t >= a - 0.05]
            if not shown: return
            txt = [w.strip('"').upper() for w, _ in shown]
            k = min(1.0, (t - st + 0.05) / 0.12); sc = 0.85 + 0.15 * (1 - (1 - k) ** 3); size = CAP_SIZE
            while True:
                f = FONT[min(168, max(40, int(size * sc) // 2 * 2))]
                widths = [f.getlength(x) for x in txt]; space = f.getlength(" ")
                if sum(widths) + space * (len(txt) - 1) < W - 120 or size <= 50: break
                size -= 6
            d = ImageDraw.Draw(img); x = W / 2 - (sum(widths) + space * (len(txt) - 1)) / 2
            for (w, j), tx, wd in zip(shown, txt, widths):
                d.text((x, CAP_Y), tx, font=f, fill=YELLOW if is_key(ci, j) else (255, 255, 255), anchor="lm", stroke_width=9, stroke_fill=(0, 0, 0))
                x += wd + space
            return

    yy, xx = np.mgrid[0:H, 0:W]
    vig = (1 - 0.4 * np.clip(((xx - W / 2) / (W * 0.8)) ** 2 + ((yy - H * 0.48) / (H * 0.65)) ** 2, 0, 1) ** 1.4)[..., None].astype(np.float32)
    grng = np.random.default_rng(3); GR = [np.repeat(np.repeat(grng.normal(0, 5, (H // 2, W // 2, 1)).astype(np.float32), 2, 0), 2, 1) for _ in range(6)]
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", outf + ".video.mp4"], stdin=subprocess.PIPE)
    cuts = C.CUTS
    for fi in range(int(C.T_END * FPS)):
        t = fi / FPS
        ci = max(i for i, c in enumerate(cuts) if c[0] <= t); st, shot = cuts[ci]
        if shot == "END":
            img = Image.new("RGB", (W, H), (8, 6, 5)); d = ImageDraw.Draw(img)
            for txt, size, y, rgb, italic, delay in C.END_LINES:
                a = min(1, max(0, (t - st - delay) / 0.6))
                if a > 0: d.text((W / 2, y), txt, font=ImageFont.truetype(FONT_ITAL if italic else FONT_BLACK, size), fill=tuple(int(v * a) for v in rgb), anchor="mm")
            proc.stdin.write(img.tobytes()); continue
        img = shot_image(shot, t - st)
        xf = xfade.get(shot)
        if xf and t - st < xf and ci > 0:
            pst, prev = cuts[ci - 1]; img = Image.blend(shot_image(prev, t - pst), img, (t - st) / xf)
        if ci + 1 < len(cuts) and cuts[ci + 1][1] == "END" and cuts[ci + 1][0] - t < 0.8:
            img = Image.blend(Image.new("RGB", (W, H), (8, 6, 5)), img, max(0, (cuts[ci + 1][0] - t) / 0.8))
        arr = np.asarray(img).astype(np.float32) * vig + GR[fi % 6]
        img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
        if hasattr(C, "overlay"): C.overlay(img, t)
        caption(img, t); proc.stdin.write(img.tobytes())
    proc.stdin.close(); proc.wait()

    S = Sound(C.T_END); S.A[:] += S.noise(len(S.A) / SR, 220) * 0.035; C.sound(S)
    tmp = outf + ".narr.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", narration, "-ac", "1", "-ar", str(SR), tmp], check=True)
    with wave.open(tmp) as wv: v = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(np.float32) / 32768
    A = S.A; m = min(len(A), len(v)); venv = np.convolve(np.abs(v), np.ones(4410) / 4410, "same")
    duck = np.ones(len(A)); duck[:m] = 1 - 0.45 * np.clip(venv[:m] / 0.05, 0, 1); A *= duck; A[:m] += v[:m]
    A = A / max(1e-9, np.max(np.abs(A))) * 0.9
    with wave.open(outf + ".mix.wav", "wb") as wv:
        wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((A * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", outf + ".video.mp4", "-i", outf + ".mix.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-shortest", outf + ".pre.mp4"], check=True)
    meas = subprocess.run(["ffmpeg", "-hide_banner", "-i", outf + ".pre.mp4", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    integ = float([l for l in meas.splitlines() if l.strip().startswith("I:")][-1].split()[1])
    gain = round(-14 - integ, 2)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", outf + ".pre.mp4", "-c:v", "copy", "-af", f"volume={gain}dB,alimiter=limit=0.89",
                    "-c:a", "aac", "-b:a", "192k", outf], check=True)
    for f in (".video.mp4", ".mix.wav", ".narr.wav", ".pre.mp4"):
        if os.path.exists(outf + f): os.remove(outf + f)
    print(f"done {outf} (loudness {integ} LUFS, trimmed {gain:+} dB)")


if __name__ == "__main__":
    main(*sys.argv[1:5])
