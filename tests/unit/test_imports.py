"""Test that deprecated imports have been replaced."""
import unittest
import sys
import re
from pathlib import Path


class TestDeprecatedImports(unittest.TestCase):
    """Test that deprecated modules are not imported."""

    def test_no_imp_module(self):
        """Verify that the deprecated 'imp' module is not used."""
        # Check toolkit_main.py
        toolkit_main = Path("openad/toolkit/toolkit_main.py").read_text()
        # Use regex to match "import imp" but not "import importlib"
        imp_pattern = r'^\s*import\s+imp\s*$|^\s*import\s+imp\s+|^\s*from\s+imp\s+import'
        self.assertIsNone(
            re.search(imp_pattern, toolkit_main, re.MULTILINE),
            "toolkit_main.py should not import 'imp' module"
        )
        
        # Check login_manager.py
        login_manager = Path("openad/app/login_manager.py").read_text()
        self.assertIsNone(
            re.search(imp_pattern, login_manager, re.MULTILINE),
            "login_manager.py should not import 'imp' module"
        )

    def test_importlib_used(self):
        """Verify that importlib.util is used instead."""
        # Check toolkit_main.py
        toolkit_main = Path("openad/toolkit/toolkit_main.py").read_text()
        self.assertIn("import importlib.util", toolkit_main, "toolkit_main.py should use importlib.util")
        
        # Check login_manager.py
        login_manager = Path("openad/app/login_manager.py").read_text()
        self.assertIn("import importlib.util", login_manager, "login_manager.py should use importlib.util")

    def test_no_imp_load_source(self):
        """Verify that imp.load_source is not used anywhere."""
        # Check toolkit_main.py
        toolkit_main = Path("openad/toolkit/toolkit_main.py").read_text()
        self.assertNotIn("imp.load_source", toolkit_main, "toolkit_main.py should not use imp.load_source")
        
        # Check login_manager.py
        login_manager = Path("openad/app/login_manager.py").read_text()
        self.assertNotIn("imp.load_source", login_manager, "login_manager.py should not use imp.load_source")


if __name__ == "__main__":
    unittest.main()

# Made with Bob
