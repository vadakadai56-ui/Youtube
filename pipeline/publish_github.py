"""Publish a finished video for Metricool through the public GitHub repo vadakadai56-ui/Dustlight-Files (no expiring tokens).

usage:  python3 pipeline/publish_github.py VIDEO.mp4 [name.mp4]
- Makes an upload copy under 95 MB if needed (GitHub refuses files over 100 MB): 1080p H.264, CRF 23 to 27, AAC 192k.
- Commits it to Dustlight-Files/videos/<name>.mp4, pushes, and prints the public raw URL to give Metricool as media.
Needs the Dustlight-Files repo (public) attached to the session and cloned at /home/user/dustlight-files (or DUSTLIGHT_MEDIA).
"""
import os, subprocess, sys

REPO = os.path.expanduser(os.environ.get("DUSTLIGHT_MEDIA", "/home/user/dustlight-files"))
LIMIT = 95 * 1024 * 1024
RAW = "https://raw.githubusercontent.com/vadakadai56-ui/Dustlight-Files/main/videos/{}"
ATTR = "\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01AYwv5HqZqh8aWTPnMgsdfG"


def run(*cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode: sys.exit(f"failed: {' '.join(cmd)}\n{r.stderr[-800:]}")
    return r.stdout


def upload_copy(src, dst):
    if os.path.getsize(src) <= LIMIT:
        run("cp", src, dst); return
    for crf in (23, 25, 27):
        run("ffmpeg", "-y", "-v", "error", "-i", src, "-c:v", "libx264", "-crf", str(crf), "-maxrate", "8M", "-bufsize", "16M",
            "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", dst)
        if os.path.getsize(dst) <= LIMIT: return
    sys.exit(f"still over 95 MB after CRF 27: {os.path.getsize(dst) / 1e6:.0f} MB")


if __name__ == "__main__":
    src = sys.argv[1]; name = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(src)
    if not os.path.isdir(os.path.join(REPO, ".git")): sys.exit(f"no clone at {REPO}")
    os.makedirs(os.path.join(REPO, "videos"), exist_ok=True)
    dst = os.path.join(REPO, "videos", name)
    upload_copy(src, dst)
    if subprocess.run(["git", "rev-parse", "-q", "--verify", "HEAD"], cwd=REPO, capture_output=True).returncode == 0:
        run("git", "pull", "-q", "--rebase", "origin", "main", cwd=REPO)
    else:
        run("git", "checkout", "-q", "-b", "main", cwd=REPO)             # first upload into an empty repo
    run("git", "add", os.path.join("videos", name), cwd=REPO)
    run("git", "commit", "-qm", f"Add {name}{ATTR}", cwd=REPO)
    run("git", "-c", "push.negotiate=true", "push", "-q", "origin", "main", cwd=REPO)
    print(f"uploaded {name} ({os.path.getsize(dst) / 1e6:.1f} MB)\nurl {RAW.format(name)}")
