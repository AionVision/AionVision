from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass(frozen=True)
class ImageRef:
    """
    A parsed ``[[img:ID|filename]]`` reference.

        Attributes:
            id_prefix: Short ID prefix from the markup (e.g. ``"a1b2c3d4"``).
            filename: Display filename extracted from the markup.
            full_id: Full UUID resolved from ``image_context``, or *None*.
    """
    id_prefix: str
    filename: str
    full_id: Optional[str] = None


@dataclass(frozen=True)
class DocumentRef:
    """
    A parsed ``[[doc:ID|filename]]`` or ``[[doc:ID|filename|p:N]]`` reference.

        Attributes:
            id_prefix: Short ID prefix from the markup.
            filename: Display filename extracted from the markup.
            full_id: Full UUID resolved from ``tool_document_data``, or *None*.
            page: Single page number (from ``p:N``), or *None*.
            page_range: Tuple of ``(start, end)`` (from ``pp:N-M``), or *None*.
    """
    id_prefix: str
    filename: str
    full_id: Optional[str] = None
    page: Optional[int] = None
    page_range: Optional[tuple[int, int]] = None


@dataclass(frozen=True)
class LinkRef:
    """
    A parsed ``[[link:ID|title]]`` reference.

        Attributes:
            id_prefix: Short ID prefix from the markup.
            title: Display title extracted from the markup.
            full_id: Full UUID resolved from ``tool_link_data``, or *None*.
            source_url: Resolved source URL from ``tool_link_data``, or *None*.
            domain: Resolved domain from ``tool_link_data``, or *None*.
    """
    id_prefix: str
    title: str
    full_id: Optional[str] = None
    source_url: Optional[str] = None
    domain: Optional[str] = None


@dataclass(frozen=True)
class ParsedReferences:
    """
    Container for all parsed references found in a chat message.

        Attributes:
            images: List of ``ImageRef`` instances.
            documents: List of ``DocumentRef`` instances.
            links: List of ``LinkRef`` instances.
            counts: Dict mapping ``[[ref:KEY]]`` keys to their resolved
                :class:`~aion.types.agent_search.ResultRefData` objects.
            has_references: *True* if any references were found.
    """
    images: list[ImageRef] = field(default_factory=list)
    documents: list[DocumentRef] = field(default_factory=list)
    links: list[LinkRef] = field(default_factory=list)
    counts: dict[str, Any] = field(default_factory=dict)

    @property
    def has_references(self) -> bool:
        ...
