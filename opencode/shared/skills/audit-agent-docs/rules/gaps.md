# Lens: Gaps

Find genuinely missing information that agents need and cannot derive from reading source code.

## Key Principle

This audits documentation **for AI agents**, not humans. Be extremely aggressive about filtering out code-derivable information. An agent can read any file in the codebase — if the answer is in the code, it doesn't need to be in the docs.

Only flag gaps for:
- **Non-obvious consequences** — "If you skip X, the system silently fails" or "Y must happen before Z or data is corrupted"
- **Behavioral rules** — Policies that aren't encoded in the codebase (e.g., "always ask the user before closing issues")
- **Workflow steps** — Procedures that are implied but never explicitly stated
- **External dependencies** — Things the agent needs to know that aren't visible in the code (e.g., "this service depends on X running locally")
- **Institutional knowledge** — Conventions or decisions not recorded anywhere the agent can find

## What NOT to Flag

- Function signatures, parameters, return types (read the code)
- File structure and directory layout (use glob/find)
- Config options and their formats (read the config files)
- CSS conventions, naming patterns (read the stylesheets)
- Test fixture details (read the test files)
- Anything documented in README files the agent can access

## OpenCode-Specific Gap Patterns

Look for these common gaps in OpenCode setups:

- **Missing agent coordination rules** — How should agents hand off work? What context should they pass?
- **Implicit assumptions about environment** — Tools, versions, or services that must be running but aren't documented
- **Permission model gaps** — Situations where the correct permission (allow/deny/ask) isn't specified
- **Missing error recovery** — What should happen when an agent's operation fails? Is there a retry or escalation path?
- **Context-switching gaps** — When switching between work/personal contexts, what changes? Are all differences documented?
- **Undocumented workflows** — Common agent tasks that lack step-by-step guidance

## Output Format

For each finding:

```
### Gap: {brief title}

**Where it's needed**: `{file}` or {which layer/context}
**What's missing**: {clear description of the missing information}
**Why an agent can't derive it**: {explain why reading code isn't sufficient}
**Impact**: {what goes wrong without this information}
**Suggested addition**: {proposed text to add}
```
