# ezgooey: Create GUIs for CLI Apps Effortlessly

`ezgooey` is a Python utility that simplifies the process of adding a Graphical User Interface (GUI) to your command-line interface (CLI) applications built with `argparse`. It acts as a lightweight wrapper around the powerful [Gooey](https://github.com/chriskiehl/Gooey) library, allowing your application to run as a GUI when no command-line arguments are provided, and as a standard CLI tool when arguments are present.

Additionally, `ezgooey` includes a convenient logging module that provides colorful, rich-text-compatible output, enhancing the user experience in both GUI and console modes.

## Who is `ezgooey` for?

`ezgooey` is for Python developers who:

*   Have existing CLI applications built with `argparse`.
*   Want to provide a user-friendly GUI alternative without rewriting their argument parsing logic.
*   Need a quick and easy way to make their tools accessible to users who prefer graphical interfaces.
*   Appreciate a seamless experience where the same script can serve both CLI and GUI users.
*   Desire enhanced logging output that looks good in both terminals and Gooey's rich text display.

## Why is `ezgooey` useful?

*   **Simplicity:** Turns an `argparse`-based CLI into a GUI application with a single decorator.
*   **Flexibility:** Your application automatically switches between GUI and CLI mode based on the presence of command-line arguments. No need for separate scripts or complex logic.
*   **Enhanced User Experience:** Provides a GUI for users who are not comfortable with the command line, while retaining full CLI functionality for advanced users.
*   **Rich Logging:** Includes a logging utility that offers colored output in terminals and is compatible with Gooey's rich text display, making logs more readable.
*   **Minimal Code Changes:** Integrates with your existing `argparse` setup with minimal modifications.
*   **Leverages Gooey:** Builds upon the robust and feature-rich Gooey library, inheriting its capabilities for UI generation.

## Installation

You can install `ezgooey` using pip:

```bash
pip install ezgooey
```

This will also install its dependencies, including `Gooey`, `wxPython`, and `colored`.

## How to Use

`ezgooey` consists of two main components: `ezgooey.ez` for GUI generation and `ezgooey.logging` for enhanced logging.

### 1. `ezgooey.ez`: Adding a GUI to your CLI

To add a GUI to your `argparse`-based application, simply import `ezgooey` and add the `@ezgooey` decorator to the function where you define your `ArgumentParser`.

**Simple Example:**

```python
from argparse import ArgumentParser
from ezgooey.ez import ezgooey # Import the decorator

@ezgooey # Add the decorator here
def create_my_parser():
    parser = ArgumentParser(
        prog='my_app',
        description='This is a demonstration app.'
    )
    parser.add_argument(
        'filename',
        help='Path to the input file',
        widget='FileChooser' # Gooey-specific widget
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
    # Your application logic here
```

**Explanation:**

*   If you run `python your_script.py` (without arguments), Gooey will render a GUI based on your `ArgumentParser` definition.
*   If you run `python your_script.py input.txt -v`, it will run as a standard CLI application.
*   The `@ezgooey` decorator handles the conditional logic. It accepts all the same arguments as the original `@Gooey` decorator from the Gooey library (e.g., for customizing appearance, layout, etc.).

**Advanced Example with Gooey Options:**

The `@ezgooey` decorator can pass various configuration options directly to Gooey.

```python
from argparse import ArgumentParser
from ezgooey.ez import ezgooey

GUI_NAME = 'My Advanced GUI App'
CLI_NAME = 'mycli'

@ezgooey(
    program_name=GUI_NAME,
    default_size=(800, 600),
    navigation='Tabbed', # Example: Use Tabbed navigation
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
    # Your application logic here
    print(f"Input: {getattr(args, 'input_file', 'N/A')}, Output Dir: {getattr(args, 'output_dir', 'N/A')}")
    print(f"Iterations: {args.iterations}, Mode: {args.mode}")

```
Refer to the [Gooey documentation](https://github.com/chriskiehl/Gooey) for a detailed list of all available decorator arguments and `gooey_options` for widgets.

### 2. `ezgooey.logging`: Colorful and GUI-Friendly Logging

`ezgooey.logging` provides a simple way to set up colorful logging that works well in both standard terminals and Gooey's rich text console display.

**Simple Usage:**

Initialize the logger once, typically at the start of your application.

```python
# In your main script (e.g., at the beginning)
import ezgooey.logging as logging
logging.init(level=logging.INFO) # Or logging.DEBUG, etc.

# Later in your code (in the same file or others)
import logging # Use the standard logging module
logging.info('This is an info message.')
logging.warning('This is a warning.')
logging.error('This is an error!')
logging.success('Operation completed successfully!') # Custom level
```

**Advanced Usage (Named Loggers):**

For more complex applications or libraries, you can use named loggers.

```python
# In your main script (e.g., at the beginning)
import ezgooey.logging as ez_logging # Alias to avoid conflict
ez_logging.init(level=ez_logging.INFO)

# In other modules or parts of your app:
import ezgooey.logging as ez_logging
log = ez_logging.logger('my_module_name') # Get a named logger

log.info('Info message from my_module.')
log.warning('Warning from my_module.')
log.success('Task in my_module succeeded.')
```

**Log Levels:**

Besides standard levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`), `ezgooey.logging` adds:
*   `SUCCESS`: For positive feedback (e.g., operation completed).

The output is color-coded for severity.

## Technical Details

### How `ezgooey.ez` Works

The `ezgooey.ez` module is designed to be a drop-in enhancement for `argparse`.

1.  **Conditional Import:** It attempts to import `gooey`. If `gooey` is not installed or if command-line arguments (`sys.argv[1:]`) are present, `ezgooey` ensures that the application behaves like a standard CLI tool.
2.  **Decorator Logic:**
    *   If Gooey mode is active (Gooey is available and no CLI args), the `@ezgooey` decorator uses `gooey.Gooey` to transform the `ArgumentParser` function into a GUI. The `ArgumentParser` used in this case is `gooey.GooeyParser`.
    *   If CLI mode is active, the `@ezgooey` decorator essentially becomes a pass-through, and the standard `argparse.ArgumentParser` is used.
3.  **Monkey-Patching `argparse`:** To allow you to use Gooey-specific options (like `widget` or `gooey_options`) directly within your `ArgumentParser`'s `add_argument`, `add_argument_group`, and `add_mutually_exclusive_group` calls without breaking CLI mode, `ezgooey.ez` performs a bit of "monkey-patching." It wraps these methods of `argparse._ActionsContainer`. The wrapped versions will simply ignore Gooey-specific keyword arguments if Gooey is not active. This means you can define your parser once with all the Gooey enhancements, and it will work seamlessly in both GUI and CLI environments.

    For example, `parser.add_argument(..., widget='FileChooser', gooey_options={...})` will use these options in GUI mode but ignore `widget` and `gooey_options` in CLI mode.

### How `ezgooey.logging` Works

The `ezgooey.logging` module configures the standard Python `logging` system with a custom formatter and stream handler to provide:

*   **Colored Output:** Uses the `colored` library to add distinct colors to log messages based on their severity (e.g., red for errors, green for success).
*   **Gooey Compatibility:** The formatting is designed to render correctly in Gooey's built-in console, which supports rich text.
*   **Unbuffered Output:** Sets `sys.stdout` to be unbuffered to ensure messages appear immediately, which is important for GUI feedback.
*   **`init()` function:** A convenience function to apply the basic configuration (`basicConfig`), set up custom level names and their styles (colors).
*   **`logger()` function:** Returns a standard Python logger instance (via `logging.getLogger(name)`) but also adds a `success` method to it for the custom `SUCCESS` level.

### Project Structure

*   `ezgooey/`: Main package directory.
    *   `__init__.py`: Initializes the package, defines `__version__`.
    *   `ez.py`: Contains the core `@ezgooey` decorator logic and `argparse` monkey-patching.
    *   `logging.py`: Provides the colorful logging setup.
*   `setup.py`: Standard script for packaging and distribution.
*   `requirements.txt`: Lists runtime dependencies.
*   `README.md`: This file.
*   `LICENSE`: Contains the MIT license text.
*   `dist.sh`: Utility script for creating distributions and publishing releases.

### Dependencies

`ezgooey` relies on the following main libraries:

*   [Gooey](https://github.com/chriskiehl/Gooey): For the core GUI generation.
*   [wxPython](https://wxpython.org/): The GUI toolkit Gooey uses (required by Gooey).
*   [colored](https://pypi.org/project/colored/): For adding colors to terminal log output.

These are automatically installed when you install `ezgooey` via pip.

## Contributing

Contributions are welcome! If you have suggestions, bug reports, or feature requests, please open an issue on the [GitHub repository](https://github.com/twardoch/ezgooey).

### Coding Conventions

*   Please follow PEP 8 style guidelines for Python code.
*   Ensure your code is well-commented, especially for complex logic.

### Development Setup (Simplified)

1.  Clone the repository.
2.  It's recommended to work in a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies, including development tools:
    ```bash
    pip install -r requirements.txt
    pip install twine wheel # For distribution
    ```

### Building and Distributing

The `dist.sh` script in the repository is used by the maintainer to create new releases and publish them to PyPI and GitHub. It handles versioning, building wheels/sdist, tagging, and uploading.

For local testing of packaging:
```bash
python setup.py sdist bdist_wheel
```
This will create distribution files in the `dist/` directory.

(Note: The project currently does not have an automated test suite. Contributions in this area would be particularly valuable.)

### Version History

For a detailed history of changes, please refer to the [GitHub Releases page](https://github.com/twardoch/ezgooey/releases).

## License

`ezgooey` is licensed under the terms of the [MIT License](./LICENSE).
Copyright © 2020-2023 Adam Twardoch.

---

*This README was enhanced with the assistance of an AI coding tool.*
