---
name: skill-fitness
description: "Audit this OpenCode repo's own agent/skill collection for structural drift — dangling skill references, orphaned skills, and roster-table/naming-table parity mismatches. Mechanical cross-referencing, not judgment calls; runs a single linear pass, no sub-agent fan-out."
---

# skill-fitness Skill

A lightweight, mechanical self-audit for this repo's agent and skill collection. Unlike `audit-agent-docs` (an 11-lens judgment-call audit that fans out to parallel `explore` sub-agents), `skill-fitness` checks are simple existence/parity comparisons — does X exist, does table Y match files on disk Z. No lenses, no `rules/` subdirectory, no sub-agent fan-out needed for the default case.

## Rationale

Dangling skill grants are silently ignored, so check them mechanically. The same applies to their siblings: orphaned skills, stale roster rows, and naming-table drift.

## Checks

Each check is independent — a grep/read/compare, not a multi-perspective judgment call. Run them in any order, in parallel if convenient (simple `grep`/`glob` calls, not `Task`/`explore` fan-out).

### 1. Dangling Skill References

For every agent file (`agents/*.md` and, if present, `<context>/agents/*.md`), inspect its frontmatter `permission.skill` block (if any). For each skill name granted, confirm it exists on disk as `shared/skills/<name>/SKILL.md` (or the equivalent context-level path, e.g. `<context>/skills/<name>/SKILL.md`). Flag any skill name referenced by an agent that has no matching `SKILL.md` file anywhere.

### 2. Orphaned Skills

For every skill that exists on disk (`shared/skills/*/SKILL.md`, `<context>/skills/*/SKILL.md`), confirm it is either:
- (a) referenced by at least one agent's `permission.skill` grant, **or**
- (b) intentionally standalone/bob-invoked-directly

Note: (b) is a legitimate, common pattern — `audit-agent-docs` itself is invoked directly by @bob via the `skill` tool and is not granted to any specific agent's permissions. "Orphaned" in this check means "not referenced by any agent AND not documented/understood as intentionally bob-only" — not simply "not referenced." When in doubt about whether a skill is intentionally bob-only, ask the user rather than flagging it as broken.

### 3. Roster Table Parity (`bob.md`)

Every `.md` file in `agents/` — excluding `README.md`, `AGENTS.md`, and `BOBIVERSE-NAMING.md` (these are docs, not agent definitions) — should have a corresponding row in `bob.md`'s "The Replicant Swarm" roster table. Conversely, every row in that table should correspond to an actual `.md` file on disk. Flag:
- Agent files with no roster row (undocumented to Bob)
- Roster rows with no matching file (stale entry for a deleted/renamed agent)

### 4. Naming Table Parity (`BOBIVERSE-NAMING.md`)

Cross-check `BOBIVERSE-NAMING.md`'s "Active Agent Mapping" table against `agents/*.md`:
- Every agent in the "Active Agent Mapping" table should correspond to an actual file in `agents/`
- No agent/character should appear in **both** the "Active Agent Mapping" table and the "Unused Characters" table
- No Bobiverse character name should be double-assigned to two different active agents

### 5. Hardcoded-Count Regression Sweep

Grep for a recurring anti-pattern: a literal digit describing a mutable count of agents/skills/reviewers (e.g. "10 code reviewers", "N agents", "3 skills", "12 total"). These counts drift the moment a file is added or removed and should be phrased as "see the roster table" rather than hardcoded. Search `agents/*.md`, `agents/README.md`, and `README.md` for patterns like `\b\d+\s+(agents?|skills?|reviewers?)\b`.

## Workflow

1. **Run each check** — they're independent; use direct `grep`/`glob`/`read` calls (or simple parallel bash calls), no `Task` tool, no sub-agent spawning needed for the default case.
2. **Collect findings** grouped by check number/name.
3. **Present a short report** — one section per check, listing concrete file/line findings (or "clean" if nothing found).
4. **Propose fixes** for each finding (e.g., "remove the `example-skill` grant from `riker.md`" or "add `skippy-gitops` row to `bob.md` roster table").
5. **Ask for user approval** before any edits. This skill only audits and reports — it does not apply fixes itself, consistent with `audit-agent-docs`'s "propose, don't apply" rule. If the user approves fixes, delegate the actual edits to @riker (this skill's own execution does not edit files).

## When to Run It

- After adding or removing an agent (`agents/*.md`) or a skill (`shared/skills/*/SKILL.md`)
- After editing `bob.md`'s roster table or `BOBIVERSE-NAMING.md`'s tables
- Periodically as repo hygiene — analogous to how `audit-agent-docs` is run periodically for AGENTS.md content hygiene, this is the periodic check for structural/referential integrity of the agent+skill collection itself

## Attribution

Sibling skill to `audit-agent-docs`; scoped down deliberately to mechanical checks only.
