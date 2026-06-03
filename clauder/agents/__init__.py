from clauder.agents.architecture import ArchitectureAgent
from clauder.agents.docs import DocsAgent
from clauder.agents.quality import QualityAgent
from clauder.agents.scout import ScoutAgent
from clauder.agents.security import SecurityAgent
from clauder.agents.synthesizer import SynthesizerAgent

AGENT_REGISTRY = {
    "scout": ScoutAgent,
    "security": SecurityAgent,
    "quality": QualityAgent,
    "architecture": ArchitectureAgent,
    "docs": DocsAgent,
}

__all__ = [
    "ScoutAgent",
    "SecurityAgent",
    "QualityAgent",
    "ArchitectureAgent",
    "DocsAgent",
    "SynthesizerAgent",
    "AGENT_REGISTRY",
]
