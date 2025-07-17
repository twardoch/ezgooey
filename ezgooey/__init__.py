#!/usr/bin/env python3
"""
ezgooey
-------
Copyright (c) 2020 Adam Twardoch <adam+github@twardoch.com>
MIT license. Python 3.8+

See `ezgooey.ez` and `ezgooey.logging` for details.
"""

import os
import sys

# Add parent directory to path to import version module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from version import get_version
    __version__ = get_version()
except ImportError:
    __version__ = "1.3.4"  # Fallback version

__all__ = ["ez", "logging"]
