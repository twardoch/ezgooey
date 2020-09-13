#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from colored import stylize, attr, fg

SUCCESS = 25

# Set up color logger

class Unbuffered(object):
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

def init(level=INFO, format='%(levelname)s%(message)s'):
    sys.stdout = Unbuffered(sys.stdout)

    basicConfig(level=level, format=format, )
    addLevelName(DEBUG, stylize("# [DEBUG] ", fg("grey_30")))
    addLevelName(INFO, '')
    addLevelName(WARNING, stylize(
        "# [WARNING] ", fg("dark_orange")))
    addLevelName(ERROR, stylize("# [ERROR] ", fg("red")))
    addLevelName(CRITICAL, stylize(
        "# [FAILURE] ", fg("light_red") + attr("bold")))
    addLevelName(SUCCESS, stylize(
        "# [SUCCESS] ", fg("green") + attr("bold")))

def logger(name='app'):
    log = getLogger(name)
    setattr(log, 'success', lambda message, *
    args: log._log(SUCCESS, message, args))
    return log
