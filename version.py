#!/usr/bin/env python3
# this_file: version.py
"""
Version management utilities for ezgooey.
Provides git-tag-based semantic versioning.
"""

import os
import re
import subprocess
from typing import Optional


def get_git_tag_version() -> Optional[str]:
    """Get the latest git tag version."""
    try:
        # Get the latest git tag
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__)),
            check=False
        )
        
        if result.returncode == 0:
            tag = result.stdout.strip()
            # Clean up tag format (remove 'v' prefix if present)
            if tag.startswith('v'):
                tag = tag[1:]
            return tag
        
        # If no tags exist, try to get from git log
        result = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__)),
            check=False
        )
        
        if result.returncode == 0:
            # Look for version pattern in commit message
            commit_msg = result.stdout.strip()
            version_match = re.search(r'v?(\d+\.\d+\.\d+)', commit_msg)
            if version_match:
                return version_match.group(1)
            
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    
    return None


def get_version_from_file(file_path: str) -> Optional[str]:
    """Get version from a file (fallback method)."""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read().strip()
                # Handle both VERSION.txt format and __version__ format
                if content.startswith('v'):
                    return content[1:]
                elif content.startswith('__version__'):
                    match = re.search(r'["\']([^"\']*)["\']', content)
                    if match:
                        return match.group(1)
                else:
                    return content
    except (IOError, OSError):
        pass
    
    return None


def get_version() -> str:
    """
    Get the current version using the following priority:
    1. Git tag (semantic versioning)
    2. VERSION.txt file
    3. ezgooey/__init__.py __version__
    4. Default fallback
    """
    # Try git tag first
    version = get_git_tag_version()
    if version:
        return version
    
    # Try VERSION.txt
    version = get_version_from_file("VERSION.txt")
    if version:
        return version
    
    # Try __init__.py
    version = get_version_from_file("ezgooey/__init__.py")
    if version:
        return version
    
    # Default fallback
    return "0.0.0"


def is_valid_semver(version: str) -> bool:
    """Check if version follows semantic versioning format."""
    pattern = r'^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$'
    return bool(re.match(pattern, version))


def bump_version(version: str, part: str = "patch") -> str:
    """
    Bump version according to semantic versioning.
    
    Args:
        version: Current version string
        part: Which part to bump ('major', 'minor', 'patch')
    
    Returns:
        New version string
    """
    if not is_valid_semver(version):
        raise ValueError(f"Invalid semantic version: {version}")
    
    # Split version into parts
    parts = version.split('.')
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid part: {part}. Must be 'major', 'minor', or 'patch'")
    
    return f"{major}.{minor}.{patch}"


if __name__ == "__main__":
    # CLI interface for version management
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "get":
            print(get_version())
        elif command == "bump":
            current = get_version()
            part = sys.argv[2] if len(sys.argv) > 2 else "patch"
            new_version = bump_version(current, part)
            print(new_version)
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)
    else:
        print(get_version())