#!/usr/bin/env python
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

__version__ = "1.2.0"

import argparse
import sys
from typing import Any, Callable, TypeVar

try:
    import gooey
except ImportError:
    gooey = None

F = TypeVar("F", bound=Callable[..., Any])

# Monkey-patch argparse to silently drop Gooey-specific kwargs
# (``widget`` and ``gooey_options``) so the same parser code works in both
# CLI mode (no Gooey) and GUI mode (Gooey present).


def flex_add_argument(f: Callable[..., Any]) -> Callable[..., Any]:
    """Return a wrapper around *f* that strips Gooey-specific keyword args.

    Allows ``parser.add_argument(..., widget='FileChooser', gooey_options={…})``
    to work without errors even when Gooey is not installed or not active.

    Args:
        f: The original ``add_argument`` method to wrap.

    Returns:
        A decorated callable that strips ``widget`` and ``gooey_options``
        before forwarding all other arguments to *f*.
    """

    def f_decorated(*args: Any, **kwargs: Any) -> Any:
        kwargs.pop("widget", None)
        kwargs.pop("gooey_options", None)
        return f(*args, **kwargs)

    return f_decorated


def flex_add_argument_group(f: Callable[..., Any]) -> Callable[..., Any]:
    """Return a wrapper around *f* that strips Gooey-specific keyword args.

    Mirrors :func:`flex_add_argument` for ``add_argument_group``.

    Args:
        f: The original ``add_argument_group`` method to wrap.

    Returns:
        A decorated callable that strips ``widget`` and ``gooey_options``.
    """

    def f_decorated(*args: Any, **kwargs: Any) -> Any:
        kwargs.pop("widget", None)
        kwargs.pop("gooey_options", None)
        return f(*args, **kwargs)

    return f_decorated


def flex_add_mutually_exclusive_group(f: Callable[..., Any]) -> Callable[..., Any]:
    """Return a wrapper around *f* that strips Gooey-specific keyword args.

    Mirrors :func:`flex_add_argument` for ``add_mutually_exclusive_group``.

    Args:
        f: The original ``add_mutually_exclusive_group`` method to wrap.

    Returns:
        A decorated callable that strips ``widget`` and ``gooey_options``.
    """

    def f_decorated(*args: Any, **kwargs: Any) -> Any:
        kwargs.pop("widget", None)
        kwargs.pop("gooey_options", None)
        return f(*args, **kwargs)

    return f_decorated


argparse._ActionsContainer.add_argument = flex_add_argument(  # type: ignore[method-assign]
    argparse.ArgumentParser.add_argument
)

argparse._ActionsContainer.add_argument_group = flex_add_argument_group(  # type: ignore[method-assign]
    argparse.ArgumentParser.add_argument_group
)

argparse._ActionsContainer.add_mutually_exclusive_group = (  # type: ignore[method-assign]
    flex_add_mutually_exclusive_group(
        argparse.ArgumentParser.add_mutually_exclusive_group
    )
)

if gooey is None or len(sys.argv) > 1:
    # CLI mode: use standard argparse; the @ezgooey decorator is a no-op.
    ArgumentParser = argparse.ArgumentParser  # type: ignore[misc,assignment]

    def ezgooey(*args: Any, **kwargs: Any) -> Any:  # type: ignore[misc]
        """No-op decorator used in CLI mode (Gooey unavailable or args given).

        When called as ``@ezgooey`` (no arguments) the decorated function is
        returned unchanged.  When called as ``@ezgooey(...)`` (with keyword
        arguments) a pass-through decorator is returned.

        Args:
            *args: Positional arguments — the first positional argument is
                treated as the decorated function when the decorator is used
                without parentheses.
            **kwargs: Keyword arguments (ignored in CLI mode).

        Returns:
            The decorated function, or a pass-through decorator.
        """
        if args:
            return args[0]

        def decorator_ezgooey(func: F) -> F:
            return func

        return decorator_ezgooey

else:
    # GUI mode: delegate to Gooey.
    ArgumentParser = gooey.GooeyParser  # type: ignore[misc,assignment]

    def ezgooey(*args: Any, **kwargs: Any) -> Any:  # type: ignore[misc]
        """Decorator that activates Gooey GUI mode.

        Forwards all arguments to :func:`gooey.Gooey`.  Use as
        ``@ezgooey`` or ``@ezgooey(program_name='…', …)``.

        Args:
            *args: Positional arguments forwarded to ``gooey.Gooey``.
            **kwargs: Keyword arguments forwarded to ``gooey.Gooey``.

        Returns:
            A Gooey-wrapped decorator.
        """
        return gooey.Gooey(*args, **kwargs)
