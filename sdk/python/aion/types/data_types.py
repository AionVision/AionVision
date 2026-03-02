from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional
from collections.abc import Callable
from .file_collection import FileCollection


@dataclass(frozen=True)
class Category:
    """
    A single category from categorization.

        Attributes:
            name: Category name
            description: Human-readable description
            file_ids: Image IDs belonging to this category
            document_ids: Document IDs belonging to this category
            top_tags: Top tags for this category
            confidence: Confidence score (0.0 to 1.0)
    """
    name: str
    description: Optional[str] = None
    file_ids: tuple[str, ...] = ()
    document_ids: tuple[str, ...] = ()
    top_tags: tuple[str, ...] = ()
    confidence: float = 1.0

    @property
    def count(self) -> int:
        """Total number of files (images + documents)."""
        ...

    @property
    def content_type(self) -> str:
        """Content type: "images", "documents", "mixed", or "empty"."""
        ...

    def merge_with(self, other: Category) -> Category:
        """Merge another category into this one."""
        ...

    def to_dict(self) -> dict[str, Any]:
        ...


@dataclass(frozen=True)
class CategorizationResult:
    """
    Structured categorization output.

        Attributes:
            categories: Tuple of Category objects
            total_files: Total number of files across all categories
            clustering_method: Method used for clustering
            status: "success", "partial", or "failed"
            error_reason: Error message if status is "failed"
            source_capability: Which capability produced this result
    """
    categories: tuple[Category, ...] = ()
    total_files: int = 0
    clustering_method: str = 'unknown'
    status: str = 'success'
    error_reason: Optional[str] = None
    source_capability: Optional[str] = None

    @classmethod
    def merge(cls, *results: CategorizationResult) -> CategorizationResult:
        """
        Merge multiple categorization results.

                Categories with matching names (case-insensitive) are combined.
        """
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CategorizationResult:
        ...


@dataclass(frozen=True)
class AnalysisResult:
    """
    Structured analysis output.

        Attributes:
            summary: Analysis summary
            findings: List of findings
            document_id: Related document ID
            metadata: Additional metadata
    """
    summary: str
    findings: tuple[str, ...] = ()
    document_id: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None

    def to_dict(self) -> dict[str, Any]:
        ...


@dataclass(frozen=True)
class TextResult:
    """
    Simple text output.

        Attributes:
            text: The text content
            metadata: Additional metadata
    """
    text: str
    metadata: Optional[dict[str, Any]] = None

    def to_dict(self) -> dict[str, Any]:
        ...


@dataclass(frozen=True)
class CrossRefResult:
    """
    Cross-reference analysis output.

        Attributes:
            relationships: Relationship data
            source_files: Source file IDs
            target_files: Target file IDs
            summary: Summary of cross-references
            metadata: Additional metadata
    """
    relationships: tuple[dict[str, Any], ...] = ()
    source_files: tuple[str, ...] = ()
    target_files: tuple[str, ...] = ()
    summary: str = ''
    metadata: Optional[dict[str, Any]] = None

    def to_dict(self) -> dict[str, Any]:
        ...


@dataclass(frozen=True)
class FolderResult:
    """
    Result of folder organization operations.

        Attributes:
            folders_created: Folder creation details
            files_moved: Number of files moved
            documents_moved: Number of documents moved
            errors: Error messages
            success: Whether the operation succeeded
    """
    folders_created: tuple[dict[str, Any], ...] = ()
    files_moved: int = 0
    documents_moved: int = 0
    errors: tuple[str, ...] = ()
    success: bool = True

    def to_dict(self) -> dict[str, Any]:
        ...


@dataclass(frozen=True)
class DataTypeDefinition:
    """
    Definition of a data type that can flow between agents.

        Attributes:
            name: Type name, e.g. "FILE_IDS"
            description: Human-readable description
            mergeable: Whether this type supports merging
    """
    name: str
    description: str = ''
    mergeable: bool = False


class DataTypeRegistry:
    """
    Registry for data types in the system.

        Allows dynamic registration of new types with optional merge functions.
    """

    def __init__(self) -> None:
        ...

    def register(self, definition: DataTypeDefinition, merge_fn: Optional[Callable] = None) -> None:
        """Register a data type with an optional merge function."""
        ...

    def get(self, name: str) -> Optional[DataTypeDefinition]:
        """Get a type definition by name."""
        ...

    def has_type(self, name: str) -> bool:
        """Check if a type is registered."""
        ...

    def can_merge(self, name: str) -> bool:
        """Check if a type supports merging."""
        ...

    def merge(self, name: str, *values: Any) -> Any:
        """
        Merge multiple values of a type.

                Raises:
                    ValueError: If the type doesn't support merging.
        """
        ...

    def list_types(self) -> list[str]:
        """List all registered type names."""
        ...

def get_default_registry() -> DataTypeRegistry:
    """
    Create a fresh DataTypeRegistry pre-loaded with built-in types.

        Each call returns a new instance so users can customize without
        affecting others.
    """
    ...
