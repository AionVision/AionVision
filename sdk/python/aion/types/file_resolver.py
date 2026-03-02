"""File resolver protocol for SDK agentic workflows.

Defines the ``FileResolver`` Protocol that users implement to connect
their own storage backends (S3, local filesystem, HTTP, etc.) for
resolving ``FileRef`` references to actual content bytes.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any, Optional, Protocol, runtime_checkable

from .file_collection import FileRef


class FileResolutionError(Exception):
    """Raised when a file reference cannot be resolved to content."""

    pass


@runtime_checkable
class FileResolver(Protocol):
    """Protocol for resolving FileRef references to content.

    Implement this to plug in your own storage backend.
    """

    async def resolve(
        self, ref: FileRef, hints: Optional[dict[str, Any]] = None
    ) -> bytes:
        """Resolve a single file reference to its content bytes."""
        ...

    async def resolve_batch(
        self, refs: list[FileRef], batch_size: int = 100
    ) -> AsyncIterator[tuple[FileRef, bytes]]:
        """Streaming batch resolution. Yields (ref, content) tuples."""
        ...

    async def resolve_metadata(self, ref: FileRef) -> FileRef:
        """Enrich a ref with metadata without fetching full content."""
        ...

    async def store(
        self,
        content: bytes,
        media_type: str,
        metadata: Optional[dict[str, Any]] = None,
    ) -> FileRef:
        """Store content and return a FileRef pointing to it."""
        ...
