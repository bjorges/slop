# Lens: Guardrails

Audit explicit prohibitions and safety boundaries in agent documentation.

## Key Principle

This audits documentation **for AI agents**, not humans. Guardrails must be specific, enforceable, and preferably positively framed. Vague safety boundaries are worse than none — they create a false sense of security.

## What to Audit

### 1. Missing Safety Boundaries
Are there destructive or irreversible actions the agent could take that lack explicit boundaries?
- Deleting data, files, or resources
- Force-pushing to shared branches
- Modifying shared state (databases, config)
- Sending external messages (emails, notifications, API calls)
- Closing or resolving issues/tickets without approval

### 2. Positive Framing
Most guardrails work better as positive directives:
- "Wait for user confirmation before closing issues" beats "NEVER close issues without approval"
- Reserve NEVER/DO NOT only for catastrophic, irreversible actions (force-push to main, dropping tables, deleting production data) where the shock value is warranted

### 3. Specificity and Enforceability
Flag vague guardrails:
- "be careful with..." — careful how?
- "avoid if possible" — when is it not possible?
- "try not to" — this is a suggestion, not a boundary
- Rewrite as concrete positive directives with scope

### 4. Reasoning
Rules with a **why** are more robust — agents generalize from explanations to novel situations instead of following the letter while violating the spirit. Flag guardrails that lack reasoning.

### 5. Guardrail Contradictions
Do guardrails contradict other instructions?
- "wait for approval before modifying X" but a workflow step says "update X automatically"
- Permission model allows an action that prose rules prohibit (or vice versa)

### 6. Prose-Only Tool Restrictions (OpenCode-Specific)
Flag when docs rely solely on prose to restrict dangerous commands. In OpenCode, the YAML frontmatter `permission.bash` section provides actual enforcement. For each prose-only restriction:
- Check if there's a matching `bash` permission entry in the agent's frontmatter
- If not, flag that the restriction is guidance only with no enforcement
- Note that OpenCode's permission model (allow/deny/ask) provides real enforcement — recommend adding frontmatter permissions rather than relying on prose alone
- Flag stacked negative prohibitions (3+ NEVER/DO NOT rules about tools) — compliance degrades as these accumulate

## Output Format

For each finding:

```
### Guardrail: {brief title}

**Type**: Missing | Vague | Contradicted | Prose-only | Missing reasoning
**Location**: `{file}` (lines N-M)
**Current**:
> {quoted text, or "No boundary exists for {action}"}

**Risk**: {what could go wrong}
**Recommendation**: {concrete positive directive with reasoning, or permission entry to add}
```
