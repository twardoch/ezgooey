# this_file: tests/conftest.py
"""Pytest configuration and fixtures for ezgooey tests."""

import os
import sys
import pytest
from unittest.mock import patch

# Add parent directory to path for all tests
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(autouse=True)
def mock_sys_argv():
    """Mock sys.argv to prevent GUI mode during tests."""
    with patch('sys.argv', ['test_script.py', '--test-mode']):
        yield


@pytest.fixture
def temp_version_file(tmp_path):
    """Create a temporary version file for testing."""
    version_file = tmp_path / "VERSION.txt"
    version_file.write_text("2.0.0")
    return str(version_file)


@pytest.fixture
def mock_git_commands():
    """Mock git commands for version testing."""
    with patch('subprocess.run') as mock_run:
        yield mock_run


@pytest.fixture
def clean_logging():
    """Clean logging configuration before each test."""
    import logging
    # Clear all handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Reset level
    root_logger.setLevel(logging.WARNING)
    
    yield
    
    # Cleanup after test
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)