#!/usr/bin/env bash
# Run agent_analyzer.py using a local venv (bootstrapped on first use).
# Usage: ./run-analyzer.sh [-h|--help] [agent_analyzer.py args...]
#
# The first run creates .venv next to this script and installs `rich` from the
# network. A marker file is written only after the install succeeds, so an
# interrupted bootstrap is rebuilt on the next run rather than reused half-made.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
MARKER="$VENV_DIR/.bootstrap-ok"
RICH_SPEC="rich>=13,<15"

case "${1:-}" in
    -h|--help)
        sed -n '2,8p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
        echo
        echo "Arguments are passed through to agent_analyzer.py:"
        echo
        if [ -x "$VENV_DIR/bin/python3" ] && [ -f "$MARKER" ]; then
            exec "$VENV_DIR/bin/python3" "$SCRIPT_DIR/agent_analyzer.py" --help
        fi
        echo "  (venv not bootstrapped yet; run once without -h to create it)"
        echo "  Common flags: -d DIR  -q (quiet)  -e (expect agents)  -p (script dir)"
        exit 0
        ;;
esac

if ! command -v python3 >/dev/null 2>&1; then
    echo "error: python3 not found in PATH" >&2
    exit 127
fi

if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)'; then
    echo "error: python >= 3.10 required (found $(python3 -V 2>&1))" >&2
    exit 1
fi

if [ ! -f "$MARKER" ]; then
    echo "Creating virtual environment in $VENV_DIR ..." >&2
    rm -rf "$VENV_DIR"
    trap 'rm -rf "$VENV_DIR"' ERR
    trap 'rm -rf "$VENV_DIR"; exit 130' INT TERM
    python3 -m venv "$VENV_DIR" >&2
    "$VENV_DIR/bin/pip" install --quiet "$RICH_SPEC" >&2
    touch "$MARKER"
    trap - ERR INT TERM
fi

exec "$VENV_DIR/bin/python3" "$SCRIPT_DIR/agent_analyzer.py" "$@"
