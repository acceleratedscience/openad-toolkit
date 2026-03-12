# OpenAD Migration Guide: Poetry to UV & Python 3.12+

## Overview

This guide documents the migration from Poetry to UV package manager and the upgrade to support Python 3.12+.

## Changes Summary

### 1. Package Manager Migration: Poetry → UV

**Why UV?**
- Faster dependency resolution (10-100x faster than Poetry)
- Better compatibility with modern Python tooling
- Simpler configuration
- Built-in virtual environment management
- Better support for monorepos and workspaces

**Migration Steps:**

```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Remove old Poetry files (backup first!)
mv poetry.lock poetry.lock.backup

# Initialize UV and install dependencies
uv sync

# Verify installation
uv run python --version
uv run pytest tests/
```

### 2. Python Version Support

**Updated:** `>=3.10,<3.13` (now supports Python 3.12)

**Previous:** `>=3.10,<3.12`

### 3. Deprecated Module Replacements

#### `imp` module → `importlib.util`

The deprecated `imp` module (removed in Python 3.12) has been replaced with `importlib.util`.

**Files Updated:**
- `openad/toolkit/toolkit_main.py`
- `openad/app/login_manager.py`

**Before:**
```python
import imp
module = imp.load_source(name, path)
```

**After:**
```python
import importlib.util
spec = importlib.util.spec_from_file_location(name, path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
```

### 4. Dependency Updates

#### Core Dependencies

| Package | Old Version | New Version | Notes |
|---------|-------------|-------------|-------|
| flask | 3.0.0 | >=3.1.0 | Security updates |
| ipython | 8.15.0 | >=8.29.0 | Python 3.12 support |
| ipywidgets | 7.8.2 | >=8.1.5 | Major version upgrade |
| numpy | ^1.26.2 | >=1.26.2,<2.0 | Prevent numpy 2.0 breaking changes |
| pandas | ^2.0.0 | >=2.2.0 | Latest stable |
| pyparsing | 3.0.9 | >=3.1.0 | Bug fixes |
| pyjwt | 2.8.0 | >=2.10.0 | Security updates |
| rdkit | ^2024 | >=2024.3.0 | Latest stable |
| tqdm | 4.66.1 | >=4.67.0 | Minor updates |
| tiktoken | >=0.5.2 | >=0.8.0 | Performance improvements |
| faiss-cpu | ^1.7.4 | >=1.9.0 | Performance improvements |
| langsmith | 0.1.131 | >=0.2.0 | API improvements |

#### Jupyter Ecosystem

| Package | Old Version | New Version | Notes |
|---------|-------------|-------------|-------|
| jupyter-client | 7.4.9 | >=8.6.0 | Major version upgrade |
| jupyter-core | 5.3.1 | >=5.7.0 | Bug fixes |
| jupyter-server | 2.7.3 | >=2.14.0 | Security updates |
| jupyterlab | 3.6.6 | >=4.3.0 | Major version upgrade |
| jupyterlab-widgets | 1.1.8 | >=3.0.0 | Major version upgrade |
| widgetsnbextension | 3.6.7 | >=4.0.0 | Major version upgrade |
| notebook | 6.5.6 | >=7.3.0 | Major version upgrade |

#### Development Tools

| Package | Old Version | New Version | Notes |
|---------|-------------|-------------|-------|
| pyright | ^1.1.331 | >=1.1.390 | Latest type checking |
| black | ^23.9.1 | >=24.10.0 | Latest formatter |
| pytest | 8.1.1 | >=8.3.0 | Latest test framework |
| pytest-cov | ^5.0.0 | >=6.0.0 | Coverage improvements |
| mypy | 1.9.0 | >=1.13.0 | Latest type checker |

### 5. Configuration Changes

#### pyproject.toml Structure

**Changed from Poetry format to standard PEP 621 format:**

```toml
# Old (Poetry)
[tool.poetry]
name = "openad"
version = "0.7.5.2"

[tool.poetry.dependencies]
python = ">=3.10,<3.12"

# New (PEP 621 / UV)
[project]
name = "openad"
version = "0.7.5.2"
requires-python = ">=3.10,<3.13"
dependencies = [...]
```

#### Build System

**Changed from Poetry to Hatchling:**

```toml
# Old
[build-system]
requires = ["poetry_core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

# New
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### 6. New Test Suite

Added comprehensive test coverage:

- `tests/unit/test_imports.py` - Verify deprecated imports removed
- `tests/unit/test_helpers.py` - Test helper functions
- `tests/unit/test_api.py` - Test API functionality

### 7. Breaking Changes

#### For Users

1. **Installation command changed:**
   ```bash
   # Old
   poetry install
   
   # New
   uv sync
   ```

2. **Running commands changed:**
   ```bash
   # Old
   poetry run openad
   poetry run pytest
   
   # New
   uv run openad
   uv run pytest
   ```

#### For Developers

1. **Module loading:** If you were using `imp.load_source()` directly, update to `importlib.util`
2. **Jupyter widgets:** Major version changes may affect custom widget implementations
3. **NumPy 2.0:** Explicitly blocked to prevent breaking changes

### 8. Testing the Migration

```bash
# 1. Install dependencies
uv sync

# 2. Run import tests
uv run pytest tests/unit/test_imports.py -v

# 3. Run helper tests
uv run pytest tests/unit/test_helpers.py -v

# 4. Run API tests
uv run pytest tests/unit/test_api.py -v

# 5. Run full test suite
uv run pytest tests/ -v

# 6. Check code quality
uv run black --check .
uv run ruff check .

# 7. Type checking
uv run mypy openad/
```

### 9. Rollback Instructions

If you need to rollback:

```bash
# 1. Restore Poetry lock file
mv poetry.lock.backup poetry.lock

# 2. Remove UV files
rm -rf .venv uv.lock .python-version

# 3. Reinstall with Poetry
poetry install
```

### 10. Common Issues & Solutions

#### Issue: Import errors after upgrade

**Solution:** Clear Python cache and reinstall:
```bash
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
uv sync --reinstall
```

#### Issue: Jupyter kernel not found

**Solution:** Reinstall kernel:
```bash
uv run python -m ipykernel install --user --name=ad-kernel
```

#### Issue: RDKit import errors

**Solution:** RDKit may need system dependencies:
```bash
# macOS
brew install rdkit

# Ubuntu/Debian
sudo apt-get install python3-rdkit
```

### 11. Performance Improvements

Expected improvements with UV:

- **Dependency resolution:** 10-100x faster
- **Installation time:** 2-5x faster
- **Lock file generation:** Near-instant
- **Virtual environment creation:** 2-3x faster

### 12. Next Steps

1. Update CI/CD pipelines to use UV
2. Update documentation with new installation instructions
3. Notify users of the migration
4. Monitor for issues in production

## Support

For issues or questions:
- GitHub Issues: https://github.com/acceleratedscience/openad-toolkit/issues
- Documentation: https://openad.accelerate.science/docs

## References

- [UV Documentation](https://docs.astral.sh/uv/)
- [PEP 621 - Project Metadata](https://peps.python.org/pep-0621/)
- [Python 3.12 Release Notes](https://docs.python.org/3/whatsnew/3.12.html)
- [importlib.util Documentation](https://docs.python.org/3/library/importlib.html#importlib.util.spec_from_file_location)