from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
from .common import DescriptionStatus


@dataclass(frozen=True)
class UploadResult:
    """

        Result of a successful upload operation.

        Attributes:
            image_id: Unique identifier for the uploaded image
            filename: Original filename
            object_key: Storage object key (S3 path)
            description: AI-generated description (if wait_for_descriptions=True)
            tags: AI-extracted tags (if available)
            visible_text: OCR-extracted text (if present in image)
            confidence_score: AI confidence score (0-1)
            description_status: Status of description generation
            thumbnail_url: URL to thumbnail image (if generated)
            created_at: Upload timestamp
            description_error: Error message if description generation failed
            description_error_type: Classification of the error (if failed)
            description_is_retryable: Whether the description can be retried (if failed)
    """
    image_id: str
    filename: str
    object_key: str
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    visible_text: Optional[str] = None
    confidence_score: Optional[float] = None
    description_status: DescriptionStatus = DescriptionStatus.PENDING
    thumbnail_url: Optional[str] = None
    created_at: Optional[datetime] = None
    description_error: Optional[str] = None
    description_error_type: Optional[str] = None
    description_is_retryable: Optional[bool] = None

    @property
    def is_failed(self) -> bool:
        """Check if description generation failed."""
        ...

    @property
    def is_completed(self) -> bool:
        """Check if description generation completed successfully."""
        ...

    @property
    def is_pending(self) -> bool:
        """Check if description generation is still pending."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """

                Convert to JSON-serializable dictionary.

                Args:
                    exclude_none: If True, exclude fields with None values (default: True)

                Returns:
                    Dictionary suitable for JSON serialization or logging

                Example:
                    result = await client.upload_one("photo.jpg")
                    logger.info("Upload complete", extra=result.to_dict())
        """
        ...

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> UploadResult:
        """Create UploadResult from API response data."""
        ...


@dataclass(frozen=True)
class QuotaInfo:
    """

        Upload quota information.

        Attributes:
            can_proceed: Whether the upload can proceed
            requested: Number of uploads requested
            available: Number of uploads still available
            monthly_limit: Total monthly limit
            current_usage: Current month's usage
            message: Optional message about quota status
    """
    can_proceed: bool
    requested: int
    available: int
    monthly_limit: int
    current_usage: int
    message: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> QuotaInfo:
        """Create QuotaInfo from API response data."""
        ...


@dataclass(frozen=True)
class PresignedUrlInfo:
    """

        Presigned URL information for S3 upload.

        Attributes:
            upload_url: URL to upload the file to
            upload_method: HTTP method to use (PUT or POST)
            upload_headers: Headers to include in the upload request
            object_key: S3 object key for the file
            image_id: Pre-created image ID (if available)
            expires_at: When the presigned URL expires
            max_size_bytes: Maximum allowed file size
    """
    upload_url: str
    upload_method: str
    upload_headers: dict[str, str]
    object_key: str
    image_id: Optional[str] = None
    expires_at: Optional[datetime] = None
    max_size_bytes: Optional[int] = None
    upload_fields: Optional[dict[str, str]] = None
    storage_target: Optional[str] = None
    bucket_name: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> PresignedUrlInfo:
        """Create PresignedUrlInfo from API response data."""
        ...


@dataclass(frozen=True)
class ConfirmResult:
    """

        Result of upload confirmation.

        Attributes:
            upload_id: Upload identifier
            object_key: S3 object key
            storage_path: Full storage path
            confirmed: Whether upload was confirmed
    """
    upload_id: str
    object_key: str
    storage_path: str
    confirmed: bool

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> ConfirmResult:
        """Create ConfirmResult from API response data."""
        ...


@dataclass(frozen=True)
class FileInfo:
    """

        File information for batch upload preparation.

        Attributes:
            filename: Name of the file
            size_bytes: File size in bytes
            content_type: MIME type of the file
            idempotency_key: Optional key for retry handling
    """
    filename: str
    size_bytes: int
    content_type: str
    idempotency_key: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to API request format."""
        ...


