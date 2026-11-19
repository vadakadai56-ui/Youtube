"""Upload a finished video to Dropbox /Youtube and print its public link (for Metricool).

usage:  python3 pipeline/publish.py VIDEO.mp4 [/Youtube/name.mp4] [--overwrite]
Needs the Dropbox token saved as an environment network secret for content.dropboxapi.com and api.dropboxapi.com
(the proxy injects it; this script sends a placeholder). Tokens are short-lived (~4 h). Never paste them in chat.
Files over 150 MB go up in 64 MB upload-session chunks.
"""
import json, os, subprocess, sys

CHUNK = 64 * 1024 * 1024
AUTH = "Authorization: Bearer proxy-injected"


def curl(url, arg=None, data_file=None, json_body=None):
    cmd = ["curl", "-sS", "-X", "POST", url, "-H", AUTH]
    if arg is not None: cmd += ["-H", "Dropbox-API-Arg: " + json.dumps(arg), "-H", "Content-Type: application/octet-stream", "--data-binary", "@" + data_file]
    if json_body is not None: cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(json_body)]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    try: return json.loads(out) if out.strip() else {}
    except json.JSONDecodeError: raise SystemExit(f"Dropbox error: {out[:300]}")


def upload(path, dest, overwrite=False):
    size = os.path.getsize(path); mode = "overwrite" if overwrite else "add"
    tmp = path + ".chunk"
    with open(path, "rb") as f:
        first = f.read(CHUNK); open(tmp, "wb").write(first)
        if size <= CHUNK:
            r = curl("https://content.dropboxapi.com/2/files/upload", {"path": dest, "mode": mode, "autorename": not overwrite, "mute": False}, tmp)
        else:
            sid = curl("https://content.dropboxapi.com/2/files/upload_session/start", {"close": False}, tmp)["session_id"]; off = len(first)
            while True:
                buf = f.read(CHUNK); open(tmp, "wb").write(buf)
                last = f.tell() >= size
                if last:
                    r = curl("https://content.dropboxapi.com/2/files/upload_session/finish",
                             {"cursor": {"session_id": sid, "offset": off}, "commit": {"path": dest, "mode": mode, "autorename": not overwrite, "mute": False}}, tmp)
                    break
                curl("https://content.dropboxapi.com/2/files/upload_session/append_v2", {"cursor": {"session_id": sid, "offset": off}, "close": False}, tmp)
                off += len(buf)
    os.remove(tmp)
    if r.get("size") != size: raise SystemExit(f"upload size mismatch: {r}")
    return r["path_display"]


def public_link(dest):
    r = curl("https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings",
             json_body={"path": dest, "settings": {"requested_visibility": "public", "audience": "public", "access": "viewer"}})
    if "url" not in r:
        r = curl("https://api.dropboxapi.com/2/sharing/list_shared_links", json_body={"path": dest, "direct_only": True})
        r = r["links"][0]
    return r["url"].replace("dl=0", "dl=1")


if __name__ == "__main__":
    video = sys.argv[1]; dest = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "/Youtube/" + os.path.basename(video)
    p = upload(video, dest, overwrite="--overwrite" in sys.argv)
    print("uploaded", p, os.path.getsize(video), "bytes")
    print("link", public_link(p))
