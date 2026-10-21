# slop

Various slop I've made for use with [OpenCode](https://opencode.ai/) and Claude Code.

Heavily inspired by — and named after — [@oroddlokken's slop repo](https://github.com/oroddlokken/slop/). Go check his out too.

## What's in here

- [`opencode/agents/`](opencode/agents/) — my OpenCode sub-agent definitions (the Bobiverse crew). A coordinator agent (`bob`) delegates to specialists for recon, implementation, verification, code review, git workflow, and cross-model critique.
- [`examples/scratch-workspace/`](examples/scratch-workspace/) — a reusable template for a scratch/coordination workspace: a local git repo used for ad-hoc investigation and multi-repo task coordination, with agent rules, an inverse-whitelist `.gitignore`, and optional [dogcat](https://github.com/oroddlokken/dogcat) integration.

- [`opencode/`](opencode/) — also holds shared skills, commands and helper scripts, plus an [`opencode.example.json`](opencode/opencode.example.json) showing the config shape (MCP servers etc.).

> **Version note:** the `opencode/` content is the **final snapshot targeting OpenCode 1.x**, tagged `opencode-1.x-final`. See [`opencode/VERSION-NOTES.md`](opencode/VERSION-NOTES.md).

## My OpenCode agent workflow

Here's how the agents collaborate on a non-trivial task — a coordinator (`bob`) orchestrates specialists through several quality gates before any code lands.

```
🤖 My OpenCode Agent Workflow
🙋 User request
   ↓
🤖 @bob (coordinator) kicks off
   ↓
🔍 @mario — quick recon (read-only)
   ↓
┌─────────────────────────────────────────────┐
│ 🔄 THINK / DUCK LOOP (iterates!)            │
│                                             │
│   🧠 @bill ──▶ 🦆 VEHEMENT (gpt + gemini)   │
│      ▲                    │                 │
│      └────── refine ──────┘                 │
│                                             │
│   Loops until plan converges                │
└─────────────────────────────────────────────┘
   ↓
👤 User approves plan  ← hard gate
   ↓
🌱 @guppi create-branch (worktree + draft PR)
   ↓
🔨 @riker implements (parallel waves)
   ↓
🦆 VEHEMENT re-critique (optional, high-complexity)
   └─▶ may loop back to @bill ↑ or @riker ↑
   ↓
✅ @bridget — goal-backward verify (MANDATORY)
   └─▶ FAIL? back to @riker
   ↓
🔒 @linus — security review
   └─▶ Issues? back to @riker
   ↓
🧑‍🏫 Language reviewers in parallel:
   homer 🐍 • garfield 🐹 • goku 📜 • marvin 🌙
   archimedes 🎨 • milo 🏛️ • arthur 🐚
   howard ☁️ • roamer ⛵ • skippy 🚀
   └─▶ Nits? back to @riker
📝 Conditional: @jeeves-comments (comment/doc prose) and
   @heaven-config (agent/config changes) when the diff touches them
   ↓
📦 @guppi commit-and-push (logical commits)
   ↓ (repeat impl → verify → commit per unit)
🚀 @guppi pr-ready
   ↓
👤 Human merges (agents NEVER merge)
```

**Key principles:**

- 🔄 `@bill` + VEHEMENT iterate until the plan is solid
- 🛡️ `@bridget` + `@linus` are mandatory quality gates
- 🌱 ALL git mutations flow through `@guppi`
- 🧑‍🏫 Language reviewers run in parallel per file type
- 🚫 Only humans merge PRs

## Related public tooling

Several agents reference [`dogcat`](https://github.com/oroddlokken/dogcat) (`dcat`) — a lightweight, file-based issue tracker for AI agents by [@oroddlokken](https://github.com/oroddlokken). Highly recommended; install via `brew install oroddlokken/tap/dogcat` or `uv tool install dogcat`. The agents work fine without it — references can be ignored or stripped.

## No warranties

Code shared here comes with **no warranties** and may reference tooling or workflow assumptions specific to my setup. Use at your own risk, fork freely, adapt as needed.

## License

MIT — see [LICENSE](LICENSE).
