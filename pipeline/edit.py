"""Edit an animated Dustlight story into a finished Short.

usage:  python3 pipeline/edit.py STORY_DIR FRAMES_DIR NARRATION.mp3 OUT.mp4
STORY_DIR/edit_config.py defines:
  CUTS   = [(start_seconds, "shot_name"), ..., (t, "END")]       # "END" = end card
  T_END  = total length in seconds
  KEY    = {"phrase", ...}                                         # caption words shown in yellow
  XFADE  = {"shot": seconds}                                       # optional dissolves into a shot
  CAPTION = {"words": 1, "y": 520, "size": 140}                    # optional caption style (default 3 words, y 1240, size 92)
  END_LINES = [(text, font_size, y, rgb, italic, delay)]           # end card text; with QUICK_END only the first line is used, over the last shot
  QUICK_END = True                                                 # default: no black end card, the video ends TAIL (0.8 s) after the payoff
  REHOOK = (t, "text") or a list of them                                             # optional: a line on screen mid-video reminding viewers what they wait for
  def sound(S): ...                                                # music and effects using the S toolkit below
  def overlay(img, t): ...                                         # optional on-screen graphics (typed headline, year counter), drawn under the captions
Real recordings: S.sample("ambience/fire", at, dur, g) plays a sound from the Dustlight library (~/dustlight-sfx, see pipeline/sfx_library.py).
STORY_DIR/words.json = [[word, start, end], ...]  (make it with pipeline/align.py)
Loudness: loudnorm to -14 LUFS, then a measured gain trim so the result lands at about -14.
"""
import importlib.util, json, math, os, re, subprocess, sys, wave
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
    inst = "bell"                                                   # set per look by main(): bell | piano | marimba | pluck
    def bell(self, f, dur=1.6):
        if self.inst == "piano": return self.piano(f, dur) * 0.8
        if self.inst == "marimba": return self.marimba(f, min(dur, 0.8))
        if self.inst == "pluck": return self.pluck(f, min(dur, 1.0))
        return self._bell(f, dur)
    def marimba(self, f, dur=0.8):
        n = int(dur * SR); x = np.arange(n) / SR
        return (np.sin(2 * np.pi * f * x) + 0.35 * np.sin(2 * np.pi * f * 4.0 * x) * np.exp(-x * 25)) * np.exp(-x * 7) * self.env(n, 0.002, 0.05) * 1.3
    def pluck(self, f, dur=1.0):
        """Karplus-Strong plucked string."""
        n = int(dur * SR); p = max(2, int(SR / f)); buf = self.rng.uniform(-1, 1, p); out = np.zeros(n)
        for i in range(n):
            out[i] = buf[i % p]; buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
        return out * self.env(n, 0.002, 0.1) * 1.2
    def drums(self, start, end, bpm=112, g=0.05):
        """A light comedy groove: kick on 1 and 3, a soft snare on 2 and 4, closed hats on the eighths."""
        beat = 60.0 / bpm; t, k = start, 0
        while t < end:
            if k % 2 == 0:
                n = int(0.25 * SR); x = np.arange(n) / SR; self.add(np.sin(2 * np.pi * (55 + 90 * np.exp(-x * 30)) * x) * np.exp(-x * 14), t, g * 1.4)
            else: self.add(self.noise(0.15, 3) * self.env(int(0.15 * SR), 0.001, 0.12), t, g * 0.6)
            for h in (0, 0.5): self.add(self.noise(0.03, 1) * self.env(int(0.03 * SR), 0.001, 0.025), t + h * beat, g * 0.35)
            t += beat; k += 1
    def _bell(self, f, dur=1.6):
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
    def fps_of(shot, _r={}):
        if shot not in _r:
            f = os.path.join(frames_dir, shot, "fps.txt"); _r[shot] = int(open(f).read()) if os.path.exists(f) else FPSA
        return _r[shot]
    def shot_image(shot, local):
        x = local * fps_of(shot); i = int(x); a = x - i; A = frame(shot, i)
        if shot in getattr(C, "STEP", ()): return A          # held frames ("on twos"): fast gestures ghost when blended
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

    look = getattr(C, "LOOK", None)
    if look is None:                                                # read the story's grade from shots.py (scene.LOOK ... or "comedy")
        m_ = re.search(r'scene\.LOOK\s*=.*?"(\w+)"', open(os.path.join(story_dir, "shots.py")).read()) if os.path.exists(os.path.join(story_dir, "shots.py")) else None
        look = m_.group(1) if m_ else "story"
    VIG = {"comedy": 0.0, "dream": 0.2, "story": 0.4, "horror": 0.55}.get(look, 0.4); GRAIN = {"comedy": 0, "dream": 3, "story": 5, "horror": 7}.get(look, 5)
    # punch-in zooms: comedy gets an automatic snap zoom halfway through every shot of 2.4 s or more; ZOOMS = [(t, scale, dur)] adds more
    zooms = list(getattr(C, "ZOOMS", []))
    if look == "comedy" and getattr(C, "AUTO_ZOOM", True):
        for i, (st_, nm_) in enumerate(cuts_all := C.CUTS):
            if nm_ == "END" or i + 1 >= len(cuts_all): continue
            dur_ = cuts_all[i + 1][0] - st_
            if dur_ >= 2.4: zooms.append((st_ + dur_ / 2, 1.16, cuts_all[i + 1][0] - (st_ + dur_ / 2)))
    def zoom_at(t):
        for z0, sc_, zd in zooms:
            if z0 <= t < z0 + zd: return sc_
        return 1.0
    # the hook line on screen from frame one (HOOK = None turns it off)
    hook = getattr(C, "HOOK", "")
    if hook == "":
        raw = re.sub(r"\[[^\]]*\]", "", open(os.path.join(story_dir, "narration.txt")).read()).strip()
        hook = re.split(r"(?<=[.?!])\s", raw.replace("...", "\u2026"), maxsplit=1)[0].strip()
    HOOK_T = getattr(C, "HOOK_SECONDS", 2.6)
    rh = getattr(C, "REHOOK", None); RH_D = 1.8
    rehooks = [rh] if rh and isinstance(rh[0], (int, float)) else list(rh or [])     # one (t, text) or a list of them
    def draw_hook(img, t):
        live = [r for r in rehooks if r[0] <= t < r[0] + RH_D]
        hy = getattr(C, "HOOK_Y", 250 if CAP_Y > 800 else 150)
        if hook and t < HOOK_T: txt_, a = hook, min(1.0, (HOOK_T - t) / 0.3)
        elif live: r = live[0]; txt_, a = r[1], min(1.0, (t - r[0]) / 0.15, (r[0] + RH_D - t) / 0.3); hy = getattr(C, "REHOOK_Y", hy)
        else: return
        f = FONT[76]; d = ImageDraw.Draw(img); words_, lines, line = txt_.split(), [], ""
        for w_ in words_:
            if f.getlength((line + " " + w_).strip()) > W - 160: lines.append(line); line = w_
            else: line = (line + " " + w_).strip()
        lines.append(line)
        for i, ln in enumerate(lines[:4]):
            d.text((W / 2, hy + i * 92), ln, font=f, fill=tuple(int(255 * a) for _ in range(3)), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))

    yy, xx = np.mgrid[0:H, 0:W]
    vig = (1 - VIG * np.clip(((xx - W / 2) / (W * 0.8)) ** 2 + ((yy - H * 0.48) / (H * 0.65)) ** 2, 0, 1) ** 1.4)[..., None].astype(np.float32)
    grng = np.random.default_rng(3); GR = [np.repeat(np.repeat(grng.normal(0, max(GRAIN, 0.01), (H // 2, W // 2, 1)).astype(np.float32), 2, 0), 2, 1) for _ in range(6)]
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", outf + ".video.mp4"], stdin=subprocess.PIPE)
    cuts = list(C.CUTS)
    quick = getattr(C, "QUICK_END", True) and cuts[-1][1] == "END"
    end_t = cuts[-1][0]
    if quick:                                                       # end on the payoff: hold the last shot TAIL s, the question on top, no black card
        T_END = end_t + getattr(C, "TAIL", 0.8); cuts = cuts[:-1]
        q = C.END_LINES[0] if getattr(C, "END_LINES", None) else None
    else: T_END = C.T_END
    def draw_question(img, t):
        if not quick or not q or t < end_t - 0.15: return
        a = min(1.0, (t - end_t + 0.15) / 0.2); f = ImageFont.truetype(FONT_BLACK, 70); d = ImageDraw.Draw(img)
        d.text((W / 2, getattr(C, "QUESTION_Y", 560)), q[0], font=f, fill=tuple(int(255 * a) for _ in range(3)), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
    for fi in range(int(T_END * FPS)):
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
        zf = zoom_at(t)
        if zf > 1.001:                                              # snap punch-in, centred a little above the middle
            cw, ch_ = int(W / zf), int(H / zf); x0 = (W - cw) // 2; y0 = int((H - ch_) * 0.42)
            img = img.crop((x0, y0, x0 + cw, y0 + ch_)).resize((W, H), Image.LANCZOS)
        arr = np.asarray(img).astype(np.float32) * vig + (GR[fi % 6] if GRAIN else 0)
        img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
        if hasattr(C, "overlay"): C.overlay(img, t)
        draw_hook(img, t); caption(img, t); draw_question(img, t); proc.stdin.write(img.tobytes())
    proc.stdin.close(); proc.wait()

    S = Sound(T_END); S.A[:] += S.noise(len(S.A) / SR + 0.01, 220)[: len(S.A)] * (0.035 if look != "comedy" else 0.01)
    S.inst = getattr(C, "INSTRUMENT", {"comedy": "marimba", "story": "piano", "dream": "piano", "horror": "bell"}.get(look, "bell"))
    if look == "comedy" and getattr(C, "DRUMS", True): S.drums(0.0, C.CUTS[-1][0], bpm=getattr(C, "BPM", 112))
    C.sound(S)
    tmp = outf + ".narr.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", narration, "-ac", "1", "-ar", str(SR), tmp], check=True)
    with wave.open(tmp) as wv: v = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(np.float32) / 32768
    A = S.A; m = min(len(A), len(v)); venv = np.convolve(np.abs(v), np.ones(4410) / 4410, "same")
    duck = np.ones(len(A)); duck[:m] = 1 - 0.45 * np.clip(venv[:m] / 0.05, 0, 1); A *= duck; A[:m] += v[:m]
    A = A[: int(T_END * SR)]; fo = int(0.25 * SR); A[-fo:] *= np.linspace(1, 0, fo)   # cut the music at the end, with a short fade
    A = A / max(1e-9, np.max(np.abs(A))) * 0.9
    with wave.open(outf + ".mix.wav", "wb") as wv:
        wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((A * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", outf + ".video.mp4", "-i", outf + ".mix.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-shortest", outf + ".pre.mp4"], check=True)
    meas = subprocess.run(["ffmpeg", "-hide_banner", "-i", outf + ".pre.mp4", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    integ = float([l for l in meas.splitlines() if l.strip().startswith("I:")][-1].split()[1])
    gain = round(-14 - integ, 2)
    for _ in range(3):                                              # gain + peak limiter, re-measured until it lands within 0.4 dB of -14
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", outf + ".pre.mp4", "-c:v", "copy", "-af", f"volume={gain}dB,alimiter=limit=0.78:level=disabled",
                        "-c:a", "aac", "-b:a", "192k", outf], check=True)
        m2 = subprocess.run(["ffmpeg", "-hide_banner", "-i", outf, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
        got = float([l for l in m2.splitlines() if l.strip().startswith("I:")][-1].split()[1])
        if abs(got + 14) <= 0.4: break
        gain = round(gain + (-14 - got), 2)
    for f in (".video.mp4", ".mix.wav", ".narr.wav", ".pre.mp4"):
        if os.path.exists(outf + f): os.remove(outf + f)
    print(f"done {outf} (loudness {integ} LUFS, trimmed {gain:+} dB)")


if __name__ == "__main__":
    main(*sys.argv[1:5])
