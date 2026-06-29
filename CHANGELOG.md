# Changelog

All notable changes to `ezgooey` are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [Unreleased]

### Fixed
- `ezgooey.logging.init()` now always updates the root logger level on repeated
  calls. Previously, Python's `basicConfig` — which is a no-op once handlers
  exist — meant that a second `init(level=DEBUG)` call left the logger at the
  level set by the first call. A direct `getLogger().setLevel(level)` call after
  `basicConfig` restores the expected behaviour.

### Added
- Full type annotations and docstrings on the public API (`ezgooey.ez` and
  `ezgooey.logging`).
- Jekyll documentation site under `docs/` with API reference and usage guide.
- `docs/index.md` explaining the easy-GUI concept, mode-switching logic,
  monkey-patching approach, and advanced usage patterns.

### Changed
- Build system migrated from `setuptools` to **hatchling + hatch-vcs** for
  PEP 517-compliant builds and automatic git-tag versioning.
- Replaced `black`, `isort`, and `flake8` lint config with **ruff** in
  `pyproject.toml`.
- `pytest.ini` removed; pytest config consolidated into
  `[tool.pytest.ini_options]` in `pyproject.toml`.
- `ezgooey/__init__.py` updated to import version from hatch-vcs generated
  `_version.py` first, falling back to the git-tag helper and then to
  `VERSION.txt`.

---

## [2.7.5] — prior release

Initial modernised release with CI, test suite (28 tests across `test_ez`,
`test_integration`, `test_logging`, `test_version`), and `src/`-style
packaging groundwork.

---

## [1.2.0] — legacy

Original public release. Core `ezgooey` decorator and colored logging module.
