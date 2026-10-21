# opencode/shared

Sanitized snippets of my OpenCode setup. In this repo `agents/` is a sibling of `shared/`; in my live install the agents sit
under `shared/` (`~/.config/opencode/agents` is a symlink to `.../shared/agents`).
Paths in the skills and scripts are written for the layout shown here.

```
opencode/
├── agents/                # agent definitions (see agents/README.md)
├── opencode.example.json  # skeleton of the live config shape (placeholders only)
└── shared/
    ├── skills/            # on-demand skills (SKILL.md each)
    │   ├── audit-agent-docs/   # multi-lens audit of agent docs (+ rules/)
    │   ├── comment-review/     # lenses for reviewing code comments
    │   ├── skill-fitness/      # mechanical agent/skill drift checks
    │   └── write-agent-docs/   # pre-flight checklist for new agents/skills
    ├── commands/          # slash commands (web.md)
    └── scripts/           # agent_analyzer.py, run-analyzer.sh, test-agents.sh,
                           # analyze-bash-frequency.py
```

## Wiring it up

In my setup `~/.config/opencode/` contains symlinks into a checkout of this tree:

```
~/.config/opencode/agents   -> <checkout>/opencode/agents
~/.config/opencode/skills   -> <checkout>/opencode/shared/skills
~/.config/opencode/commands -> <checkout>/opencode/shared/commands
~/.config/opencode/opencode.json -> your own config, shaped like opencode.example.json
```

Skills and scripts use paths relative to this layout (`agents/`, `shared/skills/`,
`shared/scripts/`); adjust them if you place the directories differently.

## opencode.example.json notes

- `mcp.example-server`: one placeholder local MCP server. `command` is an argv list,
  `environment` holds env vars passed to the process. All values are fake.
- `permission.external_directory`: glob-to-action map controlling access outside the
  project directory; the pattern here is just an example.

## Scripts

- `run-analyzer.sh` creates a local `.venv` (gitignored), installs `rich` (network needed on first run), then runs `agent_analyzer.py`.
  Verify agent frontmatter, run from `opencode/`: `shared/scripts/run-analyzer.sh -d agents -q -e`
- `test-agents.sh` runs sanity checks against `opencode/agents`.
- `analyze-bash-frequency.py` mines local OpenCode session storage for frequent bash commands
  (`--agents-dir` / `--store-dir` override the defaults; see its docstring).

## Intentionally omitted

- `dcat-jira` and `headroom-report` scripts, and the headroom plugins (private tooling).
- `shared/AGENTS.md` (private shared rules file; several skills mention it).
- `contexts/` (work/personal overlays and their `opencode.json` files).
- Any real MCP server config, URLs, tokens, or environment values.
