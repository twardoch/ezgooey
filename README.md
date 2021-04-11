# ezgooey

## ezgooey.ez

[Gooey](https://github.com/chriskiehl/Gooey) is a Python package, which lets you turn argparse-based CLI apps into cross-platform GUI apps. [ezgooey.ez](https://github.com/twardoch/ezgooey) makes this even simpler.

When you start your app without CLI arguments, it’ll run in GUI, but if you supply CLI arguments, it’ll run as CLI. Import, then add the `@ezgooey` decorator to the function where you initialize the `ArgumentParser`.

## Changelog

- 1.3.3: added support for add_mutually_exclusive_group
- 1.3.2: fixes
### Simple

```python
from ezgooey.ez import *

@ezgooey
def get_parser():
    parser = ArgumentParser(
        prog='appname',
        description='app description'
    )
    parser.add_argument(
        '-a',
        '--alternative',
        dest='alt',
        action='store_true',
        help='alternative processing',
        gooey_options={
            'show_label': False,
        }
    )
    return parser

parser = get_parser()
opts = parser.parse_args()
```

### Advanced

```Python
from ezgooey.ez import *

GUI_NAME = 'GUI App Name'
CLI_NAME = 'cliapp'

@ezgooey(
    advanced=True,
    auto_start=False,
    body_bg_color='#f0f0f0',
    clear_before_run=False,
    default_size=(800, 600),
    disable_progress_bar_animation=False,
    disable_stop_button=False,
    dump_build_config=False,
    error_color='#ea7878',
    footer_bg_color='#f0f0f0',
    force_stop_is_error=True,
    fullscreen=False,
    group_by_type=True,
    header_bg_color='#ffffff',
    header_height=80,
    header_height=90,
    header_image_center=False,
    header_show_subtitle=True,
    header_show_title=True,
    hide_progress_msg=False,
    image_dir='::gooey/default',
    language='english',
    language_dir=getResourcePath('languages'),
    load_build_config=None,
    navigation='Tabbed',
    optional_cols=1,
    poll_external_updates=False,
    program_description=None,
    program_name=GUI_NAME,
    progress_expr=None,
    progress_regex=None,
    required_cols=1,
    requires_shell=True,
    return_to_config=False,
    richtext_controls=True,
    show_failure_modal=True,
    show_restart_button=True,
    show_sidebar=False,
    show_stop_warning=True,
    show_success_modal=False,
    sidebar_bg_color='#f2f2f2',
    sidebar_title=None,
    suppress_gooey_flag=True,
    tabbed_groups=False,
    target=None,
    terminal_font_color='#000000',
    terminal_font_family=None,
    terminal_font_size=None,
    terminal_font_weight=None,
    terminal_panel_color='#F0F0F0',
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

    parser_g1 = parser.add_argument_group(
        'Group 1',
        gooey_options={
            'show_border': True,
            'columns'    : 2,
            'margin_top' : 0
            }
        )
    parser_g1.add_argument(
        nargs='+',
        dest='objects',
        type=str,
        metavar='objects',
        help='List of objects',
        widget='Textarea',
        gooey_options={
            'height': 120,
        }
    )

    parser_g2 = parser_q.add_mutually_exclusive_group(
        required=False
    )
    parser_g2.add_argument(
        '-a',
        '--add',
        dest='add',
        action='store_true',
        help='add objects',
        gooey_options={
            'show_help': False,
        }
    )
    parser_g2.add_argument(
        '-r',
        '--remove',
        dest='remove',
        action='store_true',
        help='remove objects',
        gooey_options={
            'show_help': False,
        }
    )
    parser_g1.add_argument(
        '-l',
        '--log',
        dest='log',
        action='store_true',
        help='print log',
        gooey_options={
            'show_label': False,
        }
    )

    parser_g3 = parser.add_argument_group(
        'Options',
        gooey_options={
        'show_border'   : True,
        'columns'       : 2,
        'margin_top'    : 0
    })
    parser_g3.add_argument(
        '-l',
        '--lang',
        nargs='*',
        dest='languages',
        type=str,
        metavar='language',
        help='list of languages',
        gooey_options={
            'show_label': False,
        }
    )
    parser_g3.add_argument(
        '-s',
        '--sort',
        dest='sort',
        type=str,
        choices=['asc', 'desc'],
        default='asc',
        help='sort results',
        gooey_options={
            'show_label': False,
        }
    )
    parser_g3.add_argument(
        '-o',
        '--output',
        dest='output',
        type=str,
        widget='FileSaver',
        metavar='output_file',
        help='save output to this file',
        gooey_options={
            'show_label': False,
        }
    )
    parser_g3.add_argument(
        '-i',
        '--input-dir',
        dest='input_dir',
        type=str,
        widget='DirChooser',
        metavar='input_folder',
        help='read files from this folder',
        gooey_options={
            'show_label': False,
        }
    )
    return parser

parser = get_parser()
opts = parser.parse_args()
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

Requires Python 3.9+

## License and Copyright

Copyright © 2021 Adam Twardoch. Licensed under the terms of the [MIT license](./LICENSE).
<!-- Place this tag in your head or just before your close body tag. -->
<script async defer src="https://buttons.github.io/buttons.js"></script>


