# Development Guide for ezgooey

This document describes the development setup, testing, and release process for ezgooey.

## Project Structure

```
ezgooey/
├── ezgooey/                 # Main package
│   ├── __init__.py          # Package initialization with git-tag versioning
│   ├── ez.py                # Main ezgooey decorator and argparse integration
│   └── logging.py           # Colorful logging utilities
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── conftest.py          # Pytest configuration
│   ├── test_version.py      # Version management tests
│   ├── test_ez.py           # Core functionality tests
│   ├── test_logging.py      # Logging tests
│   └── test_integration.py  # Integration tests
├── scripts/                 # Build and deployment scripts
│   ├── test.sh              # Run test suite
│   ├── build.sh             # Build package
│   ├── release.sh           # Create releases
│   ├── install.sh           # Easy installation (Unix)
│   └── install.ps1          # Easy installation (Windows)
├── .github/workflows/       # GitHub Actions CI/CD
│   ├── ci.yml               # Main CI pipeline
│   ├── dev.yml              # Development branch testing
│   └── release.yml          # Release automation
├── version.py               # Git-tag-based version management
├── pyproject.toml           # Modern Python project configuration
├── setup.py                 # Legacy setup for compatibility
├── Makefile                 # Development convenience commands
└── requirements*.txt        # Dependencies
```

## Git-Tag-Based Versioning

The project uses git tags for semantic versioning:

- **Version Source**: Git tags (`v1.2.3`) are the primary source of truth
- **Fallback**: VERSION.txt and __init__.py as fallbacks
- **Semantic Versioning**: Follows semver.org specification
- **Automatic**: Version is automatically detected during build

### Version Management Commands

```bash
# Get current version
python3 version.py get

# Bump version
python3 version.py bump patch   # 1.2.3 -> 1.2.4
python3 version.py bump minor   # 1.2.3 -> 1.3.0
python3 version.py bump major   # 1.2.3 -> 2.0.0
```

## Development Setup

### Prerequisites

- Python 3.8 or later
- Git
- Make (optional, for convenience commands)

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/twardoch/ezgooey.git
cd ezgooey

# Set up development environment
make dev-setup

# Or manually:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Development Commands

```bash
# Run tests
make test
# Or: ./scripts/test.sh

# Build package
make build
# Or: ./scripts/build.sh

# Run linting
make lint

# Run type checking
make type-check

# Run all checks
make check

# Clean build artifacts
make clean

# Show current version
make version
```

## Testing

### Test Structure

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **Cross-Platform**: Tests run on Linux, macOS, and Windows
- **Multi-Version**: Tests run on Python 3.8 through 3.12

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_version.py -v

# Run with coverage
python -m pytest tests/ --cov=ezgooey --cov-report=html

# Run only fast tests
python -m pytest tests/ -m "not slow"
```

### Test Configuration

- **pytest.ini**: Pytest configuration
- **conftest.py**: Shared fixtures and setup
- **Coverage**: Configured in pyproject.toml

## Release Process

### Automated Release (Recommended)

```bash
# Create a patch release (1.2.3 -> 1.2.4)
make release-patch

# Create a minor release (1.2.3 -> 1.3.0)
make release-minor

# Create a major release (1.2.3 -> 2.0.0)
make release-major
```

### Manual Release

```bash
./scripts/release.sh patch "Fix bug in argument parsing"
./scripts/release.sh minor "Add new feature"
./scripts/release.sh major "Breaking API changes"
```

### Release Process Steps

1. **Validation**: Ensure working directory is clean and on master/main branch
2. **Version Bump**: Calculate new version and update files
3. **Testing**: Run complete test suite
4. **Building**: Create source and wheel distributions
5. **Git Operations**: Commit changes and create git tag
6. **Artifacts**: Upload to GitHub releases and PyPI

## Continuous Integration

### GitHub Actions Workflows

- **CI (ci.yml)**: Run on pushes to main branches
  - Multi-platform testing (Linux, macOS, Windows)
  - Multi-version testing (Python 3.8-3.12)
  - Linting and type checking
  - Coverage reporting

- **Release (release.yml)**: Run on git tags
  - Full test suite
  - Package building
  - GitHub release creation
  - PyPI publishing

- **Development (dev.yml)**: Run on development branches
  - Fast testing on key platforms
  - Development feedback

### Secrets Configuration

Required GitHub secrets:
- `PYPI_API_TOKEN`: PyPI API token for publishing
- `GITHUB_TOKEN`: Automatically provided by GitHub

## Code Quality

### Standards

- **PEP 8**: Python code style
- **Type Hints**: Encouraged for new code
- **Documentation**: Docstrings for all public functions
- **Testing**: All new features should have tests

### Tools

- **flake8**: Linting
- **mypy**: Type checking
- **pytest**: Testing framework
- **black**: Code formatting (optional)

### Pre-commit Hooks

Consider setting up pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

## Installation Methods

### For End Users

```bash
# Via pip
pip install ezgooey

# Via installation script (Unix)
curl -sSL https://github.com/twardoch/ezgooey/raw/master/scripts/install.sh | bash

# Via installation script (Windows PowerShell)
iwr https://github.com/twardoch/ezgooey/raw/master/scripts/install.ps1 | iex
```

### For Developers

```bash
# Development installation
pip install -e .

# With development dependencies
pip install -e ".[dev]"
```

## Troubleshooting

### Common Issues

1. **Version not updating**: Ensure git tags are pushed to remote
2. **Tests failing**: Check Python version and dependencies
3. **Build errors**: Verify all dependencies are installed
4. **Import errors**: Ensure package is properly installed

### Debug Commands

```bash
# Check version detection
python3 version.py get

# Verify package installation
python -c "import ezgooey; print(ezgooey.__version__)"

# Check git tags
git tag --list | sort -V

# Verify dependencies
pip list | grep -E "(gooey|wxpython|colored)"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Development Workflow

1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes and add tests
3. Run tests: `make test`
4. Run linting: `make lint`
5. Commit changes: `git commit -m "Add new feature"`
6. Push branch: `git push origin feature/new-feature`
7. Create pull request

## License

MIT License. See LICENSE file for details.