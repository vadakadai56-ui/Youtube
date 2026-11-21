"""UserPromptSubmit hook: rank every skill against the owner's message and hand the shortlist to Claude as context.
Reads the hook JSON on stdin ({"prompt": ...}); prints the useful skills; never blocks the prompt."""
import json, os, subprocess, sys

try:
    prompt = (json.load(sys.stdin).get("prompt") or "").strip()
except Exception:
    sys.exit(0)
if len(prompt.split()) < 3 or prompt.startswith("/"):        # short replies ("ok", "1") and slash commands: no hint
    sys.exit(0)
root = os.environ.get("CLAUDE_PROJECT_DIR", os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
finder = os.path.join(root, ".claude", "skills", "skill-finder", "scripts", "find.py")
try:
    out = subprocess.run([sys.executable, finder, prompt[:2000], "--useful"], capture_output=True, text=True, timeout=20).stdout
except Exception:
    sys.exit(0)
lines = [l for l in out.splitlines() if l[:1].isdigit() or l.startswith("      invoke:")]
if not lines: sys.exit(0)
print("skill-finder shortlist for this message (word match; follow the skill-finder skill: keep every skill that adds "
      "something useful, drop the rest, run them in order, stop at owner gates):")
print("\n".join(l.split("   file:")[0] for l in lines))
