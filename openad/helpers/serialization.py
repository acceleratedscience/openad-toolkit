"""
Serialization helper module with backward compatibility.

This module provides safe serialization/deserialization functions that:
1. Use msgpack for new data (faster, safer than pickle)
2. Automatically detect and load legacy pickle files
3. Provide migration path from pickle to msgpack
4. Use orjson for JSON operations (2-3x faster than standard json)

Usage:
    from openad.helpers.serialization import save_data, load_data, save_json, load_json
    
    # Save/load binary data (msgpack with pickle fallback)
    save_data(data, 'file.msgpack')
    data = load_data('file.msgpack')
    
    # Save/load JSON data (orjson)
    save_json(data, 'file.json')
    data = load_json('file.json')
"""

import pickle
import msgpack
import orjson
from pathlib import Path
from typing import Any, Union


class SerializationError(Exception):
    """Raised when serialization/deserialization fails"""
    pass


def save_data(data: Any, filepath: Union[str, Path], use_msgpack: bool = True) -> None:
    """
    Save data to file using msgpack (default) or pickle.
    
    Args:
        data: Data to serialize
        filepath: Path to save file
        use_msgpack: If True, use msgpack; if False, use pickle (for compatibility)
    
    Raises:
        SerializationError: If serialization fails
    """
    filepath = Path(filepath)
    
    try:
        if use_msgpack:
            # Use msgpack for new data
            with open(filepath, 'wb') as f:
                packed = msgpack.packb(data, use_bin_type=True)
                f.write(packed)
        else:
            # Fallback to pickle if needed (e.g., for complex objects)
            with open(filepath, 'wb') as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        raise SerializationError(f"Failed to save data to {filepath}: {e}") from e


def load_data(filepath: Union[str, Path], migrate_to_msgpack: bool = True) -> Any:
    """
    Load data from file, automatically detecting pickle or msgpack format.
    
    This function provides backward compatibility by:
    1. Attempting to load as msgpack first (new format)
    2. Falling back to pickle if msgpack fails (legacy format)
    3. Optionally migrating pickle files to msgpack
    
    Args:
        filepath: Path to load file
        migrate_to_msgpack: If True, automatically migrate pickle files to msgpack
    
    Returns:
        Deserialized data
    
    Raises:
        SerializationError: If deserialization fails
        FileNotFoundError: If file doesn't exist
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    try:
        # Try msgpack first (new format)
        with open(filepath, 'rb') as f:
            data = msgpack.unpackb(f.read(), raw=False)
        return data
    except (msgpack.exceptions.ExtraData, 
            msgpack.exceptions.UnpackException,
            UnicodeDecodeError):
        # Not msgpack format, try pickle (legacy format)
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            
            # Optionally migrate to msgpack
            if migrate_to_msgpack:
                try:
                    # Create backup of original pickle file
                    backup_path = filepath.with_suffix(filepath.suffix + '.pickle_backup')
                    if not backup_path.exists():
                        filepath.rename(backup_path)
                        # Save as msgpack
                        save_data(data, filepath, use_msgpack=True)
                        print(f"Migrated {filepath} from pickle to msgpack (backup: {backup_path})")
                except Exception as e:
                    # If migration fails, restore original and continue
                    print(f"Warning: Could not migrate {filepath} to msgpack: {e}")
                    if backup_path.exists():
                        backup_path.rename(filepath)
            
            return data
        except Exception as e:
            raise SerializationError(
                f"Failed to load data from {filepath}. "
                f"File may be corrupted or in unsupported format: {e}"
            ) from e


def save_json(data: Any, filepath: Union[str, Path], pretty: bool = False) -> None:
    """
    Save data to JSON file using orjson (2-3x faster than standard json).
    
    Args:
        data: Data to serialize (must be JSON-serializable)
        filepath: Path to save file
        pretty: If True, format with indentation
    
    Raises:
        SerializationError: If serialization fails
    """
    filepath = Path(filepath)
    
    try:
        if pretty:
            json_bytes = orjson.dumps(
                data,
                option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS
            )
        else:
            json_bytes = orjson.dumps(data)
        
        with open(filepath, 'wb') as f:
            f.write(json_bytes)
    except Exception as e:
        raise SerializationError(f"Failed to save JSON to {filepath}: {e}") from e


def load_json(filepath: Union[str, Path]) -> Any:
    """
    Load data from JSON file using orjson (2-3x faster than standard json).
    
    Args:
        filepath: Path to load file
    
    Returns:
        Deserialized data
    
    Raises:
        SerializationError: If deserialization fails
        FileNotFoundError: If file doesn't exist
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    try:
        with open(filepath, 'rb') as f:
            return orjson.loads(f.read())
    except Exception as e:
        raise SerializationError(f"Failed to load JSON from {filepath}: {e}") from e


def migrate_pickle_to_msgpack(directory: Union[str, Path], 
                              pattern: str = "*.pkl",
                              backup: bool = True) -> dict:
    """
    Batch migrate pickle files to msgpack in a directory.
    
    Args:
        directory: Directory containing pickle files
        pattern: Glob pattern for pickle files (default: "*.pkl")
        backup: If True, keep backup of original pickle files
    
    Returns:
        Dictionary with migration statistics:
        {
            'total': int,
            'migrated': int,
            'failed': int,
            'skipped': int,
            'errors': list
        }
    """
    directory = Path(directory)
    stats = {
        'total': 0,
        'migrated': 0,
        'failed': 0,
        'skipped': 0,
        'errors': []
    }
    
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    for pickle_file in directory.glob(pattern):
        stats['total'] += 1
        
        try:
            # Load pickle data
            with open(pickle_file, 'rb') as f:
                data = pickle.load(f)
            
            # Determine new filename
            msgpack_file = pickle_file.with_suffix('.msgpack')
            
            # Skip if msgpack version already exists
            if msgpack_file.exists():
                stats['skipped'] += 1
                continue
            
            # Save as msgpack
            save_data(data, msgpack_file, use_msgpack=True)
            
            # Backup or remove original
            if backup:
                backup_file = pickle_file.with_suffix('.pkl.backup')
                pickle_file.rename(backup_file)
            else:
                pickle_file.unlink()
            
            stats['migrated'] += 1
            print(f"Migrated: {pickle_file} -> {msgpack_file}")
            
        except Exception as e:
            stats['failed'] += 1
            error_msg = f"Failed to migrate {pickle_file}: {e}"
            stats['errors'].append(error_msg)
            print(f"Error: {error_msg}")
    
    return stats


# Convenience aliases for backward compatibility
dump = save_data
load = load_data
dumps_json = lambda data, pretty=False: orjson.dumps(
    data, 
    option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS if pretty else 0
)
loads_json = orjson.loads

# Made with Bob
