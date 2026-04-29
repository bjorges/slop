# AGENTS.md — slop

Instructions for AI agents (and humans) contributing to this **public** repository.

This repo shares snippets of my OpenCode/Claude Code setup. The originals live in a private dotfiles tree alongside customer- and employer-specific configuration. **Everything published here must be sanitized first.** This file defines what "sanitized" means and how to verify it before committing.

## Repo workflow

- This is a **direct-commit-to-main** repo. No PRs, no branches.
- Local development first. Review the diff. Run the sanitization gate (see below). Then commit and push.
- Commits go through `@guppi` (`commit-and-push`). All file edits go through `@riker`.

## Sanitization rules

When copying or adapting content from a private source into this repo, **remove or generalize**:

1. **Customer / employer identifiers** — company names, internal codenames, product names, team names. Replace with generic placeholders (`example`, `mycompany`, `my-service`).
2. **Internal Jira / issue tracker keys** — e.g. real project keys like `PLT-123`, `PAYWALL-456`. Replace with `PROJ-123` or similar generic examples.
3. **Internal URLs** — `*.atlassian.net` instances tied to a company, internal git hosts, internal wikis, internal Slack channels. Strip or replace with `example.atlassian.net` style placeholders.
4. **Personal paths that leak identity beyond the public GitHub handle** — e.g. `/Users/<realname>/git/<company>/<product>/...`. Replace with `~/git/example/my-service/...`.
5. **Secrets, tokens, API keys** — even examples that *look* real. If an example is needed, use obviously fake values like `sk-EXAMPLE...` or `ghp_EXAMPLE...`.
6. **Real names of colleagues, managers, customers** — strip or replace with placeholders.
7. **Specific personal repos that shouldn't be advertised** — e.g. `git@github.com:user/private-repo.git`. Use `git@github.com:user/dotfiles.git` style placeholders unless the repo is genuinely public and intentionally referenced.
8. **Employer-specific compliance text or workflow assumptions** that don't generalize. Either strip or rewrite as generic guidance.

**What is OK to keep:**
- The public GitHub handle `bjorges` (this repo lives under it).
- References to public tools like [`dogcat`/`dcat`](https://github.com/oroddlokken/dogcat) — these are public and intentionally referenced.
- The Bobiverse-themed agent names and personas.
- Generic placeholders introduced during sanitization.

## Mandatory pre-commit review gate

Before **every** commit to this repo, the agent MUST:

1. **Stage the changes** (do not commit yet).
2. **Run `@linus`** as a reviewer with the following directive:

   > "You are reviewing a staged change to a PUBLIC repository. Audit the staged diff and any untracked files for sensitive content per `AGENTS.md` sanitization rules: customer/employer identifiers, internal Jira keys, internal URLs, identity-leaking paths, secrets, real names of colleagues, and any other content that should not be public. Report PASS or FAIL with specific file/line citations for any findings."

3. **If `@linus` reports FAIL** — fix the findings (delegate to `@riker`), then re-run `@linus`. Do not commit until PASS.
4. **If `@linus` reports PASS** — proceed to `@guppi (commit-and-push)`.

This gate is **non-negotiable**. Even for a one-line typo fix. The cost of a single leak is much higher than the cost of running the review.

## Quick self-check (for humans)

Before pushing, run a residual-string grep against the patterns you know are sensitive in your environment. Example for my setup:

```bash
grep -rEn 'spv|svai|PLT-|<my-employer>|<customer-name>' ~/git/bjorges/slop/
```

Any hit deserves a second look. `@linus` should already have caught these — this is belt-and-suspenders.

## When in doubt

Don't commit. Ask. The repo's purpose is sharing useful patterns, not racing to publish.
