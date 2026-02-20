from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class BatchStatus(str, Enum):
    """Status of a batch operation."""
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'
    PARTIALLY_COMPLETED = 'partially_completed'


class BatchItemStatus(str, Enum):
    """Status of an individual batch item."""
    PENDING = 'pending'
    PROCESSING = 'processing'
    SUCCESS = 'success'
    FAILED = 'failed'
    SKIPPED = 'skipped'


@dataclass(frozen=True)
class BatchImageInput:
    """

        Input for batch describe operation.

        Provide exactly one of: image_url, image_base64, or object_key.

        Attributes:
            image_url: HTTP/HTTPS URL of the image
            image_base64: Base64-encoded image data (with data URL prefix)
            object_key: S3/Spaces object key for previously uploaded image
            metadata: Optional metadata to associate with the image
    """
    image_url: Optional[str] = None
    image_base64: Optional[str] = None
    object_key: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to API request format."""
        ...


@dataclass(frozen=True)
class BatchVerifyInput:
    """

        Input for batch verify operation.

        Attributes:
            image: The image to verify (BatchImageInput)
            content: The text content to verify against the image
            verification_level: Optional per-item verification level override
    """
    image: BatchImageInput
    content: str
    verification_level: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to API request format."""
        ...


@dataclass(frozen=True)
class BatchSubmissionResult:
    """

        Result of submitting a batch operation.

        Attributes:
            batch_id: Unique batch identifier for tracking
            status: Initial batch status (typically "pending")
            total_items: Number of items in the batch
            estimated_completion_time: Estimated time for completion
    """
    batch_id: str
    status: str
    total_items: int
    estimated_completion_time: Optional[datetime] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> BatchSubmissionResult:
        """Create BatchSubmissionResult from API response data."""
        ...


@dataclass(frozen=True)
class BatchStatusResult:
    """

        Status of a batch operation.

        Attributes:
            batch_id: Unique batch identifier
            status: Current batch status
            total_items: Total number of items in batch
            processed_items: Number of items processed so far
            successful_items: Number of successfully processed items
            failed_items: Number of failed items
            success_rate: Proportion of successful items (0-1)
            created_at: When the batch was created
            started_at: When processing started
            completed_at: When processing completed
            estimated_completion_time: Estimated completion time
            progress_percentage: Progress as percentage (0-100)
            avg_processing_time_ms: Average processing time per item
    """
    batch_id: str
    status: BatchStatus
    total_items: int
    processed_items: int
    successful_items: int
    failed_items: int
    success_rate: float
    progress_percentage: float
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_completion_time: Optional[datetime] = None
    avg_processing_time_ms: Optional[int] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> BatchStatusResult:
        """Create BatchStatusResult from API response data."""
        ...

    def is_terminal(self) -> bool:
        """Check if the batch has reached a terminal state."""
        ...


@dataclass(frozen=True)
class BatchItemResult:
    """

        Result for a single item in a batch.

        Attributes:
            item_id: Unique item identifier
            item_index: Index in the original batch (0-based)
            status: Item processing status
            input_data: Original input data for the item
            output_data: Processing results (structure varies by operation)
            error_message: Error message if processing failed
            processing_time_ms: Time taken to process the item
            stored_image_url: URL to access stored image (if applicable)
    """
    item_id: str
    item_index: int
    status: BatchItemStatus
    input_data: Optional[dict[str, Any]] = None
    output_data: Optional[dict[str, Any]] = None
    error_message: Optional[str] = None
    processing_time_ms: Optional[int] = None
    stored_image_url: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> BatchItemResult:
        """Create BatchItemResult from API response data."""
        ...

    @property
    def description(self) -> Optional[str]:
        """Get description from output_data (for describe operations)."""
        ...

    @property
    def confidence_score(self) -> Optional[float]:
        """Get confidence score from output_data."""
        ...

    @property
    def is_verified(self) -> Optional[bool]:
        """Get verification result (for verify operations)."""
        ...


@dataclass(frozen=True)
class BatchResultsPagination:
    """

        Pagination info for batch results.

        Attributes:
            offset: Current page offset
            limit: Number of items per page
            total: Total number of items
            has_more: Whether more items exist
    """
    offset: int
    limit: int
    total: int
    has_more: bool

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> BatchResultsPagination:
        """Create BatchResultsPagination from API response data."""
        ...


@dataclass(frozen=True)
class BatchResultsSummary:
    """

        Summary statistics for batch results.

        Attributes:
            total_items: Total number of items in batch
            successful_items: Number of successfully processed items
            failed_items: Number of failed items
            skipped_items: Number of skipped items
            processing_time_ms: Total processing time
    """
    total_items: int
    successful_items: int
    failed_items: int
    skipped_items: int
    processing_time_ms: int

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> BatchResultsSummary:
        """Create BatchResultsSummary from API response data."""
        ...


@dataclass(frozen=True)
class BatchResults:
    """

        Full batch results with pagination.

        Attributes:
            batch_id: Unique batch identifier
            status: Current batch status
            results: List of item results
            pagination: Pagination information
            summary: Summary statistics
    """
    batch_id: str
    status: BatchStatus
    results: list[BatchItemResult]
    pagination: BatchResultsPagination
    summary: BatchResultsSummary

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> BatchResults:
        """Create BatchResults from API response data."""
        ...

    def successful_results(self) -> list[BatchItemResult]:
        """Get only successful results."""
        ...

    def failed_results(self) -> list[BatchItemResult]:
        """Get only failed results."""
        ...
