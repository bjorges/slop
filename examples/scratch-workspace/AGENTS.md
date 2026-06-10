# Scratch Workspace — Agent Rules

**Purpose**: Investigation, coordination, debugging, and multi-repo task tracking.  
**Context**: This is NOT a project repository. It is a coordination workspace.

---

## Include Shared Rules

If you maintain a shared agent-rules file (e.g. `~/.opencode/shared/AGENTS.md` or similar),
include it here as a baseline:

```
# All rules from <PATH-TO-SHARED-AGENTS-MD> apply as baseline.
```

---

## Workspace Overview

This workspace serves two purposes:

1. **Ad-hoc investigation** — Quick debugging, error analysis, research, log analysis.
   No specific project context. Work may be ephemeral.
2. **Multi-repo task coordination** — Long-running tasks or epics that span many repositories.
   Persistent state files track progress across sessions.

## Organisation Context

Update these placeholders to match your setup:

- **GitHub org**: `<YOUR-GITHUB-ORG>` (e.g. `https://github.com/<YOUR-GITHUB-ORG>/<repo>`)
- **Issue tracker project**: `<YOUR-JIRA-PROJECT>` (e.g. `PLAT`, `OPS`, `INFRA`)
- **Dependency bot**: `<YOUR-RENOVATE-OR-DEPENDABOT-USER>` (used to identify automated PRs)

---

## Task Folders

Long-running work lives in `tasks/<TASK-ID>/` folders (e.g. `tasks/<YOUR-JIRA-PROJECT>-123/`).

When the user references a task ID (e.g. `<YOUR-JIRA-PROJECT>-123`):

1. Check `tasks/<TASK-ID>/` for context files
2. Read available files to understand current state before proceeding
3. Look for session resume files (`SESSION-RESUME-*.md`) for recent handoff notes
4. Check for `.dogcats/` subdirectory for local issue tracking

### Task Folder Conventions

- Each task folder may contain: guides, status reports, session state, helper scripts,
  communication archives
- File naming: descriptive names — no need for task ID prefix (the folder provides context)
- Session state files: `SESSION-RESUME-<date>.md` format for handoff between sessions
- Dogcat (`dcat`): may be initialised per task folder for local issue tracking with optional
  issue-tracker sync

---

## Dogcat (dcat) Integration

Task folders may contain their own `.dogcats/` directory for issue tracking.

```bash
# From within a task folder:
dcat ready                    # Find available issues
dcat show <id>                # View issue details
dcat list --status open       # Browse issues
```

When working on a task with dcat:

- Check for `.dogcats/` in the task folder
- Use dcat commands from within the task folder (or use `dcat -C <path>`)
- Dcat-to-Jira sync is optional in this workspace — only sync if explicitly asked

---

## Git Behaviour

- **This repo is direct-commit to main** — no branches, no PRs
- **Most content is gitignored** — task folders and ad-hoc files are NOT tracked
- Only infrastructure files (`.gitignore`, `AGENTS.md`, `README.md`) are committed
- To track a specific file: `git add -f <path>` (only when the user explicitly asks)
- Do NOT commit task files unless the user specifically requests it

---

## Working Style

### Relaxed Rules (compared to a production-code context)

- **No task IDs required** for ad-hoc investigation
- **No mandatory issue-tracker sync** — sync only when explicitly asked
- **Pragmatic documentation** — notes and findings over formal docs
- **Experimentation encouraged** — try approaches, prototype solutions
- **No PR workflow** — direct commit to main when committing

### Standards That Still Apply

- **Security** — never write secrets, tokens, cloud credentials, or PII into files
- **Code quality basics** — if writing scripts or code, keep it clean and readable
- **Clear communication** — summarise findings, provide actionable recommendations
- **File organisation** — keep task-specific files in their task folder, ad-hoc files in root

---

## Session Continuity

When ending a session or when the user asks to save state:

1. Create or update `tasks/<TASK-ID>/SESSION-RESUME-<date>.md` with:
   - What was accomplished this session
   - What is pending / in progress
   - Key context files and their purpose
   - Next steps for resuming
2. This enables the next session to quickly pick up where work left off

When starting a session on an existing task:

1. Read the most recent `SESSION-RESUME-*.md` file
2. Review current status of dcat issues (if applicable)
3. Summarise the current state before proceeding
