from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Optional


@dataclass(frozen=True)
class DocumentItem:
    """

        Document summary in list responses.

        Attributes:
            id: Unique document identifier
            filename: Original uploaded filename
            title: User-provided or auto-generated title
            content_type: MIME type of the document
            size_bytes: File size in bytes
            page_count: Number of pages (for PDFs)
            text_extraction_status: Status of text extraction (pending/processing/completed/failed)
            embedding_status: Status of embedding generation
            created_at: Upload timestamp
            updated_at: Last update timestamp
            folder_id: Folder containing the document
            tags: List of tags
    """
    id: str
    filename: str
    content_type: str
    size_bytes: int
    text_extraction_status: str
    title: Optional[str] = None
    page_count: Optional[int] = None
    embedding_status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    folder_id: Optional[str] = None
    tags: Optional[list[str]] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DocumentItem:
        """Create DocumentItem from API response data."""
        ...


@dataclass(frozen=True)
class DocumentDetails:
    """

        Full document details (used in get response).

        Attributes:
            id: Unique document identifier
            filename: Original uploaded filename
            title: User-provided or auto-generated title
            content_type: MIME type of the document
            size_bytes: File size in bytes
            page_count: Number of pages (for PDFs)
            text_extraction_status: Status of text extraction
            embedding_status: Status of embedding generation
            chunk_count: Number of text chunks
            extracted_text_preview: Preview of extracted text
            created_at: Upload timestamp
            updated_at: Last update timestamp
            folder_id: Folder containing the document
            tags: List of tags
            object_key: S3/storage object key
            download_url: Presigned URL for download (if available)
    """
    id: str
    filename: str
    content_type: str
    size_bytes: int
    text_extraction_status: str
    title: Optional[str] = None
    page_count: Optional[int] = None
    embedding_status: Optional[str] = None
    chunk_count: Optional[int] = None
    extracted_text_preview: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    folder_id: Optional[str] = None
    tags: Optional[list[str]] = None
    object_key: Optional[str] = None
    download_url: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DocumentDetails:
        """Create DocumentDetails from API response data."""
        ...


@dataclass(frozen=True)
class DocumentList:
    """

        Paginated list of documents.

        Attributes:
            documents: List of document summaries
            total_count: Total number of documents matching query
            page: Current page number
            page_size: Items per page
            has_more: Whether more pages exist
    """
    documents: list[DocumentItem]
    total_count: int
    page: int
    page_size: int
    has_more: bool

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DocumentList:
        """Create DocumentList from API response data."""
        ...


@dataclass(frozen=True)
class DocumentChunk:
    """

        Individual document chunk with content.

        Attributes:
            id: Unique chunk identifier
            document_id: Parent document ID
            content: Text content of the chunk
            chunk_index: Position in document (0-based)
            page_numbers: Pages this chunk spans
            token_count: Number of tokens in chunk
            embedding: Vector embedding (if requested)
    """
    id: str
    document_id: str
    content: str
    chunk_index: int
    page_numbers: Optional[list[int]] = None
    token_count: Optional[int] = None
    embedding: Optional[list[float]] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DocumentChunk:
        """Create DocumentChunk from API response data."""
        ...


@dataclass(frozen=True)
class DocumentChunksResponse:
    """

        Response containing all chunks for a document.

        Attributes:
            document_id: Parent document ID
            chunks: List of document chunks
            total_chunks: Total number of chunks
    """
    document_id: str
    chunks: list[DocumentChunk]
    total_chunks: int

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DocumentChunksResponse:
        """Create DocumentChunksResponse from API response data."""
        ...


@dataclass(frozen=True)
class DocumentSearchResult:
    """

        Single search result (chunk with relevance score).

        Attributes:
            chunk_id: Unique chunk identifier
            document_id: Parent document ID
            document_filename: Filename of the document
            content: Text content of the matching chunk
            score: Similarity score (0-1)
            page_numbers: Pages this chunk spans
            chunk_index: Position in document
    """
    chunk_id: str
    document_id: str
    document_filename: str
    content: str
    score: float
    page_numbers: Optional[list[int]] = None
    chunk_index: Optional[int] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DocumentSearchResult:
        """Create DocumentSearchResult from API response data."""
        ...


@dataclass(frozen=True)
class DocumentSearchResponse:
    """

        Complete search response.

        Attributes:
            results: List of matching chunks
            total_count: Total number of matching chunks
            search_time_ms: Time taken for search in milliseconds
            query: The search query used
    """
    results: list[DocumentSearchResult]
    total_count: int
    search_time_ms: int
    query: str

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DocumentSearchResponse:
        """Create DocumentSearchResponse from API response data."""
        ...


