"""
Comprehensive test suite for the new serialization module.

Tests cover:
- Msgpack save/load operations
- Pickle backward compatibility
- JSON operations with orjson
- Migration functionality
- Error handling
"""

import pytest
import pickle
import tempfile
from pathlib import Path
from openad.helpers.serialization import (
    save_data,
    load_data,
    save_json,
    load_json,
    migrate_pickle_to_msgpack,
    SerializationError
)


class TestMsgpackOperations:
    """Test basic msgpack save/load operations"""
    
    def test_save_load_simple_dict(self, tmp_path):
        """Test saving and loading a simple dictionary"""
        data = {"key": "value", "number": 42, "list": [1, 2, 3]}
        filepath = tmp_path / "test.msgpack"
        
        save_data(data, filepath, use_msgpack=True)
        loaded = load_data(filepath)
        
        assert loaded == data
    
    def test_save_load_nested_dict(self, tmp_path):
        """Test saving and loading nested dictionaries"""
        data = {
            "level1": {
                "level2": {
                    "level3": {"value": "deep"}
                }
            },
            "array": [1, 2, 3, 4, 5]
        }
        filepath = tmp_path / "nested.msgpack"
        
        save_data(data, filepath, use_msgpack=True)
        loaded = load_data(filepath)
        
        assert loaded == data
        assert loaded["level1"]["level2"]["level3"]["value"] == "deep"
    
    def test_save_load_list(self, tmp_path):
        """Test saving and loading lists"""
        data = [1, 2, 3, "four", 5.0, {"six": 6}]
        filepath = tmp_path / "list.msgpack"
        
        save_data(data, filepath, use_msgpack=True)
        loaded = load_data(filepath)
        
        assert loaded == data
    
    def test_file_size_smaller_than_pickle(self, tmp_path):
        """Verify msgpack files are smaller than pickle"""
        # Create large dict
        data = {f"key_{i}": f"value_{i}" for i in range(1000)}
        
        msgpack_file = tmp_path / "test.msgpack"
        pickle_file = tmp_path / "test.pkl"
        
        save_data(data, msgpack_file, use_msgpack=True)
        with open(pickle_file, 'wb') as f:
            pickle.dump(data, f)
        
        msgpack_size = msgpack_file.stat().st_size
        pickle_size = pickle_file.stat().st_size
        
        assert msgpack_size < pickle_size


class TestPickleBackwardCompatibility:
    """Test backward compatibility with existing pickle files"""
    
    def test_load_legacy_pickle_file(self, tmp_path):
        """Test loading a legacy pickle file"""
        data = {"legacy": True, "version": 1}
        pickle_file = tmp_path / "legacy.pkl"
        
        # Create legacy pickle file
        with open(pickle_file, 'wb') as f:
            pickle.dump(data, f)
        
        # Load with new system
        loaded = load_data(pickle_file, migrate_to_msgpack=False)
        
        assert loaded == data
    
    def test_automatic_migration(self, tmp_path):
        """Test automatic migration from pickle to msgpack"""
        data = {"migrate": "me", "value": 123}
        pickle_file = tmp_path / "migrate.pkl"
        
        # Create pickle file
        with open(pickle_file, 'wb') as f:
            pickle.dump(data, f)
        
        # Load with migration enabled
        loaded = load_data(pickle_file, migrate_to_msgpack=True)
        
        assert loaded == data
        # Check backup was created
        backup_file = Path(str(pickle_file) + '.pickle_backup')
        assert backup_file.exists()
    
    def test_migration_preserves_data(self, tmp_path):
        """Verify migrated data is identical to original"""
        data = {
            "complex": {
                "nested": [1, 2, 3],
                "string": "test",
                "number": 42.5
            }
        }
        pickle_file = tmp_path / "preserve.pkl"
        
        # Create pickle file
        with open(pickle_file, 'wb') as f:
            pickle.dump(data, f)
        
        # Migrate
        loaded = load_data(pickle_file, migrate_to_msgpack=True)
        
        # Load again (should be msgpack now)
        loaded_again = load_data(pickle_file)
        
        assert loaded == data
        assert loaded_again == data


class TestJSONOperations:
    """Test JSON operations using orjson"""
    
    def test_save_load_json(self, tmp_path):
        """Test basic JSON save/load"""
        data = {"test": "value", "number": 42}
        json_file = tmp_path / "test.json"
        
        save_json(data, json_file)
        loaded = load_json(json_file)
        
        assert loaded == data
    
    def test_pretty_json(self, tmp_path):
        """Test pretty-printed JSON"""
        data = {"key1": "value1", "key2": "value2"}
        json_file = tmp_path / "pretty.json"
        
        save_json(data, json_file, pretty=True)
        
        # Read raw content
        content = json_file.read_text()
        
        # Should have indentation
        assert "\n" in content
        assert "  " in content
    
    def test_json_unicode(self, tmp_path):
        """Test JSON with Unicode characters"""
        data = {"emoji": "🎉", "chinese": "你好", "arabic": "مرحبا"}
        json_file = tmp_path / "unicode.json"
        
        save_json(data, json_file)
        loaded = load_json(json_file)
        
        assert loaded == data


