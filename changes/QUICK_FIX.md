# Quick Fix for Runtime Errors

## Problem
You're seeing SyntaxWarnings and ModuleNotFoundError when running `openad`.

## Root Causes
1. **Escape sequences not properly fixed** - Files need to use raw strings or double backslashes
2. **Dependencies not installed** - The `.venv` doesn't have the updated dependencies from pyproject.toml
3. **Langchain imports outdated** - Need to use langchain_text_splitters package

## Solution

### Step 1: Reinstall Dependencies (CRITICAL)

The main issue is that your `.venv` was created with Poetry but we've migrated to UV. You need to reinstall:

```bash
# Remove old virtual environment
rm -rf .venv

# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create new environment and install dependencies
uv sync

# Activate the new environment
source .venv/bin/activate
```

### Step 2: Fix Remaining Escape Sequences

Run the fix script:

```bash
python3 fix_syntax_warnings.py
```

Or manually fix these files:

#### openad/llm_assist/prime_chat.py
Change line 6:
```python
# FROM:
from langchain.text_splitter import RecursiveCharacterTextSplitter

# TO:
from langchain_text_splitters import RecursiveCharacterTextSplitter
```

Change lines 175, 186, 191, 221 - add `r` prefix:
```python
# FROM:
separators=["\@"]

# TO:
separators=[r"\@"]
```

#### openad/core/help.py
Lines 391-395 - add `r` prefix:
```python
# FROM:
cmd_str = cmd_str.replace("\ ", " ")

# TO:
cmd_str = cmd_str.replace(r"\ ", " ")
```

#### openad/core/grammar.py
All instances of `\@` in strings need to be `r"\@"` or `"\\@"`.

### Step 3: Verify

```bash
# Should start without warnings
openad
```

## Why This Happened

1. **Virtual Environment Mismatch**: Your `.venv` was created with Poetry's `poetry.lock` but we migrated to UV with new `pyproject.toml`. The dependencies aren't installed.

2. **File Changes Not Applied**: The escape sequence fixes I made weren't properly saved/reloaded in your Python environment.

3. **Langchain Package Split**: Langchain split their packages - `langchain.text_splitter` moved to `langchain_text_splitters`.

## Quick Command Sequence

```bash
# 1. Clean slate
rm -rf .venv
rm -rf openad.egg-info

# 2. Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Install dependencies
uv sync

# 4. Activate
source .venv/bin/activate

# 5. Fix syntax (if needed)
python3 fix_syntax_warnings.py

# 6. Test
openad
```

## If Still Having Issues

The pubchempy warning is from a third-party package and can be ignored, but if you still see other warnings:

```bash
# Check what's actually installed
uv pip list | grep langchain

# Should see:
# langchain
# langchain-community  
# langchain-text-splitters
# langsmith

# If not, force reinstall
uv sync --reinstall
```

## Expected Output

After fixing, `openad` should start with at most one warning from pubchempy (which is external), and no ModuleNotFoundError.