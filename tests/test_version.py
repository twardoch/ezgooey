#!/usr/bin/env python3
# this_file: tests/test_version.py
"""Tests for version management functionality."""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock
import subprocess

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from version import (
    get_git_tag_version,
    get_version_from_file,
    get_version,
    is_valid_semver,
    bump_version
)


class TestVersionManagement(unittest.TestCase):
    """Test cases for version management functions."""

    def test_is_valid_semver(self):
        """Test semantic version validation."""
        valid_versions = [
            "1.0.0",
            "2.1.3",
            "0.0.1",
            "1.0.0-alpha",
            "1.0.0-alpha.1",
            "1.0.0+build.1",
            "1.0.0-alpha+build.1"
        ]
        
        invalid_versions = [
            "1.0",
            "1.0.0.0",
            "1.0.0-",
            "1.0.0+",
            "v1.0.0",
            "1.0.0-alpha..1",
            "1.0.0+build..1"
        ]
        
        for version in valid_versions:
            with self.subTest(version=version):
                self.assertTrue(is_valid_semver(version))
        
        for version in invalid_versions:
            with self.subTest(version=version):
                self.assertFalse(is_valid_semver(version))

    def test_bump_version(self):
        """Test version bumping functionality."""
        base_version = "1.2.3"
        
        # Test patch bump
        self.assertEqual(bump_version(base_version, "patch"), "1.2.4")
        
        # Test minor bump
        self.assertEqual(bump_version(base_version, "minor"), "1.3.0")
        
        # Test major bump
        self.assertEqual(bump_version(base_version, "major"), "2.0.0")
        
        # Test invalid part
        with self.assertRaises(ValueError):
            bump_version(base_version, "invalid")
        
        # Test invalid version
        with self.assertRaises(ValueError):
            bump_version("invalid.version", "patch")

    def test_get_version_from_file(self):
        """Test reading version from file."""
        # Test with VERSION.txt format
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("v1.2.3")
            f.flush()
            
            version = get_version_from_file(f.name)
            self.assertEqual(version, "1.2.3")
            
            os.unlink(f.name)
        
        # Test with plain version format
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("2.0.0")
            f.flush()
            
            version = get_version_from_file(f.name)
            self.assertEqual(version, "2.0.0")
            
            os.unlink(f.name)
        
        # Test with __version__ format
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('__version__ = "1.5.0"')
            f.flush()
            
            version = get_version_from_file(f.name)
            self.assertEqual(version, "1.5.0")
            
            os.unlink(f.name)
        
        # Test with non-existent file
        version = get_version_from_file("/non/existent/file.txt")
        self.assertIsNone(version)

    @patch('subprocess.run')
    def test_get_git_tag_version(self, mock_run):
        """Test getting version from git tags."""
        # Test successful git describe
        mock_run.return_value = MagicMock(returncode=0, stdout="v1.2.3\n")
        version = get_git_tag_version()
        self.assertEqual(version, "1.2.3")
        
        # Test git describe without v prefix
        mock_run.return_value = MagicMock(returncode=0, stdout="2.0.0\n")
        version = get_git_tag_version()
        self.assertEqual(version, "2.0.0")
        
        # Test git describe failure, fallback to git log
        mock_run.side_effect = [
            MagicMock(returncode=1, stdout=""),  # git describe fails
            MagicMock(returncode=0, stdout="abc123 v1.5.0: some commit message\n")  # git log success
        ]
        version = get_git_tag_version()
        self.assertEqual(version, "1.5.0")
        
        # Test complete failure
        mock_run.side_effect = [
            MagicMock(returncode=1, stdout=""),  # git describe fails
            MagicMock(returncode=1, stdout="")   # git log fails
        ]
        version = get_git_tag_version()
        self.assertIsNone(version)

    @patch('version.get_git_tag_version')
    @patch('version.get_version_from_file')
    def test_get_version_priority(self, mock_file, mock_git):
        """Test version retrieval priority."""
        # Test git tag priority
        mock_git.return_value = "2.0.0"
        mock_file.return_value = "1.0.0"
        
        version = get_version()
        self.assertEqual(version, "2.0.0")
        
        # Test fallback to file when git fails
        mock_git.return_value = None
        mock_file.return_value = "1.5.0"
        
        version = get_version()
        self.assertEqual(version, "1.5.0")
        
        # Test fallback to default when all fail
        mock_git.return_value = None
        mock_file.return_value = None
        
        version = get_version()
        self.assertEqual(version, "0.0.0")


if __name__ == '__main__':
    unittest.main()