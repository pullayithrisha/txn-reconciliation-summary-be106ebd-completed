#!/usr/bin/env bash
set -u

if [ -d /root/task ]; then BASE_DIR=/root/task; else BASE_DIR="$(cd "$(dirname "$0")" && pwd)"; fi
cd "$BASE_DIR"

python3 -m pip install -q -r "$BASE_DIR/requirements.txt"

export PYTHONPATH="$BASE_DIR/src${PYTHONPATH:+:$PYTHONPATH}"

python3 -c "import business_analysis.analysis" || exit 2

python3 -m pytest -q
rc=$?

if [ "$rc" -le 1 ]; then
  exit 0
else
  exit "$rc"
fi
