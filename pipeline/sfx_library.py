"""Build the Dustlight sound library: real recorded CC0 sound effects from Openverse (mostly freesound), sorted by category.

usage:
  python3 pipeline/sfx_library.py build [LIB_DIR]      # default ~/dustlight-sfx; skips files already there
  python3 pipeline/sfx_library.py list                 # what the manifest holds

Only CC0 (no credit needed) so the library can be used anywhere without tracking credits.
channel/sfx-library.json is the manifest (committed): category, query, Openverse id, title, creator, source page, file name.
The audio itself is not committed. It is backed up to Dropbox /Dustlight-sfx/ and can be rebuilt from the manifest.
"""
import json, os, re, sys, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from openverse import call, UA

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "channel", "sfx-library.json")
# category folder -> (queries, how many per query, longest clip in seconds)
WANT = {
    "ambience/fire":       (["campfire crackle", "fireplace crackling"], 2, 90),
    "ambience/wind":       (["winter wind", "wind howling"], 2, 90),
    "ambience/rain":       (["rain on window", "light rain"], 2, 90),
    "ambience/night":      (["night crickets", "forest night ambience"], 1, 90),
    "ambience/room":       (["room tone quiet", "clock ticking"], 2, 60),
    "ambience/park":       (["park children playing distant", "city park ambience"], 1, 90),
    "nature/birds":        (["birds chirping morning", "songbird"], 2, 60),
    "foley/footsteps":     (["footsteps snow", "footsteps wood floor", "footsteps gravel"], 1, 30),
    "foley/door":          (["door creak", "door close", "door knock"], 1, 15),
    "foley/swing":         (["swing chain squeak", "playground swing creak"], 2, 30),
    "foley/cloth":         (["cloth rustle", "blanket"], 1, 15),
    "foley/kitchen":       (["teacup saucer", "kettle whistle", "pouring tea"], 1, 30),
    "foley/paper":         (["paper page turn", "envelope open"], 1, 10),
    "foley/glass":         (["tap on glass window", "glass clink"], 1, 10),
    "foley/toys":          (["music box", "wind up toy"], 1, 40),
    "foley/keys":          (["keys jingle", "lock click"], 1, 10),
    "bells/clock":         (["clock chime", "church bell distant"], 1, 30),
    "bells/chime":         (["wind chimes", "small bell"], 1, 20),
    "transitions/whoosh":  (["soft whoosh", "swoosh"], 2, 5),
    "transitions/riser":   (["riser", "swell"], 1, 12),
    "transitions/hit":     (["soft impact boom", "low thud"], 1, 6),
    "human/breath":        (["sigh", "breath"], 1, 6),
    "human/heartbeat":     (["heartbeat"], 1, 20),
}


def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40]


def build(lib):
    old = {e["id"]: e for e in json.load(open(MANIFEST))} if os.path.exists(MANIFEST) else {}
    out, seen = [], set()
    for cat, (queries, per, max_s) in WANT.items():
        os.makedirs(os.path.join(lib, cat), exist_ok=True)
        for q in queries:
            try:
                rows = call("audio/", q=q, license="cc0", page_size=20)["results"]
            except Exception as e:
                print(f"! search failed: {q}: {e}"); continue
            got = 0
            for r in rows:
                if got >= per: break
                d = (r.get("duration") or 0) / 1000
                if r["id"] in seen or not (0.2 < d <= max_s) or r["license"] != "cc0": continue
                url = r["url"]; ext = os.path.splitext(urllib.parse.urlparse(url).path)[1] or ".mp3"
                fn = f"{slug(r['title'])}-{r['id'][:8]}{ext}"; path = os.path.join(lib, cat, fn)
                if not os.path.exists(path):
                    try:
                        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as resp:
                            data = resp.read()
                        open(path, "wb").write(data)
                    except Exception as e:
                        print(f"! download failed: {r['title']}: {e}"); continue
                seen.add(r["id"]); got += 1
                out.append(old.get(r["id"]) or {"category": cat, "query": q, "id": r["id"], "title": r["title"],
                            "creator": r.get("creator"), "source": r.get("foreign_landing_url"), "license": "CC0",
                            "secs": round(d, 1), "file": f"{cat}/{fn}"})
                print(f"  {cat:<20} {d:5.1f}s  {r['title'][:50]}")
            if got < per: print(f"! only {got}/{per} for '{q}'")
    json.dump(out, open(MANIFEST, "w"), indent=1)
    print(f"{len(out)} sounds in {lib}; manifest {MANIFEST}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    lib = os.path.expanduser(sys.argv[2] if len(sys.argv) > 2 else "~/dustlight-sfx")
    if cmd == "build": build(lib)
    else:
        for e in json.load(open(MANIFEST)): print(f"{e['file']}  ({e['secs']}s, {e['creator']})")
