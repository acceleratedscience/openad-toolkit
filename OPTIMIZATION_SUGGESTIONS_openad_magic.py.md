# Formatting and Optimization Suggestions for openad_magic.py

## Overview
Analysis of `openad/app/magic/openad_magic.py` (124 lines) with formatting improvements and optimization suggestions.

---

## 🔴 Critical Issues

### 1. Dangerous Use of eval() (Lines 60, 89)

**Current Problem:**
```python
df = eval(line_list[i])  # pylint: disable=eval-used #only way to execute
```

**Security Risk:** `eval()` executes arbitrary Python code and is a major security vulnerability.

**Safe Alternative:**
```python
# Use local_ns parameter that's already available
if line_list[i] in local_ns and isinstance(local_ns[line_list[i]], pandas.DataFrame):
    api_variable[line_list[i]] = local_ns[line_list[i]]
```

**Complete Fix:**
```python
@needs_local_scope
@line_cell_magic
def openad(self, line, cell=None, local_ns=None):
    """Invokes the Magic command interface for OpenAD"""
    api_variable = {}
    GLOBAL_SETTINGS["display"] = "notebook"
    line_list = line.split()
    
    # Extract dataframe variables safely
    for i in range(1, len(line_list)):
        if line_list[i - 1].upper() == "DATAFRAME":
            var_name = line_list[i]
            # Use local_ns instead of eval()
            if local_ns and var_name in local_ns:
                df = local_ns[var_name]
                if isinstance(df, pandas.DataFrame):
                    api_variable[var_name] = df
    
    result = openad.app.main.api_remote(line, context_cache, api_variable)
    
    if isinstance(result, DataFrame):
        result = output_table(result, return_val=True)
    elif isinstance(result, str):
        result = strip_leading_blanks(result)
        result = result.replace("<br>", "\n")
    
    return result
```

---

### 2. Bare except Clause (Lines 63, 92)

**Current Problem:**
```python
except:  # pylint: disable=bare-except # We do not care what fails
    pass
```

**Issue:** Catches ALL exceptions including KeyboardInterrupt and SystemExit.

**Fix:**
```python
except (NameError, KeyError, TypeError, AttributeError) as e:
    # Log the error for debugging
    pass  # Variable not found or not a DataFrame
```

---

### 3. Bug in strip_leading_blanks() (Line 110)

**Current Problem:**
```python
def strip_leading_blanks(input):
    temp = input.split("\n")
    output = ""
    for x in temp:
        while str(x).startswith("   "):
            X = str(x).replace("   ", "  ")  # BUG: X is never used!
        output = output + x + "\n"
    return output
```

**Issues:**
- Variable `X` (uppercase) is assigned but never used
- Variable `x` (lowercase) is never updated in the loop
- Infinite loop if line starts with 3+ spaces
- Inefficient string concatenation

**Fixed Version:**
```python
def strip_leading_blanks(text: str) -> str:
    """Remove excessive leading whitespace from each line."""
    lines = text.split("\n")
    result = []
    
    for line in lines:
        # Replace triple spaces with double spaces iteratively
        while line.startswith("   "):
            line = line.replace("   ", "  ", 1)  # Replace only first occurrence
        result.append(line)
    
    return "\n".join(result)
```

---

## 🟡 Code Quality Issues

### 4. Duplicate Code (Lines 49-102)

**Problem:** `openad()` and `openadd()` are 95% identical.

