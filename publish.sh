#!/usr/bin/env bash
# this_file: publish.sh
# Build, install, bump version, and publish ezgooey to PyPI.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "==> Building..."
bash "$SCRIPT_DIR/build.sh"

echo "==> Installing..."
bash "$SCRIPT_DIR/install.sh"

echo "==> Bumping version..."
uvx gitnextver@latest .

echo "==> Building final distributions..."
uvx hatch build

echo "==> Publishing to PyPI..."
uv publish

echo "Published."
