#!/usr/bin/env python3
# this_file: ezgooey/__init__.py
"""
ezgooey
-------
Copyright (c) 2020 Adam Twardoch <adam+github@twardoch.com>
MIT license. Python 3.8+

See `ezgooey.ez` and `ezgooey.logging` for details.
"""

# Version resolution order:
#   1. hatch-vcs generated _version.py (present after `hatch build` or `pip install`)
#   2. root-level version.py git-tag helper
#   3. VERSION.txt
#   4. Hard-coded fallback
try:
    from ezgooey._version import __version__
except ImportError:
    try:
        import os
        import sys

        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from version import get_version  # type: ignore[import]

        __version__ = get_version()
    except Exception:
        __version__ = "2.7.5"

__all__ = ["ez", "logging", "__version__"]
