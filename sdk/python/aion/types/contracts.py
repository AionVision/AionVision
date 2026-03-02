from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional


class AgentCapability(str, Enum):
    """What an agent can do — matches backend capability values."""
    SEARCH = 'search'
    FILTER = 'filter'
    ANALYSIS = 'analysis'
    COMPARISON = 'comparison'
    EXPORT = 'export'
    SUMMARIZATION = 'summarization'
    RECOMMENDATION = 'recommendation'
    VISUALIZATION = 'visualization'
    ANALYTICS = 'analytics'
    CROSS_REFERENCE = 'cross_reference'
    SYNTHESIS = 'synthesis'
    ORGANIZATION = 'organization'
    CONVERSATIONAL = 'conversational'


@dataclass(frozen=True)
class TypedInput:
    """
    Declares a typed input for an agent.

        Attributes:
            name: Slot name, e.g. "file_ids"
            data_type: Registry key, e.g. "FILE_IDS"
            required: Whether the input must be present
            description: Human-readable description
            content_type_hint: Hint like "images", "documents", "links"
    """
    name: str
    data_type: str
    required: bool = True
    description: str = ''
    content_type_hint: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        ...


@dataclass(frozen=True)
class TypedOutput:
    """
    Declares a typed output produced by an agent.

        Attributes:
            name: Slot name, e.g. "results"
            data_type: Registry key, e.g. "FILE_IDS"
            mergeable: Whether multiple outputs can be merged
            description: Human-readable description
            content_type_hint: Hint like "images", "documents", "links"
    """
    name: str
    data_type: str
    mergeable: bool = False
    description: str = ''
    content_type_hint: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        ...


@dataclass(frozen=True)
class AgentContract:
    """
    Unified contract for agent declaration.

        Every agent implements ``get_contract()`` returning this.

        Attributes:
            name: Agent name, e.g. "ImageSearchAgent"
            capability: Primary capability type
            description: Natural language description
            inputs: Typed inputs the agent requires
            outputs: Typed outputs the agent produces
            example_intents: Example user intents this agent handles
            can_run_parallel: Whether the agent supports parallel execution
            typical_duration_ms: Typical execution time in milliseconds
            can_chain_with: Capabilities this agent can chain with
    """
    name: str
    capability: AgentCapability
    description: str
    inputs: tuple[TypedInput, ...] = ()
    outputs: tuple[TypedOutput, ...] = ()
    example_intents: tuple[str, ...] = ()
    can_run_parallel: bool = True
    typical_duration_ms: int = 5000
    can_chain_with: tuple[AgentCapability, ...] = ()

    def get_required_inputs(self) -> list[TypedInput]:
        """Get only the required inputs."""
        ...

    def get_input_by_name(self, name: str) -> Optional[TypedInput]:
        """Get an input by slot name."""
        ...

    def get_output_by_name(self, name: str) -> Optional[TypedOutput]:
        """Get an output by slot name."""
        ...

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AgentContract:
        """Create an AgentContract from a dictionary."""
        ...
