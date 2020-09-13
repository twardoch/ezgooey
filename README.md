# ezgooey

## ezgooey.ez

[Gooey](https://github.com/chriskiehl/Gooey) is a Python package, which lets you turn argparse-based CLI apps into cross-platform GUI apps. [ezgooey.ez](https://github.com/twardoch/ezgooey) makes this even simpler. 

When you start your app without CLI arguments, it'll run in GUI, but if you supply CLI arguments, it'll run as CLI.

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

## ezgooey.logging

This package also includes a simple colorful logger that is compatible with Gooey's richtext control.

### Simple usage

Import and initialize in one place

```python
import ezgooey.logging as logging
logging.init(level=logging.INFO)
```

Use

```python
logging.info('info')
logging.warning('warning')
logging.error('error')
logging.success('success')
```

In other places, just do:

```python
import logging
logging.info('info')
```

### Advanced usage

Import and initialize in one place

```python
import ezgooey.logging as logging
logging.init(level=logging.INFO)
```

In other places:

```python
import ezgooey.logging as logging
log = logging.logger('appname')
log.info('info')
log.warning('warning')
log.error('error')
log.success('success')
...
```

## Example

My [PyPolona](https://twardoch.github.io/pypolona/) project is an app, made with the help of ezgooey and packaged for macOS and Windows with PyInstaller. Check the [sources](https://github.com/twardoch/pypolona) for details.

## Requirements

Requires Python 3.8+

## License and Copyright

Copyright © 2020 Adam Twardoch. Licensed under the terms of the [MIT license](./LICENSE). 
<!-- Place this tag in your head or just before your close body tag. -->
<script async defer src="https://buttons.github.io/buttons.js"></script>


