# Lens: Cold Start

Pretend to be a fresh agent with zero context. Identify assumptions the documentation makes that would confuse a first-time reader.

## Key Principle

This audits documentation **for AI agents**, not humans. Skip things derivable from code. Focus on documentation that assumes the reader already knows the system — undefined terms, implicit dependencies, unexplained workflows.

## What to Look For

### 1. Undefined Terms and Jargon
- Terms used without definition (e.g., "the Bob-net", "replicant swarm", "wave execution")
- Acronyms or abbreviations not expanded on first use
- Internal project names referenced without explanation

### 2. Assumed Knowledge
- Instructions that assume familiarity with the project's history or past decisions
- References to "the usual process" or "as we discussed" without specifying what
- Workflow steps that assume the agent already knows previous steps

### 3. Missing Prerequisites
- Tools, services, or configurations that must exist before instructions can be followed
- Environment variables referenced but not explained
- Dependencies between files that aren't documented (e.g., "after updating X, also update Y")

### 4. Ambiguous Entry Points
- Where does a new agent start reading? Is there a clear starting point?
- Are the relationships between files (AGENTS.md, agent definitions, skills) clear?
- Can a fresh agent understand the hierarchy and precedence of rules?

### 5. Implicit Context (OpenCode-Specific)
- References to "the current context" without explaining what contexts are
- Agent names referenced without explaining their roles
- Permission model assumed to be understood without explanation
- Worktree conventions referenced without full explanation

## Output Format

For each finding:

```
### Cold Start: {brief title}

**Location**: `{file}` (lines N-M)
**Confusion point**: {what would confuse a fresh agent}
**Assumed knowledge**: {what the reader is expected to already know}
**Recommendation**: {add definition, link, or context — be specific}
```
