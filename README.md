# ezgooey: Create GUIs for CLI Apps Effortlessly

`ezgooey` is a Python utility that adds a GUI to `argparse`-based CLI applications. It uses [Gooey](https://github.com/chriskiehl/Gooey) under the hood, switching between GUI and CLI modes automatically based on whether command-line arguments are provided.

It also includes a logging module with colored output that works in both terminal and GUI environments.

## Who is `ezgooey` for?

Python developers who:
*   Already use `argparse` for CLI apps
*   Want a GUI option without rewriting argument parsing
*   Need to support both GUI and CLI users from one script
*   Want better-looking logs in both environments

## Key Features

*   **One decorator:** Add `@ezgooey` to your parser function
*   **Automatic mode switching:** GUI when no args given, CLI otherwise
*   **Drop-in replacement:** Works with existing `argparse` code
*   **Colored logging:** Enhanced output for both terminal and Gooey
*   **Full Gooey support:** All Gooey decorator options work unchanged

## Installation

```bash
pip install ezgooey
```

Installs `Gooey`, `wxPython`, and `colored` as dependencies.

## Usage

### 1. `ezgooey.ez`: Adding GUI to your CLI

Add the `@ezgooey` decorator to your `ArgumentParser` function:

```python
from argparse import ArgumentParser
from ezgooey.ez import ezgooey

@ezgooey
def create_my_parser():
    parser = ArgumentParser(
        prog='my_app',
        description='This is a demonstration app.'
    )
    parser.add_argument(
        'filename',
        help='Path to the input file',
        widget='FileChooser'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    return parser

if __name__ == '__main__':
    parser = create_my_parser()
    args = parser.parse_args()

    if args.verbose:
        print("Verbose mode enabled.")
    print(f"Processing file: {args.filename}")
```

**Behavior:**
*   `python script.py` → Opens GUI
*   `python script.py file.txt -v` → Runs as CLI
*   The decorator handles all conditional logic

**Advanced example with Gooey options:**

```python
from argparse import ArgumentParser
from ezgooey.ez import ezgooey

GUI_NAME = 'My Advanced GUI App'
CLI_NAME = 'mycli'

@ezgooey(
    program_name=GUI_NAME,
    default_size=(800, 600),
    navigation='Tabbed',
    menu=[{
        'name' : 'Help',
        'items': [{
            'type': 'AboutDialog',
            'menuTitle': 'About',
            'name': GUI_NAME,
            'description': 'An example application using ezgooey.',
            'website': 'https://github.com/twardoch/ezgooey',
            'license': 'MIT'
        }]
    }]
)
def get_advanced_parser():
    parser = ArgumentParser(
        prog=CLI_NAME,
        description='An advanced application with multiple options.'
    )

    group1 = parser.add_argument_group(
        'Input/Output',
        gooey_options={'columns': 1, 'show_border': True}
    )
    group1.add_argument(
        '--input-file',
        widget='FileChooser',
        help='File to process',
        gooey_options={'wildcard': "Text files (*.txt)|*.txt"}
    )
    group1.add_argument(
        '--output-dir',
        widget='DirChooser',
        help='Directory to save results'
    )

    group2 = parser.add_argument_group(
        'Settings',
        gooey_options={'columns': 2}
    )
    group2.add_argument(
        '--iterations',
        type=int,
        default=10,
        help='Number of iterations to run'
    )
    group2.add_argument(
        '--mode',
        choices=['fast', 'slow', 'balanced'],
        default='balanced',
        help='Processing mode'
    )
    return parser

if __name__ == '__main__':
    parser = get_advanced_parser()
    args = parser.parse_args()
    print(f"Input: {getattr(args, 'input_file', 'N/A')}, Output Dir: {getattr(args, 'output_dir', 'N/A')}")
    print(f"Iterations: {args.iterations}, Mode: {args.mode}")
```

See [Gooey documentation](https://github.com/chriskiehl/Gooey) for all decorator options.

### 2. `ezgooey.logging`: Colored, GUI-friendly logs

```python
# Initialize once at app start
import ezgooey.logging as logging
logging.init(level=logging.INFO)

# Use anywhere in your code
import logging
logging.info('This is an info message.')
logging.warning('This is a warning.')
logging.error('This is an error!')
logging.success('Operation completed successfully!')  # Custom level
```

**Named loggers for larger applications:**

```python
# At app start
import ezgooey.logging as ez_logging
ez_logging.init(level=ez_logging.INFO)

# In other modules
import ezgooey.logging as ez_logging
log = ez_logging.logger('my_module_name')

log.info('Info message from my_module.')
log.warning('Warning from my_module.')
log.success('Task in my_module succeeded.')
```

**Log levels:**
Standard levels plus `SUCCESS` for positive feedback. Output is color-coded by severity.

## How It Works

### `ezgooey.ez`

1.  **Conditional import:** Imports `gooey` only when needed
2.  **Mode detection:** Uses GUI mode when Gooey is available and no CLI args given
3.  **Monkey-patching:** Extends `argparse` methods to accept Gooey-specific options (`widget`, `gooey_options`) without breaking CLI mode

Example: `parser.add_argument(..., widget='FileChooser')` works in both modes.

### `ezgooey.logging`

Configures Python's standard logging with:
*   Colored output using the `colored` library
*   Rich text formatting compatible with Gooey's console
*   Unbuffered output for immediate GUI feedback
*   Custom `SUCCESS` level with green text
*   `init()` function for one-time setup
*   `logger()` function that adds `success()` method to loggers

## Project Structure

```
ezgooey/
├── ezgooey/
│   ├── __init__.py   # Package initialisation, version
│   ├── ez.py         # Core decorator logic, monkey-patching
│   └── logging.py    # Colored logging setup
├── tests/
│   ├── test_ez.py
│   ├── test_integration.py
│   ├── test_logging.py
│   └── test_version.py
├── docs/
│   └── index.md      # Jekyll documentation site
├── pyproject.toml    # Build (hatchling + hatch-vcs), ruff, mypy, pytest config
├── README.md         # This file
├── CHANGELOG.md      # Version history
└── LICENSE           # MIT license
```

## Dependencies

*   [Gooey](https://github.com/chriskiehl/Gooey) - GUI generation
*   [wxPython](https://wxpython.org/) - GUI toolkit (required by Gooey)
*   [colored](https://pypi.org/project/colored/) - Terminal colors

Installed automatically with pip.

## Contributing

Issues and pull requests welcome at [GitHub repository](https://github.com/twardoch/ezgooey).

### Development Setup

```bash
pip install hatch
hatch env create
hatch run pytest          # run test suite (29 tests)
hatch run ruff check .    # lint
hatch run mypy ezgooey/   # type-check
```

### Building

```bash
hatch build               # produces sdist + wheel in dist/
```

## Version History

See [CHANGELOG.md](CHANGELOG.md) and [GitHub Releases](https://github.com/twardoch/ezgooey/releases).

## License

MIT License. Copyright © 2020-2023 Adam Twardoch.