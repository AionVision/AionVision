from __future__ import annotations
from typing import Optional
from ..config import ClientConfig
from ..types.agent_search import DocumentSearchAgentResult, ImageSearchAgentResult


class AgentSearchResource:
    """

        Direct access to AI search agents without chat sessions.

        Provides programmatic access to ImageSearchAgent and DocumentSearchAgent
        with full ReAct reasoning capabilities.

        Example:
            ```python
            async with AionVision(api_key="aion_...") as client:
                # Image search
                result = await client.agent_search.images("damaged utility poles")
                print(f"Found {result.count} images")
                print(f"Summary: {result.summary}")
                for img in result.results[:5]:
                    print(f"- {img.filename}: score={img.score:.2f}")

                # Document search
                result = await client.agent_search.documents(
                    "safety procedures",
                    document_types=["pdf"]
                )
                for chunk in result.results:
                    print(f"{chunk.document_filename} p{chunk.page_numbers}: {chunk.text[:100]}...")
            ```
    """

    def __init__(self, http: HTTPClient, config: ClientConfig) -> None:
        ...

    async def images(self, query: str, *, limit: int = 50, folder_id: Optional[str] = None, image_ids: Optional[list[str]] = None) -> ImageSearchAgentResult:
        """

                Execute AI-powered image search.

                Args:
                    query: Natural language search query
                    limit: Maximum results (1-500, default 50)
                    folder_id: Restrict search to specific folder
                    image_ids: Restrict search to specific images

                Returns:
                    ImageSearchAgentResult with:
                    - results: Full image objects
                    - summary: Human-readable summary
                    - result_ids: Flat list of image IDs
                    - result_refs: For interactive UI building
        """
        ...

    async def documents(self, query: str, *, limit: int = 50, document_types: Optional[list[str]] = None, document_ids: Optional[list[str]] = None) -> DocumentSearchAgentResult:
        """

                Execute AI-powered document search.

                Args:
                    query: Natural language search query
                    limit: Maximum results (1-500, default 50)
                    document_types: Filter by type (pdf, docx, txt)
                    document_ids: Restrict search to specific documents

                Returns:
                    DocumentSearchAgentResult with:
                    - results: Full chunk objects with text
                    - document_ids: Unique documents found
                    - summary: Human-readable summary
                    - result_refs: For interactive UI building
        """
        ...
