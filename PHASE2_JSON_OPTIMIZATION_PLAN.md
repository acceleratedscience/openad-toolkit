# Phase 2: JSON Performance Optimization Plan

**Start Date**: March 12, 2026  
**Status**: In Progress  
**Goal**: Replace standard `json` module with `orjson` for 2-3x performance improvement

---

## 📊 Overview

### Scope
- **Files to Update**: 26 files identified
- **Expected Performance**: 2-3x faster JSON operations
- **Backward Compatibility**: 100% (orjson is drop-in replacement)
- **Risk Level**: Low (well-tested library, no breaking changes)

### Benefits
- 🚀 2-3x faster JSON parsing
- 🚀 2-3x faster JSON serialization
- 💾 More efficient memory usage
- 🔧 Better handling of datetime and UUID types
- ✅ Fully compatible with standard json API

---

## 📋 Files to Update (26 total)

### Priority 1: Core Modules (High Impact)

| File | Usage | Priority | Complexity |
|------|-------|----------|------------|
| openad/toolkit/toolkit_main.py | Config loading | High | Low |
| openad/helpers/files.py | File operations | High | Medium |
| openad/helpers/splash.py | Config | High | Low |
| openad/smols/smol_functions.py | Molecule data | High | Medium |
| openad/smols/smol_commands.py | Command data | High | Medium |
| openad/smols/smol_transformers.py | Data transforms | High | Medium |

### Priority 2: GUI/API Modules (Medium Impact)

| File | Usage | Priority | Complexity |
|------|-------|----------|------------|
| openad/gui/api/file_system_api.py | API responses | Medium | Low |
| openad/gui/api/molecules_api.py | API responses | Medium | Low |
| openad/gui/api/result_api.py | API responses | Medium | Low |
| openad/gui/api/general_api.py | API responses | Medium | Low |
| openad/gui/api/dataframe_api.py | API responses | Medium | Low |
| openad/gui/gui_launcher.py | Config | Medium | Low |

### Priority 3: Plugin/Toolkit Modules (Medium Impact)

| File | Usage | Priority | Complexity |
|------|-------|----------|------------|
| openad/user_toolkits/DS4SD/fn_search/fn_search_collection.py | Search data | Medium | Low |
| openad/user_toolkits/RXN/rxn_include.py | RXN data | Medium | Low |
| openad/openad_model_plugin/openad_model_toolkit.py | Model config | Medium | Low |
| openad/openad_model_plugin/catalog_model_services.py | Catalog data | Medium | Low |
| openad/openad_model_plugin/services.py | Service data | Medium | Low |

### Priority 4: Flask Apps (Low Impact)

| File | Usage | Priority | Complexity |
|------|-------|----------|------------|
| openad/flask_apps/dataviewer/routes.py | Web responses | Low | Low |
| openad/flask_apps/example/routes.py | Web responses | Low | Low |

### Priority 5: Specialized Modules (Low Impact)

| File | Usage | Priority | Complexity |
|------|-------|----------|------------|
| openad/mmols/mmol_commands.py | Molecule commands | Low | Low |
| openad/mmols/mmol_functions.py | Molecule functions | Low | Low |
| openad/plugins/edit_json/edit_json.py | JSON editing | Low | Medium |
| openad/helpers/json_decimal_encoder.py | Decimal encoding | Low | High |
| openad/core/grammar.py | Grammar (commented) | Low | N/A |

---

## 🔧 Implementation Strategy

### Step 1: Update Import Statements

**From**:
```python
import json
```

**To**:
```python
from openad.helpers.serialization import load_json, save_json
import orjson  # For direct json.loads/dumps usage
```

### Step 2: Update Function Calls

#### For File Operations

**From**:
```python
with open('file.json', 'r') as f:
    data = json.load(f)

with open('file.json', 'w') as f:
    json.dump(data, f)
```

**To**:
```python
from openad.helpers.serialization import load_json, save_json

data = load_json('file.json')
save_json(data, 'file.json')
```

#### For String Operations

**From**:
```python
data = json.loads(json_string)
json_string = json.dumps(data)
```

**To**:
```python
import orjson

data = orjson.loads(json_string)
json_string = orjson.dumps(data).decode('utf-8')  # orjson returns bytes
```

### Step 3: Handle Special Cases

#### Decimal Encoding
File: `openad/helpers/json_decimal_encoder.py`

**Current**:
```python
json.dumps(data, cls=DecimalEncoder)
```

**Solution**: orjson handles Decimal natively, no custom encoder needed

#### Pretty Printing
**From**:
```python
json.dumps(data, indent=2)
```

**To**:
```python
orjson.dumps(data, option=orjson.OPT_INDENT_2).decode('utf-8')
```

#### Sorting Keys
**From**:
```python
json.dumps(data, sort_keys=True)
```

**To**:
```python
orjson.dumps(data, option=orjson.OPT_SORT_KEYS).decode('utf-8')
```

---

## 📝 Implementation Checklist

### Week 1: Core Modules (Days 1-5)

- [ ] Day 1: Update toolkit_main.py
- [ ] Day 1: Update helpers/files.py
- [ ] Day 1: Update helpers/splash.py
- [ ] Day 2: Update smols/smol_functions.py
- [ ] Day 2: Update smols/smol_commands.py
- [ ] Day 3: Update smols/smol_transformers.py
- [ ] Day 3: Run tests for core modules
- [ ] Day 4: Fix any issues found
- [ ] Day 5: Code review and documentation

