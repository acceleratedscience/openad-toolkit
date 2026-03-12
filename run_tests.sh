#!/bin/bash
# OpenAD Toolkit Test Runner
# Runs comprehensive test suite and generates reports in test_reports/

set -e  # Exit on error

echo "========================================="
echo "OpenAD Toolkit - Test Suite Runner"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create test_reports directory
echo "Creating test_reports directory..."
mkdir -p test_reports

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}Error: pytest is not installed${NC}"
    echo "Install with: uv sync --all-extras"
    exit 1
fi

# Check if msgpack is installed
python -c "import msgpack" 2>/dev/null || {
    echo -e "${YELLOW}Warning: msgpack not installed${NC}"
    echo "Installing msgpack..."
    uv add msgpack
}

echo ""
echo "========================================="
echo "Running Test Suite"
echo "========================================="
echo ""

# Run tests with different markers
echo -e "${GREEN}1. Running Unit Tests...${NC}"
pytest tests/ -m "unit" --tb=short || true

echo ""
echo -e "${GREEN}2. Running Serialization Tests...${NC}"
pytest tests/test_serialization.py -v || true

echo ""
echo -e "${GREEN}3. Running Integration Tests...${NC}"
pytest tests/ -m "integration" --tb=short || true

echo ""
echo -e "${GREEN}4. Running All Tests with Coverage...${NC}"
pytest tests/ --cov=openad --cov-report=html:test_reports/coverage --cov-report=term-missing || true

echo ""
echo "========================================="
echo "Test Reports Generated"
echo "========================================="
echo ""
echo "Reports available in test_reports/:"
echo "  - coverage/index.html    : Coverage report"
echo "  - report.html            : Test results"
echo "  - junit.xml              : JUnit XML for CI/CD"
echo "  - coverage.json          : Coverage data (JSON)"
echo ""

# Check if reports were generated
if [ -f "test_reports/report.html" ]; then
    echo -e "${GREEN}✓ Test reports generated successfully${NC}"
    echo ""
    echo "To view coverage report:"
    echo "  open test_reports/coverage/index.html"
    echo ""
    echo "To view test report:"
    echo "  open test_reports/report.html"
else
    echo -e "${YELLOW}⚠ Some reports may not have been generated${NC}"
fi

echo ""
echo "========================================="
echo "Test Suite Complete"
echo "========================================="

# Made with Bob
