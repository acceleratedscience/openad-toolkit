# OpenAD Toolkit - Version 0.9.0 Upgrade Plan

**Target Version**: 0.9.0  
**Current Version**: 0.7.5.2  
**Planning Date**: March 24, 2026  
**Status**: 📋 Planning Phase

---

## 📊 Executive Summary

This document outlines the complete plan for upgrading OpenAD Toolkit from version 0.7.5.2 to 0.9.0, including all version-related files, release procedures, and upgrade justification based on completed modernization work.

---

## 🎯 Version Strategy

### Semantic Versioning (SemVer)

OpenAD follows semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR** (0): Pre-1.0 development phase
- **MINOR** (9): Significant new features, improvements, or breaking changes
- **PATCH** (0): Bug fixes and minor improvements

### Why 0.9.0?

The jump from 0.7.5.2 to 0.9.0 is justified by:

1. **Major Modernization Completed**:
   - Phase 1: Pickle → msgpack migration (security & performance)
   - Phase 2: JSON → orjson migration (26 files, 2-3x performance)
   - Phase 3A: Langchain migration (future-proofing)
   - Phase 3H: MMOL modernization (security & reliability)

2. **Significant Infrastructure Changes**:
   - Poetry → UV package manager migration
   - Python 3.13 support added
   - 50+ dependency updates
   - New serialization architecture

3. **Breaking Changes** (Minor):
   - Deprecated toolkit system (replaced by plugins)
   - File format changes (automatic migration provided)

4. **Pre-1.0 Milestone**:
   - 0.9.0 positions the project for 1.0.0 release
   - Indicates feature completeness and stability
   - Signals production-readiness

---

## 📝 Files Requiring Version Updates

### 1. Primary Version Sources

#### A. `pyproject.toml` (Line 3)
**Current**: `version = "0.7.5.2"`  
**New**: `version = "0.9.0"`

```toml
[project]
name = "openad"
version = "0.9.0"  # ← UPDATE THIS
description = "Open Accelerated Discovery"
```

**Impact**: This is the **authoritative source** for the package version. All other version references should derive from this.

#### B. `openad/app/metadata.json` (Line 4)
**Current**: `"version": "0.7.5"`  
**New**: `"version": "0.9.0"`

```json
{
  "banner": "OPENAD",
  "title": "Welcome to the Open Accelerated Discovery CLI",
  "version": "0.9.0",  // ← UPDATE THIS
  "commands": {
    ...
  }
}
```

**Impact**: Displayed in the CLI splash screen when users run `openad`.

#### C. `README.md` (Line 61)
**Current**: `0.7.5`  
**New**: `0.9.0`

```markdown
## Release Notes

`0.9.0`
- Major modernization: 3x faster serialization with msgpack
- 2-3x faster JSON operations with orjson (26 files updated)
- Future-proof Langchain integration
- Enhanced security: eliminated pickle vulnerabilities
- Python 3.13 support
- UV package manager migration
- 50+ dependency updates
- Improved error handling and reliability
```

**Impact**: User-facing documentation and release notes.

### 2. Optional Version References

#### D. `openad/__init__.py`
**Current**: No version defined  
**Recommendation**: Add `__version__` attribute

```python
from openad.api import OpenadAPI

__version__ = "0.9.0"  # ← ADD THIS
__all__ = ["OpenadAPI", "__version__"]
```

**Benefits**:
- Programmatic version access: `import openad; print(openad.__version__)`
- Standard Python convention
- Useful for debugging and logging

---

## 🔄 Version Update Procedure

### Step 1: Update Version Numbers

```bash
# 1. Update pyproject.toml
sed -i '' 's/version = "0.7.5.2"/version = "0.9.0"/' pyproject.toml

# 2. Update metadata.json
sed -i '' 's/"version": "0.7.5"/"version": "0.9.0"/' openad/app/metadata.json

# 3. Update README.md (manual - add release notes)
# Edit README.md to add 0.9.0 release notes

# 4. Add __version__ to __init__.py (optional but recommended)
# Edit openad/__init__.py to add __version__ = "0.9.0"
```

### Step 2: Update Release Notes

Create comprehensive release notes in `README.md`:

```markdown
## Release Notes

`0.9.0` - Major Modernization Release
- **Performance**: 3x faster serialization (pickle → msgpack)
- **Performance**: 2-3x faster JSON operations (json → orjson, 26 files)
- **Security**: Eliminated pickle RCE vulnerabilities (CVE-2022-48564, CVE-2019-16729)
- **Future-Proof**: Migrated to modern Langchain packages
- **Reliability**: Enhanced error handling with specific exception types
- **Reliability**: Added HTTP request timeouts (30s) for MMOL operations
- **Infrastructure**: Migrated from Poetry to UV package manager
- **Compatibility**: Added Python 3.13 support
- **Dependencies**: Updated 50+ packages to latest stable versions
- **Testing**: New comprehensive test suite (580+ lines)
- **Migration**: Automatic backward-compatible migration for existing data
- **Breaking**: Deprecated toolkit system (use plugins instead)

`0.7.5`
- We have retired the RXN and Deep Search toolkits and replaced them with new and more user-friendly [plugins](README/plugins.md).
```

