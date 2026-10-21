# Multi-Agent System

This directory contains specialized agent definitions for OpenCode. These agents work together as a coordinated swarm to handle different aspects of software development.

## A note on dogcat

Several agents reference [`dcat`](https://github.com/oroddlokken/dogcat) (aka dogcat) — a lightweight, file-based issue tracker for AI agents by [@oroddlokken](https://github.com/oroddlokken). Install via `brew install oroddlokken/tap/dogcat` or `uv tool install dogcat`. If you don't use dogcat, you can safely ignore or strip those sections — the agents work fine without it.

The `dcat-jira` references are to a private wrapper script that syncs dogcat issues with Jira; it's not included here.

## Agent Overview

### Primary Coordinators (mode: primary)

**@bob** - Strategic intelligence coordinator

- Model: sonnet-5.5
- Purpose: Delegates work to specialized agents, synthesizes findings
- Use when: Complex multi-step tasks, need to coordinate multiple agents
- Key feature: Mandatory approval protocol before implementation
- Git workflow: Automatically orchestrates branch → PR → commits → ready workflow

### Git Workflow Agent (mode: subagent, hidden)

**@guppi** - Consolidated git workflow operations

- Model: haiku-5.5 (fast, cost-effective)
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

# 2b. Sync with main if needed
"@bob sync with main"
# → @guppi (sync): merges origin/main, resolves trivial conflicts

# 3. Mark ready
"@bob this is ready for review"
# → @guppi (pr-ready): PR #123 marked ready

# 4. Merge after approval (human-only operation)
"@bob merge this PR"
# → Human merges via GitHub UI or CLI

# Result: One PR with 2+ commits, merged cleanly
```

**Direct-commit repo (dotfiles.git):**

```bash
"@bob add new git workflow agents"
# Detects dotfiles.git → skips branch/PR
# → @riker implements
# → @guppi (commit-and-push): asks confirmation, commits to main

# Result: Direct commit to main (no PR)
```

### Implementation & Testing (mode: all)

**@riker** - Implementation worker

- Model: sonnet-5.5
- Purpose: Features, bug fixes, refactoring, hands-on coding
- Cannot: Spawn other agents, make architectural decisions
- Best for: Well-defined coding tasks

### Analysis & Security (mode: all, except @henry-wiz which is mode: subagent)

**@bill** - Architecture analyst

- Model: opus-5.5 (deep reasoning)
- Purpose: Design decisions, refactoring strategies, trade-off analysis
- Best for: When you need to think through complex architectural choices

**@linus** - Security reviewer

- Model: sonnet-5.5 (smart enough for security)
- Purpose: Vulnerability detection, OWASP Top 10, secrets scanning
- Best for: Pre-deployment security audits

**@henry-wiz** - Wiz Code scan triage specialist

- Model: sonnet-5.5
- Purpose: Wiz Code scan triage, exception management, vulnerability assessment
- Best for: Wiz Code PR/VCS/CLI scan findings, exception recommendations, paranoid-mode security reviews

**@bridget** - Goal-backward verification specialist

- Model: sonnet-5.5 (smart enough for verification)
- Purpose: Verifies that implementations achieve their stated goals by deriving observable truths and checking artifacts, wiring, and key integration points
- Best for: Post-implementation verification and goal alignment checks
- Key feature: READ-ONLY but can run tests to verify behavior

---

### Cross-Model Critique (VEHEMENT)

The VEHEMENT team provides independent critique from non-Claude model families, invoked by @bob on plans and implementations (read-only, hidden subagents):

- **@vehement-gpt** - GPT-family critique; the default single reviewer for general cross-model critique
- **@vehement-gemini** - Gemini-family critique; joins for high-complexity or security-sensitive work
- **@vehement-kimi** - Kimi-family critique specialized in over-engineering detection; currently disabled (`disable: true` in its frontmatter)

---

### Subagents (mode: subagent)

**@guppi** - Git workflow operations (hidden)

- Model: haiku-5.5 (fast)
- Purpose: Handles complete git lifecycle (branch, worktree, commit, push, PR management)
- Visibility: Hidden from autocomplete, invoked by @bob
- Operations: `create-branch`, `commit-and-push`, `sync`, `rebase`, `pr-ready`

**@mario** - Quick reconnaissance (hidden)

- Model: haiku-5.5 (fast)
- Purpose: Read-only searches, file lookups, web research
- Visibility: Hidden from autocomplete, invoked by @bob or via @mention
- Strictly read-only: Cannot edit or write files

**@calvin** - Test generation specialist

- Model: haiku-5.5 (fast)
- Purpose: Unit tests, integration tests, test fixtures
- Visibility: Visible in @mention autocomplete
- Best for: Adding test coverage to existing code

### Code Reviewers (mode: all)

Language-specific reviewers (model per agent frontmatter; @archimedes-css and @milo-html use haiku-5.5, the rest sonnet-5.5):

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

### Cross-Cutting Reviewers

Unlike the language-specific reviewers above, these agents review a specific *dimension* of quality across any file type or language.

| Agent | Focus |
|-------|-------|
| **@jeeves-comments** | Comment, docstring, and code-describing documentation prose quality — staleness, contradiction with code, restatement, noise, missing rationale, machine-written filler. Loads the `comment-review` skill for its lens definitions. |
| **@heaven-config** | Application-level configuration surfaces — `.env` files, app YAML/JSON/TOML config, docker-compose. Sample-key drift, unsafe defaults, missing-key failure modes, naming/precedence inconsistency, secret handling. Explicitly excludes Terraform (`@howard-terraform`), Helm (`@roamer-helm`), GitOps/Kubernetes manifests (`@skippy-gitops`), and CI/CD workflow YAML. |

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

- **Haiku (5.5)**: Fast, cost-effective; used by some agents (e.g. @mario, @calvin, @guppi, @archimedes-css, @milo-html, @heaven-config)
- **Sonnet (5.5)**: Balanced; used by @bob, @riker, @linus, and most code reviewers
- **GPT / Gemini / Kimi**: Non-Claude models used by the VEHEMENT critique agents
- **Opus (5.5)**: Deep reasoning for strategy, architecture, complex decisions

This keeps costs reasonable while maintaining quality where it matters.

## Validation

Run the agent analyzer from `opencode/` to validate all agent configurations:

```bash
shared/scripts/run-analyzer.sh -d agents -q -e
```

With `-q`, success is silent (exit code 0). Drop `-q` to see the per-agent tables, with one entry per agent definition and a Total agents count.

## Adding New Agents

1. Create `agent-name.md` in this directory
2. Add YAML frontmatter with `mode`, `model`, `temperature`, `permission`
3. Run `shared/scripts/run-analyzer.sh -d agents -q -e` to validate
4. Test the agent
5. Update this README

## Permission System

Agents have granular bash command permissions to enforce their roles:

- **@bob**: Read-only, limited bash (dcat, git read commands)
- **@riker**: Can edit/write, no git commit
- **@mario**: Strictly read-only
- **@linus**: Read-only for security reasons
- **Code reviewers**: Read-only

This prevents accidents and enforces agent specialization.
