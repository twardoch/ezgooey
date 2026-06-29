#!/usr/bin/env bash
# this_file: install.sh
# Install ezgooey in editable mode.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "==> Installing ezgooey (editable)..."
uv pip install -e .
echo "Done."
