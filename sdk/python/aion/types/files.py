from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional


@dataclass(frozen=True)
class FullDescription:
    """

        Detailed description from VLM providers.

        Attributes:
            id: Unique identifier for the description
            description: Full AI-generated description text
            visible_text: OCR-extracted text from the image
            confidence_score: AI confidence score (0-1)
            providers_used: List of VLM providers used
            verification_level: Verification level used (quick/standard/thorough/critical)
            processing_time_ms: Time taken to generate description
            created_at: When the description was created
    """
    id: str
    description: str
    visible_text: Optional[str] = None
    confidence_score: Optional[float] = None
    providers_used: Optional[list[str]] = None
    verification_level: Optional[str] = None
    processing_time_ms: Optional[int] = None
    created_at: Optional[datetime] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> FullDescription:
        """Create FullDescription from API response data."""
        ...


@dataclass(frozen=True)
class ProcessingHistory:
    """

        Processing history entry for a file.

        Attributes:
            id: Unique identifier for the history entry
            operation_type: Type of operation (describe, verify, rules)
            status: Processing status
            created_at: When the operation started
            completed_at: When the operation completed
            error_message: Error message if operation failed
    """
    id: str
    operation_type: str
    status: str
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> ProcessingHistory:
        """Create ProcessingHistory from API response data."""
        ...


@dataclass(frozen=True)
class UserFile:
    """

        Summary of a user file (used in list responses).

        Attributes:
            id: Unique file identifier
            title: User-provided or auto-generated title
            filename: Original uploaded filename
            thumbnail_url: URL to thumbnail image
            upload_description: Quick AI-generated description
            visible_text: OCR-extracted text from image
            tags: List of tags associated with the file
            size_bytes: File size in bytes
            created_at: Upload timestamp
            content_created_at: Actual content creation date from EXIF metadata
            has_full_description: Whether full descriptions exist
            dimensions: Image dimensions {width, height}
            format: Image format (jpeg, png, etc.)
            variant_status: Status of image variant generation
            variant_count: Number of variants generated
            medium_url: URL to medium-size variant
            full_url: URL to full-size image
            blur_hash: BlurHash for blur-up placeholder effect
            description_status: Status of description generation
            description_error: Error message if description generation failed
            content_type: MIME type (image/jpeg, application/pdf, etc.)
            media_type: Computed type: 'image', 'document', or 'link'
    """
    id: str
    size_bytes: int
    has_full_description: bool
    title: Optional[str] = None
    filename: Optional[str] = None
    thumbnail_url: Optional[str] = None
    upload_description: Optional[str] = None
    visible_text: Optional[str] = None
    tags: Optional[list[str]] = None
    created_at: Optional[datetime] = None
    content_created_at: Optional[datetime] = None
    dimensions: Optional[dict[str, int]] = None
    format: Optional[str] = None
    variant_status: Optional[str] = None
    variant_count: Optional[int] = None
    medium_url: Optional[str] = None
    full_url: Optional[str] = None
    blur_hash: Optional[str] = None
    description_status: Optional[str] = None
    description_error: Optional[str] = None
    content_type: Optional[str] = None
    media_type: Optional[str] = None
    # Video fields (coming soon — uncomment when video features are enabled):
    # video_metadata: Optional[dict[str, Any]] = None
    # video_analysis_status: Optional[str] = None
    # video_analysis_job_id: Optional[str] = None
    # scene_count: Optional[int] = None
    # has_audio_transcript: Optional[bool] = None
    # video_url: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> UserFile:
        """Create UserFile from API response data."""
        ...


