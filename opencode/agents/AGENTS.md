---
disable: true
---

# AGENTS

## ⚠️ MANDATORY: Run Verification After Every Agent Modification

After **any** modification to agent definition files in this directory, you **MUST** run the verification script:

```bash
shared/scripts/run-analyzer.sh -d agents -q -e
```

Run this from `opencode/`. The script uses the designated virtual environment — **never invoke `agent_analyzer.py` with bare `python`**.

**If verification fails, fix the errors before completing your task.** Do NOT report success until verification passes.

Common errors caught:

- **BAD_INDENT**: YAML frontmatter indentation must use 2-space increments
- **DUPLICATE_KEY**: No duplicate keys allowed at any nesting level in YAML frontmatter
