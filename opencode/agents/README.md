# Multi-Agent System

This directory contains specialized agent definitions for OpenCode. These agents work together as a coordinated swarm to handle different aspects of software development.

## A note on dogcat

Several agents reference [`dcat`](https://github.com/oroddlokken/dogcat) (aka dogcat) — a lightweight, file-based issue tracker for AI agents by [@oroddlokken](https://github.com/oroddlokken). Install via `brew install oroddlokken/tap/dogcat` or `uv tool install dogcat`. If you don't use dogcat, you can safely ignore or strip those sections — the agents work fine without it.

The `dcat-jira` references are to a private wrapper script that syncs dogcat issues with Jira; it's not included here.

## Agent Overview

### Primary Coordinators (mode: primary)

**@bob** - Strategic intelligence coordinator

- Model: opus-4.6 (smartest, for strategic thinking)
- Purpose: Delegates work to specialized agents, synthesizes findings
- Use when: Complex multi-step tasks, need to coordinate multiple agents
- Key feature: Mandatory approval protocol before implementation
- Git workflow: Automatically orchestrates branch → PR → commits → ready workflow

### Git Workflow Agent (mode: subagent, hidden)

**@guppi** - Consolidated git workflow operations

- Model: haiku-4.5 (fast, cost-effective)
- Purpose: Handles complete git lifecycle — branch creation, worktrees, commits, pushes, PR creation/readiness
- Invoked by: @bob (not directly by users)
- Key features:
   - Creates worktrees at `../.worktrees/{reponame}--{flatbranch}`
   - Auto-detects [skip ci] for docs/tests/config changes
   - Runs formatters before commit (markdownlint, terraform fmt)
   - Force push protection, direct-commit repo detection
   - Draft PRs by default, structured titles (`Feat : TASK-123 Description`)

---

### Git Workflow Examples

**Standard workflow (orchestrated by @bob):**

```bash
# 1. Start work (creates branch + worktree + draft PR)
"@bob implement user auth for JIRA-456"
# → @guppi (create-branch): feat/JIRA-456-user-auth
# → Worktree at ../.worktrees/my-service--feat-JIRA-456-user-auth
# → Draft PR #123 created
# → @riker implements feature
# → @guppi (commit-and-push): "Add user authentication with JWT..."

# 2. More work (additional commits to same PR)
"@bob add password reset feature"
# → @riker implements
# → @guppi (commit-and-push): "Add password reset via email..."

# 3. Mark ready
"@bob this is ready for review"
# → @guppi (pr-ready): PR #123 marked ready

# 4. Merge after approval (human-only operation)
"@bob merge this PR"
# → Human merges via GitHub UI or CLI

# Result: One PR with 2+ commits, merged cleanly
```

**Direct-commit repo (dotfiles):**

```bash
"@bob add new git workflow agents"
# Detects dotfiles repo → skips branch/PR
# → @riker implements
# → @guppi (commit-and-push): asks confirmation, commits to main

# Result: Direct commit to main (no PR)
```

### Implementation & Testing (mode: all)

**@riker** - Implementation worker

- Model: haiku-4.5 (fast, efficient)
- Purpose: Features, bug fixes, refactoring, hands-on coding
- Cannot: Spawn other agents, make architectural decisions
- Best for: Well-defined coding tasks

### Analysis & Security (mode: all)

**@bill** - Architecture analyst

- Model: opus-4.6 (deep reasoning)
- Purpose: Design decisions, refactoring strategies, trade-off analysis
- Best for: When you need to think through complex architectural choices

**@linus** - Security reviewer

- Model: sonnet-4.6 (smart enough for security)
- Purpose: Vulnerability detection, OWASP Top 10, secrets scanning
- Best for: Pre-deployment security audits

**@bridget** - Goal-backward verification specialist

- Model: sonnet-4.6 (smart enough for verification)
- Purpose: Verifies that implementations achieve their stated goals by deriving observable truths and checking artifacts, wiring, and key integration points
- Best for: Post-implementation verification and goal alignment checks
- Key feature: READ-ONLY but can run tests to verify behavior

---

### Subagents (mode: subagent)

**@guppi** - Git workflow operations (hidden)

- Model: haiku-4.5 (fast)
- Purpose: Handles complete git lifecycle (branch, worktree, commit, push, PR management)
- Visibility: Hidden from autocomplete, invoked by @bob
- Operations: `create-branch`, `commit-and-push`, `rebase`, `pr-ready`

**@mario** - Quick reconnaissance (hidden)

- Model: haiku-4.5 (fast)
- Purpose: Read-only searches, file lookups, web research
- Visibility: Hidden from autocomplete, invoked by @bob or via @mention
- Strictly read-only: Cannot edit or write files

**@calvin** - Test generation specialist

- Model: haiku-4.5 (fast)
- Purpose: Unit tests, integration tests, test fixtures
- Visibility: Visible in @mention autocomplete
- Best for: Adding test coverage to existing code

### Code Reviewers (mode: all)

All code reviewers use sonnet-4.6 and are language-specific:

- **@homer-python** - Python (Black, Ruff, type hints, pytest)
- **@garfield-go** - Go (idiomatic patterns, error handling, concurrency)
- **@marvin-lua** - Lua (Hammerspoon, Neovim configs)
- **@goku-javascript** - Vanilla JavaScript (ES6+, DOM APIs)
- **@archimedes-css** - Modern CSS (flexbox, grid, custom properties)
- **@milo-html** - HTML/Jinja2 (semantic HTML, accessibility)
- **@arthur-zsh** - Shell scripts (Zsh/Bash best practices)
- **@howard-terraform** - Infrastructure as Code (security, best practices)
- **@roamer-helm** - Helm charts (Chart.yaml, values.yaml, templates, best practices)
- **@skippy-gitops** - GitOps/Kubernetes (Argo CD, Flux, Kustomize, environment promotion)

## Usage Examples

### Complex Feature Implementation

```
User: "I need to add user authentication"
@bob analyzes → delegates to:
   - @bill (design decisions)
   - @riker (implementation)
   - @calvin (tests)
   - @linus (security review)
   - @bridget (goal verification)
```

### Quick File Search

```
User: "Find all files containing 'authentication'"
@mario: Fast reconnaissance
```

### Security Audit Before Deployment

```
User: "@linus review src/auth/"
@linus: Scans for vulnerabilities
```

### Code Review

```
User: "@homer-python review src/api.py"
@homer-python: Language-specific review
```

## Agent Communication Protocol

When agents call other agents, they use structured JSON output:

```json
{
  "status": "COMPLETED|PARTIAL|BLOCKED|FAILED",
  "summary": "One-line description",
  "files_modified": ["path/to/file"],
  "issues_found": 0,
  "follow_up_needed": false,
  "recommended_next_agent": "@agent-name"
}
```

## Model Selection Strategy

- **Haiku (4.5)**: Fast, cost-effective for implementation, reconnaissance, testing, git operations
- **Sonnet (4.6)**: Balanced for code review, security, moderate complexity
- **Opus (4.6)**: Deep reasoning for strategy, architecture, complex decisions

This keeps costs reasonable while maintaining quality where it matters.

## Adding New Agents

1. Create `agent-name.md` in this directory
2. Add YAML frontmatter with `mode`, `model`, `temperature`, `permission`
3. Test the agent
4. Update this README

## Permission System

Agents have granular bash command permissions to enforce their roles:

- **@bob**: Read-only, limited bash (dcat, git read commands)
- **@riker**: Can edit/write, no git commit
- **@mario**: Strictly read-only
- **@linus**: Read-only for security reasons
- **Code reviewers**: Read-only

This prevents accidents and enforces agent specialization.