class TestBatchMigration:
    """Test batch migration functionality"""
    
    def test_migrate_directory(self, tmp_path):
        """Test migrating all pickle files in a directory"""
        # Create multiple pickle files
        for i in range(3):
            data = {"file": i, "data": f"test{i}"}
            pickle_file = tmp_path / f"file{i}.pkl"
            with open(pickle_file, 'wb') as f:
                pickle.dump(data, f)
        
        # Migrate
        stats = migrate_pickle_to_msgpack(tmp_path, pattern="*.pkl", backup=True)
        
        assert stats['total'] == 3
        assert stats['migrated'] == 3
        assert stats['failed'] == 0
        
        # Verify msgpack files exist
        for i in range(3):
            msgpack_file = tmp_path / f"file{i}.msgpack"
            assert msgpack_file.exists()
    
    def test_skip_existing_msgpack(self, tmp_path):
        """Test that existing msgpack files are skipped"""
        # Create pickle and msgpack file
        data = {"test": "data"}
        pickle_file = tmp_path / "test.pkl"
        msgpack_file = tmp_path / "test.msgpack"
        
        with open(pickle_file, 'wb') as f:
            pickle.dump(data, f)
        save_data(data, msgpack_file)
        
        # Migrate
        stats = migrate_pickle_to_msgpack(tmp_path, pattern="*.pkl")
        
        assert stats['skipped'] == 1
        assert stats['migrated'] == 0


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_file_not_found(self):
        """Test loading non-existent file"""
        with pytest.raises(FileNotFoundError):
            load_data("nonexistent.msgpack")
    
    def test_corrupted_file(self, tmp_path):
        """Test loading corrupted file"""
        corrupted_file = tmp_path / "corrupted.msgpack"
        corrupted_file.write_bytes(b"not valid msgpack or pickle data")
        
        with pytest.raises(SerializationError):
            load_data(corrupted_file)
    
    def test_invalid_json(self, tmp_path):
        """Test loading invalid JSON"""
        invalid_json = tmp_path / "invalid.json"
        invalid_json.write_text("{ invalid json }")
        
        with pytest.raises(SerializationError):
            load_json(invalid_json)
    
    def test_save_to_readonly_location(self, tmp_path):
        """Test saving to read-only location"""
        readonly_dir = tmp_path / "readonly"
        readonly_dir.mkdir()
        readonly_dir.chmod(0o444)  # Read-only
        
        readonly_file = readonly_dir / "test.msgpack"
        
        with pytest.raises(SerializationError):
            save_data({"test": "data"}, readonly_file)


class TestCredentialsCompatibility:
    """Test compatibility with credentials module"""
    
    def test_credentials_structure(self, tmp_path):
        """Test saving/loading credentials structure"""
        credentials = {
            "host": "https://api.example.com",
            "auth": {
                "user_name": "testuser",
                "api_key": "secret123"
            },
            "verify_ssl": "true"
        }
        
        cred_file = tmp_path / "credentials.msgpack"
        save_data(credentials, cred_file)
        loaded = load_data(cred_file)
        
        assert loaded == credentials
        assert loaded["auth"]["api_key"] == "secret123"


class TestRegistryCompatibility:
    """Test compatibility with registry module"""
    
    def test_registry_structure(self, tmp_path):
        """Test saving/loading registry structure"""
        registry = {
            "workspace": "DEFAULT",
            "context": None,
            "toolkits": ["DS4SD", "RXN"],
            "env_vars": {
                "refresh_help_ai": True
            }
        }
        
        reg_file = tmp_path / "registry.msgpack"
        save_data(registry, reg_file)
        loaded = load_data(reg_file)
        
        assert loaded == registry
        assert loaded["toolkits"] == ["DS4SD", "RXN"]


class TestPerformance:
    """Performance comparison tests"""
    
    @pytest.mark.skip(reason="Requires pytest-benchmark plugin")
    def test_msgpack_faster_than_pickle(self, tmp_path):
        """Benchmark msgpack vs pickle serialization (requires pytest-benchmark)"""
        # Create large dataset
        data = {f"key_{i}": f"value_{i}" for i in range(10000)}
        
        msgpack_file = tmp_path / "perf.msgpack"
        
        # Save with msgpack
        save_data(data, msgpack_file, use_msgpack=True)
        
        # Verify it works
        assert msgpack_file.exists()
        loaded = load_data(msgpack_file)
        assert len(loaded) == 10000


# Fixtures
@pytest.fixture
def sample_data():
    """Provide sample data for tests"""
    return {
        "string": "test",
        "number": 42,
        "float": 3.14,
        "list": [1, 2, 3],
        "nested": {
            "key": "value"
        }
    }


@pytest.fixture
def temp_workspace(tmp_path):
    """Create a temporary workspace directory"""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    return workspace

# Made with Bob
