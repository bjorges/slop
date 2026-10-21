# Lens: Hygiene

Catch quality and safety issues in agent documentation.

## Key Principle

This audits documentation **for AI agents**, not humans. Focus on issues that degrade agent performance: wasted tokens, stale instructions that mislead, and security risks.

## Checks

### 1. Secrets
Scan for API keys, connection strings, tokens, credentials, passwords in any documentation file. These should never appear in agent instruction files.

### 2. Self-Evident Instructions
Flag platitudes and instructions that add zero information:
- "write clean code", "follow best practices", "handle errors appropriately"
- "use meaningful variable names", "write tests for your code", "ensure code quality"
- Standard language conventions the model already knows (e.g., "use camelCase in JavaScript", "add type hints in Python") — unless the project deliberately deviates from convention

These waste tokens and dilute real rules.

### 3. Stale Instructions
Cross-reference documented commands, paths, tools, and patterns against the actual codebase:
- File paths that no longer exist
- Commands or scripts that have been renamed or removed
- References to tools or dependencies no longer in use
- Workflow steps that reference outdated processes

### 4. Permission Model Hygiene (OpenCode-Specific)
Check agent YAML frontmatter permissions for:
- **Overly broad permissions** — `"*": allow` when more specific patterns would be safer
- **Overly restrictive permissions** — Permissions that would prevent the agent from doing its documented job
- **Inconsistent permission patterns** — Similar agents with different permission levels for the same operations without clear justification
- **Missing permission entries** — Operations the agent is described as performing but lacking explicit permission for

### 5. Rules Maintenance Gap
Check whether documentation instructs agents to keep documentation up to date as the codebase evolves. Without this, instruction files become stale as code moves or patterns change.

### 6. Dead Agent Definitions
Agent definitions in `agents/` that are:
- Never referenced by any other agent or AGENTS.md
- Have descriptions that no longer match their actual instructions
- Define capabilities that overlap entirely with another agent

## Output Format

For each finding:

```
### Hygiene: {brief title}

**Check**: {which of the checks above}
**Location**: `{file}` (lines N-M)
**Current**:
> {quoted text or description}

**Problem**: {why this is a hygiene issue}
**Recommendation**: {concrete action — remove, update, or fix}
```
