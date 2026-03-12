"""Test helper functions."""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestGeneralHelpers(unittest.TestCase):
    """Test general helper functions."""

    def test_is_notebook_mode_false(self):
        """Test is_notebook_mode returns False in non-notebook environment."""
        from openad.helpers.general import is_notebook_mode
        
        # In test environment, should return False
        result = is_notebook_mode()
        self.assertFalse(result)

    @patch('openad.helpers.general.get_ipython')
    def test_is_notebook_mode_true(self, mock_get_ipython):
        """Test is_notebook_mode returns True when IPython is available."""
        from openad.helpers.general import is_notebook_mode
        
        mock_get_ipython.return_value = MagicMock()
        result = is_notebook_mode()
        self.assertTrue(result)


class TestPathHelpers(unittest.TestCase):
    """Test path helper functions."""

    def test_parse_path_basic(self):
        """Test basic path parsing."""
        from openad.helpers.paths import parse_path
        
        # Test absolute path
        result = parse_path("/tmp/test.txt", None)
        self.assertEqual(result, "/tmp/test.txt")
        
    def test_parse_path_relative(self):
        """Test relative path parsing."""
        from openad.helpers.paths import parse_path
        
        # Test relative path with workspace
        workspace_path = "/workspace"
        result = parse_path("test.txt", workspace_path)
        self.assertTrue(result.endswith("test.txt"))


class TestFileHelpers(unittest.TestCase):
    """Test file helper functions."""

    def test_open_file_json(self):
        """Test opening JSON files."""
        from openad.helpers.files import open_file
        import tempfile
        import json
        
        # Create temporary JSON file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"test": "data"}, f)
            temp_path = f.name
        
        try:
            result = open_file(temp_path)
            self.assertEqual(result, {"test": "data"})
        finally:
            os.unlink(temp_path)


if __name__ == "__main__":
    unittest.main()

# Made with Bob
