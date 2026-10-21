# Lens: Contradictions

Find conflicting instructions, inconsistent terminology, and garbled text across agent documentation files.

## Key Principle

This audits documentation **for AI agents**, not humans. Focus on contradictions that would cause an agent to behave incorrectly or unpredictably. Skip trivial wording differences that don't change meaning.

## What to Look For

### Direct Contradictions
- File A says "do X", file B says "don't do X" or "do Y instead"
- Conflicting workflows (e.g., one file says "commit directly", another says "use PR workflow")
- Inconsistent permission models (agent definition allows something that AGENTS.md prohibits)

### Cross-Layer Contradictions (OpenCode-Specific)
OpenCode uses a layered architecture: shared → context → machine overrides. Check for:
- **Shared vs context conflicts** — the shared `AGENTS.md` says one thing, a context `AGENTS.md` says another without explicitly overriding
- **Agent definition vs AGENTS.md** — An agent's YAML frontmatter permissions contradict prose rules in AGENTS.md
- **Intentional overrides vs accidental conflicts** — Context files MAY intentionally override shared rules. Flag only when the override seems accidental (no explicit "overrides shared rule" language)

### Cross-Tool Contradictions
If the project has instructions for multiple tools (OpenCode AGENTS.md + GitHub Copilot instructions + others):
- Different coding standards specified per tool
- Conflicting workflow instructions

### Terminology Inconsistencies
- Same concept called different names across files (e.g., "sub-agent" vs "subagent" vs "child agent")
- Inconsistent naming for the same operation or component

### Garbled Text
- Broken formatting, truncated instructions, malformed markdown
- Instructions that contradict themselves within the same paragraph

## Output Format

For each finding:

```
### Contradiction: {brief title}

**Location A**: `{file}` (lines N-M)
> {quoted text}

**Location B**: `{file}` (lines N-M)
> {quoted text}

**Conflict**: {clear explanation of what contradicts what}
**Recommendation**: {which version should win and why}
**Intentional override?**: Yes (context legitimately overrides shared) | No (likely accidental) | Unclear
```
