#!/usr/bin/env python3

import os
import re

from setuptools import find_packages, setup

NAME = "ezgooey"

readme_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")
with open(readme_file) as f:
    readme = f.read()


def get_version(*args):
    # Try to import version from version.py first
    try:
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from version import get_version as get_git_version
        return get_git_version()
    except ImportError:
        pass
    
    # Fallback to reading from __init__.py
    try:
        verstrline = open(os.path.join(NAME, "__init__.py")).read()
        VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
        mo = re.search(VSRE, verstrline, re.M)
        if mo:
            return mo.group(1)
    except (IOError, OSError):
        pass
    
    return "0.0.0"


def get_requirements(*args):
    """Get requirements from pip requirement files."""
    requirements = set()
    with open(get_absolute_path(*args)) as handle:
        for line in handle:
            # Strip comments.
            line = re.sub(r"^#.*|\s#.*", "", line)
            # Ignore empty lines
            if line and not line.isspace():
                requirements.add(re.sub(r"\s+", "", line))
    return sorted(requirements)


def get_absolute_path(*args):
    """Transform relative pathnames into absolute pathnames."""
    directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(directory, *args)


setup(
    name=NAME,
    author="Adam Twardoch",
    author_email="adam+github@twardoch.com",
    url="https://twardoch.github.io/%s/" % (NAME),
    project_urls={"Source": "https://github.com/twardoch/%s/" % (NAME)},
    version=get_version(),
    license="MIT",
    description="Simplifies making GUI+CLI apps with Gooey",
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    install_requires=get_requirements("requirements.txt"),
    extras_require={"dev": ["twine>=3.2.0"]},
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="gooey gui cli",
)
