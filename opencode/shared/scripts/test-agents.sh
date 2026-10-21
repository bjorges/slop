#!/usr/bin/env bash
# Sanity checks for the multi-agent setup.
# Paths are derived from this script's location (opencode/shared/scripts),
# agents are expected at opencode/agents. Override with AGENTS_DIR=... if needed.

# NOTE: -e is deliberately omitted so every test runs and failures are tallied.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENTS_DIR="${AGENTS_DIR:-$SCRIPT_DIR/../../agents}"
# Normalize to an absolute path when it exists (falls back to the raw value).
AGENTS_DIR="$(cd -- "$AGENTS_DIR" 2>/dev/null && pwd || printf '%s' "$AGENTS_DIR")"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass_count=0
fail_count=0

test_pass() { printf '%b\n' "${GREEN}✓${NC} $1"; pass_count=$((pass_count + 1)); }
test_fail() { printf '%b\n' "${RED}✗${NC} $1"; fail_count=$((fail_count + 1)); }
test_warn() { printf '%b\n' "${YELLOW}⚠${NC} $1"; }

echo "Test 1: Agents directory exists"
if [ -d "$AGENTS_DIR" ]; then
    test_pass "Agents directory found: $AGENTS_DIR"
else
    test_fail "Agents directory not found: $AGENTS_DIR"
fi

echo "Test 2: Scripts directory exists"
if [ -d "$SCRIPT_DIR" ]; then
    test_pass "Scripts directory found: $SCRIPT_DIR"
else
    test_fail "Scripts directory not found: $SCRIPT_DIR"
fi

echo "Test 3: Analyzer scripts are executable"
for s in agent_analyzer.py run-analyzer.sh; do
    if [ -x "$SCRIPT_DIR/$s" ]; then
        test_pass "$s is executable"
    else
        test_fail "$s not found or not executable"
    fi
done

echo "Test 4: Agent definitions present"
agent_count=$(find "$AGENTS_DIR" -maxdepth 1 -name "*.md" \
    ! -name "AGENTS.md" ! -name "README.md" ! -name "BOBIVERSE-NAMING.md" 2>/dev/null | wc -l | tr -d ' ')
if [ "$agent_count" -gt 0 ]; then
    test_pass "Found $agent_count agent definition(s)"
else
    test_fail "No agent definitions found in $AGENTS_DIR"
fi

echo "Test 5: Orchestrator and docs present"
for f in bob.md README.md; do
    if [ -f "$AGENTS_DIR/$f" ]; then
        test_pass "Found $f"
    else
        test_fail "Missing $f"
    fi
done

echo "Test 6: Agent analyzer validation (first run may bootstrap the venv via network pip)"
if "$SCRIPT_DIR/run-analyzer.sh" -d "$AGENTS_DIR" -q -e; then
    test_pass "All agents passed validation"
else
    test_fail "Agent validation failed"
fi

echo ""
echo "Passed: $pass_count"
echo "Failed: $fail_count"

if [ "$fail_count" -eq 0 ]; then
    printf '%b\n' "${GREEN}✓ All tests passed${NC}"
    exit 0
fi
printf '%b\n' "${RED}✗ Some tests failed${NC}"
exit 1
