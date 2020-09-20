#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ezgooey.ez
----------

Copyright (c) 2020 Adam Twardoch <adam+github@twardoch.com>
MIT license. Python 3.8+

[Gooey](https://github.com/chriskiehl/Gooey) is a Python
package that lets you turn argparse-based CLI apps into
cross-platform GUI apps.
[ezgooey](https://github.com/twardoch/ezgooey) makes this
even simpler.

When you start your app without CLI arguments, it'll run
in GUI, but if you supply CLI arguments, it'll run as CLI.

Import, then add the `@ezgooey` decorator to the function
where you initialize the `ArgumentParser`.

```python
from ezgooey.ez import *

@ezgooey
def get_parser():
    parser = ArgumentParser(
        prog='appname',
        description='app description'
    )
...
```
"""
__version__ = '1.2.0'

import argparse
import sys
import functools

try:
    import gooey
except ImportError:
    gooey = None

# Monkey-patching a private class…


def flex_add_argument(f):
    """Make add_argument accept or ignore gooey-specific options."""

    def f_decorated(*args, **kwargs):
        kwargs.pop('widget', None)
        kwargs.pop('gooey_options', None)
        return f(*args, **kwargs)

    return f_decorated


def flex_add_argument_group(f):
    """Make add_argument_group accept or ignore gooey-specific options."""

    def f_decorated(*args, **kwargs):
        kwargs.pop('widget', None)
        kwargs.pop('gooey_options', None)
        return f(*args, **kwargs)

    return f_decorated


argparse._ActionsContainer.add_argument = flex_add_argument(
    argparse.ArgumentParser.add_argument)

argparse._ActionsContainer.add_argument_group = flex_add_argument_group(
    argparse.ArgumentParser.add_argument_group)

if gooey is None or len(sys.argv) > 1:
    ArgumentParser = argparse.ArgumentParser

    def ezgooey(*args, **kwargs):
        if args:
            return args[0]
        def decorator_ezgooey(func):
            return func
        return decorator_ezgooey

    s = """
    def ezgooey(*args, **kwargs):
        def decorator_ezgooey(func):
            @functools.wraps(func)
            def wrapper_ezgooey(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper_ezgooey
        return decorator_ezgooey
"""

else:
    ArgumentParser = gooey.GooeyParser

    def ezgooey(*args, **kwargs):
        return gooey.Gooey(*args, **kwargs)
