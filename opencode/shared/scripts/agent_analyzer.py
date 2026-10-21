#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.12"
# dependencies = ["rich>=13,<15"]
# ///

"""
Script to analyze agent configuration files (.md files)
Reads metadata (mode, model, temperature) and organizes by type.
Includes linting functionality to validate YAML frontmatter.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import TypedDict

from rich.console import Console
from rich.markup import escape
from rich.table import Table


class AgentMetadata(TypedDict, total=False):
    """Type definition for agent metadata extracted from markdown files.

    Attributes:
        mode: The agent's operating mode (primary, all, subagent, etc.)
        model: The AI model used by the agent
        temperature: The temperature parameter for the model (0.0-1.0)
    """

    mode: str
    model: str
    temperature: float


class LintError:
    """Represents a linting error in a markdown file."""

    def __init__(self, filepath: str, line_number: int, error_type: str, message: str) -> None:
        self.filepath = filepath
        self.line_number = line_number
        self.error_type = error_type
        self.message = message

    def __str__(self) -> str:
        return f"{self.filepath}:{self.line_number} [{self.error_type}] {self.message}"


_FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---[ \t]*(?:\n|\Z)", re.DOTALL)


def extract_frontmatter(content: str) -> str | None:
    """Return the YAML frontmatter text (between leading --- markers) or None.

    CRLF line endings are normalized; a closing marker at EOF without a
    trailing newline is accepted.
    """
    match = _FRONTMATTER_RE.match(content.replace("\r\n", "\n"))
    return match.group(1) if match else None


def print2(console: Console, quiet: bool, *args: object, **kwargs: object) -> None:
    """Print to console unless quiet mode is enabled."""
    if not quiet:
        console.print(*args, **kwargs)


def lint_agent_file(filepath: Path) -> list[LintError]:
    """Lint a markdown file for YAML frontmatter issues.

    Checks for:
    1. Incorrect indentation (must be 2 spaces for nested keys)
    2. Duplicate keys within sections at any nesting level
    3. Non-numeric temperature values
    4. Unreadable files (reported as READ_ERROR)

    Args:
        filepath: Path to the markdown file to lint

    Returns:
        List of LintError objects found, empty if no issues
    """
    errors: list[LintError] = []

    try:
        content = filepath.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        return [LintError(str(filepath), 0, "READ_ERROR", f"Cannot read file: {e}")]

    yaml_content = extract_frontmatter(content)
    if yaml_content is None:
        return errors

    lines = yaml_content.split("\n")

    for line_num, line in enumerate(lines, start=2):
        temp_line = re.match(r"temperature:\s*(.+)", line)
        if temp_line:
            raw_temp = temp_line.group(1).strip()
            try:
                float(raw_temp)
            except ValueError:
                errors.append(
                    LintError(
                        str(filepath),
                        line_num,
                        "BAD_TEMPERATURE",
                        f"temperature must be a number (got {raw_temp!r})",
                    )
                )

    # Track all keys we've seen at each indentation/parent context
    # Key: (indent_level, parent_path) -> set of key names
    seen_keys: dict[tuple[int, str], set[str]] = {}

    # Stack to track parent context: list of (indent, key_name)
    parent_stack: list[tuple[int, str]] = []

    for line_num, line in enumerate(
        lines, start=2
    ):  # Line 2 is first line after opening ---
        if not line.strip():  # Skip empty lines
            continue

        # Calculate indentation
        indent = len(line) - len(line.lstrip())

        # Check indentation is 2 spaces per level
        if indent % 2 != 0:
            errors.append(
                LintError(
                    str(filepath),
                    line_num,
                    "BAD_INDENT",
                    f"Indentation must be 2-space increments (got {indent} spaces)",
                )
            )
            continue

        # Pop parent stack items that are at or deeper than current indent
        while parent_stack and parent_stack[-1][0] >= indent:
            parent_stack.pop()

        # Extract the key name
        key_match = re.match(r"(\w+|\".+?\"):", line.lstrip())
        if not key_match:
            continue

        key_name = key_match.group(1)
        indent_level = indent // 2

        # Build parent path for context
        if parent_stack:
            parent_path = ".".join(k[1] for k in parent_stack)
        else:
            parent_path = ""

        # Create unique key for tracking duplicates at this level
        depth_key = (indent_level, parent_path)

        if depth_key not in seen_keys:
            seen_keys[depth_key] = set()

        # Check if this key was already seen at this level
        if key_name in seen_keys[depth_key]:
            if parent_path:
                context = f" under '{parent_path}'"
            else:
                context = " at root level"
            errors.append(
                LintError(
                    str(filepath),
                    line_num,
                    "DUPLICATE_KEY",
                    f"Duplicate key {key_name}{context}",
                )
            )
        else:
            seen_keys[depth_key].add(key_name)

        # Add current key to parent stack for next iterations
        parent_stack.append((indent, key_name))

    return errors


def parse_agent_file(filepath: Path) -> AgentMetadata | None:
    """Parse agent metadata from markdown file.

    Extracts top-level mode/model/temperature from the YAML frontmatter.

    Args:
        filepath: Path to the markdown file to parse

    Returns:
        Dictionary with the metadata keys found, or None if the file cannot be
        read (OSError/UnicodeDecodeError) or has no frontmatter. A non-numeric
        temperature is omitted (lint_agent_file reports it).
    """
    try:
        content = filepath.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None

    yaml_content = extract_frontmatter(content)
    if yaml_content is None:
        return None

    data: AgentMetadata = {}

    mode_match = re.search(r"^mode:\s*(.+)", yaml_content, re.MULTILINE)
    if mode_match:
        data["mode"] = mode_match.group(1).strip()

    model_match = re.search(r"^model:\s*(.+)", yaml_content, re.MULTILINE)
    if model_match:
        data["model"] = model_match.group(1).strip()

    temp_match = re.search(r"^temperature:\s*(.+)", yaml_content, re.MULTILINE)
    if temp_match:
        try:
            data["temperature"] = float(temp_match.group(1).strip())
        except ValueError:
            pass  # reported by lint_agent_file as BAD_TEMPERATURE

    return data


def format_agent_name(filename: str) -> str:
    """
    Convert filename to agent name format.
    Examples: code-reviewer-css.md -> Code-Reviewer-Css
    """
    name = Path(filename).stem

    words = name.split("-")
    formatted = "-".join(word.capitalize() for word in words)
    return formatted


def create_agent_table(agents: dict[str, AgentMetadata], title: str) -> Table:
    """Create a rich Table for agents."""
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Agent", style="cyan", no_wrap=False)
    table.add_column("Model", style="green", no_wrap=False)
    table.add_column("Temperature", style="yellow", justify="right")

    for agent_name in sorted(agents.keys()):
        data = agents[agent_name]
        model = data.get("model", "N/A")
        temp = str(data.get("temperature", "N/A"))
        table.add_row(escape(agent_name), escape(model), escape(temp))

    return table


def main(args: argparse.Namespace) -> None:
    """Main execution - lint and analyze agent configuration files.

    Lints all .md files for correctness, then shows agent metadata analysis.
    """
    console = Console()
    err_console = Console(stderr=True)

    if args.parent:
        script_path = Path(__file__).resolve()
        agents_dir = script_path.parent
    elif args.directory:
        agents_dir = Path(args.directory).resolve().absolute()
    else:
        agents_dir = Path(".").resolve().absolute()

    md_files = sorted(agents_dir.glob("*.md"))
    if not md_files:
        if args.expect_agents:
            print2(
                err_console,
                False,
                f"[red]Error: Expected agent files in directory {escape(str(agents_dir))}, but none were found.[/red]",
            )
            sys.exit(1)
        print2(
            console,
            args.quiet,
            f"[yellow]No .md files found in directory: {escape(str(agents_dir))}[/yellow]",
        )
        return

    # First: Run linter
    all_errors: list[LintError] = []
    for filepath in md_files:
        errors = lint_agent_file(filepath)
        all_errors.extend(errors)

    if all_errors:
        print2(err_console, False, "[bold red]Linting errors found:[/bold red]\n")
        for error in all_errors:
            style = "yellow" if error.error_type == "DUPLICATE_KEY" else "red"
            print2(err_console, False, f"[{style}]{escape(str(error))}[/{style}]")
        print2(err_console, False, f"\n[bold]Total errors: {len(all_errors)}[/bold]")
        sys.exit(1)
    else:
        print2(console, args.quiet, "[green]✓ All files passed linting![/green]\n")

    # Second: Parse all agent files for analysis
    agents: dict[str, AgentMetadata] = {}
    for filepath in md_files:
        filename = filepath.name
        agent_name = format_agent_name(filename)
        metadata = parse_agent_file(filepath)
        if metadata:
            agents[agent_name] = metadata

    primary_agents: dict[str, AgentMetadata] = {}
    all_mode_agents: dict[str, AgentMetadata] = {}
    subagents: dict[str, AgentMetadata] = {}

    for agent_name, metadata in agents.items():
        mode = metadata.get("mode", "unknown")
        if mode == "primary":
            primary_agents[agent_name] = metadata
        elif mode == "all":
            all_mode_agents[agent_name] = metadata
        elif mode == "subagent":
            subagents[agent_name] = metadata

    if primary_agents:
        print2(
            console, args.quiet, create_agent_table(primary_agents, "📋 PRIMARY AGENTS")
        )
    else:
        print2(console, args.quiet, "[yellow]No primary agents found.[/yellow]")

    print2(console, args.quiet, "\n")

    if all_mode_agents:
        print2(
            console,
            args.quiet,
            create_agent_table(all_mode_agents, "🌐 ALL-MODE AGENTS"),
        )
    else:
        print2(console, args.quiet, "[yellow]No all-mode agents found.[/yellow]")

    print2(console, args.quiet, "\n")

    if subagents:
        print2(console, args.quiet, create_agent_table(subagents, "🔧 SUBAGENTS"))
    else:
        print2(console, args.quiet, "[yellow]No subagents found.[/yellow]")
    if args.expect_agents and not len(agents):
        print2(
            err_console,
            False,
            f"[red]Error: Expected agent files in directory {escape(str(agents_dir))}, but none were found.[/red]",
        )
        sys.exit(1)

    print2(console, args.quiet, "\n")
    stats_table = Table(title="STATISTICS", show_header=True, header_style="bold blue")
    stats_table.add_column("Category", style="cyan")
    stats_table.add_column("Count", style="green", justify="right")
    stats_table.add_row("Total agents", str(len(agents)))
    stats_table.add_row("Primary agents", str(len(primary_agents)))
    stats_table.add_row("All-mode agents", str(len(all_mode_agents)))
    stats_table.add_row("Subagents", str(len(subagents)))
    print2(console, args.quiet, stats_table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze and lint agent configuration markdown files."
    )

    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        default=".",
        help="Directory containing .md files to analyze",
    )
    parser.add_argument(
        "-p", "--parent", action="store_true", help="Use directory of parent script"
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress non-error output"
    )
    parser.add_argument(
        "-e",
        "--expect-agents",
        action="store_true",
        help="Expect agent files to be present",
    )

    args = parser.parse_args()

    main(args)
