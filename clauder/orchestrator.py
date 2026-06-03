from __future__ import annotations

import asyncio
from typing import Optional

import anthropic
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.table import Table

from clauder.agents import AGENT_REGISTRY, SynthesizerAgent
from clauder.models import AgentReport, RepoData, SynthesisReport


class Orchestrator:
    def __init__(self, api_key: str, model: str = "claude-opus-4-8"):
        self.model = model
        self._client = anthropic.AsyncAnthropic(api_key=api_key)

    async def run(
        self,
        repo_data: RepoData,
        agent_names: Optional[list[str]] = None,
        console: Optional[Console] = None,
    ) -> SynthesisReport:
        if console is None:
            console = Console()

        registry = AGENT_REGISTRY
        if agent_names:
            registry = {k: v for k, v in AGENT_REGISTRY.items() if k in agent_names}

        agents = [cls(self._client, self.model) for cls in registry.values()]

        progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold]{task.description}"),
            TimeElapsedColumn(),
            console=console,
            transient=False,
        )

        task_ids = {}
        with progress:
            for agent in agents:
                tid = progress.add_task(
                    f"{agent.emoji} {agent.name} Agent — analyzing...", total=None
                )
                task_ids[agent.name] = tid

            async def run_agent(agent):
                report = await agent.analyze(repo_data)
                progress.update(
                    task_ids[agent.name],
                    description=f"{agent.emoji} {agent.name} Agent — done  (score: {report.score}/100)",
                    completed=True,
                )
                return report

            reports: list[AgentReport] = await asyncio.gather(
                *(run_agent(a) for a in agents)
            )

        console.print()
        synth_progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold]{task.description}"),
            TimeElapsedColumn(),
            console=console,
            transient=False,
        )
        with synth_progress:
            stid = synth_progress.add_task("🧠 Synthesizer — combining findings...", total=None)
            synthesizer = SynthesizerAgent(self._client, self.model)
            synthesis = await synthesizer.synthesize(repo_data, reports)
            synth_progress.update(stid, description="🧠 Synthesizer — complete", completed=True)

        await self._client.close()
        return synthesis