@dataclass(frozen=True)
class DocumentPresignedUploadResult:
    """

        Presigned URL response for document upload.

        Attributes:
            upload_url: Presigned URL for uploading to S3
            object_key: S3 object key to use
            expires_at: When the presigned URL expires
            upload_headers: Additional headers to include in upload request
    """
    upload_url: str
    object_key: str
    expires_at: Optional[datetime] = None
    upload_headers: Optional[dict[str, str]] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DocumentPresignedUploadResult:
        """Create DocumentPresignedUploadResult from API response data."""
        ...


@dataclass(frozen=True)
class DocumentConfirmResult:
    """

        Upload confirmation response.

        Attributes:
            document_id: ID of the created document
            filename: Original filename
            status: Processing status
            message: Confirmation message
    """
    document_id: str
    filename: str
    status: str
    message: str = ''

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DocumentConfirmResult:
        """Create DocumentConfirmResult from API response data."""
        ...


@dataclass(frozen=True)
class DocumentStatusResult:
    """

        Document processing status response.

        Attributes:
            document_id: Document identifier
            text_extraction_status: Status of text extraction (pending/processing/completed/failed)
            embedding_status: Status of embedding generation
            page_count: Number of pages extracted
            chunk_count: Number of chunks created
            error_message: Error message if processing failed
    """
    document_id: str
    text_extraction_status: str
    embedding_status: Optional[str] = None
    page_count: Optional[int] = None
    chunk_count: Optional[int] = None
    error_message: Optional[str] = None

    @property
    def is_completed(self) -> bool:
        """Check if processing is fully completed."""
        ...

    @property
    def is_failed(self) -> bool:
        """Check if processing has failed."""
        ...

    @property
    def is_processing(self) -> bool:
        """Check if still processing."""
        ...

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DocumentStatusResult:
        """Create DocumentStatusResult from API response data."""
        ...


@dataclass(frozen=True)
class DocumentQuotaCheck:
    """

        Quota check response for document uploads.

        Attributes:
            can_proceed: Whether upload can proceed
            document_count: Current document count
            document_limit: Maximum allowed documents
            storage_used_bytes: Storage currently used
            storage_limit_bytes: Storage limit
            message: Additional information
    """
    can_proceed: bool
    document_count: int
    document_limit: int
    storage_used_bytes: int
    storage_limit_bytes: int
    message: str = ''

    @property
    def documents_remaining(self) -> int:
        """Number of documents that can still be uploaded."""
        ...

    @property
    def storage_remaining_bytes(self) -> int:
        """Bytes of storage remaining."""
        ...

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DocumentQuotaCheck:
        """Create DocumentQuotaCheck from API response data."""
        ...


@dataclass(frozen=True)
class DocumentBatchFileInfo:
    """

        File info for batch upload preparation.

        Attributes:
            filename: Original filename
            upload_url: Presigned URL for this file
            object_key: S3 object key
            upload_headers: Headers to include in upload
    """
    filename: str
    upload_url: str
    object_key: str
    upload_headers: Optional[dict[str, str]] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DocumentBatchFileInfo:
        """Create DocumentBatchFileInfo from API response data."""
        ...


@dataclass(frozen=True)
class DocumentBatchPrepareResult:
    """

        Batch preparation response.

        Attributes:
            batch_id: Unique batch identifier
            files: List of file info with presigned URLs
            expires_at: When the presigned URLs expire
    """
    batch_id: str
    files: list[DocumentBatchFileInfo]
    expires_at: Optional[datetime] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DocumentBatchPrepareResult:
        """Create DocumentBatchPrepareResult from API response data."""
        ...


@dataclass(frozen=True)
class DocumentBatchConfirmItem:
    """

        Individual document result in batch confirmation.

        Attributes:
            document_id: Created document ID
            filename: Original filename
            status: Status (created/failed)
            error: Error message if failed
    """
    document_id: str
    filename: str
    status: str
    error: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DocumentBatchConfirmItem:
        """Create DocumentBatchConfirmItem from API response data."""
        ...


@dataclass(frozen=True)
class DocumentBatchConfirmResult:
    """

        Batch confirmation response.

        Attributes:
            batch_id: Batch identifier
            documents: List of created documents
            created_count: Number of documents created
            failed_count: Number of failures
    """
    batch_id: str
    documents: list[DocumentBatchConfirmItem]
    created_count: int
    failed_count: int

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DocumentBatchConfirmResult:
        """Create DocumentBatchConfirmResult from API response data."""
        ...


