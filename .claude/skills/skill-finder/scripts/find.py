"""Rank the installed skills against a request.

usage:  python3 .claude/skills/skill-finder/scripts/find.py "the owner's request" [--n 5] [--all]
Reads every SKILL.md it can find: this repo's .claude/skills/, the account's synced skills (~/.claude/skills/synced/,
invoked as anthropic-skills:NAME), user skills (~/.claude/skills/) and claude.ai's built-in skills (/mnt/skills/).
Account skills that are not enabled are not on disk: search those with the SearchSkills tool.
Scores each skill on its name and description (weighted x3) and its body, with BM25 over words and simple stems.
Prints the top matches with the score and the first line of the description. --all also lists the weak matches.
No network, no dependencies.
"""
import glob, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
# (folder, source label, how to invoke it). First match of a name wins, so repo skills shadow account copies.
ROOTS = [(os.path.normpath(os.path.join(HERE, "..", "..")), "repo", "{name}"),
         (os.path.expanduser("~/.claude/skills/synced"), "account", "anthropic-skills:{name}"),
         (os.path.expanduser("~/.claude/skills"), "user", "{name}"),
         ("/mnt/skills/public", "built-in", "read SKILL.md and follow it"),
         ("/mnt/skills/examples", "built-in example", "read SKILL.md and follow it")]
STOP = set("a an the and or of to in on for with by is are be it this that as at from you your i me my we our use when "
           "whenever any not no do does can will what how into than then also only so if but about all each one two".split())


def stem(w):
    for suf in ("ings", "ing", "ies", "es", "ed", "s"):
        if len(w) > len(suf) + 2 and w.endswith(suf): return w[: -len(suf)]
    return w


def words(t): return [stem(w) for w in re.findall(r"[a-z0-9]+", t.lower()) if w not in STOP and len(w) > 1]


def load():
    seen, out = set(), []
    for root, src, how in ROOTS:
        for f in sorted(glob.glob(os.path.join(root, "**", "SKILL.md"), recursive=True)):
            txt = open(f, errors="ignore").read()
            m = re.match(r"---\s*\n(.*?)\n---\s*\n(.*)", txt, re.S)
            head, body = (m.group(1), m.group(2)) if m else ("", txt)
            name = (re.search(r"^name:\s*(.+)$", head, re.M) or [None, os.path.basename(os.path.dirname(f))])[1].strip().strip("'\"")
            desc = (re.search(r"^description:\s*(.+)$", head, re.M) or [None, ""])[1].strip()
            if name in seen: continue
            seen.add(name)
            out.append({"src": src, "invoke": how.format(name=name), "nameset": set(words(name.replace("-", " "))), "name": name, "desc": desc, "path": f,
                        "tokens": words(name.replace("-", " ")) * 8 + words(desc) * 3 + words(body)})
    return out


def rank(query, skills):
    q = set(words(query)); N = len(skills); avg = sum(len(s["tokens"]) for s in skills) / max(N, 1)
    df = {w: sum(1 for s in skills if w in set(s["tokens"])) for w in q}
    for s in skills:
        tf = {}
        for w in s["tokens"]:
            if w in q: tf[w] = tf.get(w, 0) + 1
        s["score"] = sum(math.log(1 + (N - df[w] + 0.5) / (df[w] + 0.5)) * (c * 2.2) / (c + 1.2 * (0.25 + 0.75 * len(s["tokens"]) / avg))
                         for w, c in tf.items())
        s["score"] += 2.5 * len(q & s["nameset"])                        # a request word in the skill's own name
        s["hits"] = sorted(tf, key=lambda w: -tf[w])[:6]
    return sorted(skills, key=lambda s: -s["score"])


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 5
    if "--n" in sys.argv: args.remove(str(n))
    if not args: sys.exit(__doc__)
    ranked = rank(" ".join(args), load())
    top = ranked[0]["score"] or 1
    for s in ranked if "--all" in sys.argv else ranked[:n]:
        if s["score"] <= 0: break
        print(f"{s['score'] / top:4.2f}  {s['name']:<26} [{s['src']}]  {', '.join(s['hits'])}\n"
              f"      {s['desc'][:150]}\n      invoke: {s['invoke']}   file: {s['path']}")
