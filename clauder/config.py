"""Configuration management for Clauder."""

import os
from dataclasses import dataclass, field


@dataclass
class ReviewConfig:
    api_key: str = field(default_factory=lambda: os.environ.get("ANTHROPIC_API_KEY", ""))
    model: str = "claude-sonnet-5"
    max_tokens: int = 4096
    categories: list = field(default_factory=lambda: ["bugs", "security", "performance", "style", "docs"])
    output_format: str = "terminal"

    def validate(self):
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable not set. "
                "Get your key at https://console.anthropic.com"
            )

    @classmethod
    def from_env(cls) -> "ReviewConfig":
        return cls(
            api_key=os.environ.get("ANTHROPIC_API_KEY", ""),
            model=os.environ.get("CLAUDER_MODEL", "claude-sonnet-5"),
        )
