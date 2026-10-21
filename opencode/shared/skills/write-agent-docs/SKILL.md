---
name: write-agent-docs
description: "Pre-flight checklist for writing NEW agent definitions, AGENTS.md content, or skill files correctly the first time — covers Bobiverse naming, least-privilege permission scoping, bob.md roster registration, skill-vs-agent decisions, and the mandatory verification script. Complements audit-agent-docs (which reviews existing content after the fact) by front-loading the same standards before content is written."
---

# write-agent-docs Skill

A pre-flight checklist for authoring **new** agent definitions, `AGENTS.md`
content, or `SKILL.md` files in this OpenCode repo. Where `audit-agent-docs`
audits existing documentation after the fact across eleven analytical lenses,
this skill front-loads the same standards *before* you write anything — so
new agents and skills are correct, least-privilege, and discoverable on the
first pass.

Load this skill whenever you (or an agent you're advising) are about to:

- Create a new agent `.md` file under `agents/` or a context overlay's `agents/`
- Create a new `SKILL.md` under `shared/skills/` or a context overlay's `skills/`
- Add or substantially extend an `AGENTS.md` file

## Schema Authority — Don't Duplicate It Here

This skill does **not** restate the OpenCode frontmatter schema (permission
shapes, `mode`, `model`, `variant`, `temperature`, etc.). That schema evolves
independently of this repo's conventions.

**Authoritative reference:** the built-in `customize-opencode` skill. Load it
for exact field shapes, valid enum values, and permission object structure.
Its ultimate source of truth is `https://opencode.ai/config.json`.

This skill is the value-add layer on top of that schema: **this repo's own
conventions** for naming, permission philosophy, roster registration, and
verification.

## 1. Bobiverse Naming

Every new primary/subagent-mode agent needs a name that fits the Bobiverse
convention (Dennis E. Taylor's "We Are Legion (We Are Bob)" series).

1. Read `agents/BOBIVERSE-NAMING.md`.
2. Check the **"Unused Characters (Available for Future Agents)"** table for
   a character whose personality/traits fit the new agent's role. E.g.
   *Butterworth* (plans/provides) → planning agent, *SUDDAR* (self-updating
   detection array) → monitoring agent.
3. Add the chosen name to the **"Active Agent Mapping"** table with a
   one-line rationale, matching the existing row format:

   ```
   | **@newname** (short role tag) | Character — trait summary | Why this name fits, one sentence. |
   ```

4. **Do NOT put any Bobiverse lore in the agent's own `.md` file body.**
   `BOBIVERSE-NAMING.md` itself states this explicitly: lore belongs only in
   the naming reference, never in the agent definition, because it can cause
   the LLM to roleplay instead of work. The agent's own file should open with
   a short, plain statement of role (see existing agents — none of them
   narrate backstory beyond a one-line "you are a **X**, like Y" callout, if
   that).

Some support agents (e.g. review agents named after real people like
`@homer-python`, `@garfield-go`) don't map to Bobiverse characters at all —
follow whatever pattern the *category* of agent already uses (e.g. language
reviewers are named after unrelated pop-culture references keyed to the
language, not Bobiverse characters). Check sibling agents in the same
category before assuming Bobiverse naming applies.

## 2. Permission Scoping — Least Privilege by Default

Every new agent should be scoped to the minimum permissions its job requires.
Default to `deny` and allow narrowly. Three real patterns from this repo:

**Read-only reviewer** (`archimedes-css.md`) — no mutation capability at all:

```yaml
permission:
  read: allow
  glob: allow
  grep: allow
  write: deny
  edit: deny
  bash:
    "*": deny
    "cat*": allow
    "git diff*": allow
    "git log*": allow
    "git status*": allow
    "grep*": allow
    # ...narrow read-only allowlist, nothing that mutates state
```

**Scoped mutation for a single narrow purpose** (`guppi.md`) — `edit: allow`
globally, but the agent's own prose narrows *when* it may be used:

```yaml
permission:
  write: deny
  edit: allow   # only for conflict resolution — enforced by written policy, not YAML
  bash:
    "gh pr merge*": deny   # explicit deny carve-out even within an allowed prefix
    "*": deny
    "git *": allow
    "gh *": allow
```

> Guppi's own body then states: *"Edit permission is for conflict resolution
> only... Never edit files for any other purpose."* — the YAML grants the
> capability, the prose constrains its use. Don't rely on prose alone if a
> tighter YAML scope is possible; use prose only for policy that YAML can't
> express (e.g. "under what circumstances").

**Verifier that must not spawn sub-agents** (`bridget.md`):

```yaml
permission:
  read: allow
  write: deny
  edit: deny
  webfetch: deny
  bash:
    "*": deny
    "dcat close*": deny   # explicit deny even for an allowed-prefix command
    "npm test*": allow
    "go test*": allow
    "python3 -m pytest*": allow
```

Note there's no `task: deny` shown in `bridget.md`'s frontmatter directly, but
the same principle applies from `jeeves-comments.md`, which explicitly denies
task spawning for a thin reviewer that only needs to load one skill:

```yaml
permission:
  write: deny
  edit: deny
  task: deny        # reviewers/verifiers are specialists, not coordinators
  skill:
    "comment-review": allow   # scope skill access to exactly what's needed
```

**Rule of thumb:**

- If the agent reviews/verifies but never changes files → `write: deny`,
  `edit: deny`, and `task: deny` (it must not spawn other agents either).
- If the agent mutates files for one specific narrow reason → grant the
  capability but write an explicit prose constraint on when it applies, and
  add an explicit `deny` for any dangerous sub-command that would otherwise
  match an `allow` prefix (see `"gh pr merge*": deny` above).
- Default the `bash` map's `"*"` to `deny` and allowlist specific command
  prefixes — never leave `bash: allow` unscoped.
- If the agent only needs one skill's content, scope `permission.skill` to
  that skill name explicitly rather than leaving skill loading unscoped.

## 3. Roster Registration

New agents intended to be addressable in the swarm (primary or subagent mode,
not `hidden: true` internal helpers) almost always need a row in
`agents/bob.md`'s roster table, under `## The Replicant Swarm`. Match
the exact column format:

```markdown
| **@newagent** | Purpose (short) | When to Use (longer guidance, including caveats/scope boundaries) |
```

Look at the existing table for the tone: purpose is terse (a few words),
"when to use" carries the nuance — including any read-only or scope warnings
(compare how `@mario`'s row is flagged **(READ-ONLY - NEVER edits/writes)**
and repeated as a blockquote warning immediately below the table).

Hidden/internal agents (like `guppi.md` with `hidden: true`, invoked only by
@bob with an operation name) may be documented differently or omitted from
the user-facing roster — check whether the agent is meant to be called
directly by a human before assuming a roster row is required.

## 4. Skill vs. Agent — Which One Do You Need?

**Write a `SKILL.md`** when the new capability is:

- Reference/workflow content that doesn't need its own model, permissions, or
  persona — it's knowledge or a procedure to be *loaded into* an existing
  agent's context (e.g. `comment-review`'s twelve lenses, loaded by
  `@jeeves-comments`; or this skill, loaded by whoever's authoring docs).
- Reusable across multiple agents, or usable directly by @bob without a
  dedicated persona.
- Not something that needs its own least-privilege permission boundary — it
  inherits the permissions of whichever agent loads it.

**Write a `agents/<name>.md`** when the new capability is:

- A distinct specialist with its own permission boundary, model choice, and
  persona — something @bob should be able to address by name and delegate a
  task to (e.g. a new language reviewer, a new verification specialist).
  Needs a roster row (see §3) so it's discoverable in the swarm.
- Something that needs to say "no" to certain tool calls independently of
  whatever called it (permission enforcement is per-agent, not per-skill).

**Rule of thumb:** if you're tempted to write "an agent that just loads one
skill and does nothing else" (like `jeeves-comments.md` loading
`comment-review`), that's often correct — the *skill* holds the reusable
lens/procedure content, the *agent* holds the permission boundary and persona
that makes it addressable and safely scoped in the swarm.

## 5. Discoverability

Check `shared/README.md`'s description of `skills/` ("skills that can be used
in any context") — as of this writing there is no per-skill index/listing
section to update (only that one generic mention). If a skills-listing
section exists by the time you read this (check `README.md` and
`shared/README.md` for a table similar to the agent roster in `bob.md`), add
an entry there matching its format. If no such section exists, don't invent
one — flag it to @bob instead so the decision to add an index is made
deliberately.

## 6. Mandatory Verification

After **any** edit to files under `agents/` (new agent file, edited
frontmatter, anything), run from `opencode/` (the directory containing `agents/` and `shared/`):

```bash
shared/scripts/run-analyzer.sh -d agents -q -e
```

This checks for `BAD_INDENT` (non-2-space YAML frontmatter indentation) and
`DUPLICATE_KEY` (duplicate keys at any nesting level). **Do not report the
new agent as done until this passes with a zero exit code.** New `SKILL.md`
files under `shared/skills/` are not covered by this analyzer (it targets
`agents/` specifically) — run it anyway after any agent-file edits
made alongside a new skill, since skills are often added together with a
thin loader agent.

## Final Pre-Commit Checklist

Before considering a new agent or skill "done":

- [ ] Frontmatter validated against the `customize-opencode` skill's schema
      (correct `mode`, `permission` shape, valid enum values)
- [ ] Agent name checked against `BOBIVERSE-NAMING.md` (Bobiverse convention)
      or the sibling naming pattern for its category (e.g. language reviewers)
- [ ] If Bobiverse-named: row added to `BOBIVERSE-NAMING.md`'s "Active Agent
      Mapping" table with rationale; character removed from mental "unused" list
- [ ] **No Bobiverse lore in the agent's own `.md` file body** — role
      description only
- [ ] Permissions scoped least-privilege: mutation capabilities (`write`,
      `edit`, `bash` allowlist, `task`) denied by default and allowed only
      where the role requires it, with explicit `deny` carve-outs for
      dangerous sub-commands within any allowed prefix
- [ ] If addressable in the swarm: row added to `bob.md`'s roster table in
      the exact column format, including any scope/safety caveats
- [ ] Confirmed skill-vs-agent choice matches §4's rule of thumb
- [ ] Checked `README.md` / `shared/README.md` for a skills index to update
      (none exists as of writing — flag to @bob if you believe one should)
- [ ] `shared/scripts/run-analyzer.sh -d agents -q -e` run from
      `opencode/` and passing (exit code 0)

## Attribution

Designed as the write-time companion to `audit-agent-docs` (itself adapted
from [oroddlokken/slop](https://github.com/oroddlokken/slop)).
