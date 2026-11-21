"""Free, openly licensed sounds and images from the Openverse public API (api.openverse.org).

usage:
  python3 pipeline/openverse.py audio "campfire crackle" [--license cc0] [--n 10] [--max-secs 60]
  python3 pipeline/openverse.py image "snowy pine forest" [--license cc0,by] [--n 10]
  python3 pipeline/openverse.py get audio|image ID STORY_DIR      # downloads to STORY_DIR/assets/, adds a line to STORY_DIR/CREDITS.md

Licences: only cc0, pdm (public domain), by (credit required) and by-sa (credit, share-alike) are allowed here. Non-commercial (nc) and
no-derivatives (nd) licences are refused because the channel is monetised and every clip gets edited.
Downloads come from the provider's own host (mostly cdn.freesound.org and upload.wikimedia.org); other hosts may be blocked by the
environment's network settings.
"""
import argparse, json, os, re, sys, urllib.parse, urllib.request

API = "https://api.openverse.org/v1"
OK = {"cc0", "pdm", "by", "by-sa"}
UA = {"User-Agent": "dustlight-pipeline/1.0"}
EP = {"audio": "audio", "image": "images"}   # API path for each kind


def call(path, **q):
    url = f"{API}/{path}" + ("?" + urllib.parse.urlencode(q) if q else "")
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return json.load(r)


def check_licences(s):
    lic = [x.strip().lower() for x in s.split(",") if x.strip()]
    bad = [x for x in lic if x not in OK]
    if bad: sys.exit(f"licence not allowed for this channel: {', '.join(bad)} (use {', '.join(sorted(OK))})")
    return ",".join(lic)


def search(kind, q, lic, n, max_secs):
    d = call(f"{EP[kind]}/", q=q, license=lic, page_size=min(n * 2 if max_secs else n, 50))
    rows = d["results"]
    if kind == "audio" and max_secs: rows = [r for r in rows if (r.get("duration") or 0) <= max_secs * 1000]
    print(f"{d['result_count']} matches for '{q}' ({lic}); showing {min(n, len(rows))}")
    for r in rows[:n]:
        extra = f"{(r.get('duration') or 0) / 1000:5.1f}s" if kind == "audio" else f"{r.get('width')}x{r.get('height')}"
        print(f"{r['id']}  {extra}  {r['license']:<5}  {r['provider']:<12}  {r['title'][:60]}")


def credit_line(r):
    lic = r["license"].upper() + (" " + r["license_version"] if r.get("license_version") else "")
    by = r.get("creator") or "unknown creator"
    return f"- \"{r['title']}\" by {by} ({r.get('foreign_landing_url') or r.get('url')}), {lic} ({r.get('license_url', '')}), via Openverse"


def get(kind, ident, story_dir):
    r = call(f"{EP[kind]}/{ident}/")
    if r["license"] not in OK: sys.exit(f"refused: licence {r['license']} is not allowed")
    url = r["url"]; ext = os.path.splitext(urllib.parse.urlparse(url).path)[1] or (".mp3" if kind == "audio" else ".jpg")
    name = re.sub(r"[^a-z0-9]+", "-", r["title"].lower()).strip("-")[:40] or ident[:8]
    dest_dir = os.path.join(story_dir, "assets"); os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, f"{name}-{ident[:8]}{ext}")
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as resp, open(dest, "wb") as f:
        f.write(resp.read())
    cred = os.path.join(story_dir, "CREDITS.md"); line = credit_line(r)
    old = open(cred).read() if os.path.exists(cred) else "# Credits\n\nOpenly licensed media used in this video. Paste the BY / BY-SA lines into the YouTube description.\n\n"
    if line not in old: open(cred, "w").write(old + line + "\n")
    print(f"saved {dest}\ncredit: {line}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["audio", "image", "get"]); ap.add_argument("args", nargs="+")
    ap.add_argument("--license", default="cc0,pdm"); ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--max-secs", type=float, default=0)
    a = ap.parse_args()
    if a.cmd == "get":
        if len(a.args) != 3 or a.args[0] not in EP: sys.exit("usage: get audio|image ID STORY_DIR")
        get(*a.args)
    else:
        search(a.cmd, " ".join(a.args), check_licences(a.license), a.n, a.max_secs)
