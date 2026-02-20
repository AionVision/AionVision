from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PipelineStep:
    """A step in a pipeline workflow."""
    agent: str
    intent: str
    params: dict[str, Any] = field(default_factory=dict)
    depends_on: tuple[int, ...] | None = None


@dataclass(frozen=True)
class StepResult:
    """Result from a single pipeline step."""
    agent: str
    status: str
    summary: str | None
    outputs: dict[str, Any]
    error: str | None
    execution_time_ms: int

    @staticmethod
    def from_api_response(data: dict[str, Any]) -> StepResult:
        ...


@dataclass(frozen=True)
class PipelineResult:
    """Result of pipeline execution."""
    success: bool
    steps: list[StepResult]
    execution_time_ms: int
    total_waves: int
    errors: list[str]
    token_usage: dict[str, int] | None

    def step(self, index: int) -> StepResult:
        """Get step result by index."""
        ...

    @property
    def final(self) -> StepResult:
        """Get the last step's result."""
        ...

    @staticmethod
    def from_api_response(data: dict[str, Any]) -> PipelineResult:
        ...