### Week 2: GUI/API & Plugins (Days 6-10)

- [ ] Day 6: Update all GUI API files (5 files)
- [ ] Day 6: Update gui_launcher.py
- [ ] Day 7: Update toolkit search functions (2 files)
- [ ] Day 7: Update model plugin files (3 files)
- [ ] Day 8: Run tests for GUI/API modules
- [ ] Day 9: Update Flask apps (2 files)
- [ ] Day 10: Update specialized modules (4 files)

### Week 3: Testing & Documentation (Days 11-15)

- [ ] Day 11: Create comprehensive JSON performance tests
- [ ] Day 12: Run full test suite
- [ ] Day 13: Performance benchmarking
- [ ] Day 14: Fix any remaining issues
- [ ] Day 15: Final documentation and Phase 2 summary

---

## 🧪 Testing Strategy

### Unit Tests
Create tests for each updated module:
```python
def test_json_operations_with_orjson():
    """Test that orjson works correctly"""
    data = {"key": "value", "number": 123}
    
    # Test save/load
    save_json(data, "test.json")
    loaded = load_json("test.json")
    assert loaded == data
    
    # Test string operations
    json_str = orjson.dumps(data).decode('utf-8')
    parsed = orjson.loads(json_str)
    assert parsed == data
```

### Performance Tests
```python
def test_json_performance_improvement():
    """Verify orjson is faster than standard json"""
    import json
    import orjson
    import time
    
    large_data = [{"key": f"value_{i}"} for i in range(10000)]
    
    # Standard json
    start = time.time()
    json_str = json.dumps(large_data)
    json_time = time.time() - start
    
    # orjson
    start = time.time()
    orjson_str = orjson.dumps(large_data)
    orjson_time = time.time() - start
    
    # Should be at least 2x faster
    assert orjson_time < json_time / 2
```

### Integration Tests
- Test file operations with real data
- Test API responses
- Test molecule data handling
- Test configuration loading

---

## ⚠️ Potential Issues & Solutions

### Issue 1: orjson Returns Bytes
**Problem**: `orjson.dumps()` returns bytes, not str

**Solution**: Always decode when string is needed
```python
json_str = orjson.dumps(data).decode('utf-8')
```

### Issue 2: Custom Encoders
**Problem**: Some code uses custom JSON encoders (e.g., DecimalEncoder)

**Solution**: orjson handles most types natively. For special cases:
```python
# orjson handles Decimal, datetime, UUID natively
# No custom encoder needed
```

### Issue 3: File Mode
**Problem**: orjson works with bytes

**Solution**: Use binary mode for files
```python
# Read
with open('file.json', 'rb') as f:
    data = orjson.loads(f.read())

# Write
with open('file.json', 'wb') as f:
    f.write(orjson.dumps(data))
```

### Issue 4: Pretty Printing
**Problem**: Different API for formatting

**Solution**: Use orjson options
```python
orjson.dumps(data, option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS)
```

---

## 📊 Expected Performance Improvements

### Serialization (dumps)
| Data Size | json | orjson | Improvement |
|-----------|------|--------|-------------|
| Small (1KB) | 0.1ms | 0.04ms | 2.5x faster |
| Medium (100KB) | 10ms | 3.5ms | 2.8x faster |
| Large (10MB) | 1000ms | 350ms | 2.8x faster |

### Deserialization (loads)
| Data Size | json | orjson | Improvement |
|-----------|------|--------|-------------|
| Small (1KB) | 0.08ms | 0.03ms | 2.6x faster |
| Medium (100KB) | 8ms | 2.8ms | 2.8x faster |
| Large (10MB) | 800ms | 280ms | 2.8x faster |

### Real-World Impact
- **API Response Times**: 40-60% faster
- **File Loading**: 2-3x faster
- **Data Processing**: 2-3x faster
- **Memory Usage**: 20-30% less

---

## 🎯 Success Criteria

### Performance
- [ ] JSON operations 2-3x faster (verified by benchmarks)
- [ ] No performance regressions in other areas
- [ ] Memory usage improved or unchanged

### Compatibility
- [ ] All existing tests pass
- [ ] No breaking changes to API
- [ ] Backward compatible with existing JSON files

### Quality
- [ ] Code review completed
- [ ] Documentation updated
- [ ] New tests added for JSON operations
- [ ] Performance benchmarks documented

---

## 📚 Resources

### Documentation
- orjson: https://github.com/ijl/orjson
- Performance benchmarks: https://github.com/ijl/orjson#performance
- API reference: https://github.com/ijl/orjson#api

### Related Files
- `openad/helpers/serialization.py` - JSON helper functions
- `tests/test_serialization.py` - Existing tests
- `LIBRARY_OPTIMIZATION_RECOMMENDATIONS.md` - Original analysis

---

## 🔄 Rollback Plan

If issues arise:

1. **Immediate Rollback**: Revert commits
2. **Partial Rollback**: Keep working modules, revert problematic ones
3. **Gradual Rollout**: Update modules one at a time with testing

All changes will be in separate commits for easy rollback.

---

**Document Version**: 1.0  
**Last Updated**: March 12, 2026  
**Status**: Ready to Begin Implementation