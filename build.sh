#!/usr/bin/env bash
# this_file: build.sh
# Build script for ezgooey (legacy setuptools-based package)
# Lints, formats, runs tests, and builds the package.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "==> Linting and formatting..."
uvx ruff check --fix ezgooey tests || true
uvx ruff format ezgooey tests || true

echo "==> Running tests..."
uvx pytest tests/

echo "==> Building package..."
uvx hatch build

echo "Build complete. Distributions in dist/"
