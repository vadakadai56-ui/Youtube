#!/bin/bash
# Reinstall the Edit Kit skills (41 skills, about 113 MB) in a fresh cloud session.
# The kit is not committed (too big for git). It is downloaded from the owner's Google Drive copy.
# Needs drive.usercontent.google.com and raw.githubusercontent.com in the environment's allowed hosts.
# Usage: bash pipeline/install_editkit.sh
set -e
KIT_ID="1f31jxWaWg1XRs4C8t9xZdb1N0FqwBLwU"     # Edit-Kit.zip in the owner's shared Drive folder
WORK="${TMPDIR:-/tmp}/editkit-install"
rm -rf "$WORK" && mkdir -p "$WORK" && cd "$WORK"

echo "Downloading Edit-Kit.zip ..."
curl -sSL -o Edit-Kit.zip "https://drive.usercontent.google.com/download?id=$KIT_ID&export=download&confirm=t"
unzip -q Edit-Kit.zip
bash Edit-Kit/install.sh >/dev/null && echo "Installed $(ls Edit-Kit/skills | wc -l) skills into ~/.claude/skills"

# The kit fetches fonts from github.com (blocked here) and GSAP from jsDelivr (blocked here).
# Pre-fill its cache from raw.githubusercontent.com and npm instead.
CACHE="$HOME/.cache/motionkit"; mkdir -p "$CACHE"
python3 -I - <<'EOF'
import os, re, urllib.request
src = open(os.path.expanduser("~/.claude/skills/fx/scripts/new_project.py")).read()
cache = os.path.expanduser("~/.cache/motionkit")
for name, url in re.findall(r'"([^"]+\.ttf)":\s*"([^"]+)"', src):
    url = url.replace("https://github.com/google/fonts/raw/main/", "https://raw.githubusercontent.com/google/fonts/main/")
    p = os.path.join(cache, name)
    if not os.path.exists(p) or os.path.getsize(p) < 1000:
        urllib.request.urlretrieve(url, p)
print("fonts cached")
EOF
if [ ! -s "$CACHE/gsap.min.js" ]; then
  npm pack gsap@3.12.5 --silent >/dev/null && tar xzf gsap-3.12.5.tgz && cp package/dist/gsap.min.js "$CACHE/"
fi
echo "GSAP cached"

if [ "$1" = "--test" ]; then python3 -I Edit-Kit/selftest.py | grep -E "PASS|FAIL|ALL|SOMETHING"; fi
echo "Done. Start a new Claude Code session (or reload) so the skills are picked up."
