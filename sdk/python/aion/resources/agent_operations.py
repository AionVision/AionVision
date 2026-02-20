from __future__ import annotations
from typing import Optional
from ..config import ClientConfig
from ..types.agent_operations import DocumentAnalysisResult, OrganizeResult, SynthesizeResult


class AgentOperationsResource:
    """

        Direct access to AI agent operations without chat sessions.

        Provides programmatic access to SynthesisAgent, DocumentAnalysisAgent,
        and FolderAgent with full ReAct reasoning capabilities.

        Example:
            ```python
            async with AionVision(api_key="aion_...") as client:
                # Synthesize a report
                result = await client.agent_operations.synthesize(
                    "Write a report on spending patterns",
                    document_ids=["doc-1", "doc-2"],
                )
                print(result.report)

                # Analyze documents
                result = await client.agent_operations.analyze_documents(
                    "Summarize and compare these contracts",
                    document_ids=["doc-1", "doc-2"],
                )
                print(result.analysis)

                # Organize files
                result = await client.agent_operations.organize(
                    "Sort these files by category",
                    image_ids=["img-1", "img-2"],
                )
                print(result.summary)
            ```
    """

    def __init__(self, http: HTTPClient, config: ClientConfig) -> None:
        ...

    async def synthesize(self, intent: str, *, image_ids: Optional[list[str]] = None, document_ids: Optional[list[str]] = None, auto_save: bool = False) -> SynthesizeResult:
        """

                Execute AI-powered report synthesis.

                Args:
                    intent: What to synthesize, e.g. 'Write a report on spending patterns'
                    image_ids: Images to include in synthesis
                    document_ids: Documents to include in synthesis
                    auto_save: Auto-save the generated report as a document

                Returns:
                    SynthesizeResult with report content and metadata
        """
        ...

    async def analyze_documents(self, intent: str, document_ids: list[str]) -> DocumentAnalysisResult:
        """

                Execute AI-powered document analysis.

                Args:
                    intent: Analysis intent, e.g. 'Summarize and compare these contracts'
                    document_ids: Documents to analyze (at least one required)

                Returns:
                    DocumentAnalysisResult with analysis content and chunk references
        """
        ...

    async def organize(self, intent: str, *, image_ids: Optional[list[str]] = None, document_ids: Optional[list[str]] = None, parent_folder_id: Optional[str] = None) -> OrganizeResult:
        """

                Execute AI-driven file organization.

                Args:
                    intent: Organization intent, e.g. 'Sort these files by category'
                    image_ids: Images to organize
                    document_ids: Documents to organize
                    parent_folder_id: Parent folder for new folders

                Returns:
                    OrganizeResult with summary of actions taken
        """
        ...
