# Testing Instructions for OpenAD Upgrade

## Prerequisites

Before testing, ensure you have:

1. **UV installed:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Python 3.10, 3.11, or 3.12 available**

3. **Git repository cloned:**
   ```bash
   git clone https://github.com/acceleratedscience/openad-toolkit.git
   cd openad-toolkit
   ```

## Installation Testing

### Step 1: Clean Environment

```bash
# Remove any existing virtual environments
rm -rf .venv

# Clean Python cache
make clean
```

### Step 2: Install with UV

```bash
# Sync all dependencies
uv sync

# Verify installation
uv run python --version
uv run python -c "import openad; print('OpenAD imported successfully')"
```

**Expected Output:**
- Python version should be 3.10, 3.11, or 3.12
- OpenAD should import without errors

### Step 3: Install Jupyter Kernel

```bash
uv run python -m ipykernel install --user --name=ad-kernel
```

**Expected Output:**
- Kernel installed successfully message

## Unit Tests

### Test 1: Import Validation

Tests that deprecated `imp` module has been replaced with `importlib.util`.

```bash
uv run pytest tests/unit/test_imports.py -v
```

**Expected Output:**
```
tests/unit/test_imports.py::TestDeprecatedImports::test_no_imp_module PASSED
tests/unit/test_imports.py::TestDeprecatedImports::test_importlib_used PASSED
```

### Test 2: Helper Functions

Tests core helper functions for path handling, file operations, and notebook detection.

```bash
uv run pytest tests/unit/test_helpers.py -v
```

**Expected Output:**
```
tests/unit/test_helpers.py::TestGeneralHelpers::test_is_notebook_mode_false PASSED
tests/unit/test_helpers.py::TestGeneralHelpers::test_is_notebook_mode_true PASSED
tests/unit/test_helpers.py::TestPathHelpers::test_parse_path_basic PASSED
tests/unit/test_helpers.py::TestPathHelpers::test_parse_path_relative PASSED
tests/unit/test_helpers.py::TestFileHelpers::test_open_file_json PASSED
```

### Test 3: API Functionality

Tests the OpenAD API initialization and request handling.

```bash
uv run pytest tests/unit/test_api.py -v
```

**Expected Output:**
```
tests/unit/test_api.py::TestOpenadAPI::test_api_initialization PASSED
tests/unit/test_api.py::TestOpenadAPI::test_api_request_basic PASSED
tests/unit/test_api.py::TestAPIDataFrameHandling::test_dataframe_parameter PASSED
```

### Test 4: All Unit Tests with Coverage

```bash
make test-unit
```

**Expected Output:**
- All tests should pass
- Coverage report should be generated

## Code Quality Tests

### Test 5: Linting

```bash
make check-lint
```

**Expected Output:**
- Black: All files should pass formatting check
- Ruff: No linting errors

### Test 6: Type Checking

```bash
make type-check
```

**Expected Output:**
- MyPy should complete (some warnings expected due to third-party libraries)

### Test 7: Pre-commit Hooks

```bash
make pre-commit
```

**Expected Output:**
- All pre-commit hooks should pass

## Integration Tests

### Test 8: CLI Functionality

```bash
# Test basic CLI
uv run openad --help

# Test version
uv run openad --version
```

**Expected Output:**
- Help text should display
- Version should show 0.7.5.2

### Test 9: API Usage

Create a test script `test_api_usage.py`:

```python
from openad import OpenadAPI

# Initialize API
api = OpenadAPI("test")

# Test basic command
result = api.request("? help")
print("API test successful!")
```

Run it:
```bash
uv run python test_api_usage.py
```

**Expected Output:**
- "API test successful!" message

### Test 10: Jupyter Integration

```bash
# Start Jupyter Lab
uv run jupyter lab

# In a notebook, test:
%load_ext openad.app.magic.openad_magic
```

**Expected Output:**
- Jupyter Lab should start
- Magic commands should load without errors

## Dependency Verification

### Test 11: Critical Dependencies

