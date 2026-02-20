from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from .cloud_storage import CloudStorageJob
    from .documents import DocumentUploadResult
    from .upload import UploadResult


@dataclass(frozen=True)
class UploadProgressEvent:
    """

        Event fired once per file after it is read from disk and prepared for upload.

        This tracks file *preparation*, not HTTP transfer progress. Each file emits
        exactly one event after it has been fully read into memory. Use ``file_index``
        to track how many files have been prepared out of the total batch.

        Note:
            Because all files in a batch are sent in a single multipart HTTP request,
            per-file network transfer progress is not available. This event indicates
            the file has been read and is queued for upload.

        Example:
            Track batch preparation progress::

                results = await client.upload(
                    "/photos",
                    on_progress=lambda e: print(f"Prepared {e.file_index + 1} files: {e.filename}"),
                )

        Attributes:
            file_index: Zero-based index of the file that was prepared
            uploaded_bytes: Size of the prepared file in bytes (always equals total_bytes)
            total_bytes: Total size of the file in bytes
            filename: Name of the file that was prepared
    """
    file_index: int
    uploaded_bytes: int
    total_bytes: int
    filename: Optional[str] = None

    @property
    def progress_percent(self) -> float:
        """Per-file progress: always 100.0 since each event is emitted after the file is fully read."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


@dataclass(frozen=True)
class FileCompleteEvent:
    """

        Event fired when a single file upload completes.

        Attributes:
            file_index: Zero-based index of the completed file
            result: Upload result with image_id, filename, etc.
    """
    file_index: int
    result: UploadResult

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


@dataclass(frozen=True)
class DescriptionProgressEvent:
    """

        Event fired as AI descriptions complete during polling.

        Attributes:
            completed_count: Number of descriptions completed so far
            total_count: Total number of files awaiting descriptions
            latest_result: The most recently completed result
    """
    completed_count: int
    total_count: int
    latest_result: UploadResult

    @property
    def progress_percent(self) -> float:
        """Calculate description progress as percentage (0-100)."""
        ...

    @property
    def remaining_count(self) -> int:
        """Number of descriptions still pending."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


@dataclass(frozen=True)
class DescriptionFailedEvent:
    """

        Event fired when an AI description fails.

        Attributes:
            file_index: Zero-based index of the failed file
            result: Upload result with error details populated
    """
    file_index: int
    result: UploadResult

    @property
    def error_message(self) -> Optional[str]:
        """Get the error message from the result."""
        ...

    @property
    def is_retryable(self) -> bool:
        """Check if the failure is retryable."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


@dataclass(frozen=True)
class DocumentUploadProgressEvent:
    """

        Event fired once per file after it has been uploaded to storage.

        Each file emits exactly one event after the upload completes.
        Use ``file_index`` to track how many files have been uploaded
        out of the total batch.

        Attributes:
            file_index: Zero-based index of the file that was uploaded
            uploaded_bytes: Size of the uploaded file in bytes (always equals total_bytes)
            total_bytes: Total size of the file in bytes
            filename: Name of the file that was uploaded
    """
    file_index: int
    uploaded_bytes: int
    total_bytes: int
    filename: Optional[str] = None

    @property
    def progress_percent(self) -> float:
        """Per-file progress: always 100.0 since each event is emitted after the file is fully uploaded."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


@dataclass(frozen=True)
class DocumentFileCompleteEvent:
    """

        Event fired when a single document upload completes.

        Attributes:
            file_index: Zero-based index of the completed file
            result: Document upload result with document_id, filename, etc.
    """
    file_index: int
    result: DocumentUploadResult

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


@dataclass(frozen=True)
class DocumentProcessingProgressEvent:
    """

        Event fired as document processing (text extraction) completes during polling.

        Attributes:
            completed_count: Number of documents completed so far
            total_count: Total number of documents awaiting processing
            latest_result: The most recently completed result
    """
    completed_count: int
    total_count: int
    latest_result: DocumentUploadResult

    @property
    def progress_percent(self) -> float:
        """Calculate processing progress as percentage (0-100)."""
        ...

    @property
    def remaining_count(self) -> int:
        """Number of documents still pending processing."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


@dataclass(frozen=True)
class DocumentProcessingFailedEvent:
    """

        Event fired when document processing fails.

        Attributes:
            file_index: Zero-based index of the failed file
            result: Document upload result with error details populated
    """
    file_index: int
    result: DocumentUploadResult

    @property
    def error_message(self) -> Optional[str]:
        """Get the error message from the result."""
        ...

    @property
    def is_retryable(self) -> bool:
        """Check if the failure is retryable."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


@dataclass(frozen=True)
class CloudStorageJobProgressEvent:
    """

        Event fired as a cloud storage job progresses during polling.

        Attributes:
            job: The current job state
    """
    job: CloudStorageJob

    @property
    def progress_percent(self) -> float:
        """Calculate job progress as percentage (0-100)."""
        ...

    @property
    def is_terminal(self) -> bool:
        """Whether the job has reached a final state."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...
