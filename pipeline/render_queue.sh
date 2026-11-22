#!/bin/bash
# Render stories one after another (only one render at a time on this machine). Resumable: finished frames are skipped.
# usage: pipeline/render_queue.sh FRAMES_ROOT story [story ...]     frames go to FRAMES_ROOT/<story>/
ROOT=$1; shift
cd "$(dirname "$0")/.."
for s in "$@"; do
  while pgrep -f "pipeline/anim.py stories/" >/dev/null; do sleep 60; done
  mkdir -p "$ROOT/$s"
  echo "START $s $(date -u +%H:%M)"
  PCT=50; ES=12; [ -f "stories/$s/render.env" ] && . "stories/$s/render.env"     # per-story overrides (e.g. PCT=75 for story videos)
  STYLE=lowpoly ENGINE=EEVEE PCT=$PCT ES=$ES ~/.dustlight-venv/bin/python pipeline/anim.py "stories/$s" "$ROOT/$s" all > "$ROOT/$s/render.log" 2>&1
  echo "END $s $(date -u +%H:%M) $(grep -c SHOT_DONE "$ROOT/$s/render.log") shots, errors: $(grep -c Traceback "$ROOT/$s/render.log")"
done
