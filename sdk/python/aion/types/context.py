from __future__ import annotations
import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass(frozen=True)
class TypedSlot:
    """
    A typed slot holding a value with provenance.

        Attributes:
            value: The data (dict, list, scalar, etc.)
            data_type: Registry key, e.g. "FILE_IDS"
            source_node: Which agent produced this value
            timestamp: ISO 8601 timestamp (auto-set if None)
    """
    value: Any
    data_type: str
    source_node: str
    timestamp: Optional[str] = None

    def __post_init__(self) -> None:
        ...


class ExecutionContext:
    """
    Mutable, async-safe shared state container for agent workflows.

        Agents read inputs from and write outputs to named slots. Each slot
        is typed and tracks which agent produced it.
    """

    def __init__(self) -> None:
        ...

    def write(self, slot_name: str, value: Any, data_type: str, source_node: str) -> None:
        """Write a value to a typed slot."""
        ...

    def read(self, slot_name: str, expected_type: Optional[str] = None) -> Any:
        """
        Read a value from a typed slot.

                Raises:
                    KeyError: If the slot doesn't exist.
                    TypeError: If the slot's data_type doesn't match *expected_type*.
        """
        ...

    def has_slot(self, slot_name: str) -> bool:
        """Check whether a slot exists."""
        ...

    async def write_async(self, slot_name: str, value: Any, data_type: str, source_node: str) -> None:
        """Write a value to a typed slot (async-safe)."""
        ...

    async def read_async(self, slot_name: str, expected_type: Optional[str] = None) -> Any:
        """
        Read a value from a typed slot (async-safe).

                Raises:
                    KeyError: If the slot doesn't exist.
                    TypeError: If the slot's data_type doesn't match *expected_type*.
        """
        ...

    async def has_slot_async(self, slot_name: str) -> bool:
        """Check whether a slot exists (async-safe)."""
        ...

    def get_slot_type(self, slot_name: str) -> Optional[str]:
        """Get the data type of a slot, or None if it doesn't exist."""
        ...

    def get_slots_by_type(self, data_type: str) -> dict[str, Any]:
        """Get all slot values matching a given data type."""
        ...

    def list_slots(self) -> list[dict[str, str]]:
        """List all slots with their types and sources."""
        ...

    @property
    def slots(self) -> dict[str, TypedSlot]:
        """Read-only copy of the internal slots dictionary."""
        ...

    def to_dict(self) -> dict[str, Any]:
        """Serialize context for checkpointing."""
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ExecutionContext:
        """Restore context from a serialized dictionary."""
        ...
