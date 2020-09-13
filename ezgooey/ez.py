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
__version__ = '1.1.0'

import argparse
import sys

try:
    import gooey
except ImportError:
    gooey = None


# Monkey-patching a private class…
def flex_add_argument(f):
    """Make the add_argument accept (and ignore) the widget option."""

    def f_decorated(*args, **kwargs):
        kwargs.pop('widget', None)
        return f(*args, **kwargs)

    return f_decorated


argparse._ActionsContainer.add_argument = flex_add_argument(
    argparse.ArgumentParser.add_argument)

# Do not run GUI if it is not available or if command-line arguments are given.
if gooey is None or len(sys.argv) > 1:
    ArgumentParser = argparse.ArgumentParser

    def ezgooey(f):
        return f
else:
    ArgumentParser = gooey.GooeyParser
    gui_decorator = gooey.Gooey(
        program_name='Application',
        suppress_gooey_flag=True,
        richtext_controls=True,
        advanced=True,
        tabbed_groups=True,
        navigation='Tabbed',
        optional_cols=1
    )
