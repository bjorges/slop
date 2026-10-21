# Lens: Redundancy

Find duplicated information across agent documentation files.

## Key Principle

This audits documentation **for AI agents**, not humans. Agents can read source code. Only flag redundancies in agent-facing documentation — behavioral rules, configuration, workflow instructions. Skip anything an agent could derive by reading the codebase.

## What to Look For

For each piece of duplicated information found:

1. **Cite both locations** — exact file paths and line ranges
2. **Classify the duplication**:
   - **Exact**: Word-for-word or near-identical text
   - **Paraphrase**: Same information stated differently
   - **Partial**: Overlapping content where one is a subset of the other
3. **Recommend which location is canonical** — where should the single source of truth live?
4. **Assess risk** — Do the duplicates risk diverging? Is one already slightly different (early contradiction)?

## OpenCode-Specific Patterns

Pay special attention to these common duplication vectors in OpenCode:

- **Shared AGENTS.md vs context AGENTS.md** — Rules stated in `AGENTS.md` (shared rules file; private, not in the public repo) repeated in a context-level `AGENTS.md` overlay
- **Agent definitions vs AGENTS.md** — Instructions in individual agent `.md` files that repeat what's already in the shared or context AGENTS.md
- **Machine overrides vs context rules** — `~/AGENTS.md` repeating content from context-level files
- **Cross-agent duplication** — Multiple agent definition files containing identical instruction blocks (e.g., git workflow rules repeated across agents)
- **Bob's system prompt vs agent files** — Bob's definition often contains summaries of other agents' roles; check these haven't drifted from the actual agent definitions

## Output Format

For each finding:

```
### Redundancy: {brief title}

**Type**: Exact | Paraphrase | Partial
**Location A**: `{file}` (lines N-M)
> {quoted text}

**Location B**: `{file}` (lines N-M)
> {quoted text}

**Canonical location**: {which file should keep it and why}
**Risk**: {Low|Medium|High} — {brief explanation}
```