@dataclass(frozen=True)
class UserFileDetails:
    """

        Full file details (used in get response).

        Attributes:
            id: Unique file identifier
            object_key: S3/storage object key
            title: User-provided or auto-generated title
            tags: List of tags
            size_bytes: File size in bytes
            content_type: MIME type of the file
            dimensions: Image dimensions {width, height}
            format: Image format
            full_url: URL to full-size image (1024px variant, None if not yet generated)
            thumbnail_url: URL to thumbnail
            medium_url: URL to medium-size variant
            original_url: URL to original uploaded file (always available as fallback)
            upload_description: Quick AI description
            visible_text: OCR-extracted text
            description_generated_at: When description was generated
            full_descriptions: List of detailed descriptions
            processing_history: List of processing operations
            hash: File hash
            created_at: Upload timestamp
            updated_at: Last update timestamp
            upload_method: Upload method used - 'DIRECT' or 'POST'
            original_filename: Original filename from upload
            variant_status: Status of variant generation (pending/processing/completed/failed)
            variant_count: Number of variants generated
            blur_hash: BlurHash string for blur-up placeholder loading effect
            description_status: Status of AI description generation (pending/processing/completed/failed)
    """
    id: str
    object_key: str
    size_bytes: int
    content_type: str
    hash: str
    title: Optional[str] = None
    tags: Optional[list[str]] = None
    dimensions: Optional[dict[str, int]] = None
    format: Optional[str] = None
    full_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    medium_url: Optional[str] = None
    original_url: Optional[str] = None
    upload_description: Optional[str] = None
    visible_text: Optional[str] = None
    description_generated_at: Optional[datetime] = None
    full_descriptions: Optional[list[FullDescription]] = None
    processing_history: Optional[list[ProcessingHistory]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    content_created_at: Optional[datetime] = None
    upload_method: Optional[str] = None
    original_filename: Optional[str] = None
    variant_status: Optional[str] = None
    variant_count: Optional[int] = None
    blur_hash: Optional[str] = None
    description_status: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> UserFileDetails:
        """Create UserFileDetails from API response data."""
        ...


@dataclass(frozen=True)
class FileList:
    """

        Paginated list of files.

        Attributes:
            files: List of file summaries
            total_count: Total number of files matching query
            has_more: Whether more files exist beyond current page
    """
    files: list[UserFile]
    total_count: int
    has_more: bool

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> FileList:
        """Create FileList from API response data."""
        ...


@dataclass(frozen=True)
class UpdateFileResult:
    """

        Result of file update operation.

        Attributes:
            id: File identifier
            title: Updated title
            tags: Updated tags
            updated_at: Update timestamp
    """
    id: str
    title: Optional[str] = None
    tags: Optional[list[str]] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> UpdateFileResult:
        """Create UpdateFileResult from API response data."""
        ...


@dataclass(frozen=True)
class DeleteFileResult:
    """

        Result of file deletion operation.

        Attributes:
            id: Deleted file identifier
            deleted_at: Deletion timestamp
            message: Confirmation message
    """
    id: str
    deleted_at: Optional[datetime] = None
    message: str = ''

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DeleteFileResult:
        """Create DeleteFileResult from API response data."""
        ...


@dataclass(frozen=True)
class BatchDeleteFileResult:
    """

        Result for a single file in batch delete operation.

        Attributes:
            id: File identifier
            status: Status of deletion - 'deleted', 'skipped', or 'failed'
            message: Additional details about the operation
            deleted_at: Deletion timestamp (if deleted)
    """
    id: str
    status: str
    message: Optional[str] = None
    deleted_at: Optional[datetime] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> BatchDeleteFileResult:
        """Create BatchDeleteFileResult from API response data."""
        ...


@dataclass(frozen=True)
class BatchDeleteFilesResponse:
    """

        Response for batch delete operation.

        Attributes:
            deleted: Successfully deleted files
            skipped: Files skipped (e.g., currently processing)
            failed: Files that failed to delete
            summary: Summary stats - {total, deleted, skipped, failed}
    """
    deleted: list[BatchDeleteFileResult]
    skipped: list[BatchDeleteFileResult]
    failed: list[BatchDeleteFileResult]
    summary: dict[str, int]

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> BatchDeleteFilesResponse:
        """Create BatchDeleteFilesResponse from API response data."""
        ...
