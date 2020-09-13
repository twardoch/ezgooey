# ezgooey

## ezgooey.ez

[Gooey](https://github.com/chriskiehl/Gooey) is a Python package, which lets you turn argparse-based CLI apps into cross-platform GUI apps. [ezgooey.ez](https://github.com/twardoch/ezgooey) makes this even simpler.

When you start your app without CLI arguments, it’ll run in GUI, but if you supply CLI arguments, it’ll run as CLI. Import, then add the `@ezgooey` decorator to the function where you initialize the `ArgumentParser`.

### Simple

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

### Advanced

```Python
from ezgooey.ez import *

GUI_NAME = 'GUI App Name'
CLI_NAME = 'cliapp'

@ezgooey(
    advanced=True,
    auto_start=False,
    default_size=(800, 600),
    disable_progress_bar_animation=False,
    disable_stop_button=False,
    dump_build_config=False,
    group_by_type=True,
    header_height=80,
    hide_progress_msg=False,
    image_dir='::gooey/default',
    language='english',
    language_dir=getResourcePath('languages'),
    load_build_config=None,
    monospace_display=False,
    navigation='Tabbed',
    optional_cols=1,
    program_description=None,
    program_name=GUI_NAME,
    progress_expr=None,
    progress_regex=None,
    required_cols=1,
    richtext_controls=True,
    suppress_gooey_flag=True,
    tabbed_groups=False,
    target=None,
    use_legacy_titles=True,
    menu=[{
        'name' : 'Help',
        'items': [{
            'type'       : 'AboutDialog',
            'menuTitle'  : 'About',
            'name'       : GUI_NAME,
            'description': 'Click the link for more info',
            'website'    : 'https://your.link/',
            'license'    : 'MIT'
        }, {
            'type'     : 'Link',
            'menuTitle': '%s Help' % (GUI_NAME),
            'url'      : 'https://your.link/docs/'
        }]
    }]
    )
def get_parser():
    parser = ArgumentParser(
        prog=CLI_NAME,
        description='app description'
    )
...
```

The `@ezgooey` decorator uses the same arguments as the original `@Gooey` decorator. `See [Gooey documentation](https://github.com/chriskiehl/Gooey) for a detailed description.

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


