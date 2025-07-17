#!/usr/bin/env bash
# this_file: scripts/release.sh
# Release script for ezgooey with git tag-based versioning

set -e

USAGE="Usage: ./scripts/release.sh [patch|minor|major] [release_message]"

if [ $# -lt 2 ]; then
    echo "$USAGE"
    exit 1
fi

BUMP_TYPE=$1
RELEASE_MESSAGE=$2

echo "🚀 Starting release process..."

# Ensure we're on the main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "master" ] && [ "$CURRENT_BRANCH" != "main" ]; then
    echo "❌ Must be on master or main branch to release"
    exit 1
fi

# Ensure working directory is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ Working directory is not clean. Please commit or stash changes."
    exit 1
fi

# Get current version
CURRENT_VERSION=$(python3 version.py get)
echo "📋 Current version: $CURRENT_VERSION"

# Bump version
NEW_VERSION=$(python3 version.py bump $BUMP_TYPE)
echo "📋 New version: $NEW_VERSION"

# Update VERSION.txt
echo "v$NEW_VERSION" > VERSION.txt

# Update version in __init__.py fallback
sed -i.bak "s/__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" ezgooey/__init__.py
rm ezgooey/__init__.py.bak

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

# Run tests
echo "🧪 Running tests..."
./scripts/test.sh

# Build package
echo "🏗️  Building package..."
./scripts/build.sh

# Commit changes
echo "📝 Committing changes..."
git add --all
git commit -m "v$NEW_VERSION: $RELEASE_MESSAGE"

# Create and push tag
echo "🏷️  Creating git tag..."
git tag -a "v$NEW_VERSION" -m "v$NEW_VERSION: $RELEASE_MESSAGE"

echo "📤 Pushing to remote..."
git push origin $(git branch --show-current)
git push origin "v$NEW_VERSION"

echo "✅ Release $NEW_VERSION completed successfully!"
echo "🏷️  Git tag: v$NEW_VERSION"
echo "📦 Package files are in dist/"
echo ""
echo "Next steps:"
echo "1. Go to GitHub and create a release for tag v$NEW_VERSION"
echo "2. Upload dist/* files as release assets"
echo "3. To publish to PyPI: python -m twine upload dist/*"