#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 build.py
node --check dist/app.js
python3 scripts/check-site.py
