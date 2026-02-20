from __future__ import annotations
from typing import Any, Optional, TYPE_CHECKING
from .types.pipeline import PipelineResult, PipelineStep

if TYPE_CHECKING:
    from .client import AionVision


class Pipeline:
    """

        Fluent builder for multi-step agent pipelines.

        Each builder method appends a step and returns ``self`` for chaining.
        Call :meth:`run` to submit the pipeline for execution.

        Steps are auto-wired by data type when ``depends_on`` is not specified
        (linear chain). Use ``depends_on`` for DAG patterns (e.g., parallel
        searches feeding into a single synthesis step).
    """

    def __init__(self, client: AionVision) -> None:
        ...

    def with_images(self, image_ids: list[str]) -> Pipeline:
        """Seed the pipeline with image IDs (no search step needed)."""
        ...

    def with_documents(self, document_ids: list[str]) -> Pipeline:
        """Seed the pipeline with document IDs (no search step needed)."""
        ...

    def search_images(self, query: str) -> Pipeline:
        """Add an image search step."""
        ...

    def search_documents(self, query: str) -> Pipeline:
        """Add a document search step."""
        ...

    def search_links(self, query: str) -> Pipeline:
        """Add a link search step."""
        ...

    def analyze(self, intent: str, *, depends_on: Optional[list[int]] = None) -> Pipeline:
        """Add an image analysis step."""
        ...

    def analyze_documents(self, intent: str, *, depends_on: Optional[list[int]] = None) -> Pipeline:
        """Add a document analysis step."""
        ...

    def analyze_links(self, intent: str, *, depends_on: Optional[list[int]] = None) -> Pipeline:
        """Add a link analysis step."""
        ...

    def synthesize(self, intent: str, *, depends_on: Optional[list[int]] = None) -> Pipeline:
        """Add a synthesis / report generation step."""
        ...

    def organize(self, intent: str, *, depends_on: Optional[list[int]] = None) -> Pipeline:
        """Add a file organization step."""
        ...

    def cross_reference(self, intent: str, *, depends_on: Optional[list[int]] = None) -> Pipeline:
        """Add a cross-reference step."""
        ...

    async def run(self) -> PipelineResult:
        """

                Submit the pipeline for execution and return results.

                The pipeline is sent to ``POST /agents/pipeline`` where the server
                builds an execution graph, auto-wires data dependencies, and runs
                agents in parallel waves.

                Returns:
                    PipelineResult with per-step results, execution time, and errors.

                Raises:
                    ValidationError: If the pipeline is invalid (bad agent names, etc.)
                    AionvisionError: On server-side errors.
        """
        ...
