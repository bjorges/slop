---
name: audit-agent-docs
description: "Audit agent-facing documentation (AGENTS.md, agent definitions) for redundancies, contradictions, gaps, and misplaced content. Adapted for OpenCode from oroddlokken/slop."
---

# audit-agent-docs Skill

A multi-lens audit tool for AI agent documentation in OpenCode. Discovers and analyzes agent-facing documentation across the layered architecture (shared → context → machine) to identify redundancies wasting tokens, contradictions, gaps, and content in the wrong file.

## Key Principle

This skill audits documentation **FOR AI agents**, not humans. Agents can read source code. Only flag findings that matter:

- **Redundancies**: Rules stated identically in multiple files (token waste)
- **Contradictions**: Rules conflict or override silently
- **Genuine gaps**: Context required for agent behavior NOT derivable from code
- **Wrong file**: Content placed in the wrong layer or scope
- **Behavioral clarity**: Rules about permissions, limits, and workflows are clearly stated

Ignore findings that agents can derive from code inspection. Don't audit for style, tone, or human readability.

## Lens Overview

Each lens is a distinct angle of analysis. Load `rules/{filename}.md` for the corresponding lens before launching each sub-agent. Run all selected lenses in parallel.

| # | Lens | File | Type | Description |
|----|------|------|------|-------------|
| 1 | Redundancy | `rules/redundancy.md` | Core | Duplicated information across files and layers |
| 2 | Contradictions | `rules/contradictions.md` | Core | Conflicting instructions, inconsistent terminology |
| 3 | Gaps | `rules/gaps.md` | Core | Missing context agents need and can't derive from code |
| 4 | Actionability | `rules/actionability.md` | Core | Vague rules, negative framing, weak modals, missing reasoning |
| 5 | Information Architecture | `rules/info-architecture.md` | Core | Content in the wrong file or layer |
| 6 | Structure | `rules/structure.md` | Core | Token budget, YAML quality, lost-in-the-middle, layered architecture |
| 7 | Hygiene | `rules/hygiene.md` | Core | Secrets, stale instructions, self-evident rules, dead agents |
| 8 | Guardrails | `rules/guardrails.md` | Core | Missing or vague safety boundaries, prose-only restrictions |
| 9 | Cold Start | `rules/cold-start.md` | Extended | First-time agent confusion, undefined terms, missing prerequisites |
| 10 | Domain Deep-Dive | `rules/domain.md` | Extended | Deep-dive gap analysis for a specific domain area |
| 11 | Agent Quality | `rules/agent-quality.md` | Extended | Agent definition quality, permissions, role focus |

**Default**: Lenses 1–8 (Core)  
**Full scope**: Lenses 1–11 (add extended lenses)

## File Discovery

The skill discovers documentation in this order (OpenCode layered architecture):

| Location | Glob Patterns |
|----------|---------------|
| Shared rules | `AGENTS.md` (shared rules file; private, not in the public repo) |
| Shared agents | `agents/*.md` |
| Shared skills | `shared/skills/*/SKILL.md` |
| Context rules | `<context>/AGENTS.md` |
| Context agents | `<context>/agents/*.md` |
| Context skills | `<context>/skills/*/SKILL.md` |
| Machine overrides | `~/AGENTS.md` |
| Project-level | `**/AGENTS.md` in project roots |
| GitHub cross-tool | `.github/copilot-instructions.md`, `.github/copilot/**/*.md` |

**Note**: OpenCode uses layered resolution, not `@` imports. Shared rules apply globally; context rules override per context; machine rules override all.

## Workflow

**Step 1: Scope & Target**
- Ask: Which files/directories to audit? (default: the directory containing `agents/` and `shared/`)
- Ask: Scope? (`standard`=lenses 1–8, `full`=1–11, or specific lens list)
- If `full`: Ask which domain area to deep-dive (optional)

**Step 2: Discover Files**
- Use patterns above to locate all AGENTS.md, agent .md, SKILL.md files
- Report findings; ask user to confirm

**Step 3: Load & Launch Lenses**
- Load the corresponding `rules/*.md` file for each selected lens (see table above)
- Launch each lens as a parallel sub-agent (using Task tool, `subagent_type: "explore"`)
- Each sub-agent receives: all doc file contents, its lens instructions, the key principle

**Step 4: Distill & Propose**
- Wait for all sub-agents to complete
- Deduplicate findings across lenses
- Classify: Remove / Move / Rewrite / Add
- Group proposed edits by file
- Present to user; ask for approval before applying

## Options

| Option | Values | Default |
|--------|--------|---------|
| Scope | `standard`, `full`, or comma-separated lens names | `standard` |
| Path | Target directory or file paths | the directory containing `agents/` and `shared/` |
| Domain | Area for domain deep-dive (full scope only) | Asked at runtime |

## Rules

- **Run lenses in parallel**: All selected lenses audit simultaneously; faster than sequential
- **Independence**: Each sub-agent audits independently, no cross-talk
- **Distill after completion**: Deduplicate and synthesize after all lenses finish
- **Propose, don't apply**: Always ask user before making edits
- **Filter aggressively**: Ignore code-derivable findings; focus on token-wasting redundancies and behavioral gaps
- **Respect hierarchy**: AGENTS.md = behavioral rules for AI; agent .md files = role definitions with permissions; SKILL.md = skill workflows
- **Domain deep-dive**: For full scope, optionally focus on one domain (e.g., "git workflow", "jira integration", "agent definitions")

## Attribution

Based on [audit-agent-docs](https://github.com/oroddlokken/slop/tree/main/audit-agent-docs) by oroddlokken. Adapted for OpenCode.
