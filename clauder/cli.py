"""Clauder CLI — entry point for all commands."""

import sys
from pathlib import Path

import click
from rich.markdown import Markdown

from . import __version__
from .ui import (
    banner,
    console,
    error,
    info,
    section,
    show_code,
    show_findings_table,
    show_heal_summary,
    success,
    warn,
)


@click.group()
@click.version_option(__version__, prog_name="clauder")
def cli():
    """Clauder — The Autonomous Code Healer powered by Claude."""
    pass


# ─────────────────────────────────────────────────────────────────────────────
# clauder heal
# ─────────────────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--cmd", "-c", default="pytest -v", show_default=True, help="Test command to run.")
@click.option("--iterations", "-n", default=5, show_default=True, help="Max healing iterations.")
@click.option("--dry-run", is_flag=True, help="Show proposed fixes without applying them.")
@click.option("--no-auto", is_flag=True, help="Ask before applying each fix.")
@click.option("--model", "-m", default="claude-sonnet-5", show_default=True, help="Claude model to use.")
@click.option("--dir", "-d", "workdir", default=".", show_default=True, help="Working directory.")
def heal(cmd, iterations, dry_run, no_auto, model, workdir):
    """
    Autonomously fix failing tests using Claude.

    Clauder runs your test suite, sends failures to Claude, applies the
    suggested fixes, and loops until all tests pass or the iteration
    limit is reached.

    \b
    Examples:
      clauder heal
      clauder heal --cmd "pytest tests/ -x" --iterations 3
      clauder heal --dry-run
    """
    banner()
    section("Heal Mode", "🩺")

    from .healer import Healer, HealerConfig

    cwd = Path(workdir).resolve()
    config = HealerConfig(
        test_command=cmd,
        max_iterations=iterations,
        dry_run=dry_run,
        auto_apply=not no_auto,
        model=model,
    )

    info(f"Working directory: [cyan]{cwd}[/]")
    info(f"Test command:      [cyan]{cmd}[/]")
    info(f"Max iterations:    [cyan]{iterations}[/]")
    if dry_run:
        warn("Dry-run mode: fixes will NOT be applied.")

    try:
        healer = Healer(config, cwd)
        passed, iters_used, fixes = healer.heal()
    except RuntimeError as exc:
        error(str(exc))
        sys.exit(1)
    except KeyboardInterrupt:
        warn("\nHealing interrupted by user.")
        sys.exit(130)

    section("Results", "📋")
    from .runner import run_tests
    final = run_tests(cmd, cwd)
    show_heal_summary(iters_used, fixes, final.failed_count)

    if passed:
        success("All tests green. Healing complete!")
        sys.exit(0)
    else:
        error(f"Healing stopped with {final.failed_count} test(s) still failing.")
        sys.exit(1)


# ─────────────────────────────────────────────────────────────────────────────
# clauder analyze
# ─────────────────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--model", "-m", default="claude-sonnet-5", show_default=True, help="Claude model to use.")
@click.option("--show-code", "show_src", is_flag=True, help="Print the source file before findings.")
def analyze(file, model, show_src):
    """
    Analyze a Python file for bugs and code smells.

    Sends the file to Claude and displays a ranked list of findings
    with severity levels, descriptions, and fix suggestions.

    \b
    Examples:
      clauder analyze my_module.py
      clauder analyze app/utils.py --show-code
    """
    banner()
    section("Analyze Mode", "🔬")
    info(f"Analyzing [cyan]{file}[/] …")

    if show_src:
        show_code(file.read_text(), filename=file.name)

    from .analyzer import analyze_file
    try:
        findings = analyze_file(file, model=model)
    except RuntimeError as exc:
        error(str(exc))
        sys.exit(1)

    if not findings:
        success("No issues found — looks clean!")
        return

    section(f"{len(findings)} Finding(s)", "📌")
    show_findings_table(findings)

    high = sum(1 for f in findings if f.get("severity") == "HIGH")
    if high:
        warn(f"{high} HIGH severity issue(s) found — please review.")
    else:
        success("No HIGH severity issues.")


# ─────────────────────────────────────────────────────────────────────────────
# clauder explain
# ─────────────────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("source", required=False)
@click.option("--file", "-f", "traceback_file", type=click.Path(exists=True), help="Read traceback from a file.")
@click.option("--model", "-m", default="claude-sonnet-5", show_default=True, help="Claude model to use.")
def explain(source, traceback_file, model):
    """
    Explain a Python traceback in plain English.

    Pass a traceback as an argument, pipe it via stdin, or provide a file.

    \b
    Examples:
      clauder explain "$(cat error.txt)"
      pytest 2>&1 | clauder explain
      clauder explain --file traceback.txt
    """
    banner()
    section("Explain Mode", "💬")

    if traceback_file:
        tb_text = Path(traceback_file).read_text()
    elif source:
        tb_text = source
    elif not sys.stdin.isatty():
        tb_text = sys.stdin.read()
    else:
        error("Provide a traceback via argument, --file, or stdin.")
        sys.exit(1)

    if not tb_text.strip():
        error("Traceback is empty.")
        sys.exit(1)

    info("Sending traceback to Claude…")

    from .analyzer import explain_traceback
    try:
        explanation = explain_traceback(tb_text, model=model)
    except RuntimeError as exc:
        error(str(exc))
        sys.exit(1)

    section("Explanation", "🧠")
    console.print(Markdown(explanation))


def main():
    cli()


if __name__ == "__main__":
    main()
