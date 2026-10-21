# Lens: Information Architecture

Check if content is in the right file within the documentation hierarchy.

## Key Principle

This audits documentation **for AI agents**, not humans. Focus on whether documentation placement helps or hinders agent comprehension and token efficiency.

## OpenCode Documentation Hierarchy

OpenCode has a specific layered architecture. Each layer has a purpose:

| Layer | Location | Purpose |
|-------|----------|---------|
| **Shared rules** | `AGENTS.md` (shared rules file; private, not in the public repo) | Universal behavioral rules, coding standards, conventions |
| **Shared agents** | `agents/*.md` | Agent role definitions, permissions, capabilities |
| **Context rules** | `<context>/AGENTS.md` (private overlay) | Context-specific overrides and additions |
| **Context agents** | `<context>/agents/*.md` | Context-specific agent definitions |
| **Skills** | `shared/skills/*/SKILL.md` | Domain-specific instructions loaded on demand |
| **Machine overrides** | `~/AGENTS.md` | Machine-specific configuration (git repos, preferences) |
| **Project-level** | `AGENTS.md` in project roots | Project-specific agent instructions |

## What to Flag

### Content in the Wrong Layer
- **Agent-specific rules in AGENTS.md** — Instructions that only apply to one agent should be in that agent's `.md` file, not in the shared AGENTS.md
- **Universal rules in context files** — Rules that apply to all contexts shouldn't be only in a context `AGENTS.md`
- **Machine-specific config in shared files** — Repository URLs, local paths, or machine-specific preferences should be in `~/AGENTS.md`, not in shared files
- **Shared rules in machine overrides** — Universal conventions in `~/AGENTS.md` that belong in the shared `AGENTS.md`

### Content in the Wrong File Type
- **Behavioral rules in agent definitions** — Agent `.md` files should define the role, permissions, and capabilities. General behavioral rules belong in AGENTS.md
- **Role definitions in AGENTS.md** — Detailed agent role descriptions should be in the agent's own file, not in AGENTS.md
- **Skill content in agent definitions** — Domain-specific knowledge that could be a loadable skill should be in `skills/`, not embedded in an agent definition

### Token Waste
- **Always-loaded vs on-demand** — AGENTS.md and agent definitions load every session. Content that's only relevant sometimes should be a skill (loaded on demand) instead
- **README duplication** — Agent docs that duplicate README content waste tokens; READMEs are for humans

## Output Format

For each finding:

```
### Misplaced: {brief title}

**Current location**: `{file}` (lines N-M)
> {quoted text}

**Belongs in**: `{target file or layer}`
**Why**: {explanation of why current placement is wrong}
**Impact**: {token waste / confusion / maintenance burden}
```
