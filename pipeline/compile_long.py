"""Long-form compilation: several finished vertical stories in one 16:9 video for YouTube.

usage:  python3 pipeline/compile_long.py OUT.mp4 "Title|path.mp4" "Title|path.mp4" ...
Each story: the vertical video centred, a blurred and darkened copy of itself filling the frame, a chapter card for the first
3.5 s ("STORY 1 · The Second Cup"). A 4 s intro card, 1 s fades between stories, and an outro card. Loudness -14 LUFS.
Prints YouTube chapter timestamps for the description.
"""
import json, os, subprocess, sys, tempfile

W, H, FPS = 1920, 1080, 30
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
ITAL = "/usr/share/fonts/opentype/inter/Inter-Italic.otf"


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)


def esc(t): return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’")


def card(out, lines, seconds):
    """A dark title card with centred lines: [(text, size, colour, italic)]."""
    dt = []
    n = len(lines)
    for i, (txt, size, col, ital) in enumerate(lines):
        y = f"(h/2)+({i}-{(n - 1) / 2})*{int(size * 1.6)}-th/2"
        dt.append(f"drawtext=fontfile={ITAL if ital else FONT}:text='{esc(txt)}':fontsize={size}:fontcolor={col}:x=(w-tw)/2:y={y}:"
                  f"alpha='min(1,t/0.8)*min(1,({seconds}-t)/0.6)'")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"color=c=0x0c0907:s={W}x{H}:r={FPS}:d={seconds}",
                    "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo", "-t", str(seconds), "-vf", ",".join(dt),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", out], check=True)


def story(out, src, num, title):
    d = dur(src)
    fg = f"[0:v]scale=-2:{H},setsar=1[fg]"
    bg = f"[0:v]scale={W}:-2,crop={W}:{H},boxblur=40:3,eq=brightness=-0.18:saturation=0.8[bg]"
    lab = (f"drawtext=fontfile={FONT}:text='STORY {num}':fontsize=34:fontcolor=0xFFD640:x=90:y=h-250:alpha='if(lt(t,3.5),min(1,t/0.5)*min(1,(3.5-t)/0.5),0)',"
           f"drawtext=fontfile={FONT}:text='{esc(title)}':fontsize=64:fontcolor=white:x=90:y=h-200:alpha='if(lt(t,3.5),min(1,t/0.5)*min(1,(3.5-t)/0.5),0)'")
    fade = f"fade=t=in:st=0:d=1,fade=t=out:st={d - 1:.2f}:d=1"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-filter_complex",
                    f"{fg};{bg};[bg][fg]overlay=(W-w)/2:0,{lab},{fade},fps={FPS},format=yuv420p[v];"
                    f"[0:a]aresample=44100,afade=t=in:d=0.6,afade=t=out:st={d - 1:.2f}:d=1,aformat=channel_layouts=stereo[a]",
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", out], check=True)
    return d


if __name__ == "__main__":
    out = sys.argv[1]; items = [a.split("|", 1) for a in sys.argv[2:]]
    tmp = tempfile.mkdtemp(); parts, t, chapters = [], 0.0, []
    intro = os.path.join(tmp, "intro.mp4")
    card(intro, [("D U S T L I G H T", 72, "0xFFECC8", False), ("stories about the things we forgot", 40, "white", True)], 4.0)
    parts.append(intro); t += 4.0; chapters.append((0, "Intro"))
    for i, (title, src) in enumerate(items, 1):
        p = os.path.join(tmp, f"s{i}.mp4"); d = story(p, src, i, title)
        chapters.append((t, title)); parts.append(p); t += d
    outro = os.path.join(tmp, "outro.mp4")
    card(outro, [("Thank you for watching.", 56, "white", True), ("New stories every few days", 40, "0xFFD640", False), ("D U S T L I G H T", 60, "0xFFECC8", False)], 6.0)
    parts.append(outro); chapters.append((t, "Thank you")); t += 6.0
    lst = os.path.join(tmp, "list.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    joined = os.path.join(tmp, "joined.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", joined, "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", out], check=True)
    print(f"done {out} ({dur(out) / 60:.1f} min)")
    print("chapters:")
    for s, name in chapters: print(f"{int(s // 60)}:{int(s % 60):02d} {name}")
