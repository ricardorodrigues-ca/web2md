#!/usr/bin/env bash
# Launcher for web2md: creates a local virtualenv, installs dependencies, and runs the app.
# Usage: ./web2md.sh <url> [options]   (all arguments are passed through to web2md.py)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
REQUIREMENTS="$SCRIPT_DIR/requirements.txt"
STAMP="$VENV_DIR/.requirements.stamp"

if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: python3 not found. Please install Python 3." >&2
    exit 1
fi

if [ ! -x "$VENV_DIR/bin/python" ]; then
    echo "Creating virtual environment in $VENV_DIR..." >&2
    python3 -m venv "$VENV_DIR"
fi

# Reinstall dependencies only when requirements.txt changes
if [ ! -f "$STAMP" ] || [ "$REQUIREMENTS" -nt "$STAMP" ]; then
    echo "Installing dependencies..." >&2
    "$VENV_DIR/bin/python" -m pip install --quiet --upgrade pip
    "$VENV_DIR/bin/python" -m pip install --quiet -r "$REQUIREMENTS"
    touch "$STAMP"
fi

exec "$VENV_DIR/bin/python" "$SCRIPT_DIR/web2md.py" "$@"
