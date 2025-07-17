#!/usr/bin/env bash
# this_file: scripts/install.sh
# Easy installation script for ezgooey

set -e

INSTALL_DIR="${INSTALL_DIR:-$HOME/.local/bin}"
PYTHON_CMD="${PYTHON_CMD:-python3}"

echo "🚀 Installing ezgooey..."

# Check if Python is available
if ! command -v "$PYTHON_CMD" &> /dev/null; then
    echo "❌ Python 3 is required but not found. Please install Python 3.8 or later."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || [ "$PYTHON_MAJOR" -eq 3 -a "$PYTHON_MINOR" -lt 8 ]; then
    echo "❌ Python 3.8 or later is required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION found"

# Create install directory
mkdir -p "$INSTALL_DIR"

# Install ezgooey
echo "📦 Installing ezgooey package..."
$PYTHON_CMD -m pip install --user ezgooey

# Verify installation
echo "🔍 Verifying installation..."
$PYTHON_CMD -c "
import ezgooey
print(f'✅ ezgooey {ezgooey.__version__} installed successfully')

# Test basic functionality
from ezgooey.ez import ezgooey, ArgumentParser
import ezgooey.logging as logging

print('✅ All modules imported successfully')
"

echo ""
echo "🎉 ezgooey installation completed!"
echo ""
echo "📚 Quick start:"
echo "  1. Create a Python script with argparse"
echo "  2. Add @ezgooey decorator to your argument parser function"
echo "  3. Run without arguments for GUI, with arguments for CLI"
echo ""
echo "📖 Documentation: https://github.com/twardoch/ezgooey"
echo "🐛 Issues: https://github.com/twardoch/ezgooey/issues"
echo ""
echo "Example usage:"
echo "  python -c \"from ezgooey.ez import ezgooey, ArgumentParser; print('Ready to use!')\""