**Refactored Solution:**
```python
@magics_class
class AD(Magics):
    """Magic Command Class"""
    
    def _execute_openad_command(self, line: str, local_ns: dict, display_mode: str) -> any:
        """Common logic for openad magic commands."""
        api_variable = {}
        GLOBAL_SETTINGS["display"] = display_mode
        line_list = line.split()
        
        # Extract dataframe variables safely
        for i in range(1, len(line_list)):
            if line_list[i - 1].upper() == "DATAFRAME":
                var_name = line_list[i]
                if local_ns and var_name in local_ns:
                    df = local_ns[var_name]
                    if isinstance(df, pandas.DataFrame):
                        api_variable[var_name] = df
        
        return openad.app.main.api_remote(line, context_cache, api_variable)
    
    @needs_local_scope
    @line_cell_magic
    def openad(self, line, cell=None, local_ns=None):
        """Invokes the Magic command interface for OpenAD"""
        result = self._execute_openad_command(line, local_ns, "notebook")
        
        if isinstance(result, DataFrame):
            result = output_table(result, return_val=True)
        elif isinstance(result, str):
            result = strip_leading_blanks(result)
            result = result.replace("<br>", "\n")
        
        return result
    
    @needs_local_scope
    @line_cell_magic
    def openadd(self, line, cell=None, local_ns=None):
        """Invokes the Magic command interface for OpenAD (data mode)"""
        result = self._execute_openad_command(line, local_ns, "api")
        
        # MAJOR-RELEASE-TODO: data function should never display
        if isinstance(result, Styler):
            result = result.data
        
        return result
```

---

### 5. Inefficient Loop (Lines 56-65, 84-94)

**Current:**
```python
x = len(line_list)
i = 1
if x > 1:
    while i < x:
        if line_list[i - 1].upper() == "DATAFRAME":
            # ...
        i += 1
```

**Optimized:**
```python
# More Pythonic iteration
for i in range(1, len(line_list)):
    if line_list[i - 1].upper() == "DATAFRAME":
        # ...
```

---

### 6. Unused Imports and Variables

**Issues:**
- Line 27: `sys.path.insert(0, "../")` - Modifies path but may not be needed
- Line 28-29: Path manipulation that might be redundant
- Line 32-39: `handle_cache` is defined but never used in this file

**Cleanup:**
```python
# Remove if not needed:
# sys.path.insert(0, "../")
# os.sys.path.append(os.path.dirname(os.path.abspath("./")))
# module_path = os.path.abspath(os.path.join(".."))

# If handle_cache is not used, remove it:
# handle_cache = {...}
```

---

## 🟢 Formatting Improvements

### 7. Add Type Hints

**Current:**
```python
def strip_leading_blanks(input):
    temp = input.split("\n")
```

**With Type Hints:**
```python
def strip_leading_blanks(text: str) -> str:
    """Remove excessive leading whitespace from each line.
    
    Args:
        text: Input string with potential leading whitespace
        
    Returns:
        String with normalized whitespace
    """
    lines = text.split("\n")
```

---

### 8. Improve Variable Names

**Current Issues:**
- `x` - unclear (line 54, 83)
- `i` - generic counter
- `X` - uppercase unused variable (line 110)
- `input` - shadows built-in function name

**Better Names:**
```python
# Before
x = len(line_list)
i = 1

# After
num_tokens = len(line_list)
token_index = 1

# Before
def strip_leading_blanks(input):

# After
def strip_leading_blanks(text: str) -> str:
```

---

### 9. Add Docstrings

**Current:** Missing detailed docstrings

**Improved:**
```python
@magics_class
class AD(Magics):
    """
    IPython magic commands for OpenAD integration.
    
    Provides two magic commands:
    - %openad: Execute OpenAD commands in notebook mode
    - %openadd: Execute OpenAD commands in API mode (returns raw data)
    
    Example:
        %openad set workspace my_workspace
        %openad add molecule dataframe my_df
    """
    
    @needs_local_scope
    @line_cell_magic
    def openad(self, line, cell=None, local_ns=None):
        """
        Execute OpenAD command in notebook display mode.
        
        Args:
            line: Command line string
            cell: Cell content (for cell magic, unused)
            local_ns: Local namespace for variable access
            
        Returns:
            Command result (formatted for notebook display)
            
        Example:
            %openad list molecules
            %openad add molecule dataframe my_df
        """
```

---

## 📋 Complete Refactored Version

