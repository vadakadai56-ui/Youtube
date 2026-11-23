"""Post to Instagram with the owner's own Meta app (Instagram API with Instagram Login). No Windsor, no Metricool.
The token never touches this repo: the cloud proxy adds it to every request to graph.instagram.com (a network secret,
saved through the secure form). Media must be at a public URL (Dustlight-Files on GitHub works).

  python3 pipeline/ig_direct.py me                                       # check the token: prints the account
  python3 pipeline/ig_direct.py reel URL "caption" [--thumb MS] [--trial] [--comment "text"]
  python3 pipeline/ig_direct.py story URL
  python3 pipeline/ig_direct.py carousel "caption" URL1 URL2 ... [--comment "text"]
Prints one JSON line: {"ok": true, "media_id": ..., "permalink": ...} or {"ok": false, "error": ...}."""
import json, sys, time, urllib.error, urllib.parse, urllib.request

API = "https://graph.instagram.com/v23.0/"


def call(path, method="GET", **params):
    data = urllib.parse.urlencode({k: (json.dumps(v) if isinstance(v, (dict, list)) else v) for k, v in params.items()}).encode()
    url = API + path + ("?" + data.decode() if method == "GET" and params else "")
    req = urllib.request.Request(url, data=data if method == "POST" else None, method=method,
                                 headers={"Authorization": "Bearer proxy-adds-the-real-token"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as e:
        raise SystemExit(json.dumps({"ok": False, "error": e.read().decode()[:600]}))


def publish(container):
    """Wait for Instagram to fetch and process the media, then publish it. Video takes about 30 s to 3 min."""
    for _ in range(60):
        st = call(container, fields="status_code,status")
        if st.get("status_code") == "FINISHED": break
        if st.get("status_code") == "ERROR": raise SystemExit(json.dumps({"ok": False, "error": st.get("status")}))
        time.sleep(10)
    else: raise SystemExit(json.dumps({"ok": False, "error": "media still processing after 10 min", "container": container}))
    mid = call("me/media_publish", "POST", creation_id=container)["id"]
    return mid, call(mid, fields="permalink").get("permalink")


def main(a):
    opt = lambda k: a[a.index(k) + 1] if k in a else None
    cmd = a[0]
    if cmd == "me": print(json.dumps(call("me", fields="user_id,username,account_type"))); return
    if cmd == "reel":
        p = dict(media_type="REELS", video_url=a[1], caption=a[2], share_to_feed="true")
        if opt("--thumb"): p["thumb_offset"] = opt("--thumb")
        if "--trial" in a: p["trial_params"] = {"graduation_strategy": "SS_PERFORMANCE"}
        c = call("me/media", "POST", **p)["id"]
    elif cmd == "story":
        c = call("me/media", "POST", media_type="STORIES", video_url=a[1])["id"]
    elif cmd == "carousel":
        urls = [u for u in a[2:] if u.startswith("https://")]
        kids = [call("me/media", "POST", image_url=u, is_carousel_item="true")["id"] for u in urls]   # images are ready at once
        c = call("me/media", "POST", media_type="CAROUSEL", children=",".join(kids), caption=a[1])["id"]
    else: raise SystemExit(__doc__)
    mid, link = publish(c)
    if opt("--comment"): call(mid + "/comments", "POST", message=opt("--comment"))
    print(json.dumps({"ok": True, "media_id": mid, "permalink": link}))


if __name__ == "__main__":
    main(sys.argv[1:] or ["me"])
