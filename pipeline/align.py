"""Make words.json (word, start, end) for captions from a narration mp3 and its script, without a transcription service.

usage:  python3 pipeline/align.py NARRATION.mp3 SCRIPT.txt OUT_words.json
SCRIPT.txt = the exact narration text (ElevenLabs tags like [whispering] are ignored).
Speech segments come from ffmpeg silencedetect. The script is split into phrases at . , ? ! and "...".
If the segment count matches the phrase count they are paired one to one; otherwise phrase boundaries snap to the
pauses closest to where the character count says they should be. Inside a phrase, words share its time by length.
(If ElevenLabs Scribe is available, its word timings are more exact; store them in the same format.)
"""
import json, re, subprocess, sys


def segments(mp3, db=-38, dur=0.16):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", mp3, "-af", f"silencedetect=n={db}dB:d={dur}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    h, mnt, sec = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err).groups()
    total = int(h) * 3600 + int(mnt) * 60 + float(sec)
    ev = [(m.group(1), float(m.group(2))) for m in re.finditer(r"silence_(start|end): ([\d.]+)", err)]
    segs, cur = [], 0.0
    for kind, t in ev:
        if kind == "start":
            if t - cur > 0.05: segs.append([cur, t])
        else: cur = t
    if total - cur > 0.15: segs.append([cur, total])
    return segs


def phrases(text):
    text = re.sub(r"\[[^\]]*\]", " ", text)
    words = text.split(); out, cur = [], []
    for w in words:
        cur.append(w)
        if re.search(r'(\.\.\.|[.,?!])["”]?$', w): out.append(cur); cur = []
    if cur: out.append(cur)
    return out


def align(segs, phr):
    if len(segs) == len(phr): return [(p, s[0], s[1]) for p, s in zip(phr, segs)]
    chars = [sum(len(w) for w in p) for p in phr]; tot = sum(chars)
    speech = sum(b - a for a, b in segs); gaps = [(segs[i][1], segs[i + 1][0]) for i in range(len(segs) - 1)]
    out, acc, start, used = [], 0, segs[0][0], set()
    for i, p in enumerate(phr):
        acc += chars[i]
        if i == len(phr) - 1: out.append((p, start, segs[-1][1])); break
        target_speech = speech * acc / tot; t, s_acc = segs[0][0], 0.0     # convert speech-time to clock time
        for a, b in segs:
            if s_acc + (b - a) >= target_speech: t = a + (target_speech - s_acc); break
            s_acc += b - a
        cand = [g for k, g in enumerate(gaps) if k not in used and g[0] > start]
        g = min(cand, key=lambda g: abs(g[0] - t)) if cand else (t, t)
        if cand: used.add(gaps.index(g))
        out.append((p, start, g[0])); start = g[1]
    return out


def words(aligned):
    res = []
    for p, a, b in aligned:
        wt = [len(w.strip('".,?!”')) + 1.5 for w in p]; tot = sum(wt); t = a
        for w, x in zip(p, wt):
            d = (b - a) * x / tot; res.append([w, round(t, 3), round(t + d * 0.9, 3)]); t += d
    return res


if __name__ == "__main__":
    mp3, script, out = sys.argv[1:4]
    segs = segments(mp3); phr = phrases(open(script).read())
    print(f"{len(segs)} speech segments, {len(phr)} phrases" + ("  (exact match)" if len(segs) == len(phr) else "  (snapped)"))
    w = words(align(segs, phr)); json.dump(w, open(out, "w")); print(f"wrote {len(w)} words to {out}")
