#!/usr/bin/env python3
"""Fix all invalid escape sequences in the codebase."""

import re
from pathlib import Path

def fix_file(filepath):
    """Fix escape sequences in a single file."""
    print(f"Fixing {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix escape sequences in strings
    # Pattern: finds strings with invalid escape sequences
    patterns = [
        (r'(separators=\[)"\\@"', r'\1r"\\@"'),  # Fix separators with @
        (r'\.replace\("\\([\ \[\]<>])"', r'.replace(r"\\\\1"'),  # Fix replace calls
        (r'(?<!\\)\\@(?!\\)', r'\\\\@'),  # Fix standalone \@ in strings
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Fixed {filepath}")
        return True
    else:
        print(f"  - No changes needed for {filepath}")
        return False

def main():
    """Fix all Python files with escape sequence issues."""
    files_to_fix = [
        'openad/llm_assist/prime_chat.py',
        'openad/core/help.py',
        'openad/core/grammar.py',
    ]
    
    fixed_count = 0
    for filepath in files_to_fix:
        path = Path(filepath)
        if path.exists():
            if fix_file(path):
                fixed_count += 1
        else:
            print(f"  ✗ File not found: {filepath}")
    
    print(f"\n✓ Fixed {fixed_count} files")
    print("\nNext steps:")
    print("1. Reinstall dependencies: uv sync")
    print("2. Test: openad")

if __name__ == '__main__':
    main()

# Made with Bob
