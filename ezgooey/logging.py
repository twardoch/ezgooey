#!/usr/bin/env python
"""
ezgooey.logging
---------------

Copyright (c) 2020 Adam Twardoch <adam+github@twardoch.com>
MIT license. Python 3.8+

Sets up a simple colorful logger,
compatible with Gooey's richtext control

## Simple usage

### Import and initialize in one place

```python
import ezgooey.logging as logging
logging.init()
```

### Use

```python
logging.info('info')
logging.warning('warning')
logging.error('error')
```

### In other places, just do:

```python
import logging
logging.info('info')
```

## Advanced usage

### Import and initialize in one place

```python
import ezgooey.logging as logging
logging.init(level=logging.INFO)
```

### In other places:

```python
import ezgooey.logging as logging
log = logging.logger('appname')
log.info('info')
log.warning('warning')
log.error('error')
log.success('success') # Only with adv
...
```
"""

__version__ = "1.2.0"

import sys
from logging import *

from colored import attr, fg, stylize

SUCCESS = 25

# Set up color logger


class Unbuffered:
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


def init(level: int = INFO, format: str = "%(levelname)s%(message)s") -> None:
    """Initialize colored logging compatible with Gooey's rich-text console.

    Sets up the root logger with color-coded level names and unbuffered stdout.
    Safe to call multiple times; subsequent calls update the log level even after
    the first call has already installed handlers (working around the standard
    ``basicConfig`` one-shot behaviour).

    Args:
        level: Root logging level (default ``logging.INFO``).
        format: Log format string (default suppresses the level prefix for INFO).
    """
    sys.stdout = Unbuffered(sys.stdout)

    basicConfig(
        level=level,
        format=format,
    )
    # basicConfig is a no-op when handlers already exist, so always force the
    # level on the root logger so repeated init() calls behave predictably.
    getLogger().setLevel(level)
    addLevelName(DEBUG, stylize("# [DEBUG] ", fg("grey_30")))
    addLevelName(INFO, "")
    addLevelName(WARNING, stylize("# [WARNING] ", fg("dark_orange")))
    addLevelName(ERROR, stylize("# [ERROR] ", fg("red")))
    addLevelName(CRITICAL, stylize("# [FAILURE] ", fg("light_red") + attr("bold")))
    addLevelName(SUCCESS, stylize("# [SUCCESS] ", fg("green") + attr("bold")))


def logger(name: str = "app") -> "Logger":
    """Return a named logger augmented with a ``success()`` method.

    The returned logger behaves like a standard :class:`logging.Logger` but
    gains a ``success(message)`` method that logs at the custom ``SUCCESS``
    level (25), displayed in green when :func:`init` has been called.

    Args:
        name: Logger name (default ``"app"``).

    Returns:
        A :class:`logging.Logger` instance with an extra ``success`` attribute.

    Example::

        import ezgooey.logging as logging
        logging.init()
        log = logging.logger("my_app")
        log.info("starting…")
        log.success("all done")
    """
    log = getLogger(name)
    setattr(log, "success", lambda message, *args: log._log(SUCCESS, message, args))
    return log
