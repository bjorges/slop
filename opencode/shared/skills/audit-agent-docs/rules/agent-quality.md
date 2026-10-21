# Lens: Agent Quality

Audit agent definition files for quality, focus, and consistency.

## Key Principle

This audits agent definitions in OpenCode format. OpenCode agents use YAML frontmatter with markdown body. Each agent should have a clear, focused role with appropriate permissions.

## OpenCode Agent Format

Agent definitions live in `agents/*.md` (or a context overlay's `agents/*.md`) and follow this structure:

```yaml
---
description: <one-line description — used for delegation decisions>
mode: subagent | primary
model: <model identifier>
temperature: <0.0-1.0>
hidden: <true|false>
permission:
  read: allow | deny
  write: allow | deny | ask
  edit: allow | deny | ask
  glob: allow | deny
  grep: allow | deny
  webfetch: allow | deny
  bash:
    "*": allow | deny | ask
    "<pattern>": allow | deny | ask
  skill:
    "<skill-name>": allow | deny
---

# Agent Role

<markdown body with instructions>
```

## What to Audit

### 1. Description Quality
- The `description` field is critical — the orchestrating agent (Bob) uses it to decide when to delegate. It must be specific and actionable.
- Flag: vague descriptions like "general helper" or "does various things"
- Flag: descriptions that don't match the agent's actual instructions
- Flag: missing description field

### 2. Permission Scope
- **Overly broad**: Does the agent have more access than its role requires? (e.g., a read-only agent with write permissions)
- **Too restrictive**: Does the agent lack permissions it needs to do its documented job?
- **Inconsistent patterns**: Similar agents with very different permission levels without justification
- **Security-sensitive**: Agents with `bash: "*": allow` — is this intentional and necessary?

### 3. Role Focus
- Agents should do one thing well. Flag agents that:
  - Have instructions covering too many unrelated domains
  - Could be split into focused sub-agents
  - Have overlapping responsibilities with other agents

### 4. Instruction Quality
- Are the agent's markdown instructions clear and actionable?
- Do they follow the actionability principles (positive framing, concrete directives)?
- Are there contradictions between the frontmatter and the markdown body?
- Is the instruction length proportional to the agent's complexity?

### 5. Cross-Agent Consistency
- Do agents that perform similar functions follow similar patterns?
- Are naming conventions consistent across agent files?
- Do agent references to each other use correct names?

### 6. Mode Appropriateness
- `primary` mode agents can spawn sub-agents — is this capability needed and appropriate?
- `subagent` mode agents cannot spawn others — are any sub-agents trying to do work that requires spawning?

## Output Format

For each finding:

```
### Agent Quality: {brief title}

**Agent**: `{filename}`
**Check**: {which of the checks above}
**Current**:
> {quoted frontmatter or instruction text}

**Problem**: {what's wrong and why it matters}
**Recommendation**: {concrete fix}
```
