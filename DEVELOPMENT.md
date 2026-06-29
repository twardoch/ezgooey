# ezgooey Development Guide

This document covers the development setup, testing, and release process for ezgooey.

## Project Structure

```
ezgooey/
├── ezgooey/                 # Main package
│   ├── __init__.py          # Package initialization with version info
│   ├── ez.py               # Main decorator and argparse integration
│   └── logging.py          # Color logging utilities
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── conftest.py         # Pytest configuration
│   ├── test_version.py     # Version management tests
│   ├── test_ez.py          # Core functionality tests
│   ├── test_logging.py     # Logging tests
│   └── test_integration.py # Integration tests
├── scripts/                # Build and deployment scripts
│   ├── test.sh             # Run test suite
│   ├── build.sh            # Build package
│   ├── release.sh          # Create releases
│   ├── install.sh          # Unix installation
│   └── install.ps1         # Windows installation
├── .github/workflows/      # GitHub Actions CI/CD
│   ├── ci.yml              # Main CI pipeline
│   ├── dev.yml             # Development branch testing
│   └── release.yml         # Release automation
├── version.py              # Git-tag-based version management
├── pyproject.toml          # Python project configuration
├── setup.py                # Legacy setup for compatibility
├── Makefile                # Development commands
└── requirements*.txt       # Dependencies
```

## Git-Tag-Based Versioning

Versioning uses git tags following semantic versioning:

- **Primary source**: Git tags (`v1.2.3`)
- **Fallbacks**: VERSION.txt and __init__.py
- **Automatic detection**: Version determined during build

### Version Commands

```bash
# Get current version
python3 version.py get

# Bump version
python3 version.py bump patch   # 1.2.3 -> 1.2.4
python3 version.py bump minor   # 1.2.3 -> 1.3.0
python3 version.py bump major   # 1.2.3 -> 2.0.0
```

## Development Setup

### Requirements

- Python 3.8+
- Git
- Make (optional)

### Setup

```bash
# Clone repository
git clone https://github.com/twardoch/ezgooey.git
cd ezgooey

# Quick setup
make dev-setup

# Manual setup
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Development Commands

```bash
make test        # Run tests
make build       # Build package
make lint        # Run flake8
make type-check  # Run mypy
make check       # Run all checks
make clean       # Clean artifacts
make version     # Show version
```

## Testing

### Test Organization

- **Unit tests**: Individual components
- **Integration tests**: Component interactions
- **Cross-platform**: Linux, macOS, Windows
- **Multi-version**: Python 3.8-3.12

### Running Tests

```bash
# All tests
python -m pytest tests/ -v

# Specific file
python -m pytest tests/test_version.py -v

# With coverage
python -m pytest tests/ --cov=ezgooey --cov-report=html

# Fast tests only
python -m pytest tests/ -m "not slow"
```

### Configuration Files

- **pytest.ini**: Pytest settings
- **conftest.py**: Shared fixtures
- **pyproject.toml**: Coverage configuration

## Release Process

### Automated Releases

```bash
make release-patch  # 1.2.3 -> 1.2.4
make release-minor  # 1.2.3 -> 1.3.0
make release-major  # 1.2.3 -> 2.0.0
```

### Manual Releases

```bash
./scripts/release.sh patch "Fix argument parsing bug"
./scripts/release.sh minor "Add new feature"
./scripts/release.sh major "API breaking changes"
```

### Release Steps

1. **Validation**: Clean working directory, on main branch
2. **Version bump**: Calculate and update version
3. **Testing**: Full test suite
4. **Build**: Create distributions
5. **Git operations**: Commit and tag
6. **Publish**: Upload to GitHub and PyPI

## Continuous Integration

### GitHub Actions

- **ci.yml**: Main pipeline
  - Multi-platform (Linux, macOS, Windows)
  - Multi-version (Python 3.8-3.12)
  - Linting and type checking
  - Coverage reports

- **release.yml**: Release automation
  - Full testing
  - Package building
  - GitHub releases
  - PyPI publishing

- **dev.yml**: Development feedback
  - Fast testing on key platforms

### Required Secrets

- `PYPI_API_TOKEN`: PyPI publishing access
- `GITHUB_TOKEN`: Provided automatically

## Code Quality

### Standards

- **PEP 8**: Code style compliance
- **Type hints**: Required for new code
- **Documentation**: Docstrings for public functions
- **Testing**: Tests for new features

### Tools

- **flake8**: Linting
- **mypy**: Type checking
- **pytest**: Testing
- **black**: Formatting (optional)

### Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

## Installation

### For Users

```bash
pip install ezgooey

# Unix
curl -sSL https://github.com/twardoch/ezgooey/raw/master/scripts/install.sh | bash

# Windows PowerShell
iwr https://github.com/twardoch/ezgooey/raw/master/scripts/install.ps1 | iex
```

### For Developers

```bash
pip install -e .          # Development install
pip install -e ".[dev]"   # With dev dependencies
```

## Troubleshooting

### Common Problems

1. **Version not updating**: Push git tags to remote
2. **Tests failing**: Check Python version and dependencies
3. **Build errors**: Verify all dependencies installed
4. **Import errors**: Reinstall package

### Debug Commands

```bash
python3 version.py get                    # Check version detection
python -c "import ezgooey; print(ezgooey.__version__)"  # Verify installation
git tag --list | sort -V                 # List git tags
pip list | grep -E "(gooey|wxpython|colored)"           # Check key dependencies
```

## Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Add tests
5. Pass all tests
6. Submit pull request

### Workflow

```bash
git checkout -b feature/new-feature
# Make changes and add tests
make test
make lint
git commit -m "Add new feature"
git push origin feature/new-feature
# Create pull request
```

## License

MIT License. See LICENSE file.