#!/usr/bin/env bash
set -euo pipefail

# Run the Chimera visual dashboard with the project's virtualenv activated.
# Usage: bash scripts/run_chimera.sh

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

# Activate virtualenv if present
if [ -f ".venv/bin/activate" ]; then
  # shellcheck disable=SC1091
  source ".venv/bin/activate"
fi

export PYTHONPATH="$ROOT_DIR"

echo "Starting Chimera visual dashboard..."
python3 scripts/visual_dashboard.py
