"""Test OpenAD API functionality."""
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestOpenadAPI(unittest.TestCase):
    """Test OpenadAPI class."""

    @patch('openad.api.importlib.util.find_spec')
    @patch('openad.api.importlib.util.module_from_spec')
    def test_api_initialization(self, mock_module_from_spec, mock_find_spec):
        """Test API initialization."""
        # Mock the spec and module
        mock_spec = MagicMock()
        mock_spec.loader = MagicMock()
        mock_find_spec.return_value = mock_spec
        
        mock_module = MagicMock()
        mock_module_from_spec.return_value = mock_module
        
        from openad.api import OpenadAPI
        
        api = OpenadAPI(name="test_api")
        self.assertEqual(api.name, "test_api")
        self.assertIsNotNone(api.main_app)

    @patch('openad.api.importlib.util.find_spec')
    @patch('openad.api.importlib.util.module_from_spec')
    def test_api_request_basic(self, mock_module_from_spec, mock_find_spec):
        """Test basic API request."""
        # Mock the spec and module
        mock_spec = MagicMock()
        mock_spec.loader = MagicMock()
        mock_find_spec.return_value = mock_spec
        
        mock_module = MagicMock()
        mock_module.GLOBAL_SETTINGS = {"display": "cli"}
        mock_module_from_spec.return_value = mock_module
        
        from openad.api import OpenadAPI
        
        api = OpenadAPI(name="test_api")
        
        # Mock the command execution
        with patch.object(api.main_app, 'do_cmd', return_value="test_result"):
            result = api.request("test command")
            # Verify display mode was set to api
            self.assertEqual(api.main_app.GLOBAL_SETTINGS["display"], "api")


class TestAPIDataFrameHandling(unittest.TestCase):
    """Test API DataFrame handling."""

    @patch('openad.api.importlib.util.find_spec')
    @patch('openad.api.importlib.util.module_from_spec')
    def test_dataframe_parameter(self, mock_module_from_spec, mock_find_spec):
        """Test DataFrame parameter handling."""
        import pandas as pd
        
        # Mock the spec and module
        mock_spec = MagicMock()
        mock_spec.loader = MagicMock()
        mock_find_spec.return_value = mock_spec
        
        mock_module = MagicMock()
        mock_module.GLOBAL_SETTINGS = {"display": "cli"}
        mock_module_from_spec.return_value = mock_module
        
        from openad.api import OpenadAPI
        
        api = OpenadAPI(name="test_api")
        
        # Create test DataFrame
        test_df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
        
        # Test with DataFrame parameter
        with patch.object(api.main_app, 'do_cmd', return_value="test_result"):
            result = api.request("test dataframe test_df", test_df=test_df)
            self.assertEqual(api.main_app.GLOBAL_SETTINGS["display"], "api")


if __name__ == "__main__":
    unittest.main()

# Made with Bob
