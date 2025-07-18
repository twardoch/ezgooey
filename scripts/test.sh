#!/usr/bin/env bash
# this_file: scripts/test.sh
# Test script for ezgooey

set -e

echo "🧪 Running ezgooey test suite..."

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

# Run tests with coverage
echo "🔍 Running tests..."
python -m pytest tests/ -v --cov=ezgooey --cov-report=html --cov-report=term-missing

# Run linting
echo "🔍 Running linting..."
python -m flake8 ezgooey/ --max-line-length=88 --ignore=E203,W503

# Run type checking
echo "🔍 Running type checking..."
python -m mypy ezgooey/ --ignore-missing-imports

# Run basic functionality test
echo "🔍 Testing basic functionality..."
python -c "
import ezgooey
print(f'✅ ezgooey version: {ezgooey.__version__}')

from ezgooey.ez import ezgooey, ArgumentParser
print('✅ ezgooey.ez imports successfully')

import ezgooey.logging as logging
logging.init()
print('✅ ezgooey.logging works')

from version import get_version
print(f'✅ Version management works: {get_version()}')
"

echo "✅ All tests passed!"