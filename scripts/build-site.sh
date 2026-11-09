#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
node scripts/build-components.mjs
python3 build.py
python3 - <<'PY'
import json
import os
import subprocess
from pathlib import Path

# Public release marker lets either agent verify the exact hosted Git commit.
commit = os.environ.get("CF_PAGES_COMMIT_SHA") or subprocess.check_output(
    ["git", "rev-parse", "HEAD"], text=True
).strip()
Path("dist/deployment.json").write_text(json.dumps({"commit": commit}) + "\n")
PY
node --check dist/app.js
python3 scripts/check-site.py
