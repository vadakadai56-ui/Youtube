#!/usr/bin/env bash
# One-time setup for a fresh cloud session: Blender as a Python module (3.11) + Mesa for headless Eevee.
set -e
VENV="${VENV:-$HOME/.dustlight-venv}"
if ! "$VENV/bin/python" -c "import bpy" 2>/dev/null; then
  python3.11 -m venv "$VENV"
  "$VENV/bin/pip" install -q bpy==5.0.1 numpy
fi
if ! ldconfig -p | grep -q libEGL.so.1; then
  (apt-get install -y -q libegl1 libgl1-mesa-dri libegl-mesa0 libgles2 || (apt-get update -q && apt-get install -y -q libegl1 libgl1-mesa-dri libegl-mesa0 libgles2)) >/dev/null
fi
"$VENV/bin/python" -c "import bpy; print('bpy', bpy.app.version_string)"
