"""Exact word timings for captions with a local Whisper model (free, no service). Use when align.py reports "snapped" or the
captions drift. Words keep the script's spelling; times come from Whisper, matched word by word.

usage:  python3 pipeline/align_whisper.py NARRATION.mp3 SCRIPT.txt OUT_words.json [model=base.en]
Needs: pip install faster-whisper (the model downloads once to ~/.cache/huggingface).
"""
import difflib, json, re, subprocess, sys
import numpy as np


def norm(w): return re.sub(r"[^a-z0-9']", "", w.lower())


def main(mp3, script, out, model="base.en"):
    from faster_whisper import WhisperModel
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", mp3, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"], capture_output=True).stdout
    audio = np.frombuffer(raw, np.float32)
    segs, _ = WhisperModel(model, device="cpu", compute_type="int8").transcribe(audio, word_timestamps=True)
    heard = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
    words = re.sub(r"\[[^\]]*\]", " ", open(script).read()).split()
    a = [norm(w) for w in words]; b = [norm(w) for w, _, _ in heard]
    t = [None] * len(words)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size): t[blk.a + k] = (heard[blk.b + k][1], heard[blk.b + k][2])
    # words Whisper heard differently (numbers, names): spread them between their matched neighbours
    i = 0
    while i < len(words):
        if t[i] is None:
            j = i
            while j < len(words) and t[j] is None: j += 1
            lo = t[i - 1][1] if i > 0 else 0.0
            hi = t[j][0] if j < len(words) else (heard[-1][2] if heard else lo + 0.5 * (j - i))
            step = max(0.05, (hi - lo) / (j - i))
            for k in range(i, j): t[k] = (lo + (k - i) * step, lo + (k - i + 1) * step)
            i = j
        else: i += 1
    res = [[w, round(s, 3), round(e, 3)] for w, (s, e) in zip(words, t)]
    json.dump(res, open(out, "w"))
    miss = sum(1 for x in t if x is None)
    print(f"wrote {len(res)} words to {out} ({len(words) - sum(blk.size for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks())} filled between matches)")


if __name__ == "__main__":
    main(*sys.argv[1:])