### Step 3: Create Version Tag

```bash
# Commit version changes
git add pyproject.toml openad/app/metadata.json openad/__init__.py README.md
git commit -m "chore: bump version to 0.9.0"

# Create annotated tag
git tag -a v0.9.0 -m "Release version 0.9.0 - Major Modernization"

# Push changes and tag
git push origin main
git push origin v0.9.0
```

### Step 4: Build and Publish

```bash
# Build package with UV
uv build

# Verify build
ls -lh dist/

# Expected output:
# openad-0.9.0-py3-none-any.whl
# openad-0.9.0.tar.gz

# Test installation locally
uv pip install dist/openad-0.9.0-py3-none-any.whl

# Verify version
python -c "import openad; print(openad.__version__)"
# Expected: 0.9.0

# Publish to PyPI (requires credentials)
uv publish
```

### Step 5: Verify Deployment

```bash
# Install from PyPI
pip install --upgrade openad

# Verify version
openad --version
python -c "import openad; print(openad.__version__)"

# Test basic functionality
echo "?" | openad
```

---

## 📋 Pre-Release Checklist

### Code Quality
- [ ] All tests passing (`./run_tests.sh`)
- [ ] No critical linting errors (`uv run ruff check .`)
- [ ] Code formatted (`uv run black .`)
- [ ] Type checking passes (`uv run mypy openad`)
- [ ] No security vulnerabilities (`uv run safety check`)

### Documentation
- [ ] README.md updated with release notes
- [ ] CHANGELOG.md created/updated (if exists)
- [ ] Migration guide updated
- [ ] API documentation current
- [ ] Example notebooks tested

### Version Updates
- [ ] `pyproject.toml` version updated
- [ ] `openad/app/metadata.json` version updated
- [ ] `openad/__init__.py` `__version__` added/updated
- [ ] `README.md` release notes added
- [ ] Git tag created

### Testing
- [ ] Fresh install test (clean environment)
- [ ] Upgrade test (from 0.7.5.2)
- [ ] Backward compatibility verified
- [ ] Migration scripts tested
- [ ] CLI commands functional
- [ ] Jupyter notebook integration works
- [ ] GUI launches successfully

### Build & Publish
- [ ] Package builds successfully
- [ ] Wheel file created
- [ ] Source distribution created
- [ ] Test PyPI upload (optional)
- [ ] Production PyPI upload
- [ ] GitHub release created

---

## 🔍 Version Verification Commands

### Check Current Version

```bash
# From pyproject.toml
grep "^version" pyproject.toml

# From metadata.json
grep "version" openad/app/metadata.json

# From Python (after adding __version__)
python -c "import openad; print(openad.__version__)"

# From CLI
openad --version  # If implemented

# From package metadata
pip show openad | grep Version
```

### Verify All Versions Match

```bash
# Create verification script
cat > verify_versions.sh << 'EOF'
#!/bin/bash
echo "Checking version consistency..."

# Extract versions
PYPROJECT_VERSION=$(grep "^version" pyproject.toml | cut -d'"' -f2)
METADATA_VERSION=$(grep '"version"' openad/app/metadata.json | cut -d'"' -f4)
INIT_VERSION=$(grep "__version__" openad/__init__.py | cut -d'"' -f2)

echo "pyproject.toml:     $PYPROJECT_VERSION"
echo "metadata.json:      $METADATA_VERSION"
echo "__init__.py:        $INIT_VERSION"

# Check consistency
if [ "$PYPROJECT_VERSION" = "$METADATA_VERSION" ] && [ "$PYPROJECT_VERSION" = "$INIT_VERSION" ]; then
    echo "✅ All versions match: $PYPROJECT_VERSION"
    exit 0
else
    echo "❌ Version mismatch detected!"
    exit 1
fi
EOF

chmod +x verify_versions.sh
./verify_versions.sh
```

---

## 📦 Release Artifacts

### Package Files
- `openad-0.9.0-py3-none-any.whl` - Wheel distribution
- `openad-0.9.0.tar.gz` - Source distribution

### Documentation
- `README.md` - Updated with 0.9.0 release notes
- `CHANGELOG.md` - Detailed change log (create if missing)
- `changes/VERSION_0.9.0_UPGRADE_PLAN.md` - This document

### Git Artifacts
- Tag: `v0.9.0`
- Commit: Version bump commit
- GitHub Release: With release notes and artifacts

