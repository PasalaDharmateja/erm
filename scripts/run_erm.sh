#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH="$PWD/src"
.venv/bin/python -m erm.main --config config/erm_config.yml
