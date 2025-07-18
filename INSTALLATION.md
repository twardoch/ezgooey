# Installation Guide for ezgooey

## Quick Installation

### Option 1: Using pip (Recommended)

```bash
pip install ezgooey
```

### Option 2: Using Installation Script

#### Unix/Linux/macOS
```bash
curl -sSL https://github.com/twardoch/ezgooey/raw/master/scripts/install.sh | bash
```

#### Windows PowerShell
```powershell
iwr https://github.com/twardoch/ezgooey/raw/master/scripts/install.ps1 | iex
```

### Option 3: From Source

```bash
git clone https://github.com/twardoch/ezgooey.git
cd ezgooey
pip install -e .
```

## Requirements

- **Python**: 3.8 or later
- **Operating System**: Windows, macOS, or Linux
- **Dependencies**: Automatically installed with package
  - wxPython (≥4.1.1)
  - Gooey (≥1.0.8)
  - colored (≥1.4.2)

## Installation Methods Comparison

| Method | Use Case | Advantages | Disadvantages |
|--------|----------|------------|---------------|
| pip | General use | Simple, standard | Requires Python/pip knowledge |
| Script | First-time users | Automatic setup, verification | Requires internet connection |
| Source | Development | Latest features, editable | Requires git, more complex |

## Verification

After installation, verify it works:

```python
import ezgooey
print(f"ezgooey version: {ezgooey.__version__}")

# Test basic functionality
from ezgooey.ez import ezgooey, ArgumentParser
import ezgooey.logging as logging

print("✅ ezgooey is ready to use!")
```

## Development Installation

For contributors and developers:

```bash
# Clone repository
git clone https://github.com/twardoch/ezgooey.git
cd ezgooey

# Set up development environment
make dev-setup

# Or manually:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .
```

## Platform-Specific Notes

### Windows
- **Python Installation**: Download from python.org or use Microsoft Store
- **PowerShell**: Use PowerShell (not Command Prompt) for best experience
- **wxPython**: May require Visual C++ redistributables

### macOS
- **Python Installation**: Use Homebrew (`brew install python`) or python.org
- **Xcode**: May need Xcode command-line tools for wxPython

### Linux
- **Python Installation**: Use package manager (`apt install python3-pip`)
- **System Dependencies**: May need development packages for wxPython:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install libgtk-3-dev libwebkitgtk-3.0-dev

  # CentOS/RHEL
  sudo yum install gtk3-devel webkit2gtk3-devel

  # Fedora
  sudo dnf install gtk3-devel webkit2gtk4.0-devel
  ```

## Troubleshooting

### Common Issues

1. **wxPython Installation Fails**
   - **Solution**: Install system dependencies (see Linux section)
   - **Alternative**: Use conda: `conda install wxpython`

2. **Permission Errors**
   - **Solution**: Use `pip install --user ezgooey`
   - **Alternative**: Use virtual environment

3. **Python Version Issues**
   - **Solution**: Ensure Python 3.8+ is installed
   - **Check**: `python --version` or `python3 --version`

4. **Import Errors**
   - **Solution**: Verify installation: `pip list | grep ezgooey`
   - **Fix**: Reinstall: `pip uninstall ezgooey && pip install ezgooey`

### Getting Help

- **Documentation**: [GitHub Repository](https://github.com/twardoch/ezgooey)
- **Issues**: [GitHub Issues](https://github.com/twardoch/ezgooey/issues)
- **Discussions**: [GitHub Discussions](https://github.com/twardoch/ezgooey/discussions)

## Uninstallation

```bash
pip uninstall ezgooey
```

## Alternative Installation Methods

### Using pipx (Isolated Installation)
```bash
pipx install ezgooey
```

### Using conda
```bash
# Note: May not always have latest version
conda install -c conda-forge ezgooey
```

### Using poetry
```bash
poetry add ezgooey
```

## Security Notes

- Installation scripts are provided for convenience but should be reviewed before execution
- Always verify package integrity when downloading from third-party sources
- Use virtual environments to isolate dependencies

## Next Steps

After installation, check out:
- [README.md](README.md) - Basic usage and examples
- [DEVELOPMENT.md](DEVELOPMENT.md) - Development guide
- [Examples](examples/) - Sample applications (if available)

## Version Information

This installation guide is for ezgooey with git-tag-based versioning. The version is automatically determined from git tags and follows semantic versioning (semver.org).