from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

app = typer.Typer(
    name="clauder",
    help="Multi-agent AI repository intelligence powered by Claude.",
    add_completion=False,
    rich_markup_mode="rich",
)
console = Console()

BANNER = r"""
 ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗██████╗
██╔════╝██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝██╔══██╗
██║     ██║     ███████║██║   ██║██║  ██║█████╗  ██████╔╝
██║     ██║     ██╔══██║██║   ██║██║  ██║██╔══╝  ██╔══██╗
╚██████╗███████╗██║  ██║╚██████╔╝██████╔╝███████╗██║  ██║
 ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
  Multi-Agent AI Repository Intelligence
"""


@app.command()
def analyze(
    repo: str = typer.Argument(
        ...,
        help="GitHub repo as [bold]owner/name[/bold], full URL, or [bold]owner/name@branch[/bold]",
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Save Markdown report to this file"
    ),
    agents: str = typer.Option(
        "all",
        "--agents",
        "-a",
        help="Comma-separated subset: scout,security,quality,architecture,docs",
    ),
    max_files: int = typer.Option(60, "--max-files", help="Max source files to feed each agent"),
    model: str = typer.Option(
        "claude-opus-4-8", "--model", "-m", help="Claude model ID to use"
    ),
    no_banner: bool = typer.Option(False, "--no-banner", hidden=True),
):
    """Analyze a GitHub repository with five specialized AI agents.

    Each agent focuses on a different dimension:
    🔭 Scout — structure & tech stack
    🔒 Security — vulnerabilities & secrets
    ✨ Quality — code quality & tests
    🏛️  Architecture — design patterns & coupling
    📚 Docs — documentation & comments

    Results are synthesized into an overall health report.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        console.print(
            Panel(
                "[bold red]Missing API Key[/bold red]\n\n"
                "Set [cyan]ANTHROPIC_API_KEY[/cyan] to your Anthropic API key.\n"
                "Get one at: [link=https://console.anthropic.com]https://console.anthropic.com[/link]",
                border_style="red",
            )
        )
        raise typer.Exit(1)

    if not no_banner:
        console.print(Text(BANNER, style="bold cyan"))

    agent_names = None if agents == "all" else [a.strip() for a in agents.split(",")]
    asyncio.run(_run(repo, output, agent_names, max_files, model, api_key))


async def _run(
    repo: str,
    output: Optional[Path],
    agent_names: Optional[list[str]],
    max_files: int,
    model: str,
    api_key: str,
) -> None:
    from clauder.github import RepoFetcher
    from clauder.orchestrator import Orchestrator
    from clauder.reporter import Reporter

    console.print(f"[bold]Repository:[/bold] [cyan]{repo}[/cyan]")
    console.print(f"[bold]Model:[/bold]      [cyan]{model}[/cyan]")
    console.print(f"[bold]Max files:[/bold]  [cyan]{max_files}[/cyan]")
    console.print()

    console.print("[dim]Fetching repository…[/dim]")
    async with RepoFetcher() as fetcher:
        repo_data = await fetcher.fetch(repo, max_files=max_files)

    console.print(
        f"[green]✓[/green] Fetched [bold]{len(repo_data.files)}[/bold] files "
        f"from [cyan]{repo_data.owner}/{repo_data.name}[/cyan] "
        f"([dim]{repo_data.language or 'unknown language'}[/dim])\n"
    )

    orchestrator = Orchestrator(api_key=api_key, model=model)
    synthesis = await orchestrator.run(repo_data, agent_names=agent_names, console=console)

    reporter = Reporter(console=console)
    reporter.display(synthesis)

    if output:
        reporter.save_markdown(synthesis, output)
        console.print(f"[green]Report saved →[/green] {output}")


@app.command()
def models() -> None:
    """List recommended Claude models for Clauder."""
    table_data = [
        ("claude-opus-4-8", "Opus 4.8", "Most capable, best analysis", "~60s"),
        ("claude-sonnet-4-6", "Sonnet 4.6", "Balanced speed/quality", "~25s"),
        ("claude-haiku-4-5-20251001", "Haiku 4.5", "Fastest, lightweight repos", "~10s"),
    ]
    from rich.table import Table
    t = Table(title="Available Models", border_style="cyan")
    t.add_column("Model ID")
    t.add_column("Name")
    t.add_column("Best For")
    t.add_column("Est. Time")
    for row in table_data:
        t.add_row(*row)
    console.print(t)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