```python
"""IPython magic commands for OpenAD integration."""

import os
import sys
import atexit
from typing import Any, Optional, Dict

import pandas
from pandas import DataFrame
from pandas.io.formats.style import Styler

from IPython.display import Markdown, display
from IPython.core.magic import (
    Magics,
    magics_class,
    line_magic,
    cell_magic,
    line_cell_magic,
    needs_local_scope,
)
from IPython.core.interactiveshell import InteractiveShell

import openad.app.main
from openad.app.main import GLOBAL_SETTINGS
from openad.helpers.output import output_table, output_text

# Configure IPython to display all expressions
InteractiveShell.ast_node_interactivity = "all"

# Context cache for maintaining state across magic commands
context_cache: Dict[str, Optional[str]] = {
    "workspace": None,
    "toolkit": None
}


def strip_leading_blanks(text: str) -> str:
    """
    Remove excessive leading whitespace from each line.
    
    Replaces triple spaces with double spaces iteratively until
    no triple spaces remain at the start of any line.
    
    Args:
        text: Input string with potential leading whitespace
        
    Returns:
        String with normalized whitespace
    """
    lines = text.split("\n")
    result = []
    
    for line in lines:
        # Replace triple spaces with double spaces iteratively
        while line.startswith("   "):
            line = line.replace("   ", "  ", 1)
        result.append(line)
    
    return "\n".join(result)


@magics_class
class AD(Magics):
    """
    IPython magic commands for OpenAD integration.
    
    Provides two magic commands:
    - %openad: Execute OpenAD commands in notebook mode (formatted output)
    - %openadd: Execute OpenAD commands in API mode (raw data)
    
    Examples:
        %openad set workspace my_workspace
        %openad add molecule dataframe my_df
        %openadd list molecules  # Returns raw DataFrame
    """
    
    def _extract_dataframe_variables(
        self, 
        line_tokens: list[str], 
        local_ns: Optional[Dict[str, Any]]
    ) -> Dict[str, DataFrame]:
        """
        Safely extract DataFrame variables from command line.
        
        Args:
            line_tokens: Tokenized command line
            local_ns: Local namespace containing variables
            
        Returns:
            Dictionary mapping variable names to DataFrames
        """
        api_variables = {}
        
        if not local_ns:
            return api_variables
        
        # Look for "dataframe <var_name>" pattern
        for i in range(1, len(line_tokens)):
            if line_tokens[i - 1].upper() == "DATAFRAME":
                var_name = line_tokens[i]
                
                # Safely get variable from namespace
                if var_name in local_ns:
                    var_value = local_ns[var_name]
                    if isinstance(var_value, pandas.DataFrame):
                        api_variables[var_name] = var_value
        
        return api_variables
    
    def _execute_openad_command(
        self, 
        line: str, 
        local_ns: Optional[Dict[str, Any]], 
        display_mode: str
    ) -> Any:
        """
        Common logic for executing OpenAD magic commands.
        
        Args:
            line: Command line string
            local_ns: Local namespace for variable access
            display_mode: Display mode ("notebook" or "api")
            
        Returns:
            Command execution result
        """
        GLOBAL_SETTINGS["display"] = display_mode
        line_tokens = line.split()
        
        # Extract DataFrame variables from local namespace
        api_variables = self._extract_dataframe_variables(line_tokens, local_ns)
        
        # Execute command through OpenAD API
        return openad.app.main.api_remote(line, context_cache, api_variables)
    
    @needs_local_scope
    @line_cell_magic
    def openad(self, line: str, cell: Optional[str] = None, local_ns: Optional[Dict] = None) -> Any:
        """
        Execute OpenAD command in notebook display mode.
        
        Formats output for display in Jupyter notebooks, including
        styled tables and formatted text.
        
        Args:
            line: Command line string
            cell: Cell content (for cell magic, currently unused)
            local_ns: Local namespace for variable access
            
        Returns:
            Formatted command result for notebook display
            
        Examples:
            %openad list molecules
            %openad add molecule dataframe my_df
            %openad set workspace my_workspace
        """
        result = self._execute_openad_command(line, local_ns, "notebook")
        
        # Format result for notebook display
        if isinstance(result, DataFrame):
            result = output_table(result, return_val=True)
        elif isinstance(result, str):
            result = strip_leading_blanks(result)
            result = result.replace("<br>", "\n")
        
        return result
    
    @needs_local_scope
    @line_cell_magic
    def openadd(self, line: str, cell: Optional[str] = None, local_ns: Optional[Dict] = None) -> Any:
        """
        Execute OpenAD command in API mode (returns raw data).
        
        Returns raw data structures without notebook formatting,
        useful for programmatic access to results.
        
        Args:
            line: Command line string
            cell: Cell content (for cell magic, currently unused)
            local_ns: Local namespace for variable access
            
        Returns:
            Raw command result (DataFrame, dict, etc.)
            
        Examples:
            df = %openadd list molecules
            result = %openadd search molecules
        """
        result = self._execute_openad_command(line, local_ns, "api")
        
        # MAJOR-RELEASE-TODO: data function should never display
        # Extract raw data from Styler objects
        if isinstance(result, Styler):
            result = result.data
        
        return result


def cleanup() -> None:
    """Clean up OpenAD magic command state on exit."""
    print("Cleaning up OpenAD magic commands...")
    if openad.app.main.MAGIC_PROMPT:
        openad.app.main.MAGIC_PROMPT.do_exit("exit magic")


# Register magic commands with IPython
ip = get_ipython()  # noqa: F821 # pylint: disable=undefined-variable
ip.register_magics(AD)

# Register cleanup handler
atexit.register(cleanup)
```

