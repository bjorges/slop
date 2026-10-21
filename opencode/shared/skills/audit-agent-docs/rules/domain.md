# Lens: Domain Deep-Dive

Deep-dive gap analysis for a specific domain area. Reads both documentation AND relevant source code to find where docs mislead or where non-obvious patterns aren't captured.

## Key Principle

This audits documentation **for AI agents**, not humans. The domain lens is unique — it actively reads source code to compare documented patterns against actual implementation. Only flag gaps where the documentation actively misleads or where non-obvious patterns need explicit documentation.

## How This Lens Works

Unlike other lenses that only read documentation, this lens:

1. **Receives a domain area** from the user (e.g., "git workflow", "agent permissions", "skill loading", "testing", "deployment")
2. **Reads relevant source files** — scripts, configs, agent definitions related to that domain
3. **Compares documentation against reality** — are documented patterns actually how things work?
4. **Identifies undocumented patterns** — are there important patterns in the code that aren't captured in docs?

## What to Look For

### 1. Documentation vs Reality Drift
- Documented commands or scripts that behave differently than described
- Documented workflows that skip steps the code actually requires
- Documented file locations that don't match where things actually live

### 2. Undocumented Complexity
- Error handling in scripts that agents should know about
- Edge cases in workflows that documentation glosses over
- Configuration options that exist in code but aren't documented

### 3. Missing Domain Context
- Domain-specific conventions that agents need to follow
- Relationships between components that aren't documented
- Non-obvious side effects of domain operations

### 4. Stale Domain Knowledge
- Domain documentation that references old versions or patterns
- Instructions for tools or APIs that have changed

## Output Format

For each finding:

```
### Domain ({area}): {brief title}

**Documentation**: `{file}` (lines N-M)
> {quoted text, or "Not documented"}

**Reality**: `{source file}` (lines N-M)
> {what the code actually does}

**Gap type**: Drift | Undocumented | Missing context | Stale
**Impact**: {what goes wrong when an agent follows the docs}
**Recommendation**: {update docs, add new docs, or remove stale content}
```
