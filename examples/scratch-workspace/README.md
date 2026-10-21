# Scratch Workspace — Template

A reusable template for a **scratch/coordination workspace**: a local git repo that serves as
your personal scratchpad for ad-hoc investigation and as a coordination hub for long-running
multi-repo tasks.

This is **not** an application repository. It has no build system, no deployable artefacts, and
no required CI pipeline. Its value is in keeping a lightweight, structured place for context that
doesn't belong in any one project repo.

---

## What this workspace is for

| Use case | Example |
|---|---|
| **Ad-hoc investigation** | Analysing a bug, parsing logs, writing a one-off script |
| **Multi-repo task coordination** | Tracking an epic that touches 5 repos over 3 weeks |
| **Agent context** | Giving AI agents a stable `AGENTS.md` and task-folder structure |
| **Session continuity** | Leaving breadcrumbs so the next session picks up exactly where you left |

---

## Quick setup

```bash
# 1. Clone or copy this template somewhere convenient
git clone <this-repo> ~/my-scratch   # or any path you like
cd ~/my-scratch

# 2. Customise AGENTS.md
#    Replace placeholders like <YOUR-ORG>, <YOUR-JIRA-PROJECT> with your values.

# 3. (Optional) Initialise dogcat for local issue tracking
#    https://github.com/oroddlokken/dogcat
brew install oroddlokken/tap/dogcat
dcat init

# 4. (Optional) Install OpenCode and point it at this workspace
#    https://opencode.ai/
#    The bundled AGENTS.md is picked up automatically.

# 5. (Optional) Add the shell aliases from "Shell aliases" below

# 6. Start working — create a task folder for any long-running work
mkdir -p tasks/<TASK-ID>
```

---

## Directory layout

```
~/my-scratch/                  ← workspace root (tracked by git)
├── AGENTS.md                  ← agent rules for this workspace (tracked)
├── README.md                  ← this file (tracked)
├── .gitignore                 ← inverse-whitelist: most content ignored (tracked)
├── LICENSE                    ← license text (tracked)
│
├── tasks/                     ← long-running task folders (gitignored by default)
│   └── <TASK-ID>/
│       ├── SESSION-RESUME-<date>.md   ← handoff notes between sessions
│       ├── notes.md                   ← free-form investigation notes
│       ├── *.sh                       ← helper scripts
│       └── .dogcats/                  ← optional per-task issue tracking
│
└── <ad-hoc-files>             ← ephemeral scripts, snippets, etc. (gitignored)
```

---

## Shell aliases (optional)

Designed for use with [opencode](https://opencode.ai). Add to `~/.zshrc` / `~/.bashrc`,
adjusting the path and agent name to your setup:

```bash
# Quick scratch session — ad-hoc investigation, no task context
alias ocx="opencode ~/my-scratch --agent bob"

# Task-focused session — creates the folder if needed, injects context via --prompt
ocxt() {
    local task_id="${1:?Usage: ocxt <TASK-ID>}"
    local task_dir="$HOME/my-scratch/tasks/$task_id"
    mkdir -p "$task_dir"
    opencode "$HOME/my-scratch" --agent bob \
        --prompt "Working on task $task_id. Context files are in tasks/$task_id/. Read the files there to understand current state before proceeding."
}
```

Usage: `ocx` for ad-hoc work, `ocxt <YOUR-JIRA-PROJECT>-123` for a task-focused session.
Reload your shell afterwards (`exec zsh` or `source ~/.bashrc`).

### MCP configuration

If you use MCP servers, an `opencode.json` symlink in the workspace root can point at your
real config (e.g. `ln -s ~/opencode.json opencode.json`) so the servers are available here.
It is gitignored by default; ignore this if you don't use MCP.

### Direct-commit repository

This repo is meant for direct commits to main (no branches or PRs). If your opencode setup
uses git-workflow orchestration, add this repo to its direct-commit list.

### Clean committed files

When agents work on other repos from this workspace, files they commit must stay free of
ticket references, PR numbers and process commentary — see `AGENTS.md`.

---

## Optional tooling

### OpenCode agent rules (`AGENTS.md`)

The bundled `AGENTS.md` gives AI agents (OpenCode, Claude Code, etc.) instructions
specific to this workspace:

- Workspace purpose and working style
- Task-folder conventions and session-continuity protocol
- Git behaviour (direct-to-main, most content gitignored)
- Optional dcat / Jira integration hints

Edit it to match your organisation and workflow. Replace all `<YOUR-*>` placeholders.

### dogcat / dcat — local issue tracking

[dogcat](https://github.com/oroddlokken/dogcat) (`dcat`) is a lightweight, file-based issue
tracker designed for AI-agent workflows. Each task folder can have its own `.dogcats/` store.

```bash
# Inside a task folder:
dcat init                    # initialise issue tracking
dcat create "Fix auth bug"   # create an issue
dcat ready                   # list available work
dcat show <id>               # view issue details
```

Optional Jira sync is available via `dcat-jira` if your team uses Jira.
See the dogcat docs for configuration.

### Jira / GitHub integration (optional)

If you coordinate work across Jira and GitHub, update `AGENTS.md` with:

- `<YOUR-JIRA-PROJECT>` — your Jira project key (e.g. `PLAT`, `OPS`)
- `<YOUR-GITHUB-ORG>` — your GitHub organisation slug

Agents can then reference Jira issue keys and GitHub URLs without extra disambiguation.

---

## Public-safety checklist

> ⚠️ **Before pushing this workspace or any task content to a public repo**, review:

- [ ] No secrets, tokens, API keys, or passwords anywhere (including notes)
- [ ] No cloud provider credentials or CLI state files (AWS `~/.aws/`, Azure `~/.azure/`, etc.)
- [ ] No kubeconfig files or SSH private keys (`id_rsa`, `id_ed25519`, etc.)
- [ ] No internal URLs, hostnames, or IP addresses
- [ ] No customer data, PII, or confidential business information
- [ ] `tasks/` folders are gitignored — verify with `git status` before any `git add`
- [ ] **`SESSION-RESUME-*.md` files are hard-denied in `.gitignore`** — these files accumulate
  task context (issue keys, internal org names, URLs, coordination state) and should **never**
  be published without explicit sanitisation. If you need to share a session-resume file,
  sanitise it first and save it under a different name.
- [ ] `.dogcats/` directories are gitignored
- [ ] Log files, cert files, key files are gitignored
- [ ] Replace all real org/team/project names with `<YOUR-*>` placeholders before sharing

The bundled `.gitignore` uses an **inverse whitelist** — only explicitly listed infrastructure
files are tracked. Everything else is ignored by default. This means ad-hoc work and task state
**cannot be accidentally committed**.

To deliberately track a specific file:

```bash
git add -f path/to/file.md    # force-add an otherwise-ignored file
```

---

## Licence

MIT — adapt freely.
