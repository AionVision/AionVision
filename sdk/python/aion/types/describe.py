from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from .common import DescriptionStatus as DescriptionStatusEnum


@dataclass(frozen=True)
class DescriptionResult:
    """

        Result from image description.

        Attributes:
            operation_id: Unique operation identifier
            description: Main AI-generated description
            confidence_score: Confidence score (0-1)
            key_elements: Key elements detected in image
            tags: Extracted tags
            visible_text: OCR-extracted text
            verification_level: Verification level used
            provider_count: Number of AI providers used
            processing_time_ms: Time to generate description
            metadata: Additional metadata
    """
    operation_id: str
    description: str
    confidence_score: float
    key_elements: Optional[list[str]] = None
    tags: Optional[list[str]] = None
    visible_text: Optional[str] = None
    verification_level: str = 'standard'
    provider_count: int = 1
    processing_time_ms: int = 0
    metadata: Optional[dict[str, Any]] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DescriptionResult:
        """Create DescriptionResult from API response data."""
        ...


@dataclass(frozen=True)
class DescriptionStatus:
    """

        Status of a description generation operation.

        Attributes:
            image_id: Image identifier
            status: Current status (pending, queued, processing, completed, failed)
            description: Generated description (if completed)
            tags: Extracted tags (if completed)
            visible_text: OCR text (if completed)
            confidence_score: Confidence score (if completed)
            error_message: Error message (if failed)
            created_at: When the operation started
            completed_at: When the operation completed
    """
    image_id: str
    status: str
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    visible_text: Optional[str] = None
    confidence_score: Optional[float] = None
    error_message: Optional[str] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    @property
    def is_complete(self) -> bool:
        """Check if the description is complete (success or failure)."""
        ...

    @property
    def is_successful(self) -> bool:
        """Check if the description completed successfully."""
        ...

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DescriptionStatus:
        """Create DescriptionStatus from API response data."""
        ...


class DescriptionErrorType(str, Enum):
    """

        Classification of description generation errors.

        Used to help SDK users determine appropriate retry strategies.

        Attributes:
            TIMEOUT: VLM provider timed out (retryable)
            RATE_LIMIT: Rate limit exceeded - 429 response (retryable)
            VLM_ERROR: VLM provider error - 5xx, malformed response (retryable)
            VALIDATION_ERROR: Input validation failed (permanent)
            RESOURCE_LIMIT: User quota or resource limit exceeded (permanent)
            UNKNOWN: Unclassified error (not retryable by default)
    """
    TIMEOUT = 'timeout'
    RATE_LIMIT = 'rate_limit'
    VLM_ERROR = 'vlm_error'
    VALIDATION_ERROR = 'validation'
    RESOURCE_LIMIT = 'resource_limit'
    UNKNOWN = 'unknown'


@dataclass(frozen=True)
class DescriptionFailure:
    """

        Details about a failed description operation.

        Provides structured information about why a description failed,
        including error classification to help with retry decisions.

        Attributes:
            image_id: ID of the image that failed
            error_message: Human-readable error message
            error_type: Classification of the error
            is_retryable: Whether the operation can be retried
            filename: Original filename (if available)
            raw_error: Original error details from backend (if available)
    """
    image_id: str
    error_message: str
    error_type: DescriptionErrorType
    is_retryable: bool
    filename: Optional[str] = None
    raw_error: Optional[str] = None

    @staticmethod
    def classify_error(error_msg: str) -> tuple[DescriptionErrorType, bool]:
        """

                Classify an error message and determine if it's retryable.

                Args:
                    error_msg: The error message to classify

                Returns:
                    Tuple of (error_type, is_retryable)
        """
        ...

    @classmethod
    def from_error_message(cls, image_id: str, error_msg: str, filename: Optional[str] = None) -> DescriptionFailure:
        """

                Create a DescriptionFailure from an error message.

                Automatically classifies the error and determines retryability.

                Args:
                    image_id: ID of the failed image
                    error_msg: The error message
                    filename: Optional original filename

                Returns:
                    DescriptionFailure instance with classified error
        """
        ...
