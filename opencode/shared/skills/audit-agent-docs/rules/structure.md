# Lens: Structure

Quantitative and architectural checks on agent documentation files.

## Key Principle

This audits documentation **for AI agents**, not humans. Structural issues directly impact agent performance — bloated files degrade instruction adherence, critical rules buried in the middle get ignored.

## Checks

### 1. Token Budget
- **Count lines per file.** Warn at >200 lines, critical at >300.
- **Estimate token count** (characters / 4).
- Agent definition files and AGENTS.md load every session, so every line costs tokens on every message. Keeping them lean directly improves instruction adherence — research shows compliance degrades as instruction count grows.

### 2. Layered Architecture Usage
OpenCode supports a layered system: shared → context-specific → machine overrides. Check for:
- **Monolithic AGENTS.md files** that could split content into context-specific files or skills
- **Agent definitions with embedded knowledge** that should be extracted into loadable skills
- **Context-specific rules in shared files** — instructions that only apply to work or personal context should be in the appropriate context overlay directory

### 3. Skills Boundary
OpenCode skills (`shared/skills/*/SKILL.md`) only load when invoked. Flag domain knowledge in AGENTS.md or agent definitions that loads every session but is only relevant sometimes — these should be skills instead.

### 4. YAML Frontmatter Quality
OpenCode agent definitions use YAML frontmatter. Check:
- **Indentation consistency** — must use 2-space increments
- **No duplicate keys** at any nesting level
- **Required fields present** — `description`, `mode`, `permission`
- **Permission completeness** — are critical permissions (read, write, edit, bash) specified?

### 5. Lost in the Middle
In documents >= 20 lines, check if critical rules are buried in the 40-60% zone of the file. LLMs pay more attention to the beginning and end of long documents (Liu et al., 2023). Recommend moving critical rules to the top or bottom.

### 6. README Duplication
Compare AGENTS.md content against adjacent README.md files. Flag high overlap — README content is for humans and wastes agent tokens when duplicated.

### 7. Cross-File Structure
- **Circular references** — Agent A references Agent B's rules which reference Agent A
- **Orphaned content** — Rules or agent definitions that nothing references or uses
- **Missing cross-references** — Important relationships between files that aren't documented

## Output Format

For each finding:

```
### Structure: {brief title}

**Check**: {which of the checks above}
**Location**: `{file}`
**Detail**: {specific finding with numbers where applicable}
**Recommendation**: {concrete action to take}
**Impact**: {token savings / improved adherence / reduced confusion}
```
