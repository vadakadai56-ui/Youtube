"""Pre-upload quality check for a finished YouTube Short (used by the /yt-qc skill).

usage:  python3 pipeline/qc.py VIDEO.mp4 [--json]
Checks: vertical 9:16, resolution, frame rate, length (Shorts limit 180 s, Dustlight target 55-75 s),
audio present, loudness (-14 LUFS +/- 1, true peak <= -1 dBTP), silence or black at the very start
(the first 3 s are the hook), and file size. Exit code 1 if any check FAILs (WARNs do not fail).
Pacing (WARN only): cuts per minute and the longest shot, picture motion in the first 3 s, and speaking speed
(words per minute, from stories/<slug>/narration.txt when it exists). These are plain measurements, no prediction model.
"""
import json, os, re, subprocess, sys
import numpy as np


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path):
    out = run(["ffprobe", "-v", "error", "-show_entries",
               "format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate",
               "-of", "json", path]).stdout
    return json.loads(out)


def loudness(path):
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "loudnorm=print_format=json",
               "-vn", "-f", "null", "-"]).stderr
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", err, re.S)
    return json.loads(m.group(0)) if m else None


def start_gaps(path):
    """Seconds of silence and of black at the start of the video."""
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-t", "4", "-i", path,
               "-af", "silencedetect=noise=-45dB:d=0.3", "-vf", "blackdetect=d=0.2:pix_th=0.08",
               "-f", "null", "-"]).stderr
    sil = blk = 0.0
    m = re.search(r"silence_start: (-?[\d.]+).*?silence_end: ([\d.]+)", err, re.S)
    if m and float(m.group(1)) <= 0.05: sil = float(m.group(2))
    m = re.search(r"black_start:([\d.]+) black_end:([\d.]+)", err)
    if m and float(m.group(1)) <= 0.05: blk = float(m.group(2))
    return sil, blk


def story_dir(path):
    slug = re.sub(r"-v\d+$", "", os.path.splitext(os.path.basename(path))[0])
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "stories", slug)
    return d if os.path.isdir(d) else None


def cuts(path, dur):
    """Cut times and the longest shot. Uses the story's own CUTS (edit_config.py) when it exists, because picture-based
    detection misses soft crossfades between near-identical shots; otherwise falls back to the ffmpeg scene score."""
    d = story_dir(path)
    if d and os.path.exists(os.path.join(d, "edit_config.py")):
        import runpy
        C = runpy.run_path(os.path.join(d, "edit_config.py"))
        ts = [t for t, n in C["CUTS"] if 0 < t < dur and n != "END"]
        edges = [0.0] + ts + [dur]
        return ts, max(b - a for a, b in zip(edges, edges[1:]))
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-an", "-vf",
               "scale=270:480,select='gt(scene,0.22)',showinfo", "-f", "null", "-"]).stderr
    ts = [float(t) for t in re.findall(r"pts_time:([\d.]+)", err)]
    ts = [t for i, t in enumerate(ts) if not i or t - ts[i - 1] > 0.4]        # one crossfade = one cut
    edges = [0.0] + ts + [dur]
    return ts, max(b - a for a, b in zip(edges, edges[1:]))


def hook_motion(path, secs=3.0):
    """Mean frame-to-frame change (0-255 grey) over the first secs, at 12 fps, 135x240."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-t", str(secs), "-i", path, "-vf", "fps=12,scale=135:240,format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    f = np.frombuffer(raw, np.uint8).reshape(-1, 240, 135).astype(np.float32)
    return float(np.abs(np.diff(f, axis=0)).mean()) if len(f) > 1 else 0.0


def wpm(path, dur):
    d = story_dir(path); txt = d and os.path.join(d, "narration.txt")
    if not txt or not os.path.exists(txt): return None
    words = re.sub(r"\[[^\]]*\]", " ", open(txt).read()).split()
    return len(words) / (dur / 60)


def check(path):
    p = probe(path)
    v = next((s for s in p["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in p["streams"] if s["codec_type"] == "audio"), None)
    dur = float(p["format"]["duration"]); size_mb = int(p["format"]["size"]) / 1e6
    res = []

    def add(level, name, msg): res.append({"level": level, "check": name, "msg": msg})

    if not v: add("FAIL", "video", "no video stream"); return res
    w, h = v["width"], v["height"]; num, den = map(int, v["r_frame_rate"].split("/")); fps = num / den
    add("PASS" if abs(w / h - 9 / 16) < 0.01 else "FAIL", "aspect", f"{w}x{h} (need 9:16 vertical)")
    add("PASS" if h >= 1920 else "WARN", "resolution", f"{h}p" + ("" if h >= 1920 else ", 1080x1920 recommended"))
    add("PASS" if 24 <= fps <= 60 else "WARN", "fps", f"{fps:.2f}")
    add("PASS" if v.get("codec_name") in ("h264", "hevc", "vp9", "av1") else "WARN", "codec", v.get("codec_name"))
    if dur > 180: add("FAIL", "length", f"{dur:.1f} s, over the 180 s Shorts limit")
    elif 55 <= dur <= 75: add("PASS", "length", f"{dur:.1f} s")
    else: add("WARN", "length", f"{dur:.1f} s (channel target 55-75 s)")
    add("PASS" if size_mb < 1000 else "WARN", "size", f"{size_mb:.1f} MB" + (" (Dropbox chunked upload)" if size_mb > 150 else ""))

    if not a: add("FAIL", "audio", "no audio stream")
    else:
        L = loudness(path)
        if L:
            i, tp = float(L["input_i"]), float(L["input_tp"])
            add("PASS" if -15 <= i <= -13 else "FAIL", "loudness", f"{i:.1f} LUFS (target -14)")
            add("PASS" if tp <= -1.0 else "WARN", "true peak", f"{tp:.1f} dBTP (want <= -1)")
        sil, blk = start_gaps(path)
        add("PASS" if sil < 0.5 else "WARN", "hook audio", f"{sil:.2f} s of silence at the start" if sil else "sound from frame 1")
        add("PASS" if blk < 0.3 else "WARN", "hook picture", f"{blk:.2f} s of black at the start" if blk else "picture from frame 1")
    ts, longest = cuts(path, dur); cpm = len(ts) / (dur / 60)
    add("PASS" if cpm >= 6 else "WARN", "cut pace", f"{len(ts)} cuts, {cpm:.1f} per minute (want 6+)")
    add("PASS" if longest <= 8 else "WARN", "longest shot", f"{longest:.1f} s (want 8 s or less)")
    m = hook_motion(path)
    add("PASS" if m >= 1.5 else "WARN", "hook motion", f"{m:.1f} frame change in 0-3 s (want 1.5+, a still opening loses swipers)")
    r = wpm(path, dur)
    if r: add("PASS" if 130 <= r <= 190 else "WARN", "speech pace", f"{r:.0f} words per minute (want 130-190)")
    return res


if __name__ == "__main__":
    r = check(sys.argv[1])
    if "--json" in sys.argv: print(json.dumps(r, indent=1))
    else:
        for x in r: print(f"{x['level']:4}  {x['check']:<13} {x['msg']}")
    fails = sum(x["level"] == "FAIL" for x in r)
    print(f"\n{'READY' if not fails else 'NOT READY'}: {fails} fail, {sum(x['level'] == 'WARN' for x in r)} warn")
    sys.exit(1 if fails else 0)
