#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
analyze-bash-frequency.py — surface frequently-approved bash patterns not yet in any agent allow-list.

PURPOSE
-------
Tallies bash commands executed by each agent across the OpenCode part store and
reports the top candidates for promotion to an agent's allow-list: commands that
ran frequently but aren't matched by any existing allow/deny pattern.

WHY IT EXISTS
-------------
Every time an agent runs a bash command that isn't covered by its allow-list, the
user gets an approval prompt. This script reduces that friction by identifying
high-volume approved commands that are still missing from the allow-list, so they
can be promoted without guesswork. It only suggests; it never edits anything.

DATA SOURCES
------------
- Part files:    <store>/part/<messageID>/<partID>.json
                 Fields: id, sessionID, messageID, type, tool ("bash"),
                         state.status ("completed"|"error"),
                         state.input.command, state.input.description
- Message files: <store>/message/<sessionID>/<msgID>.json
                 Fields: id, sessionID, role, agent (e.g. "riker"), model, time
                 Note: agent attribution lives on the MESSAGE, not the part.
- Agent defs:    <agents-dir>/*.md  (YAML frontmatter, permission.bash rules)

  <store> defaults to ${XDG_DATA_HOME:-~/.local/share}/opencode/storage
  (override with --store-dir). <agents-dir> defaults to the first existing of
  ../../agents relative to this script, then ~/.config/opencode/agents
  (override with --agents-dir). The script exits non-zero if either is missing.

USAGE
-----
  ./analyze-bash-frequency.py                        # top 20, all agents, min-count 2
  ./analyze-bash-frequency.py --top 5                # show only top 5 per agent
  ./analyze-bash-frequency.py --agent bob --top 10   # focus on one agent
  ./analyze-bash-frequency.py --include-covered      # sanity-check already-matched patterns
  ./analyze-bash-frequency.py --min-count 5          # suppress low-volume noise
  ./analyze-bash-frequency.py --store-dir /path/to/storage --agents-dir ./agents

CLI FLAGS
---------
  --top N           Number of top patterns to show per agent (default: 20)
  --agent NAME      Filter to a single agent name (default: all agents)
  --min-count N     Minimum occurrence count to include a pattern (default: 2)
  --include-covered Also show patterns already matched by an existing rule
  --agents-dir DIR  Directory of agent .md definitions
  --store-dir DIR   OpenCode storage dir containing part/ and message/

OUTPUT FORMAT
-------------
Each result line:
  <count>  <pattern>*    (would currently: <action>)

  <count>   — number of times this normalized pattern was executed
  <pattern> — normalized command (e.g. "git *", "npm *")
  <action>  — what the agent's current rules would do with this command today
              (allow / deny / ask — "ask" means no rule matches, falls to default)

High-count rows with "would currently: ask" are the friction candidates. Rows
whose prefix is in the dangerous set (rm, sudo, curl, ssh, git push, ...) are
flagged "review manually - do not blanket allow-list": a prefix pattern such as
"rm *" or "curl *" is far broader than any one approved invocation.

SECURITY NOTES
--------------
- Prefixes are derived conservatively: leading VAR=value assignments are
  skipped, and a second token is only kept when it looks like a plain
  subcommand (no leading '-', no '=' or ':', short). Anything else collapses to
  the first token or is dropped, so secrets passed as args/env are not echoed.
- Permission rules use OpenCode semantics: the LAST matching pattern wins.
- The report lists command prefixes from your history; treat it as private and
  write it somewhere user-private, e.g.
    (umask 077; ./analyze-bash-frequency.py > ~/.cache/bash-frequency-report.txt)

LIMITATIONS / KNOWN QUIRKS
---------------------------
- Compound "cd X && cmd" commands: the "cd" preamble is stripped before
  normalization, so the real command is what gets counted.
- Commands starting with "~/" or "/" are bucketed as "<path>" — not actionable
  as patterns since they're too specific.
- Part files larger than 200KB are skipped (they're large tool outputs, not bash calls).
- Historical agents with no current .md definition still appear in output; they
  have no patterns to compare against, so everything shows as uncovered. Use
  --agent <name> to focus on currently-defined agents.
- Performance scales with the number of part files (every file is opened);
  subsequent runs are faster due to OS page cache.
"""

import argparse
import json
import os
import re
import shlex
import sys
from collections import defaultdict
from collections.abc import Iterator
from pathlib import Path

# os is used for os.scandir (faster than pathlib on macOS for large dirs)

# ── Constants ────────────────────────────────────────────────────────────────

# Two-token prefixes for these well-known CLIs
TWO_TOKEN_CMDS = {
    "git", "gh", "kubectl", "brew", "npm", "pnpm", "yarn",
    "cargo", "docker", "helm", "kubectx", "kubens", "op",
    "aws", "gcloud", "az", "terraform", "tf",
}

# Prefixes where a blanket "<prefix> *" allow rule is risky.
DANGEROUS_PREFIXES = {
    "rm", "sudo", "curl", "wget", "dd", "chmod", "chown", "ssh", "scp",
    "eval", "bash", "sh", "su", "doas", "env", "xargs", "exec", "source",
    "zsh", "python", "python3", "node", "perl", "ruby", "npx", "kill", "mv",
    "rsync", "nc", "tee",
    "docker run", "git push", "git reset", "git clean", "kubectl delete",
    "kubectl apply", "terraform apply", "terraform destroy", "npm publish",
    "gh api",
}
DANGEROUS_NOTE = "review manually - do not blanket allow-list"

ENV_ASSIGN_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
MAX_TOKEN_LEN = 32

# Recoverable per-file read/parse failures; counted and reported, not hidden.
READ_ERRORS = (OSError, json.JSONDecodeError, UnicodeDecodeError)


# ── YAML frontmatter parser (stdlib, focused on permission.bash block) ───────

def parse_bash_permissions(md_path: Path) -> dict[str, str]:
    """
    Parse the YAML frontmatter of an agent .md file and return the
    permission.bash mapping as {pattern: action}.
    Returns {} if no bash permissions found.
    """
    try:
        text = md_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        print(f"  WARN: cannot read {md_path}: {e}", file=sys.stderr)
        return {}

    text = text.replace("\r\n", "\n")

    # Extract frontmatter between first pair of ---
    fm_match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not fm_match:
        return {}
    fm = fm_match.group(1)

    # Find the bash: block under permission:
    # We look for lines after "  bash:" (2-space indent) and collect
    # indented key-value pairs until indentation drops.
    result = {}
    in_permission = False
    in_bash = False

    for line in fm.splitlines():
        # Detect "permission:" at top level (no leading spaces)
        if re.match(r'^permission\s*:', line):
            in_permission = True
            in_bash = False
            continue

        if in_permission:
            # Detect "  bash:" (2-space indent)
            if re.match(r'^  bash\s*:', line):
                in_bash = True
                continue
            # If we hit another top-level key, stop
            if re.match(r'^\S', line):
                in_permission = False
                in_bash = False
                continue
            # If we hit a different 2-space key under permission, stop bash
            if re.match(r'^  \S', line) and not re.match(r'^  bash\s*:', line):
                in_bash = False
                continue

        if in_bash:
            # Expect lines like:    "pattern": action
            m = re.match(r'^    "([^"]+)"\s*:\s*(\S+)', line)
            if m:
                pattern, action = m.group(1), m.group(2)
                result[pattern] = action
            elif re.match(r'^  \S', line) or re.match(r'^\S', line):
                # Indentation dropped — end of bash block
                in_bash = False
                in_permission = False

    return result


# ── Command normalization ─────────────────────────────────────────────────────

_PLAIN_TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9._+-]{0,31}")
_SHELL_OPS = {"&&", "||", ";", "|", "&"}
_SHELL_META_SUBSTRINGS = (";", "|", "&", "$(", "`", "\n", ">", "<")


def _plain_token(tok: str) -> bool:
    """True if tok is a short plain word (allowlist) safe to echo in a report."""
    return _PLAIN_TOKEN_RE.fullmatch(tok) is not None


def _has_shell_meta(tokens: list[str]) -> bool:
    return any(
        t in _SHELL_OPS or any(m in t for m in _SHELL_META_SUBSTRINGS)
        for t in tokens
    )


def normalize_command(cmd: str, _depth: int = 0) -> str | None:
    """
    Return a prefix pattern string (without trailing *) or None to skip.

    Never echoes argument values: the command is tokenized shell-style (so
    quoted values stay one token), leading VAR=value assignments are skipped,
    and a second token is only used when it is a plain subcommand word.
    Unparseable or compound (pipes, ;, &&, $(...)) commands are bucketed as
    "<other>". _depth caps recursion when stripping cd preambles.
    """
    if _depth > 5:
        return None

    # shlex treats newlines as plain whitespace, so detect multi-line first
    if "\n" in cmd.strip():
        return "<other>"

    try:
        tokens = shlex.split(cmd.strip(), posix=True)
    except ValueError:
        return "<other>"
    if not tokens:
        return None

    # Strip "cd <dir> &&" preamble and re-normalize the real command
    if tokens[0] == "cd" and "&&" in tokens:
        amp_idx = tokens.index("&&")
        if amp_idx == 2 and not _has_shell_meta(tokens[:2]):
            remainder = tokens[amp_idx + 1:]
            if remainder:
                return normalize_command(shlex.join(remainder), _depth=_depth + 1)
        return "<other>"

    # Compound commands / substitutions: never attribute a benign head
    if _has_shell_meta(tokens):
        return "<other>"

    # Skip leading VAR=value environment assignments (may contain secrets)
    while tokens and ENV_ASSIGN_RE.match(tokens[0]):
        tokens.pop(0)
    if not tokens:
        return None

    first = tokens[0]

    # Skip path-based commands
    if (first.startswith("/") or first.startswith("./")
            or first.startswith("../") or first.startswith("~/")):
        return "<path>"

    if not _plain_token(first):
        return "<other>"

    if first in TWO_TOKEN_CMDS and len(tokens) >= 2 and _plain_token(tokens[1]):
        return f"{first} {tokens[1]}"

    return first


def is_dangerous(prefix: str) -> bool:
    for entry in DANGEROUS_PREFIXES:
        if " " in entry:
            if prefix == entry or prefix.startswith(entry + " "):
                return True
        elif prefix == entry or prefix.split(" ", 1)[0] == entry:
            return True
    return False


# ── Pattern matching ──────────────────────────────────────────────────────────

def _glob_match(pat: str, text: str) -> bool:
    """OpenCode-style wildcard match: '*' = any run, '?' = one char.
    A trailing ' *' also matches the bare command (e.g. 'git *' matches 'git')."""
    def to_re(p: str) -> str:
        return "".join(".*" if c == "*" else "." if c == "?" else re.escape(c) for c in p)
    if re.fullmatch(to_re(pat), text, re.DOTALL):
        return True
    return pat.endswith(" *") and re.fullmatch(to_re(pat[:-2]), text, re.DOTALL) is not None


def match_rule(prefix: str, patterns: dict[str, str]) -> tuple[str, str] | None:
    """
    Return (pattern, action) of the LAST rule matching prefix (OpenCode
    precedence: last match wins), or None. The prefix is tested bare and with
    a trailing argument so "git status*" matches "git status --short".
    """
    result = None
    for pat, action in patterns.items():
        if _glob_match(pat, prefix) or _glob_match(pat, prefix + " x"):
            result = (pat, action)
    return result


def is_covered(prefix: str, patterns: dict[str, str]) -> bool:
    """True if the winning (last) matching rule is an explicit non-default one."""
    hit = match_rule(prefix, patterns)
    return hit is not None and hit[0] != "*"


def default_action(patterns: dict[str, str]) -> str:
    return patterns.get("*", "ask")


# ── Message index builder ─────────────────────────────────────────────────────

def build_message_index(msg_store: Path, stats: dict[str, int], progress: bool = True) -> dict[str, str]:
    """
    Walk the message store and build {messageID: agentName}.
    Only messages with role != "user" and a non-empty agent field are indexed.
    Uses os.scandir for performance. Unreadable files bump stats["warnings"].
    """
    index: dict[str, str] = {}
    scanned = 0

    try:
        session_dirs = list(os.scandir(msg_store))
    except OSError as e:
        print(f"ERROR: Cannot read message store {msg_store}: {e}", file=sys.stderr)
        sys.exit(2)

    for session_entry in session_dirs:
        if not session_entry.is_dir():
            continue
        try:
            msg_entries = list(os.scandir(session_entry.path))
        except OSError:
            stats["warnings"] += 1
            continue
        for msg_entry in msg_entries:
            if not msg_entry.name.endswith(".json"):
                continue
            scanned += 1
            if progress and scanned % 1000 == 0:
                print(f"  [msg index] scanned {scanned} message files…", file=sys.stderr)
            try:
                with open(msg_entry.path, encoding="utf-8") as f:
                    data = json.load(f)
            except READ_ERRORS:
                stats["warnings"] += 1
                continue
            if not isinstance(data, dict):
                stats["warnings"] += 1
                continue
            msg_id = data.get("id", "")
            agent  = data.get("agent", "")
            role   = data.get("role", "")
            if msg_id and agent and role != "user":
                index[msg_id] = agent

    return index


# ── Part store walker ─────────────────────────────────────────────────────────

# Bash tool call parts are small — commands + output fit in a few KB typically.
# We skip files larger than this to avoid reading huge output blobs.
# (A bash part with a large output will still have a small "input.command" field,
#  but we can't easily read just that without parsing. In practice, completed bash
#  parts with large outputs are rare and we accept missing them.)
MAX_PART_SIZE = 200_000  # 200 KB — generous enough for any reasonable bash call


def walk_parts(msg_index: dict[str, str], part_store: Path, stats: dict[str, int],
               progress: bool = True) -> Iterator[tuple[str, str]]:
    """
    Yield (agent, prefix) for each completed bash tool call.
    Updates stats["scanned"], stats["skipped"], stats["warnings"] in place.
    Uses os.scandir for performance; skips files > MAX_PART_SIZE.
    """
    try:
        msg_dirs = list(os.scandir(part_store))
    except OSError as e:
        print(f"ERROR: Cannot read part store {part_store}: {e}", file=sys.stderr)
        sys.exit(2)

    for msg_dir_entry in msg_dirs:
        if not msg_dir_entry.is_dir():
            continue
        try:
            part_entries = list(os.scandir(msg_dir_entry.path))
        except OSError:
            stats["warnings"] += 1
            continue

        for part_entry in part_entries:
            if not part_entry.name.endswith(".json"):
                continue
            stats["scanned"] += 1
            if progress and stats["scanned"] % 1000 == 0:
                print(f"  [parts] scanned {stats['scanned']} part files…", file=sys.stderr)

            try:
                # Skip oversized files — they won't be simple bash calls
                if part_entry.stat().st_size > MAX_PART_SIZE:
                    stats["skipped"] += 1
                    continue

                with open(part_entry.path, "rb") as f:
                    raw = f.read()

                # Fast pre-filter: skip files that don't mention "bash"
                if b'"bash"' not in raw:
                    stats["skipped"] += 1
                    continue

                data = json.loads(raw)
            except READ_ERRORS:
                stats["warnings"] += 1
                stats["skipped"] += 1
                continue

            if not isinstance(data, dict):
                stats["warnings"] += 1
                stats["skipped"] += 1
                continue

            # Only bash tool calls
            if data.get("type") != "tool" or data.get("tool") != "bash":
                stats["skipped"] += 1
                continue

            state = data.get("state")
            if not isinstance(state, dict) or state.get("status") != "completed":
                stats["skipped"] += 1
                continue

            agent = msg_index.get(data.get("messageID", ""))
            if not agent:
                stats["skipped"] += 1
                continue

            inp = state.get("input")
            cmd = inp.get("command", "") if isinstance(inp, dict) else ""
            if not isinstance(cmd, str):
                stats["skipped"] += 1
                continue
            prefix = normalize_command(cmd)
            if not prefix or prefix in ("<path>", "<other>"):
                stats["skipped"] += 1
                continue

            yield agent, prefix


# ── Main ──────────────────────────────────────────────────────────────────────

def default_agents_dir() -> Path | None:
    candidates = [
        Path(__file__).resolve().parent.parent.parent / "agents",
        Path.home() / ".config/opencode/agents",
    ]
    return next((c for c in candidates if c.is_dir()), None)


def default_store_dir() -> Path:
    xdg = os.environ.get("XDG_DATA_HOME")
    base = Path(xdg) if xdg else Path.home() / ".local/share"
    return base / "opencode/storage"


def _positive_int(value: str) -> int:
    n = int(value)
    if n < 1:
        raise argparse.ArgumentTypeError("must be >= 1")
    return n


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze bash command frequency across OpenCode sessions."
    )
    parser.add_argument("--top", type=_positive_int, default=20,
                        help="Top N candidates per agent (default: 20)")
    parser.add_argument("--agent", type=str, default=None,
                        help="Filter to a single agent name")
    parser.add_argument("--min-count", type=_positive_int, default=2,
                        help="Minimum occurrences to include (default: 2)")
    parser.add_argument("--include-covered", action="store_true",
                        help="Also show patterns already in allow/deny list")
    parser.add_argument("--agents-dir", type=Path, default=None,
                        help="Agent .md directory (default: ../../agents next to "
                             "this script, else ~/.config/opencode/agents)")
    parser.add_argument("--store-dir", type=Path, default=None,
                        help="OpenCode storage dir with part/ and message/ "
                             "(default: $XDG_DATA_HOME or ~/.local/share, + opencode/storage)")
    args = parser.parse_args()

    agents_dir = args.agents_dir or default_agents_dir()
    if agents_dir is None or not agents_dir.is_dir():
        print(f"ERROR: agents directory not found ({agents_dir or 'no default exists'}); "
              "use --agents-dir.", file=sys.stderr)
        sys.exit(2)

    store_dir = args.store_dir or default_store_dir()
    part_store = store_dir / "part"
    msg_store = store_dir / "message"
    for label, path in (("part store", part_store), ("message store", msg_store)):
        if not path.is_dir():
            print(f"ERROR: {label} not found at {path}; use --store-dir.", file=sys.stderr)
            sys.exit(2)

    # ── Load agent permissions ────────────────────────────────────────────────
    agent_perms: dict[str, dict[str, str]] = {}
    for md_file in sorted(agents_dir.glob("*.md")):
        perms = parse_bash_permissions(md_file)
        if perms:
            agent_perms[md_file.stem] = perms

    print(f"Loaded permissions for {len(agent_perms)} agents from {agents_dir}.",
          file=sys.stderr)

    stats = {"scanned": 0, "skipped": 0, "warnings": 0}

    # ── Build message → agent index ───────────────────────────────────────────
    print("Scanning message store…", file=sys.stderr)
    msg_index = build_message_index(msg_store, stats)
    print(f"Message index: {len(msg_index)} entries.", file=sys.stderr)

    # ── Walk parts ────────────────────────────────────────────────────────────
    print("Scanning part store…", file=sys.stderr)

    # {agent: {prefix: count}}
    tallies: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for agent, prefix in walk_parts(msg_index, part_store, stats):
        if args.agent and agent != args.agent:
            continue
        tallies[agent][prefix] += 1

    print(f"Part store scan complete: {stats['scanned']} files scanned, "
          f"{stats['skipped']} skipped.", file=sys.stderr)
    if stats["warnings"]:
        print(f"WARN: {stats['warnings']} file(s)/dir(s) were unreadable or malformed "
              "and were skipped.", file=sys.stderr)
    print("", file=sys.stderr)

    # ── Report ────────────────────────────────────────────────────────────────
    agents_with_data = 0

    for agent in sorted(tallies.keys()):
        counts = tallies[agent]
        perms  = agent_perms.get(agent, {})
        deflt  = default_action(perms)

        total_calls = sum(counts.values())

        # Build candidate list (deterministic: -count, then prefix)
        candidates = []
        covered_list = []
        for prefix, count in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
            if count < args.min_count:
                continue
            if is_covered(prefix, perms):
                covered_list.append((count, prefix))
            else:
                candidates.append((count, prefix))

        if not candidates and not (args.include_covered and covered_list):
            continue

        agents_with_data += 1
        print(f"=== @{agent} (default: {deflt}) ===")
        print(f"Total bash calls: {total_calls}")
        print("Top candidates NOT in current allow/deny list:")

        shown = 0
        for count, prefix in candidates:
            if shown >= args.top:
                break
            note = f"  [{DANGEROUS_NOTE}]" if is_dangerous(prefix) else ""
            print(f"  {count:5d}  {prefix}*"
                  f"    (would currently: {deflt}){note}")
            shown += 1

        if shown == 0:
            print("  (none above min-count threshold)")

        if args.include_covered and covered_list:
            print("Already covered (for reference):")
            for count, prefix in covered_list[:args.top]:
                hit = match_rule(prefix, perms)
                action = hit[1] if hit else "?"
                print(f"  {count:5d}  {prefix}*    (matched: {action})")

        print()

    # ── Summary ───────────────────────────────────────────────────────────────
    print("─" * 60)
    print("Summary:")
    print(f"  Part files scanned : {stats['scanned']}")
    print(f"  Parts skipped      : {stats['skipped']}")
    print(f"  Unreadable/malformed: {stats['warnings']}")
    print(f"  Agents with data   : {agents_with_data}")


if __name__ == "__main__":
    main()
