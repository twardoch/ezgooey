#!/usr/bin/env bash
# this_file: scripts/build.sh
# Build script for ezgooey

set -e

echo "🏗️  Building ezgooey package..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Get version from git tag
VERSION=$(python3 version.py get)
echo "📋 Building version: $VERSION"

# Build package
echo "🏗️  Building package..."
python -m build

# Verify package contents
echo "🔍 Verifying package contents..."
python -m twine check dist/*

# List built files
echo "📦 Built files:"
ls -la dist/

echo "✅ Build completed successfully!"
echo "📦 Package files are in dist/"
echo "🚀 To upload to PyPI: python -m twine upload dist/*"