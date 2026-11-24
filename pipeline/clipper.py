"""Cut a stream clip into a vertical Short for clipping campaigns (huss.clip account): the streamer's face cam large on top,
the gameplay below (chat and overlays cropped out), word-by-word captions (Inter Display Black from the edit kit, every
caption in white, punch words in yellow) and a hook line at the top for the first 3 seconds. No logos or watermarks.

  python3 pipeline/clipper.py SRC.mp4 OUT.mp4 --hook "He forgot the controller exists 💀" [--start 0 --end 45] [--layout asianjeff]

Layouts are crop boxes on the 1920x1080 stream: face = the face cam, game = the gameplay to show under it."""
import argparse, os, subprocess, sys
import numpy as np

LAYOUTS = {   # (x, y, w, h) on 1920x1080 (check each clip: he moves and resizes his cam between streams)
    "asianjeff": dict(face=(0, 318, 590, 322), game=(620, 190, 1040, 740)),   # 19 Nov: cam left; chat, "Rice today" and his caption bar cut off
    "asianjeff2": dict(face=(0, 370, 452, 340), game=(560, 200, 1100, 740)),  # from 20 Nov: smaller cam, lower
    "zoomaa": dict(face=(1490, 0, 320, 254), game=(500, 70, 920, 900)),       # FaZe Flank Invitational POV (1080p restream); his burnt captions below y 980 cut off
}
FONT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "edit-kit", "03 Fonts & Captions", "Fonts")
PUNCH = {"what", "no", "bro", "wait", "why", "how", "scared", "crazy", "insane", "help", "run", "money", "gone"}


def words(src, start, end):
    from faster_whisper import WhisperModel
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(start), "-to", str(end), "-i", src, "-ac", "1", "-ar", "16000",
                          "-f", "f32le", "-"], capture_output=True).stdout
    segs, _ = WhisperModel("small.en", device="cpu", compute_type="int8").transcribe(np.frombuffer(raw, np.float32), word_timestamps=True)
    return [(w.word.strip(), w.start, w.end) for s in segs for w in s.words if w.word.strip()]


import re
_MASK = [(r"fuck", "f*ck"), (r"shit", "sh*t"), (r"bitch", "b*tch"), (r"damn", "d*mn"), (r"dick", "d*ck"), (r"\bass(es)?\b", "a**")]


def clean(w):
    """Mask swear words in on-screen captions (the audio stays as it is): FUCKING -> F*CKING. Reach drops on visible swearing."""
    for pat, rep in _MASK: w = re.sub(pat, rep, w, flags=re.I)
    return w


def ass_time(t):
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def write_ass(path, ws, hook, hook_dur=3.0, hook_y=90):
    """Captions in chunks of up to 3 words (a new chunk after punctuation), centred where the cam meets the game."""
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter Display Black,96,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,7,3,5,60,60,0,1
Style: Hook,Inter Display Black,76,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,3,18,0,8,70,70,{hook_y},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev, chunk = [], []
    def flush():
        if not chunk: return
        txt = " ".join(("{\\c&H00D7FF&}" + clean(w).upper() + "{\\c&HFFFFFF&}") if w.strip(".,!?'").lower() in PUNCH else clean(w).upper() for w, _, _ in chunk)
        ev.append(f"Dialogue: 0,{ass_time(chunk[0][1])},{ass_time(max(chunk[-1][2], chunk[0][1] + 0.35))},Cap,,0,0,0,,{{\\pos(540,960)\\fscx80\\fscy80\\t(0,80,\\fscx100\\fscy100)}}{txt}")
        chunk.clear()
    for w in ws:
        chunk.append(w)
        if len(chunk) == 3 or w[0][-1] in ".,!?": flush()
    flush()
    ev.append(f"Dialogue: 1,{ass_time(0)},{ass_time(hook_dur)},Hook,,0,0,0,,{hook}")
    open(path, "w").write(head + "\n".join(ev) + "\n")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("out"); ap.add_argument("--hook", required=True)
    ap.add_argument("--start", type=float, default=0.0); ap.add_argument("--end", type=float, default=None); ap.add_argument("--layout", default="asianjeff")
    ap.add_argument("--logo", help="PNG kept on screen the whole clip, top-left of the cam (campaigns that require it, e.g. FaZe)")
    ap.add_argument("--face", help="x,y,w,h of the face cam on the 1920x1080 stream, overriding the layout (cams move between streams)")
    a = ap.parse_args()
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.src], capture_output=True, text=True).stdout)
    end = min(a.end or dur, dur)
    L = LAYOUTS[a.layout]; fx, fy, fw, fh = map(int, a.face.split(",")) if a.face else L["face"]; gx, gy, gw, gh = L["game"]
    face_h = round(1080 * fh / fw / 2) * 2; game_h = 1920 - face_h
    ass = a.out + ".ass"; write_ass(ass, words(a.src, a.start, end), a.hook, hook_y=210 if a.logo else 90)
    vf = (f"[0:v]split[a][b];[a]crop={fw}:{fh}:{fx}:{fy},scale=1080:{face_h}[f];"
          f"[b]crop={gw}:{gh}:{gx}:{gy},scale=-2:{game_h},crop=1080:{game_h}[g];"
          f"[f][g]vstack,subtitles={ass}:fontsdir='{FONT_DIR}'" + ("[s];[1:v]scale=330:-1[l];[s][l]overlay=28:28[v]" if a.logo else "[v]"))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a.start), "-to", str(end), "-i", a.src, *(["-i", a.logo] if a.logo else []), "-filter_complex", vf, "-map", "[v]", "-map", "0:a",
                    "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-c:a", "aac", "-b:a", "160k", "-af", "loudnorm=I=-14:TP=-1.5",
                    "-r", "30", "-movflags", "+faststart", a.out], check=True)
    os.remove(ass); print("done", a.out, f"{end - a.start:.1f} s")


if __name__ == "__main__":
    sys.exit(main())
