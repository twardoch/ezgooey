---
layout: default
title: ezgooey — Easy GUI for CLI Apps
description: Add a Gooey GUI to any argparse-based Python CLI with one decorator
---

# ezgooey

**One decorator. Two modes. Zero rewrites.**

`ezgooey` wraps [Gooey](https://github.com/chriskiehl/Gooey) — the library that turns argparse CLIs into cross-platform desktop GUIs — and adds automatic mode-switching so your script always does the right thing:

| How it is launched | What happens |
|---|---|
| `python script.py` (no args) | Opens Gooey GUI window |
| `python script.py --flag value` | Runs as a normal CLI |

You write one parser. `ezgooey` decides which mode to use at runtime.

## Installation

```bash
pip install ezgooey
```

Requirements: Python 3.8+, Gooey ≥ 1.0.8, wxPython ≥ 4.1.1, colored ≥ 1.4.2.

## Quick Start

### `ezgooey.ez` — the GUI/CLI decorator

```python
from ezgooey.ez import ArgumentParser, ezgooey

@ezgooey(program_name="My App")
def get_parser():
    parser = ArgumentParser(description="Resize an image")
    parser.add_argument("input",  help="Input file",  widget="FileChooser")
    parser.add_argument("output", help="Output file", widget="FileSaver")
    parser.add_argument("--width", type=int, default=800,
                        help="Target width in pixels")
    return parser

if __name__ == "__main__":
    args = get_parser().parse_args()
    print(f"Resizing {args.input} → {args.output} at {args.width}px")
```

`widget="FileChooser"` is silently ignored in CLI mode, so the identical code
runs correctly in both environments.

### `ezgooey.logging` — colored, GUI-friendly logs

```python
import ezgooey.logging as logging

logging.init()                          # call once at app start
log = logging.logger("my_app")

log.debug("verbose details")            # grey
log.info("normal progress")             # plain
log.warning("something looks off")      # orange
log.error("something broke")            # red
log.critical("unrecoverable failure")   # bold red
log.success("all done!")                # green   ← custom level 25
```

`init()` wraps stdout in an unbuffered stream so GUI output appears
immediately in Gooey's rich-text console.  The same code works unchanged
in a terminal.

## How It Works

### Mode detection (`ezgooey.ez`)

```
import gooey available?  AND  len(sys.argv) == 1?
         │ yes                        │ no
         ▼                            ▼
  ArgumentParser = GooeyParser    ArgumentParser = argparse.ArgumentParser
  @ezgooey → gooey.Gooey(…)      @ezgooey → no-op pass-through
```

### Monkey-patching argparse

`ezgooey` patches three `argparse._ActionsContainer` methods to silently
drop `widget=` and `gooey_options=` keyword arguments:

- `add_argument`
- `add_argument_group`
- `add_mutually_exclusive_group`

This means Gooey-specific options in your parser code never raise
`TypeError` when the app runs in CLI mode.

### Custom log level

`SUCCESS = 25` sits between `INFO` (20) and `WARNING` (30).  The `logger()`
factory attaches a `success()` convenience method that logs at this level.

## API Reference

### `ezgooey.ez`

| Symbol | Description |
|---|---|
| `ezgooey(*args, **kwargs)` | Decorator/decorator-factory. In GUI mode delegates to `gooey.Gooey`. In CLI mode is a no-op. |
| `ArgumentParser` | Alias for `gooey.GooeyParser` (GUI) or `argparse.ArgumentParser` (CLI). Import this instead of `argparse.ArgumentParser` for IDE-friendly code. |

### `ezgooey.logging`

| Symbol | Description |
|---|---|
| `init(level=INFO, format=…)` | Configure root logger. Safe to call multiple times; always updates the log level. |
| `logger(name="app")` | Return a named logger with an extra `success()` method. |
| `SUCCESS` | Integer constant `25` — the custom success log level. |
| All `logging.*` names | Re-exported from the standard `logging` module. |

## Advanced Example

```python
from ezgooey.ez import ArgumentParser, ezgooey
import ezgooey.logging as logging

logging.init(level=logging.DEBUG)
log = logging.logger("converter")

@ezgooey(
    program_name="File Converter",
    default_size=(720, 480),
    navigation="Tabbed",
)
def get_parser():
    parser = ArgumentParser(prog="convert", description="Convert files")

    src = parser.add_argument_group(
        "Source", gooey_options={"columns": 1, "show_border": True}
    )
    src.add_argument("--input",  widget="FileChooser", help="Input file")
    src.add_argument("--format", choices=["pdf", "png", "svg"],
                     default="pdf", help="Output format")

    dst = parser.add_argument_group("Destination")
    dst.add_argument("--output", widget="DirChooser", help="Output directory")
    return parser

if __name__ == "__main__":
    args = get_parser().parse_args()
    log.info(f"Converting {args.input} → {args.format} in {args.output}")
    # … conversion logic …
    log.success("Conversion complete.")
```

## Project Links

- [GitHub repository](https://github.com/twardoch/ezgooey)
- [PyPI package](https://pypi.org/project/ezgooey/)
- [Gooey documentation](https://github.com/chriskiehl/Gooey)
- [Issue tracker](https://github.com/twardoch/ezgooey/issues)

## License

MIT — Copyright © 2020–2026 Adam Twardoch.