```bash
uv run python -c "
import flask
import pandas
import numpy
import rdkit
import langchain
import ipython
print('Flask:', flask.__version__)
print('Pandas:', pandas.__version__)
print('NumPy:', numpy.__version__)
print('RDKit:', rdkit.__version__)
print('LangChain:', langchain.__version__)
print('IPython:', ipython.__version__)
print('All critical dependencies imported successfully!')
"
```

**Expected Output:**
- All packages should import
- Versions should match or exceed minimum requirements

### Test 12: Python 3.12 Specific

If testing on Python 3.12:

```bash
uv run python -c "
import sys
assert sys.version_info >= (3, 12), 'Not Python 3.12+'
import importlib.util  # Should work
try:
    import imp  # Should fail
    print('ERROR: imp module still available!')
except ModuleNotFoundError:
    print('SUCCESS: imp module properly removed in Python 3.12')
"
```

**Expected Output:**
- "SUCCESS: imp module properly removed in Python 3.12"

## Performance Tests

### Test 13: Installation Speed

```bash
# Clean environment
rm -rf .venv

# Time the installation
time uv sync
```

**Expected Output:**
- Should complete in under 2 minutes (vs 5-10 minutes with Poetry)

### Test 14: Dependency Resolution

```bash
# Time lock file generation
time uv lock
```

**Expected Output:**
- Should complete in under 10 seconds

## Regression Tests

### Test 15: Existing Functionality

Run the existing test suite:

```bash
uv run pytest tests/ -v --tb=short
```

**Expected Output:**
- All existing tests should pass
- No new failures introduced

### Test 16: Example Notebooks

If example notebooks exist:

```bash
# Test notebook execution
uv run jupyter nbconvert --to notebook --execute tests/_for_testing/test_help.ipynb
```

**Expected Output:**
- Notebook should execute without errors

## Troubleshooting

### Issue: UV not found

**Solution:**
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH
export PATH="$HOME/.cargo/bin:$PATH"
```

### Issue: Import errors

**Solution:**
```bash
# Clean and reinstall
make clean
uv sync --reinstall
```

### Issue: Jupyter kernel not found

**Solution:**
```bash
# Reinstall kernel
uv run python -m ipykernel install --user --name=ad-kernel --force
```

### Issue: RDKit import errors

**Solution:**
```bash
# macOS
brew install rdkit

# Ubuntu/Debian
sudo apt-get install python3-rdkit

# Then reinstall
uv sync --reinstall
```

## Test Results Checklist

Use this checklist to track your testing progress:

- [ ] Clean environment setup
- [ ] UV installation successful
- [ ] Dependencies synced
- [ ] Import validation tests pass
- [ ] Helper function tests pass
- [ ] API tests pass
- [ ] All unit tests pass with coverage
- [ ] Linting passes
- [ ] Type checking completes
- [ ] Pre-commit hooks pass
- [ ] CLI functionality works
- [ ] API usage works
- [ ] Jupyter integration works
- [ ] Critical dependencies verified
- [ ] Python 3.12 specific tests pass (if applicable)
- [ ] Installation performance acceptable
- [ ] Dependency resolution fast
- [ ] Existing tests still pass
- [ ] Example notebooks work (if applicable)

## Reporting Issues

If you encounter issues:

1. **Capture the error:**
   ```bash
   uv run pytest tests/unit/test_imports.py -v > test_output.log 2>&1
   ```

2. **Gather environment info:**
   ```bash
   uv --version
   uv run python --version
   uv run pip list > installed_packages.txt
   ```

3. **Create an issue** with:
   - Error message
   - Test output log
   - Environment information
   - Steps to reproduce

## Success Criteria

The upgrade is successful if:

1. ✅ All unit tests pass
2. ✅ No import errors for critical dependencies
3. ✅ CLI and API functionality work
4. ✅ Jupyter integration works
5. ✅ Code quality checks pass
6. ✅ Installation is faster than Poetry
7. ✅ Python 3.12 support confirmed
8. ✅ No regression in existing functionality

## Next Steps After Testing

Once all tests pass:

1. Update CI/CD pipelines
2. Update documentation
3. Create release notes
4. Notify users of upgrade
5. Monitor production deployment

---

**Last Updated:** 2026-03-12  
**Version:** 0.7.5.2  
**Status:** Ready for Testing