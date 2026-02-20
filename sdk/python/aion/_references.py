"""Parse and resolve ``[[ref:…]]``, ``[[img:…]]``, ``[[doc:…]]`` and ``[[link:…]]`` markup.

This module gives SDK and API consumers two functions:

* :func:`parse_references` — structured extraction of all markup patterns.
* :func:`resolve_content` — plain-text replacement (CLI-friendly).

Regex patterns are ported from the Next.js frontend ``ChatMessage.tsx``
and the API-side ``ref_resolver.py``.
"""

from __future__ import annotations

from typing import Any, Optional

from .types.references import (
    DocumentRef,
    ImageRef,
    LinkRef,
    ParsedReferences,
)


def parse_references(
    content: str,
    metadata: Optional[dict[str, Any]] = None,
) -> ParsedReferences:
    """Parse all markup patterns from *content* and resolve IDs where possible.

    Args:
        content: Chat message text potentially containing ``[[…]]`` patterns.
        metadata: Response metadata dict (``ChatResponse.metadata``).  Used to
            resolve short ID prefixes to full UUIDs via ``image_context``,
            ``tool_document_data``, ``tool_link_data``, and ``result_refs``.

    Returns:
        A :class:`~aion.types.references.ParsedReferences` instance.

    Example:
        >>> response = await session.send("Find images")
        >>> refs = parse_references(response.content, response.metadata)
        >>> for img in refs.images:
        ...     print(img.full_id, img.filename)
    """
    ...


def resolve_content(
    content: str,
    metadata: Optional[dict[str, Any]] = None,
) -> str:
    """Replace all markup patterns in *content* with human-readable text.

    Replacement rules:

    * ``[[ref:KEY]]`` → count number (e.g. ``"47"``).
    * ``[[img:ID|filename]]`` → ``filename``.
    * ``[[doc:ID|filename]]`` → ``filename``.
    * ``[[doc:ID|filename|p:5]]`` → ``filename (p.5)``.
    * ``[[doc:ID|filename|pp:3-7]]`` → ``filename (pp.3-7)``.
    * ``[[link:ID|title]]`` → ``title``.

    Args:
        content: Chat message text potentially containing ``[[…]]`` patterns.
        metadata: Response metadata dict.  Only ``result_refs`` is used (to
            resolve ``[[ref:KEY]]`` to count values).

    Returns:
        Plain text with all markup replaced.

    Example:
        >>> response = await session.send("Find images")
        >>> plain = resolve_content(response.content, response.metadata)
        >>> print(plain)
    """
    ...