@dataclass(frozen=True)
class UploadConfirmation:
    """

        Confirmation data for a single file in a batch.

        Attributes:
            object_key: S3 object key
            success: Whether the upload succeeded
            file_size: Actual uploaded file size
            checksum: Optional file checksum
            error_message: Error message if failed
    """
    object_key: str
    success: bool
    file_size: int
    checksum: Optional[str] = None
    error_message: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to API request format."""
        ...


@dataclass(frozen=True)
class BatchPresignedUrl:
    """Presigned URL info for a file in a batch."""
    file_index: int
    filename: str
    upload_url: str
    upload_method: str
    upload_headers: dict[str, str]
    object_key: str
    expires_at: Optional[datetime]
    image_id: Optional[str]
    upload_fields: Optional[dict[str, str]] = None


@dataclass(frozen=True)
class UploadPlan:
    """Upload strategy plan from batch prepare."""
    strategy: str
    max_concurrent: int
    timeout_per_upload: int
    retry_policy: Optional[dict[str, Any]] = None


@dataclass(frozen=True)
class BatchPrepareResult:
    """

        Result of batch upload preparation.

        Attributes:
            batch_id: Batch identifier for tracking
            upload_plan: Recommended upload strategy
            presigned_urls: Presigned URLs for each file
            total_size_bytes: Total size of all files
            estimated_time_seconds: Estimated upload time
    """
    batch_id: str
    upload_plan: UploadPlan
    presigned_urls: list[BatchPresignedUrl]
    total_size_bytes: int
    estimated_time_seconds: int

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> BatchPrepareResult:
        """Create BatchPrepareResult from API response data."""
        ...


@dataclass(frozen=True)
class StoredImage:
    """Information about a stored image from batch confirm."""
    image_id: str
    object_key: str
    filename: str
    thumbnail_url: Optional[str]
    variant_status: str
    created_at: Optional[datetime]


@dataclass(frozen=True)
class BatchConfirmResult:
    """

        Result of batch upload confirmation.

        Attributes:
            batch_id: Batch identifier
            successful_uploads: Number of successful uploads
            failed_uploads: Number of failed uploads
            processing_status: Status of batch processing
            failed_files: List of failed filenames
            message: Status message
            stored_images: Details of successfully stored images
    """
    batch_id: str
    successful_uploads: int
    failed_uploads: int
    processing_status: str
    failed_files: Optional[list[str]]
    message: str
    stored_images: list[StoredImage]

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> BatchConfirmResult:
        """Create BatchConfirmResult from API response data."""
        ...


@dataclass(frozen=True)
class UploadBatchStatusResult:
    """

        Status of an upload batch operation.

        Used for efficient batch polling instead of polling individual files.

        Attributes:
            batch_id: Batch identifier
            overall_status: Overall batch status (uploading, queued, processing, completed, failed, partially_completed)
            completion_percentage: Progress percentage (0-100)
            total: Total number of items in batch
            completed: Number of completed items
            failed: Number of failed items
            processing: Number of items currently processing
            queued: Number of items queued for processing
    """
    batch_id: str
    overall_status: str
    completion_percentage: float
    total: int
    completed: int
    failed: int
    processing: int
    queued: int

    @property
    def is_terminal(self) -> bool:
        """Check if batch is in terminal state."""
        ...

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> UploadBatchStatusResult:
        """Create UploadBatchStatusResult from API response data."""
        ...


class BatchUploadResults(list):
    """

        List of UploadResult with convenience methods for batch operations.

        This is a regular Python list with additional helper properties and methods
        for working with batch upload results.

        For single-file uploads, use upload_one() which returns UploadResult directly:

            result = await client.upload_one("photo.jpg")
            print(result.description)  # Direct access on UploadResult

        For multiple files, use upload() and iterate or use helper methods:

            results = await client.upload(["a.jpg", "b.jpg"])
            if results.has_failures:
                print(f"{results.succeeded_count}/{len(results)} succeeded")
                for r in results.failed():
                    print(f"{r.filename}: {r.description_error}")
    """

    @property
    def has_failures(self) -> bool:
        """True if any descriptions failed."""
        ...

    @property
    def failed_count(self) -> int:
        """Number of results with failed descriptions."""
        ...

    @property
    def succeeded_count(self) -> int:
        """Number of results with successful descriptions."""
        ...

    @property
    def pending_count(self) -> int:
        """Number of results still pending description generation."""
        ...

    def failed(self) -> list[UploadResult]:
        """Get all results with failed descriptions."""
        ...

    def succeeded(self) -> list[UploadResult]:
        """Get all results with successful descriptions."""
        ...

    def pending(self) -> list[UploadResult]:
        """Get all results still pending description generation."""
        ...

    def retryable(self) -> list[UploadResult]:
        """Get all results with retryable failures."""
        ...

    def raise_on_failures(self) -> BatchUploadResults:
        """

                Raise DescriptionError if any descriptions failed.

                Returns self for method chaining if no failures.

                Example:
                    results = await client.upload(files)
                    results.raise_on_failures()  # Raises if any failed
        """
        ...

    def summary(self) -> str:
        """

                Get a human-readable summary of results.

                Returns:
                    String like "3 succeeded, 1 failed (1 retryable)"

                Example:
                    results = await client.upload(files)
                    logger.info(f"Upload complete: {results.summary()}")
        """
        ...