@dataclass(frozen=True)
class DocumentBatchStatusItem:
    """

        Status of individual document in batch.

        Attributes:
            document_id: Document identifier
            filename: Original filename
            text_extraction_status: Status of text extraction
            embedding_status: Status of embedding generation
            error_message: Error if processing failed
    """
    document_id: str
    filename: str
    text_extraction_status: str
    embedding_status: Optional[str] = None
    error_message: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DocumentBatchStatusItem:
        """Create DocumentBatchStatusItem from API response data."""
        ...


@dataclass(frozen=True)
class DocumentBatchStatusResult:
    """

        Batch status response.

        Attributes:
            batch_id: Batch identifier
            documents: List of document statuses
            completed_count: Number completed
            processing_count: Number still processing
            failed_count: Number failed
            is_complete: Whether all documents are done
    """
    batch_id: str
    documents: list[DocumentBatchStatusItem]
    completed_count: int
    processing_count: int
    failed_count: int
    is_complete: bool

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DocumentBatchStatusResult:
        """Create DocumentBatchStatusResult from API response data."""
        ...


@dataclass(frozen=True)
class DocumentDeleteResult:
    """

        Single document deletion result.

        Attributes:
            id: Document identifier
            status: Deletion status (deleted/failed)
            message: Additional information
            deleted_at: Deletion timestamp
    """
    id: str
    status: str
    message: str = ''
    deleted_at: Optional[datetime] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DocumentDeleteResult:
        """Create DocumentDeleteResult from API response data."""
        ...


@dataclass(frozen=True)
class DocumentBatchDeleteResponse:
    """

        Batch delete response.

        Attributes:
            deleted: Successfully deleted documents
            failed: Documents that failed to delete
            summary: Summary stats {total, deleted, failed}
    """
    deleted: list[DocumentDeleteResult]
    failed: list[DocumentDeleteResult]
    summary: dict[str, int]

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DocumentBatchDeleteResponse:
        """Create DocumentBatchDeleteResponse from API response data."""
        ...


class DocumentProcessingStatus(str, Enum):
    """

        Status of document text extraction and processing.

        Attributes:
            PENDING: Document uploaded, processing not yet started
            PROCESSING: Text extraction in progress
            COMPLETED: Processing completed successfully
            FAILED: Processing failed
    """
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'


class DocumentProcessingErrorType(str, Enum):
    """

        Classification of document processing errors.

        Used to help SDK users determine appropriate retry strategies.

        Attributes:
            TIMEOUT: Processing timed out (retryable)
            EXTRACTION_ERROR: Text extraction failed (may be retryable)
            UNSUPPORTED_FORMAT: Document format not supported (permanent)
            CORRUPT_FILE: File is corrupted or unreadable (permanent)
            PASSWORD_PROTECTED: Document requires password (permanent)
            TOO_LARGE: Document exceeds size limits (permanent)
            EMBEDDING_ERROR: Embedding generation failed (retryable)
            RESOURCE_LIMIT: Resource quota exceeded (permanent)
            UNKNOWN: Unclassified error (not retryable by default)
    """
    TIMEOUT = 'timeout'
    EXTRACTION_ERROR = 'extraction_error'
    UNSUPPORTED_FORMAT = 'unsupported_format'
    CORRUPT_FILE = 'corrupt_file'
    PASSWORD_PROTECTED = 'password_protected'
    TOO_LARGE = 'too_large'
    EMBEDDING_ERROR = 'embedding_error'
    RESOURCE_LIMIT = 'resource_limit'
    UNKNOWN = 'unknown'


@dataclass(frozen=True)
class DocumentProcessingFailure:
    """

        Details about a failed document processing operation.

        Provides structured information about why processing failed,
        including error classification to help with retry decisions.

        Attributes:
            document_id: ID of the document that failed
            error_message: Human-readable error message
            error_type: Classification of the error
            is_retryable: Whether the operation can be retried
            filename: Original filename (if available)
    """
    document_id: str
    error_message: str
    error_type: DocumentProcessingErrorType
    is_retryable: bool
    filename: Optional[str] = None

    @staticmethod
    def classify_error(error_msg: str) -> tuple[DocumentProcessingErrorType, bool]:
        """

                Classify an error message and determine if it's retryable.

                Args:
                    error_msg: The error message to classify

                Returns:
                    Tuple of (error_type, is_retryable)
        """
        ...

    @classmethod
    def from_error_message(cls, document_id: str, error_msg: str, filename: Optional[str] = None) -> DocumentProcessingFailure:
        """

                Create a DocumentProcessingFailure from an error message.

                Automatically classifies the error and determines retryability.

                Args:
                    document_id: ID of the failed document
                    error_msg: The error message
                    filename: Optional original filename

                Returns:
                    DocumentProcessingFailure instance with classified error
        """
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


