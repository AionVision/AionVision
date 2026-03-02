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
            object_key: Storage object key
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
            max_batch_size: Maximum files per batch upload
            prepaid_credits: Prepaid credit balance
            max_concurrent_uploads: Maximum concurrent uploads allowed
    """
    can_proceed: bool
    requested: int
    available: int
    monthly_limit: int
    current_usage: int
    message: Optional[str] = None
    max_batch_size: Optional[int] = None
    prepaid_credits: int = 0
    max_concurrent_uploads: Optional[int] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> QuotaInfo:
        """Create QuotaInfo from API response data."""
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
