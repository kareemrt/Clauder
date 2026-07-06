"""Rich terminal rendering for repository stories."""

import re
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.text import Text
from rich.columns import Columns
from rich.rule import Rule
from rich import box
from rich.align import Align
from rich.live import Live

from .github_client import RepoData


SECTION_COLORS = {
    "The Origin": "bright_cyan",
    "The Architects": "bright_yellow",
    "The Journey": "bright_green",
    "The Technology": "bright_magenta",
    "The Current State": "bright_blue",
    "The Future": "bright_red",
    "One-Line Story": "bold bright_white",
}

SECTION_ICONS = {
    "The Origin": "★",
    "The Architects": "◆",
    "The Journey": "◈",
    "The Technology": "◉",
    "The Current State": "◎",
    "The Future": "◌",
    "One-Line Story": "✦",
}


class StoryRenderer:
    def __init__(self, console: Console = None):
        self.console = console or Console()

    def render_header(self, data: RepoData, tagline: str):
        name = data.stats.full_name
        stars = data.stats.stars
        forks = data.stats.forks
        lang = data.stats.language or "—"

        title_text = Text()
        title_text.append("  ◈ CLAUDER  ", style="bold black on bright_cyan")
        title_text.append("  Repository Storyteller  ", style="bold bright_cyan")

        self.console.print()
        self.console.print(Align.center(title_text))
        self.console.print()

        repo_text = Text()
        repo_text.append(f"  {name}  ", style="bold white on blue")
        self.console.print(Align.center(repo_text))

        tagline_text = Text(f'"{tagline}"', style="italic bright_cyan")
        self.console.print(Align.center(tagline_text))
        self.console.print()

        stats_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
        stats_table.add_column(justify="center")
        stats_table.add_column(justify="center")
        stats_table.add_column(justify="center")
        stats_table.add_column(justify="center")
        stats_table.add_row(
            Text(f"★ {stars:,}", style="yellow bold"),
            Text(f"⑂ {forks:,}", style="cyan bold"),
            Text(f"◈ {lang}", style="green bold"),
            Text(f"⊕ {data.stats.open_issues}", style="red bold"),
        )
        self.console.print(Align.center(stats_table))
        self.console.print(Rule(style="bright_cyan dim"))

    def render_language_bar(self, languages: dict):
        if not languages:
            return
        total = sum(languages.values())
        if total == 0:
            return

        colors = ["bright_cyan", "bright_yellow", "bright_green", "bright_magenta",
                  "bright_blue", "bright_red", "white"]

        self.console.print()
        self.console.print("  [bold]Language Breakdown[/bold]", style="dim")

        bar_width = 60
        bar = Text()
        for i, (lang, bytes_count) in enumerate(
            sorted(languages.items(), key=lambda x: -x[1])[:7]
        ):
            pct = bytes_count / total
            width = max(1, int(bar_width * pct))
            color = colors[i % len(colors)]
            bar.append("█" * width, style=color)

        self.console.print(f"  {bar}")

        legend = Text()
        for i, (lang, bytes_count) in enumerate(
            sorted(languages.items(), key=lambda x: -x[1])[:7]
        ):
            pct = bytes_count / total * 100
            color = colors[i % len(colors)]
            legend.append(f"  [{color}]■[/{color}] {lang} {pct:.1f}%")
        self.console.print(legend)

    def render_contributors(self, data: RepoData):
        if not data.contributors:
            return
        table = Table(
            title="Top Contributors",
            box=box.ROUNDED,
            border_style="bright_cyan dim",
            header_style="bold bright_cyan",
            show_lines=False,
        )
        table.add_column("#", style="dim", width=4)
        table.add_column("Contributor", style="bold")
        table.add_column("Commits", justify="right", style="bright_yellow")
        table.add_column("Share", justify="right", style="bright_green")

        total_commits = sum(c.contributions for c in data.contributors)
        for i, contrib in enumerate(data.contributors[:10], 1):
            pct = contrib.contributions / total_commits * 100 if total_commits else 0
            bar = "█" * min(20, max(1, int(20 * pct / 100)))
            table.add_row(
                str(i),
                contrib.login,
                f"{contrib.contributions:,}",
                f"{bar} {pct:.1f}%",
            )
        self.console.print()
        self.console.print(table)

    def render_commit_timeline(self, data: RepoData):
        commits = data.commits[:15]
        if not commits:
            return

        self.console.print()
        self.console.print(Rule("[bold bright_green]Recent Commits[/bold bright_green]", style="bright_green dim"))

        for i, commit in enumerate(commits):
            connector = "│" if i < len(commits) - 1 else "╰"
            date_str = commit.date[:10] if commit.date else "?"
            msg = commit.message[:80] + ("…" if len(commit.message) > 80 else "")

            self.console.print(
                f"  [bright_green]{connector}[/bright_green] "
                f"[dim]{date_str}[/dim] "
                f"[cyan dim]{commit.sha}[/cyan dim] "
                f"[white]{msg}[/white] "
                f"[dim italic]— {commit.author}[/dim italic]"
            )

    def _parse_sections(self, story: str) -> list[tuple[str, str]]:
        sections = []
        pattern = r"##\s+(.+?)\n(.*?)(?=##\s|\Z)"
        matches = re.findall(pattern, story, re.DOTALL)
        for title, content in matches:
            sections.append((title.strip(), content.strip()))
        return sections

    def render_story(self, story: str):
        sections = self._parse_sections(story)
        if not sections:
            self.console.print(story)
            return

        for title, content in sections:
            color = SECTION_COLORS.get(title, "bright_white")
            icon = SECTION_ICONS.get(title, "◆")

            self.console.print()
            self.console.print(
                Panel(
                    content,
                    title=f"[bold {color}]{icon} {title}[/bold {color}]",
                    border_style=f"{color} dim",
                    padding=(1, 2),
                )
            )

    def render_full(self, data: RepoData, story: str, tagline: str):
        self.render_header(data, tagline)
        self.render_language_bar(data.languages)
        self.render_contributors(data)
        self.render_commit_timeline(data)
        self.console.print()
        self.console.print(Rule("[bold bright_white]The Story[/bold bright_white]", style="bright_white"))
        self.render_story(story)
        self.console.print()
        self.console.print(Rule(style="bright_cyan dim"))
        self.console.print(
            Align.center(
                Text("Generated by Clauder · Powered by Claude AI", style="dim italic")
            )
        )
        self.console.print()
