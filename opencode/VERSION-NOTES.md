# Version notes

This directory is the **final snapshot targeting OpenCode 1.x**
(`opencode` 1.19.3, `@opencode-ai/plugin` 1.4.6). It is marked by the git tag
`opencode-1.x-final`.

Conventions below may change in later releases. If something here doesn't work on a
newer OpenCode, check the tag against your installed version first.

## 1.x conventions used

### Agents (`agents/*.md`)

- Markdown with YAML frontmatter. Keys used: `description`, `mode` (`primary`, `subagent` or `all`),
  `model`, `temperature`, `variant`, `hidden`, `disable`, `options`.
- Permissions live in a `permission:` block: `allow`/`deny` values, glob maps per tool
  (e.g. bash command patterns), `external_directory`, skill allow-lists, and `task`
  (which sub-agents may be spawned).
- **No legacy `tools:` key** — use `permission:` instead.
- Model ids use `provider/model` style, e.g. `github-copilot/<model>`.
- Disabled agents: keep the file, set `disable: true` (see `vehement-kimi` pattern) so the
  definition stays around without being offered.
- Agent files are verified with a YAML indentation/duplicate-key check before use.

### Skills

- A directory per skill containing a `SKILL.md` (frontmatter: `name`, `description`).

### Commands

- Markdown files; frontmatter carries `description` and `argument-hint`, body is the prompt.

### Layout

In this repo, `agents/` sits next to `shared/` (which holds skills and scripts). In a live
install, the `~/.config/opencode/{agents,commands,skills}` symlinks point into a shared
directory, and `opencode.json` can likewise be a symlink to a context-specific file:

```
~/.config/opencode/agents   -> <shared-dir>/agents
~/.config/opencode/commands -> <shared-dir>/commands
~/.config/opencode/skills   -> <shared-dir>/skills
~/.config/opencode/opencode.json -> <context-specific opencode.json>
```

(`<shared-dir>` is wherever you keep your own copy; it need not mirror this repo's layout.)

### MCP servers (`opencode.json`)

```jsonc
{
  "mcp": {
    "my-server": {
      "type": "local",
      "command": ["npx", "-y", "some-mcp-server"],
      "enabled": true,
      "environment": { "API_TOKEN": "{env:API_TOKEN}" }
    }
  }
}
```

Tools from MCP servers are addressed as `mcp__<server>__<tool>` in permissions.
Never put real secrets in the file; reference environment variables.

### Plugins

- No plugin source is included in this repo. Plugins are TypeScript modules written against
  `@opencode-ai/plugin`.
- A `tool.execute.after` hook runs after a tool call and receives the tool name (`input.tool`)
  and the result (`output.output`). In a small experiment, replacing `output.output` in this
  hook changed what the model saw, so it can be used for post-processing tool output.
- Plugins are loaded once at startup; restart OpenCode after changing a plugin or the
  environment variables it reads.

## Re-check when moving to 2.x

- [ ] Agent frontmatter keys still valid (`mode`, `variant`, `hidden`, `disable`, `options`)
- [ ] `permission:` schema (glob maps, `external_directory`, skill allow-lists, `task`)
- [ ] Skill discovery path and `SKILL.md` frontmatter
- [ ] Command frontmatter (`description`, `argument-hint`)
- [ ] Symlink layout under `~/.config/opencode/` still the expected config location
- [ ] MCP declaration shape and `mcp__<server>__<tool>` naming
- [ ] Plugin API and the `tool.execute.after` hook signature
- [ ] Model id naming for providers (`github-copilot/<model>`)
- [ ] Disabled-agent handling
