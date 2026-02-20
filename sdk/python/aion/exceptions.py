from __future__ import annotations
from typing import Any, Optional


class AionvisionError(Exception):
    """

        Base exception for all Aionvision SDK errors.

        Attributes:
            code: Error code identifying the type of error
            message: Human-readable error message
            details: Additional error details
    """

    def __init__(self, code: str, message: str, *, details: Optional[dict[str, Any]] = None) -> None:
        ...


class AuthenticationError(AionvisionError):
    """Invalid or missing API key."""

    def __init__(self, message: str = 'Authentication failed') -> None:
        ...


class RateLimitError(AionvisionError):
    """

        API rate limit exceeded.

        Attributes:
            retry_after: Seconds to wait before retrying (from Retry-After header)
            limit: Maximum requests allowed in the rate limit window
            remaining: Requests remaining in current window (always 0 when raised)
            reset: Unix timestamp when the rate limit window resets
    """

    def __init__(self, message: str = 'Rate limit exceeded', *, retry_after: Optional[int] = None, limit: Optional[int] = None, remaining: Optional[int] = None, reset: Optional[int] = None) -> None:
        ...


class ValidationError(AionvisionError):
    """Request validation failed."""

    def __init__(self, message: str, *, details: Optional[dict[str, Any]] = None) -> None:
        ...


class QuotaExceededError(AionvisionError):
    """

        Upload or processing quota exceeded.

        Attributes:
            available: Number of operations still available
            limit: Total quota limit
            partial_results: Results from chunks completed before quota was exceeded.
                Only populated during chunked batch uploads. Contains a BatchUploadResults
                with the successfully uploaded files.
    """

    def __init__(self, message: str, *, available: int = 0, limit: int = 0, partial_results: Any = None) -> None:
        ...


class ResourceNotFoundError(AionvisionError):
    """Requested resource not found."""

    def __init__(self, resource_type: str, resource_id: str, *, message: Optional[str] = None, details: Optional[dict[str, Any]] = None) -> None:
        ...


class AionvisionTimeoutError(AionvisionError):
    """

        Operation timed out.

        Note: Named AionvisionTimeoutError to avoid shadowing the built-in TimeoutError.

        Attributes:
            last_result: The last result received before timeout (if any)
    """

    def __init__(self, message: str = 'Operation timed out', *, last_result: Optional[Any] = None) -> None:
        ...


class ServerError(AionvisionError):
    """Server-side error (5xx)."""

    def __init__(self, message: str = 'Server error') -> None:
        ...


class AionvisionPermissionError(AionvisionError):
    """

        Insufficient permissions (HTTP 403).

        Note: Named AionvisionPermissionError to avoid shadowing the built-in PermissionError.
    """

    def __init__(self, message: str = 'Permission denied') -> None:
        ...


class UploadError(AionvisionError):
    """

        File upload failed.

        Attributes:
            filename: Name of the file that failed to upload
            stage: Stage where the failure occurred (quota, presigned, upload, confirm,
                session_results, chunk_upload)
            session_id: Upload session identifier, when available. Can be used to
                manually recover results via the session results endpoint.
            partial_results: Results from chunks completed before the failure.
                Only populated during chunked batch uploads. Contains a BatchUploadResults
                with the successfully uploaded files.
    """

    def __init__(self, message: str, *, filename: Optional[str] = None, stage: Optional[str] = None, session_id: Optional[str] = None, partial_results: Any = None) -> None:
        ...


class DescriptionError(AionvisionError):
    """

        Description generation failed.

        Attributes:
            image_id: ID of the image that failed
            status: Final status of the description operation
    """

    def __init__(self, message: str, *, image_id: Optional[str] = None, status: Optional[str] = None) -> None:
        ...


class DocumentProcessingError(AionvisionError):
    """

        Document processing (text extraction/embedding) failed.

        Attributes:
            document_id: ID of the document that failed
            status: Final status of the processing operation
    """

    def __init__(self, message: str, *, document_id: Optional[str] = None, status: Optional[str] = None) -> None:
        ...


class CloudStorageError(AionvisionError):
    """

        Cloud storage operation failed.

        Attributes:
            job_id: ID of the cloud storage job
            job_status: Final status of the job
    """

    def __init__(self, message: str, *, job_id: Optional[str] = None, job_status: Optional[str] = None) -> None:
        ...


class ChatError(AionvisionError):
    """

        Chat operation failed.

        Attributes:
            session_id: ID of the chat session
    """

    def __init__(self, message: str, *, session_id: Optional[str] = None, error_code: Optional[str] = None) -> None:
        ...


class BatchError(AionvisionError):
    """

        Batch operation failed.

        Attributes:
            batch_id: ID of the batch operation
            failed_items: List of items that failed
    """

    def __init__(self, message: str, *, batch_id: Optional[str] = None, failed_items: Optional[list[str]] = None) -> None:
        ...


class AionvisionConnectionError(AionvisionError):
    """

        Network connection failed.

        Note: Named AionvisionConnectionError to avoid shadowing the built-in ConnectionError.
    """

    def __init__(self, message: str = 'Connection failed') -> None:
        ...


class CircuitBreakerError(AionvisionError):
    """

        Circuit breaker is open due to repeated failures.

        The circuit breaker prevents requests to a failing endpoint to allow
        it to recover. Requests will be blocked until the timeout expires.

        Attributes:
            endpoint: The endpoint that triggered the circuit breaker
            retry_after: Seconds until the circuit breaker will allow requests
    """

    def __init__(self, endpoint: str, retry_after: float) -> None:
        ...


class SSEStreamError(AionvisionError):
    """

        SSE stream failed after exhausting reconnection attempts.

        This error is raised when the SSE streaming connection fails repeatedly
        and all reconnection attempts have been exhausted.

        Attributes:
            last_event_id: Last successfully received event ID
            events_received: Total number of events received before failure
            reconnect_attempts: Number of reconnection attempts made
    """

    def __init__(self, message: str, *, last_event_id: Optional[str] = None, events_received: int = 0, reconnect_attempts: int = 0) -> None:
        ...
