#!/bin/bash
# Version Verification Script for OpenAD Toolkit
# Checks that all version numbers are consistent across the codebase

set -e

echo "================================================"
echo "OpenAD Toolkit - Version Verification"
echo "================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Extract versions from different files
echo "Extracting versions from files..."
echo ""

# 1. pyproject.toml
if [ -f "pyproject.toml" ]; then
    PYPROJECT_VERSION=$(grep "^version" pyproject.toml | cut -d'"' -f2)
    echo "  pyproject.toml:           ${PYPROJECT_VERSION}"
else
    echo -e "  ${RED}✗ pyproject.toml not found${NC}"
    exit 1
fi

# 2. openad/app/metadata.json
if [ -f "openad/app/metadata.json" ]; then
    METADATA_VERSION=$(grep '"version"' openad/app/metadata.json | cut -d'"' -f4)
    echo "  openad/app/metadata.json: ${METADATA_VERSION}"
else
    echo -e "  ${RED}✗ openad/app/metadata.json not found${NC}"
    exit 1
fi

# 3. openad/__init__.py
if [ -f "openad/__init__.py" ]; then
    if grep -q "^__version__" openad/__init__.py; then
        INIT_VERSION=$(grep "^__version__" openad/__init__.py | cut -d'"' -f2)
        echo "  openad/__init__.py:       ${INIT_VERSION}"
    else
        echo -e "  ${YELLOW}⚠ __version__ not found in openad/__init__.py${NC}"
        INIT_VERSION=""
    fi
else
    echo -e "  ${RED}✗ openad/__init__.py not found${NC}"
    exit 1
fi

echo ""
echo "================================================"
echo ""

# Check consistency
ALL_MATCH=true

if [ -n "$INIT_VERSION" ]; then
    # All three versions should match
    if [ "$PYPROJECT_VERSION" = "$METADATA_VERSION" ] && [ "$PYPROJECT_VERSION" = "$INIT_VERSION" ]; then
        echo -e "${GREEN}✓ All versions match: ${PYPROJECT_VERSION}${NC}"
        echo ""
        echo "Version consistency check: PASSED"
    else
        echo -e "${RED}✗ Version mismatch detected!${NC}"
        echo ""
        echo "Expected all versions to be: ${PYPROJECT_VERSION}"
        [ "$METADATA_VERSION" != "$PYPROJECT_VERSION" ] && echo -e "  ${RED}✗ metadata.json has: ${METADATA_VERSION}${NC}"
        [ "$INIT_VERSION" != "$PYPROJECT_VERSION" ] && echo -e "  ${RED}✗ __init__.py has: ${INIT_VERSION}${NC}"
        ALL_MATCH=false
    fi
else
    # Only check pyproject.toml and metadata.json
    if [ "$PYPROJECT_VERSION" = "$METADATA_VERSION" ]; then
        echo -e "${GREEN}✓ pyproject.toml and metadata.json match: ${PYPROJECT_VERSION}${NC}"
        echo -e "${YELLOW}⚠ Consider adding __version__ to openad/__init__.py${NC}"
        echo ""
        echo "Version consistency check: PASSED (with warning)"
    else
        echo -e "${RED}✗ Version mismatch detected!${NC}"
        echo ""
        echo "Expected: ${PYPROJECT_VERSION}"
        echo -e "  ${RED}✗ metadata.json has: ${METADATA_VERSION}${NC}"
        ALL_MATCH=false
    fi
fi

echo ""
echo "================================================"

# Exit with appropriate code
if [ "$ALL_MATCH" = true ]; then
    exit 0
else
    echo ""
    echo "Please update all version numbers to match."
    echo "Run the following commands to fix:"
    echo ""
    echo "  # Update metadata.json"
    echo "  sed -i '' 's/\"version\": \".*\"/\"version\": \"${PYPROJECT_VERSION}\"/' openad/app/metadata.json"
    echo ""
    echo "  # Update __init__.py"
    echo "  sed -i '' 's/__version__ = \".*\"/__version__ = \"${PYPROJECT_VERSION}\"/' openad/__init__.py"
    echo ""
    exit 1
fi

# Made with Bob
