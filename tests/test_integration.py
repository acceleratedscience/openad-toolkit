"""
Integration tests for OpenAD toolkit.

Tests the interaction between different modules and real-world scenarios.
"""

import pytest
import tempfile
from pathlib import Path


@pytest.mark.integration
class TestWorkspaceIntegration:
    """Test workspace creation and management"""
    
    @pytest.mark.skip(reason="Requires full OpenAD environment")
    def test_create_workspace(self):
        """Test creating a new workspace"""
        # This would test actual workspace creation
        pass
    
    @pytest.mark.skip(reason="Requires full OpenAD environment")
    def test_switch_workspace(self):
        """Test switching between workspaces"""
        pass


@pytest.mark.integration
class TestToolkitIntegration:
    """Test toolkit installation and usage"""
    
    @pytest.mark.skip(reason="Requires full OpenAD environment")
    def test_install_toolkit(self):
        """Test installing a toolkit"""
        pass
    
    @pytest.mark.skip(reason="Requires full OpenAD environment")
    def test_set_context(self):
        """Test setting toolkit context"""
        pass


@pytest.mark.integration
class TestMoleculeIntegration:
    """Test molecule operations"""
    
    @pytest.mark.skip(reason="Requires PubChem access")
    def test_fetch_molecule_from_pubchem(self):
        """Test fetching molecule from PubChem"""
        pass
    
    @pytest.mark.skip(reason="Requires full OpenAD environment")
    def test_add_molecule_to_workspace(self):
        """Test adding molecule to workspace"""
        pass


@pytest.mark.integration
class TestSerializationIntegration:
    """Test serialization in real scenarios"""
    
    def test_credentials_save_load_cycle(self, tmp_path):
        """Test complete credentials save/load cycle"""
        from openad.helpers.serialization import save_data, load_data
        
        credentials = {
            "host": "https://api.test.com",
            "auth": {
                "user_name": "testuser",
                "api_key": "test_key_123"
            },
            "verify_ssl": "true"
        }
        
        cred_file = tmp_path / "test_credentials.msgpack"
        
        # Save
        save_data(credentials, cred_file, use_msgpack=True)
        
        # Load
        loaded = load_data(cred_file)
        
        assert loaded == credentials
        assert loaded["auth"]["api_key"] == "test_key_123"
    
    def test_registry_save_load_cycle(self, tmp_path):
        """Test complete registry save/load cycle"""
        from openad.helpers.serialization import save_data, load_data
        
        registry = {
            "workspace": "TEST_WORKSPACE",
            "context": "DS4SD",
            "toolkits": ["DS4SD", "RXN"],
            "env_vars": {
                "refresh_help_ai": True,
                "test_mode": True
            }
        }
        
        reg_file = tmp_path / "test_registry.msgpack"
        
        # Save
        save_data(registry, reg_file, use_msgpack=True)
        
        # Load
        loaded = load_data(reg_file)
        
        assert loaded == registry
        assert "DS4SD" in loaded["toolkits"]


@pytest.mark.integration
@pytest.mark.slow
class TestPerformanceIntegration:
    """Test performance in realistic scenarios"""
    
    def test_large_dataset_serialization(self, tmp_path):
        """Test serialization of large datasets"""
        from openad.helpers.serialization import save_data, load_data
        import time
        
        # Create large dataset
        large_data = {
            f"key_{i}": {
                "value": f"data_{i}",
                "number": i,
                "list": list(range(10))
            }
            for i in range(1000)
        }
        
        file_path = tmp_path / "large_data.msgpack"
        
        # Measure save time
        start = time.time()
        save_data(large_data, file_path, use_msgpack=True)
        save_time = time.time() - start
        
        # Measure load time
        start = time.time()
        loaded = load_data(file_path)
        load_time = time.time() - start
        
        assert loaded == large_data
        assert save_time < 1.0  # Should be fast
        assert load_time < 1.0  # Should be fast
        
        print(f"\nLarge dataset performance:")
        print(f"  Save time: {save_time:.3f}s")
        print(f"  Load time: {load_time:.3f}s")
        print(f"  File size: {file_path.stat().st_size / 1024:.2f} KB")


@pytest.mark.integration
class TestBugFixes:
    """Test that reported bugs are fixed"""
    
    @pytest.mark.skip(reason="Requires full OpenAD environment with PubChem")
    def test_display_mol_no_false_error(self):
        """
        Test fix for bug where 'display mol tritace' showed error
        even though molecule was found.
        
        Bug: SMILES search failed but name search succeeded,
        yet error was shown for SMILES failure.
        
        Fix: Only show error if ALL search methods fail.
        """
        # This would test the actual display mol command
        # For now, we test the logic in smol_functions.py
        pass


@pytest.mark.smoke
class TestSmokeTests:
    """Quick smoke tests to verify basic functionality"""
    
    def test_import_serialization_module(self):
        """Test that serialization module can be imported"""
        from openad.helpers import serialization
        assert hasattr(serialization, 'save_data')
        assert hasattr(serialization, 'load_data')
        assert hasattr(serialization, 'save_json')
        assert hasattr(serialization, 'load_json')
    
    def test_msgpack_available(self):
        """Test that msgpack is installed"""
        try:
            import msgpack
            assert True
        except ImportError:
            pytest.fail("msgpack not installed")
    
    def test_orjson_available(self):
        """Test that orjson is installed"""
        try:
            import orjson
            assert True
        except ImportError:
            pytest.fail("orjson not installed")
    
    def test_basic_serialization_works(self, tmp_path):
        """Quick test that basic serialization works"""
        from openad.helpers.serialization import save_data, load_data
        
        data = {"test": "smoke"}
        file_path = tmp_path / "smoke.msgpack"
        
        save_data(data, file_path)
        loaded = load_data(file_path)
        
        assert loaded == data

# Made with Bob
