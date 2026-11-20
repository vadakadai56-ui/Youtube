"""Pre-upload quality check for a finished YouTube Short (used by the /yt-qc skill).

usage:  python3 pipeline/qc.py VIDEO.mp4 [--json]
Checks: vertical 9:16, resolution, frame rate, length (Shorts limit 180 s, Dustlight target 55-75 s),
audio present, loudness (-14 LUFS +/- 1, true peak <= -1 dBTP), silence or black at the very start
(the first 3 s are the hook), and file size. Exit code 1 if any check FAILs (WARNs do not fail).
"""
import json, re, subprocess, sys


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
    return res


if __name__ == "__main__":
    r = check(sys.argv[1])
    if "--json" in sys.argv: print(json.dumps(r, indent=1))
    else:
        for x in r: print(f"{x['level']:4}  {x['check']:<13} {x['msg']}")
    fails = sum(x["level"] == "FAIL" for x in r)
    print(f"\n{'READY' if not fails else 'NOT READY'}: {fails} fail, {sum(x['level'] == 'WARN' for x in r)} warn")
    sys.exit(1 if fails else 0)
