from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional, Protocol, runtime_checkable
from .contracts import AgentContract
from .context import ExecutionContext


@dataclass(frozen=True)
class AgentResult:
    """
    Result returned by an agent after execution.

        Attributes:
            success: Whether the agent executed successfully
            agent_name: Name of the agent that produced this result
            capability: AgentCapability value string
            outputs: Mapping of slot_name -> value for produced outputs
            error: Error message if execution failed
            summary: Human-readable summary of what the agent did
            execution_time_ms: How long execution took in milliseconds
            metadata: Additional metadata
    """
    success: bool
    agent_name: str
    capability: str
    outputs: Optional[dict[str, Any]] = None
    error: Optional[str] = None
    summary: Optional[str] = None
    execution_time_ms: float = 0
    metadata: Optional[dict[str, Any]] = None

    def get_output(self, slot_name: str, default: Any = None) -> Any:
        """Get an output value by slot name."""
        ...

    def has_output(self, slot_name: str) -> bool:
        """Check if an output slot exists."""
        ...

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


@runtime_checkable
class Agent(Protocol):
    """
    Protocol for SDK agents.

        Users implement this interface to define their own agents.
        No inheritance required — just implement the two methods.

        Example::

            class MySearchAgent:
                def get_contract(self) -> AgentContract:
                    return AgentContract(
                        name="MySearch",
                        capability=AgentCapability.SEARCH,
                        description="Searches images",
                    )

                async def execute(self, context: ExecutionContext) -> AgentResult:
                    query = context.read("query")
                    # ... do work ...
                    return AgentResult(
                        success=True,
                        agent_name="MySearch",
                        capability="search",
                        outputs={"results": [...]},
                    )
    """

    def get_contract(self) -> AgentContract:
        ...

    async def execute(self, context: ExecutionContext) -> AgentResult:
        ...