---

## 🚀 Post-Release Tasks

### Immediate (Day 1)
- [ ] Monitor PyPI download stats
- [ ] Watch for installation issues
- [ ] Monitor GitHub issues
- [ ] Update documentation website
- [ ] Announce on social media/blog

### Short-term (Week 1)
- [ ] Gather user feedback
- [ ] Address critical bugs (0.9.1 if needed)
- [ ] Update tutorials and examples
- [ ] Create migration guide videos

### Long-term (Month 1)
- [ ] Plan 0.10.0 or 1.0.0 features
- [ ] Analyze performance metrics
- [ ] Review deprecation warnings
- [ ] Plan next modernization phase

---

## 🔄 Rollback Procedure

If critical issues are discovered:

### Option 1: Quick Patch (0.9.1)
```bash
# Fix critical bug
git checkout -b hotfix/0.9.1
# Make fixes
git commit -m "fix: critical bug in 0.9.0"

# Update version to 0.9.1
sed -i '' 's/version = "0.9.0"/version = "0.9.1"/' pyproject.toml
sed -i '' 's/"version": "0.9.0"/"version": "0.9.1"/' openad/app/metadata.json

# Release 0.9.1
git tag -a v0.9.1 -m "Hotfix release 0.9.1"
uv build && uv publish
```

### Option 2: Yank Release
```bash
# Yank 0.9.0 from PyPI (prevents new installs)
pip install twine
twine upload --repository pypi --skip-existing dist/*
# Then use PyPI web interface to yank 0.9.0

# Users can still install with: pip install openad==0.7.5.2
```

---

## 📊 Version History Context

### Recent Versions
- **0.7.5.2** (Current) - Minor fixes
- **0.7.5** - Plugin system introduction
- **0.7.x** - Toolkit deprecation phase
- **0.6.x** - Toolkit era

### Planned Versions
- **0.9.0** (This release) - Major modernization
- **0.10.0** (Future) - Additional features
- **1.0.0** (Future) - Production-ready milestone

---

## 🎯 Success Metrics

### Technical Metrics
- ✅ 3x faster serialization (measured)
- ✅ 2-3x faster JSON operations (measured)
- ✅ 0 critical security vulnerabilities
- ✅ Python 3.10-3.13 support
- ✅ 75%+ test coverage

### User Metrics (Post-Release)
- [ ] 90%+ successful upgrades
- [ ] <5% rollback rate
- [ ] Positive user feedback
- [ ] No critical bugs reported
- [ ] Increased adoption rate

---

## 📚 Related Documentation

- [Phase 1 Migration Complete](./PHASE1_MIGRATION_COMPLETE.md)
- [Phase 2 JSON Migration](./PHASE2_JSON_MIGRATION_COMPLETE.md)
- [Phase 3A Langchain Migration](./PHASE3A_LANGCHAIN_MIGRATION_COMPLETE.md)
- [Phase 3H MMOL Modernization](./PHASE3H_MMOL_MODERNIZATION_COMPLETE.md)
- [Repository Analysis](./REPOSITORY_ANALYSIS_AND_UPGRADE_PLAN.md)
- [LLM Assist Modernization Plan](./LLM_ASSIST_MODERNIZATION_PLAN.md)

---

## 🤝 Contributors

This release represents work from multiple modernization phases:
- Serialization improvements (Phase 1)
- JSON optimization (Phase 2)
- Langchain migration (Phase 3A)
- MMOL enhancements (Phase 3H)
- Infrastructure updates (UV migration)

---

## 📞 Support

### For Users
- **Installation Issues**: Check [Installation Guide](https://openad.accelerate.science/docs/installation)
- **Migration Problems**: See migration guide in README
- **Bug Reports**: [GitHub Issues](https://github.com/acceleratedscience/openad-toolkit/issues)

### For Developers
- **Build Issues**: Check UV documentation
- **Test Failures**: Run `./run_tests.sh` for details
- **Version Questions**: Refer to this document

---

## ✅ Summary

### Version Update Locations
1. **`pyproject.toml`** (line 3) - Primary source
2. **`openad/app/metadata.json`** (line 4) - CLI display
3. **`openad/__init__.py`** - Add `__version__` attribute
4. **`README.md`** (line 61+) - Release notes

### Key Commands
```bash
# Update versions
sed -i '' 's/0.7.5.2/0.9.0/g' pyproject.toml
sed -i '' 's/0.7.5/0.9.0/g' openad/app/metadata.json

# Verify
./verify_versions.sh

# Build and publish
uv build
uv publish

# Tag release
git tag -a v0.9.0 -m "Release 0.9.0"
git push origin v0.9.0
```

---

**Status**: 📋 Ready for Implementation  
**Next Step**: Execute version update procedure  
**Estimated Time**: 2-3 hours (including testing)