@dataclass(frozen=True)
class DocumentUploadResult:
    """

        Result of a document upload operation.

        Attributes:
            document_id: Unique identifier for the uploaded document
            filename: Original filename
            object_key: Storage object key (S3 path)
            content_type: MIME type of the document
            size_bytes: File size in bytes
            text_extraction_status: Status of text extraction
            embedding_status: Status of embedding generation
            page_count: Number of pages (for PDFs)
            chunk_count: Number of text chunks created
            extracted_text_preview: Preview of extracted text
            created_at: Upload timestamp
            processing_error: Error message if processing failed
            processing_error_type: Classification of the error as string (DocumentProcessingErrorType.value)
            processing_is_retryable: Whether the processing can be retried (if failed)
    """
    document_id: str
    filename: str
    object_key: str
    content_type: str
    size_bytes: int
    text_extraction_status: DocumentProcessingStatus = DocumentProcessingStatus.PENDING
    embedding_status: Optional[str] = None
    page_count: Optional[int] = None
    chunk_count: Optional[int] = None
    extracted_text_preview: Optional[str] = None
    created_at: Optional[datetime] = None
    processing_error: Optional[str] = None
    processing_error_type: Optional[str] = None
    processing_is_retryable: Optional[bool] = None

    @property
    def is_failed(self) -> bool:
        """Check if document processing failed."""
        ...

    @property
    def is_completed(self) -> bool:
        """Check if document processing completed successfully."""
        ...

    @property
    def is_pending(self) -> bool:
        """Check if document processing is still pending."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """

                Convert to JSON-serializable dictionary.

                Args:
                    exclude_none: If True, exclude fields with None values (default: True)

                Returns:
                    Dictionary suitable for JSON serialization or logging

                Example:
                    result = await client.documents.upload_one("report.pdf")
                    logger.info("Upload complete", extra=result.to_dict())
        """
        ...

    @classmethod
    def from_status_result(cls, status: DocumentStatusResult, initial: DocumentUploadResult) -> DocumentUploadResult:
        """

                Create an updated DocumentUploadResult from a status result.

                Args:
                    status: The status result from polling
                    initial: The initial upload result with base info

                Returns:
                    Updated DocumentUploadResult with processing status
        """
        ...


class BatchDocumentUploadResults(list):
    """

        List of DocumentUploadResult with convenience methods for batch operations.

        This is a regular Python list with additional helper properties and methods
        for working with batch document upload results.

        For single-file uploads, use upload_one() which returns DocumentUploadResult directly:

            result = await client.documents.upload_one("report.pdf")
            print(f"Processed {result.page_count} pages")

        For multiple files, use upload() and iterate or use helper methods:

            results = await client.documents.upload("/path/to/docs")
            if results.has_failures:
                print(f"{results.succeeded_count}/{len(results)} succeeded")
                for r in results.failed():
                    print(f"{r.filename}: {r.processing_error}")
    """

    @property
    def has_failures(self) -> bool:
        """True if any document processing failed."""
        ...

    @property
    def failed_count(self) -> int:
        """Number of results with failed processing."""
        ...

    @property
    def succeeded_count(self) -> int:
        """Number of results with successful processing."""
        ...

    @property
    def pending_count(self) -> int:
        """Number of results still pending processing."""
        ...

    def failed(self) -> list[DocumentUploadResult]:
        """Get all results with failed processing."""
        ...

    def succeeded(self) -> list[DocumentUploadResult]:
        """Get all results with successful processing."""
        ...

    def pending(self) -> list[DocumentUploadResult]:
        """Get all results still pending processing."""
        ...

    def retryable(self) -> list[DocumentUploadResult]:
        """Get all results with retryable failures."""
        ...

    def raise_on_failures(self) -> BatchDocumentUploadResults:
        """

                Raise DocumentProcessingError if any processing failed.

                Returns self for method chaining if no failures.

                Example:
                    results = await client.documents.upload(files)
                    results.raise_on_failures()  # Raises if any failed
        """
        ...

    def summary(self) -> str:
        """

                Get a human-readable summary of results.

                Returns:
                    String like "3 succeeded, 1 failed (1 retryable)"

                Example:
                    results = await client.documents.upload(files)
                    logger.info(f"Upload complete: {results.summary()}")
        """
        ...
