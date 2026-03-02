from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class ChunkReference:
    """Reference to a document chunk cited in an analysis."""
    chunk_id: str
    document_id: str
    document_filename: Optional[str] = None
    page_numbers: Optional[list[int]] = None

    @classmethod
    def from_api_response(cls, data: dict) -> ChunkReference:
        ...


@dataclass(frozen=True)
class SynthesizeResult:
    """Result from AI-powered report synthesis."""
    success: bool
    report: str
    summary: str
    image_count: int
    document_count: int
    saved_document_id: Optional[str]
    execution_time_ms: int
    iterations: int
    token_usage: Optional[dict[str, int]] = None

    @classmethod
    def from_api_response(cls, data: dict) -> SynthesizeResult:
        ...


@dataclass(frozen=True)
class DocumentAnalysisResult:
    """Result from AI-powered document analysis."""
    success: bool
    analysis: str
    summary: str
    document_count: int
    categorization: Optional[dict[str, Any]]
    chunk_references: list[ChunkReference]
    execution_time_ms: int
    iterations: int
    token_usage: Optional[dict[str, int]] = None

    @classmethod
    def from_api_response(cls, data: dict) -> DocumentAnalysisResult:
        ...


@dataclass(frozen=True)
class FolderActionDetail:
    """Detail of a single folder operation performed."""
    action: str
    folder_id: Optional[str] = None
    folder_name: Optional[str] = None
    file_count: Optional[int] = None

    @classmethod
    def from_api_response(cls, data: dict) -> FolderActionDetail:
        ...


@dataclass(frozen=True)
class OrganizeResult:
    """Result from AI-driven file organization."""
    success: bool
    summary: str
    actions: list[FolderActionDetail]
    folders_created: int
    files_moved: int
    execution_time_ms: int
    iterations: int
    token_usage: Optional[dict[str, int]] = None

    @classmethod
    def from_api_response(cls, data: dict) -> OrganizeResult:
        ...
