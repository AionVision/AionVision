from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional
from collections.abc import Callable, Iterator


@dataclass(frozen=True)
class FileRef:
    """
    A reference to a single file with optional metadata.

        Attributes:
            id: Unique file identifier (UUID, content hash, or URI)
            media_type: MIME type of the file
            filename: Original filename
            size_bytes: File size in bytes
            metadata: Additional key-value metadata
    """
    id: str
    media_type: str = 'application/octet-stream'
    filename: Optional[str] = None
    size_bytes: Optional[int] = None
    metadata: Optional[dict[str, Any]] = None

    @classmethod
    def from_api_response(cls, data: dict) -> FileRef:
        """Create FileRef from API response data."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


class FileCollection:
    """
    Typed, immutable collection of file references with merge, filter, and slice.

        All operations return new instances. Refs are stored internally as a tuple
        for true immutability.

        Attributes:
            refs: Tuple of FileRef objects in the collection
            ids: List of file IDs
            count: Number of refs in the collection
            content_type: Type of content ("images", "documents", "mixed", "unknown")
            source_capability: Which capability produced this collection
    """
    __slots__ = ('_refs', '_content_type', '_source_capability')

    def __init__(self, refs: Optional[list[FileRef] | tuple[FileRef, ...]] = None, content_type: str = 'unknown', source_capability: Optional[str] = None) -> None:
        ...

    def __setattr__(self, name: str, value: Any) -> None:
        ...

    def __delattr__(self, name: str) -> None:
        ...

    @property
    def refs(self) -> tuple[FileRef, ...]:
        """All file references in insertion order."""
        ...

    @property
    def ids(self) -> list[str]:
        """List of file IDs."""
        ...

    @property
    def count(self) -> int:
        """Number of refs in the collection."""
        ...

    @property
    def content_type(self) -> str:
        """Content type label."""
        ...

    @property
    def source_capability(self) -> Optional[str]:
        """Source capability that produced this collection."""
        ...

    def __len__(self) -> int:
        ...

    def __bool__(self) -> bool:
        ...

    def __iter__(self) -> Iterator[FileRef]:
        ...

    def __getitem__(self, key: int | slice) -> FileRef | FileCollection:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    def __repr__(self) -> str:
        ...

    def filter(self, predicate: Callable[[FileRef], bool]) -> FileCollection:
        """Return a new collection with only refs matching predicate."""
        ...

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...

    @classmethod
    def from_ids(cls, ids: list[str], content_type: str = 'unknown', source_capability: Optional[str] = None) -> FileCollection:
        """Create a collection from bare ID strings."""
        ...

    @classmethod
    def merge(cls, *collections: FileCollection) -> FileCollection:
        """
        Merge collections with deduplication by ref.id.

                Keeps the ref with more metadata keys, or one with a filename where
                the other lacks one. Content type becomes ``"mixed"`` when collections
                have different non-``"unknown"`` types. Source capabilities are joined
                with ``"+"``.
        """
        ...