---

## 📊 Summary of Changes

| Issue | Type | Severity | Lines Affected |
|-------|------|----------|----------------|
| **eval() usage** | Security | Critical | 2 locations |
| **Bare except** | Safety | High | 2 locations |
| **Bug in strip_leading_blanks** | Bug | High | 1 function |
| **Duplicate code** | Maintainability | Medium | 50+ lines |
| **Inefficient loops** | Performance | Low | 2 locations |
| **Missing type hints** | Quality | Low | All functions |
| **Poor variable names** | Readability | Low | 10+ variables |
| **Missing docstrings** | Documentation | Low | All functions |

---

## 🎯 Implementation Priority

### Phase 1: Critical Fixes (Do Immediately)
1. **Replace eval() with safe variable lookup** - Security risk
2. **Fix strip_leading_blanks() bug** - Broken functionality
3. **Replace bare except clauses** - Safety issue

### Phase 2: Code Quality (Next)
4. Extract common logic to reduce duplication
5. Improve variable names
6. Add type hints

### Phase 3: Documentation (Polish)
7. Add comprehensive docstrings
8. Add usage examples
9. Document security considerations

---

## ⚠️ Breaking Changes

**None** - All changes maintain backward compatibility:
- Same function signatures
- Same return types
- Same behavior (except bug fixes)

---

## 🔒 Security Notes

The current use of `eval()` is a **critical security vulnerability**. While it's in a Jupyter notebook context (somewhat sandboxed), it should still be avoided. The `local_ns` parameter provides safe access to variables without executing arbitrary code.

---

## 📈 Expected Benefits

- **Security**: Eliminates eval() vulnerability
- **Reliability**: Fixes infinite loop bug
- **Maintainability**: 50% less duplicate code
- **Readability**: Clear variable names and documentation
- **Type Safety**: Type hints enable better IDE support

---

## 🧪 Testing Recommendations

```python
# Test DataFrame extraction
df = pd.DataFrame({'a': [1, 2, 3]})
%openad add molecule dataframe df

# Test strip_leading_blanks
assert strip_leading_blanks("   test") == "  test"
assert strip_leading_blanks("      test") == "  test"

# Test both magic commands
result1 = %openad list molecules
result2 = %openadd list molecules
assert type(result1) != type(result2)  # Different formatting