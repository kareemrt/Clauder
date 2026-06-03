from __future__ import annotations

from typing import Literal, Optional
from pydantic import BaseModel, Field


class FileInfo(BaseModel):
    path: str
    content: str
    size: int
    language: Optional[str] = None


class RepoData(BaseModel):
    owner: str
    name: str
    description: Optional[str] = None
    url: str
    default_branch: str = "main"
    stars: int = 0
    language: Optional[str] = None
    files: list[FileInfo] = Field(default_factory=list)
    file_tree: list[str] = Field(default_factory=list)
    topics: list[str] = Field(default_factory=list)


class Finding(BaseModel):
    severity: Literal["critical", "high", "medium", "low", "info"]
    category: str
    title: str
    description: str
    file: Optional[str] = None
    line: Optional[int] = None
    recommendation: str


class AgentReport(BaseModel):
    agent: str
    emoji: str
    summary: str
    score: int = Field(ge=0, le=100)
    findings: list[Finding] = Field(default_factory=list)
    highlights: list[str] = Field(default_factory=list)


class SynthesisReport(BaseModel):
    overall_score: int = Field(ge=0, le=100)
    grade: Literal["A", "B", "C", "D", "F"]
    executive_summary: str
    critical_issues: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    roadmap: list[str] = Field(default_factory=list)
    agent_reports: list[AgentReport] = Field(default_factory=list)
