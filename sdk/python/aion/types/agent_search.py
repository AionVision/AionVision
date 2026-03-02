from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class ResultRefData:
    """Reference data for interactive UI resolution."""
    count: int
    ids: list[str]
    image_ids: list[str]
    id_type: str
    label: str

    @classmethod
    def from_api_response(cls, data: dict) -> ResultRefData:
        ...


@dataclass(frozen=True)
class ImageSearchResultItem:
    """Individual image result from agent search."""
    image_id: str
    score: float
    filename: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    folder_id: Optional[str] = None
    thumbnail_url: Optional[str] = None
    features: Optional[list[dict[str, Any]]] = None

    @classmethod
    def from_api_response(cls, data: dict) -> ImageSearchResultItem:
        ...


@dataclass(frozen=True)
class ImageSearchAgentResult:
    """Complete result from image search agent."""
    success: bool
    results: list[ImageSearchResultItem]
    count: int
    result_ids: list[str]
    summary: str
    summary_raw: str
    result_refs: dict[str, ResultRefData]
    execution_time_ms: int
    iterations: int
    search_strategy: Optional[dict[str, Any]] = None
    token_usage: Optional[dict[str, int]] = None

    @classmethod
    def from_api_response(cls, data: dict) -> ImageSearchAgentResult:
        ...

    def as_collection(self) -> 'FileCollection':
        """
        Convert search results to a :class:`FileCollection`.

                Each :class:`ImageSearchResultItem` becomes a :class:`FileRef` with
                ``media_type="image/*"`` and metadata populated from non-None fields
                (score, title, description, folder_id).
        """
        ...


@dataclass(frozen=True)
class DocumentChunkResultItem:
    """Individual document chunk result from agent search."""
    chunk_id: str
    document_id: str
    document_filename: str
    text: str
    score: float
    page_numbers: Optional[list[int]] = None
    chunk_index: Optional[int] = None

    @classmethod
    def from_api_response(cls, data: dict) -> DocumentChunkResultItem:
        ...


@dataclass(frozen=True)
class DocumentSearchAgentResult:
    """Complete result from document search agent."""
    success: bool
    results: list[DocumentChunkResultItem]
    count: int
    chunk_ids: list[str]
    document_ids: list[str]
    summary: str
    summary_raw: str
    result_refs: dict[str, ResultRefData]
    search_mode: str
    execution_time_ms: int
    iterations: int
    search_strategy: Optional[dict[str, Any]] = None
    token_usage: Optional[dict[str, int]] = None

    @classmethod
    def from_api_response(cls, data: dict) -> DocumentSearchAgentResult:
        ...

    def as_collection(self, by: str = 'document') -> 'FileCollection':
        """
        Convert search results to a :class:`FileCollection`.

                Args:
                    by: Grouping mode.
                        ``"document"`` (default) — one :class:`FileRef` per unique
                        ``document_id``, keeping the highest-scoring chunk entry.
                        ``"chunk"`` — one :class:`FileRef` per chunk.
        """
        ...


@dataclass(frozen=True)
class MatchedSceneItem:
    """Individual scene match within a video result."""
    scene_id: str
    scene_index: int
    start_time: float
    end_time: float
    time_range_formatted: str
    description: str
    score: float
    tags: Optional[list[str]] = None
    thumbnail_url: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict) -> MatchedSceneItem:
        ...


@dataclass(frozen=True)
class VideoSearchResultItem:
    """Individual video result with matched scenes."""
    video_id: str
    video_filename: str
    score: float
    video_description: str = ''
    duration_seconds: Optional[float] = None
    resolution: Optional[str] = None
    thumbnail_url: Optional[str] = None
    matched_scenes: Optional[list[MatchedSceneItem]] = None

    @classmethod
    def from_api_response(cls, data: dict) -> VideoSearchResultItem:
        ...


@dataclass(frozen=True)
class VideoSearchAgentResult:
    """Complete result from video search agent."""
    success: bool
    results: list[VideoSearchResultItem]
    count: int
    video_ids: list[str]
    summary: str
    summary_raw: str
    result_refs: dict[str, ResultRefData]
    search_mode: str
    execution_time_ms: int
    iterations: int
    search_strategy: Optional[dict[str, Any]] = None
    token_usage: Optional[dict[str, int]] = None

    @classmethod
    def from_api_response(cls, data: dict) -> VideoSearchAgentResult:
        ...

    def as_collection(self) -> 'FileCollection':
        """Convert search results to a FileCollection."""
        ...
