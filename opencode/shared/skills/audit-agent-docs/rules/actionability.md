# Lens: Actionability

Find vague, weak, or unenforceable instructions. Apply positive framing principles grounded in LLM attention research.

## Key Principle

This audits documentation **for AI agents**, not humans. Focus on instructions that agents cannot reliably follow because they are vague, negatively framed, or lack reasoning.

## Framing Principle

**Positive directives outperform negative prohibitions.** LLMs attend to what you mention — saying "NEVER use X" activates X in the model's attention, making it *more* likely (the "Pink Elephant" effect, documented in arxiv 2402.07896, 2503.22395). Anthropic's own docs recommend: "Tell Claude what to do instead of what not to do."

Rewrite rules as positive directives with reasoning wherever possible.

## Anti-Patterns to Flag

### 1. Negative Framing → Positive Rewrite
- "NEVER close issues without user approval" → "Wait for explicit user approval before closing any issue"
- "Don't use `any` type" → "Use interfaces and type guards for all function parameters"
- "Do NOT combine these into one question" → "Always ask these as separate questions"
- **Exception**: Keep NEVER/DO NOT for truly catastrophic, irreversible actions (force-push to main, deleting production data) where the shock value is warranted

### 2. Negative-Only Rules
Rules that say "don't do X" without stating what to do instead. Every prohibition MUST include the positive alternative — what the agent should do in that situation. A rule that only says "no" leaves the agent guessing.

### 3. Missing Reasoning
Rules without a "why" are weaker. Agents generalize from explanations — "TTS engines cannot pronounce ellipses, so use complete sentences" is more robust than "NEVER use ellipses" because the agent can apply the principle to novel situations.

### 4. Weak Modals
"should", "consider", "try to", "ideally", "prefer to" — rewrite as clear positive directives. If truly optional, say so explicitly ("MAY ... but only when ...").

### 5. Weasel Phrases
"use appropriate...", "if it works", "when relevant", "as needed", "if possible", "usually", "sometimes", "typically", "generally", "normally", "occasionally", "frequently" — these give agents an escape hatch from every rule. Rewrite with concrete conditions.

### 6. Unmeasurable Quality
"write clean code", "keep it simple", "use best practices", "be careful with" — agents can't evaluate these. Replace with specific, checkable criteria or delete.

### 7. Aggressive Emphasis
"CRITICAL!", "YOU MUST", "NEVER EVER", "ABSOLUTELY DO NOT" — calm, direct instructions perform better on modern Claude models. Reserve emphasis (caps, bold) for the 2-3 most important rules; overuse dilutes all of them.

## Output Format

For each finding:

```
### Actionability: {brief title}

**Anti-pattern**: {which of the 7 categories above}
**Location**: `{file}` (lines N-M)
**Current**:
> {quoted instruction}

**Problem**: {why this is weak/unenforceable}
**Proposed rewrite**:
> {concrete positive directive with reasoning}
```
