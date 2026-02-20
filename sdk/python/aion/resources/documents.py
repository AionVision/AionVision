from __future__ import annotations
import asyncio
import logging
import mimetypes
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any, Callable, Optional, Union
import aiofiles
from ..config import ClientConfig
from ..exceptions import DocumentProcessingError, QuotaExceededError, UploadError, ValidationError
from ..types.callbacks import DocumentFileCompleteEvent, DocumentProcessingFailedEvent, DocumentProcessingProgressEvent, DocumentUploadProgressEvent
from ..types.documents import BatchDocumentUploadResults, DocumentBatchConfirmResult, DocumentBatchDeleteResponse, DocumentBatchPrepareResult, DocumentBatchStatusResult, DocumentChunksResponse, DocumentConfirmResult, DocumentDetails, DocumentItem, DocumentList, DocumentPresignedUploadResult, DocumentProcessingFailure, DocumentProcessingStatus, DocumentQuotaCheck, DocumentSearchResponse, DocumentStatusResult, DocumentUploadResult
logger = logging.getLogger(__name__)
ALLOWED_CONTENT_TYPES = {'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain', 'text/markdown'}
MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024
SUPPORTED_DOCUMENT_EXTENSIONS = {'.pdf', '.docx', '.txt', '.md'}
EXTENSION_TO_CONTENT_TYPE = {'.pdf': 'application/pdf', '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.txt': 'text/plain', '.md': 'text/markdown'}
BATCH_CHUNK_SIZE = 100
MAX_BATCH_FILES = 10000
DEFAULT_PROCESSING_TIMEOUT = 600.0


class DocumentsResource:
    """

        Document operations for the Aionvision SDK.

        Provides methods to upload, list, search, and manage documents
        including PDFs, Word documents, text files, and markdown files.
        Documents are automatically processed for text extraction and
        semantic search capabilities.
    """

    def __init__(self, http: HTTPClient, config: ClientConfig) -> None:
        """

                Initialize the documents resource.

                Args:
                    http: HTTP client for API communication
                    config: Client configuration
        """
        ...

    async def request_upload(self, filename: str, content_type: str, size_bytes: int, *, storage_target: str = 'default') -> DocumentPresignedUploadResult:
        """

                Request a presigned URL for document upload.

                This is the first step in the upload workflow. After receiving the
                presigned URL, upload the file directly to S3, then call confirm_upload().

                Args:
                    filename: Original filename (used for display)
                    content_type: MIME type (pdf, docx, txt, md)
                    size_bytes: File size in bytes (max 50MB)
                    storage_target: Storage target - "default" or "custom"

                Returns:
                    DocumentPresignedUploadResult with upload_url and object_key

                Raises:
                    ValidationError: If content_type or size_bytes is invalid

                Example:
                    ```python
                    # Step 1: Request presigned URL
                    presigned = await client.documents.request_upload(
                        filename="manual.pdf",
                        content_type="application/pdf",
                        size_bytes=1024000
                    )

                    # Step 2: Upload to S3 using presigned.upload_url
                    # ... your S3 upload code ...

                    # Step 3: Confirm the upload
                    result = await client.documents.confirm_upload(
                        object_key=presigned.object_key,
                        size_bytes=1024000,
                        content_type="application/pdf"
                    )
                    ```
        """
        ...

    async def confirm_upload(self, object_key: str, size_bytes: int, content_type: str, *, checksum: Optional[str] = None) -> DocumentConfirmResult:
        """

                Confirm a document upload after uploading to S3.

                This triggers text extraction and embedding generation.

                Args:
                    object_key: S3 object key from request_upload()
                    size_bytes: Actual file size in bytes
                    content_type: MIME type of the uploaded file
                    checksum: Optional MD5 checksum for verification

                Returns:
                    DocumentConfirmResult with document_id and status

                Example:
                    ```python
                    result = await client.documents.confirm_upload(
                        object_key=presigned.object_key,
                        size_bytes=1024000,
                        content_type="application/pdf"
                    )
                    print(f"Document ID: {result.document_id}")
                    ```
        """
        ...

    async def get_status(self, document_id: str) -> DocumentStatusResult:
        """

                Get document processing status.

                Use this to poll for completion after uploading a document.

                Args:
                    document_id: Document identifier from confirm_upload()

                Returns:
                    DocumentStatusResult with text_extraction_status and embedding_status

                Example:
                    ```python
                    import asyncio

                    # Poll for completion
                    while True:
                        status = await client.documents.get_status(document_id)
                        if status.is_completed:
                            print(f"Processed {status.page_count} pages")
                            break
                        if status.is_failed:
                            print(f"Error: {status.error_message}")
                            break
                        await asyncio.sleep(2)
                    ```
        """
        ...

    async def quota_check(self, file_count: int = 1) -> DocumentQuotaCheck:
        """

                Check if upload quota allows for new document uploads.

                Args:
                    file_count: Number of files to be uploaded (default: 1)

                Returns:
                    DocumentQuotaCheck with can_proceed and quota information

                Example:
                    ```python
                    quota = await client.documents.quota_check(file_count=5)
                    if quota.can_proceed:
                        # Proceed with upload
                        ...
                    else:
                        print(f"Quota exceeded: {quota.message}")
                        print(f"Remaining: {quota.documents_remaining} documents")
                    ```
        """
        ...

    async def list(self, *, page: int = 1, page_size: int = 20, status_filter: Optional[str] = None) -> DocumentList:
        """

                List documents with pagination.

                Args:
                    page: Page number (1-based, default: 1)
                    page_size: Items per page (1-100, default: 20)
                    status_filter: Filter by text_extraction_status
                        (pending/processing/completed/failed)

                Returns:
                    DocumentList with documents and pagination info

                Example:
                    ```python
                    # List all completed documents
                    docs = await client.documents.list(
                        page_size=50,
                        status_filter="completed"
                    )
                    print(f"Total: {docs.total_count}")
                    for doc in docs.documents:
                        print(f"- {doc.filename} ({doc.page_count} pages)")
                    ```
        """
        ...

    async def list_all(self, *, page_size: int = 50, status_filter: Optional[str] = None) -> AsyncIterator[DocumentItem]:
        """

                Iterate through all documents with automatic pagination.

                Args:
                    page_size: Items per page (1-100, default: 50)
                    status_filter: Filter by text_extraction_status

                Yields:
                    DocumentItem objects one at a time

                Example:
                    ```python
                    # Iterate through all documents
                    async for doc in client.documents.list_all():
                        print(f"{doc.filename}: {doc.text_extraction_status}")

                    # Collect all into a list
                    all_docs = [d async for d in client.documents.list_all()]
                    ```
        """
        ...

    async def get(self, document_id: str) -> DocumentDetails:
        """

                Get detailed information about a document.

                Args:
                    document_id: Unique document identifier

                Returns:
                    DocumentDetails with full document information

                Example:
                    ```python
                    details = await client.documents.get(document_id)
                    print(f"Filename: {details.filename}")
                    print(f"Pages: {details.page_count}")
                    print(f"Chunks: {details.chunk_count}")
                    if details.extracted_text_preview:
                        print(f"Preview: {details.extracted_text_preview[:200]}...")
                    ```
        """
        ...

    async def get_text(self, document_id: str) -> str:
        """

                Get full extracted text from a document.

                Args:
                    document_id: Unique document identifier

                Returns:
                    Full extracted text as a string

                Example:
                    ```python
                    text = await client.documents.get_text(document_id)
                    print(f"Extracted {len(text)} characters")
                    ```
        """
        ...

    async def get_chunks(self, document_id: str, *, include_embeddings: bool = False) -> DocumentChunksResponse:
        """

                Get all chunks for a document.

                Chunks are the text segments used for semantic search.

                Args:
                    document_id: Unique document identifier
                    include_embeddings: Include vector embeddings (default: False)

                Returns:
                    DocumentChunksResponse with list of chunks

                Example:
                    ```python
                    chunks = await client.documents.get_chunks(document_id)
                    print(f"Total chunks: {chunks.total_chunks}")
                    for chunk in chunks.chunks:
                        print(f"Chunk {chunk.chunk_index}: {chunk.content[:100]}...")
                    ```
        """
        ...

    async def download(self, document_id: str) -> str:
        """

                Get download URL for a document.

                Args:
                    document_id: Unique document identifier

                Returns:
                    Presigned URL for downloading the document

                Example:
                    ```python
                    url = await client.documents.download(document_id)
                    # Use URL to download the file
                    ```
        """
        ...

    async def search(self, query: str, *, limit: int = 20, similarity_threshold: float = 0.3, document_ids: Optional[list[str]] = None) -> DocumentSearchResponse:
        """

                Search documents using semantic similarity.

                Searches across all document chunks and returns the most
                relevant matches based on the query.

                Args:
                    query: Search query text
                    limit: Maximum results to return (1-100, default: 20)
                    similarity_threshold: Minimum similarity score (0.0-1.0, default: 0.3)
                    document_ids: Optional list of document IDs to search within

                Returns:
                    DocumentSearchResponse with matching chunks and scores

                Example:
                    ```python
                    results = await client.documents.search(
                        "safety inspection procedures",
                        limit=10,
                        similarity_threshold=0.5
                    )

                    print(f"Found {results.total_count} matches in {results.search_time_ms}ms")
                    for chunk in results.results:
                        print(f"- {chunk.document_filename} (p{chunk.page_numbers})")
                        print(f"  Score: {chunk.score:.2f}")
                        print(f"  {chunk.content[:100]}...")
                    ```
        """
        ...

    async def delete(self, document_id: str) -> None:
        """

                Delete a document.

                Args:
                    document_id: Unique document identifier

                Example:
                    ```python
                    await client.documents.delete(document_id)
                    print("Document deleted")
                    ```
        """
        ...

    async def batch_delete(self, document_ids: list[str]) -> DocumentBatchDeleteResponse:
        """

                Delete multiple documents in a single batch operation.

                Args:
                    document_ids: List of document IDs to delete (1-100, no duplicates)

                Returns:
                    DocumentBatchDeleteResponse with deleted, failed, and summary

                Raises:
                    ValidationError: If document_ids is empty, has duplicates, or exceeds 100

                Example:
                    ```python
                    result = await client.documents.batch_delete(
                        document_ids=["id1", "id2", "id3"]
                    )
                    print(f"Deleted: {result.summary['deleted']}")
                    print(f"Failed: {result.summary['failed']}")
                    ```
        """
        ...

    async def batch_prepare(self, files: list[dict[str, Any]]) -> DocumentBatchPrepareResult:
        """

                Prepare batch upload for multiple documents.

                Args:
                    files: List of file info dicts with:
                        - filename: Original filename
                        - content_type: MIME type
                        - size_bytes: File size

                Returns:
                    DocumentBatchPrepareResult with batch_id and presigned URLs for each file

                Example:
                    ```python
                    prepared = await client.documents.batch_prepare([
                        {"filename": "doc1.pdf", "content_type": "application/pdf", "size_bytes": 1000},
                        {"filename": "doc2.pdf", "content_type": "application/pdf", "size_bytes": 2000},
                    ])

                    # Upload each file to its presigned URL
                    for file_info in prepared.files:
                        # Upload using file_info.upload_url
                        ...

                    # Then confirm the batch
                    result = await client.documents.batch_confirm(
                        batch_id=prepared.batch_id,
                        confirmations=[...]
                    )
                    ```
        """
        ...

    async def batch_confirm(self, batch_id: str, confirmations: list[dict[str, Any]]) -> DocumentBatchConfirmResult:
        """

                Confirm batch upload after uploading files to S3.

                Args:
                    batch_id: Batch identifier from batch_prepare()
                    confirmations: List of confirmation dicts with:
                        - object_key: S3 object key
                        - size_bytes: Actual file size
                        - content_type: MIME type
                        - checksum: Optional MD5 checksum

                Returns:
                    DocumentBatchConfirmResult with created documents and counts

                Example:
                    ```python
                    result = await client.documents.batch_confirm(
                        batch_id=prepared.batch_id,
                        confirmations=[
                            {"object_key": "key1", "size_bytes": 1000, "content_type": "application/pdf"},
                            {"object_key": "key2", "size_bytes": 2000, "content_type": "application/pdf"},
                        ]
                    )
                    print(f"Created: {result.created_count}, Failed: {result.failed_count}")
                    ```
        """
        ...

    async def batch_status(self, batch_id: str) -> DocumentBatchStatusResult:
        """

                Get processing status for a batch of documents.

                Args:
                    batch_id: Batch identifier

                Returns:
                    DocumentBatchStatusResult with document statuses and counts

                Example:
                    ```python
                    import asyncio

                    # Poll for batch completion
                    while True:
                        status = await client.documents.batch_status(batch_id)
                        print(f"Completed: {status.completed_count}, Processing: {status.processing_count}")
                        if status.is_complete:
                            break
                        await asyncio.sleep(5)
                    ```
        """
        ...

    async def wait_for_processing(self, document_id: str, *, timeout: Optional[float] = None, poll_interval: Optional[float] = None) -> DocumentStatusResult:
        """

                Poll until document text extraction completes or fails.

                Args:
                    document_id: Document identifier from confirm_upload()
                    timeout: Maximum wait time in seconds (default: 600)
                    poll_interval: Interval between polls in seconds (default: from config)

                Returns:
                    DocumentStatusResult with final processing status

                Raises:
                    AionvisionTimeoutError: If timeout is exceeded
                    DocumentProcessingError: If processing fails

                Example:
                    ```python
                    # Upload without waiting
                    result = await client.documents.upload_one(
                        "report.pdf",
                        wait_for_processing=False
                    )

                    # Later, wait for processing
                    status = await client.documents.wait_for_processing(result.document_id)
                    if status.is_completed:
                        print(f"Processed {status.page_count} pages, {status.chunk_count} chunks")
                    ```
        """
        ...

    async def upload_one(self, file: Union[str, Path, bytes], *, filename: Optional[str] = None, wait_for_processing: bool = True, raise_on_failure: bool = True, processing_timeout: Optional[float] = None, storage_target: str = 'default') -> DocumentUploadResult:
        """

                Upload a single document with automatic text extraction.

                This is the preferred method for single document uploads. Returns a
                DocumentUploadResult directly (not wrapped in BatchDocumentUploadResults).

                Uses the streaming upload path (POST /user-files/upload/stream-batch)
                which is faster and avoids the 3-step presigned URL flow.

                Args:
                    file: File path or bytes to upload
                    filename: Override filename (required if file is bytes)
                    wait_for_processing: Wait for text extraction to complete (default: True)
                    raise_on_failure: Raise DocumentProcessingError if processing fails
                        (default: True). Set to False to handle failures manually.
                    processing_timeout: Override default processing timeout in seconds
                    storage_target: Where to store:
                        - "default": Aionvision's S3 bucket
                        - "custom": Your organization's configured S3 bucket

                Returns:
                    DocumentUploadResult with document_id, page_count, chunk_count, etc.

                Raises:
                    ValidationError: If file type is unsupported
                    QuotaExceededError: If upload quota is insufficient
                    UploadError: If upload fails
                    DocumentProcessingError: If processing fails and raise_on_failure=True

                Example:
                    ```python
                    # Simple usage - raises on processing failure
                    result = await client.documents.upload_one("report.pdf")
                    print(f"Processed {result.page_count} pages, {result.chunk_count} chunks")

                    # Handle failures manually
                    result = await client.documents.upload_one(
                        "report.pdf",
                        raise_on_failure=False
                    )
                    if result.is_failed:
                        print(f"Failed: {result.processing_error}")
                    ```
        """
        ...

    async def upload(self, files: Union[str, Path, bytes, list[Union[str, Path, bytes]]], *, filename: Optional[str] = None, filenames: Optional[list[str]] = None, recursive: bool = True, include_hidden: bool = False, wait_for_processing: bool = True, raise_on_failure: bool = True, processing_timeout: Optional[float] = None, on_progress: Optional[Callable[[DocumentUploadProgressEvent], None]] = None, on_file_complete: Optional[Callable[[DocumentFileCompleteEvent], None]] = None, on_processing_progress: Optional[Callable[[DocumentProcessingProgressEvent], None]] = None, on_processing_failed: Optional[Callable[[DocumentProcessingFailedEvent], None]] = None, storage_target: str = 'default') -> BatchDocumentUploadResults:
        """

                Upload one or more documents with automatic text extraction.

                Supports single files, directories, or lists of files/directories.
                Directories are automatically expanded to include all supported document
                files (pdf, docx, txt, md). Always returns BatchDocumentUploadResults.

                For single file uploads, prefer upload_one() which returns DocumentUploadResult directly.

                Args:
                    files: File path, bytes, directory, or list of any of these
                    filename: Override filename (for single bytes upload)
                    filenames: Override filenames (for multiple uploads)
                    recursive: Search directories recursively (default: True)
                    include_hidden: Include hidden files starting with . (default: False)
                    wait_for_processing: Wait for text extraction to complete
                    raise_on_failure: Raise DocumentProcessingError if any processing fails
                        (default: True). Set to False to handle failures via
                        results.has_failures and results.failed().
                    processing_timeout: Override default processing timeout in seconds
                    on_progress: Callback(DocumentUploadProgressEvent) for file upload completion
                    on_file_complete: Callback(DocumentFileCompleteEvent) per completed upload
                    on_processing_progress: Callback(DocumentProcessingProgressEvent) during polling
                    on_processing_failed: Callback(DocumentProcessingFailedEvent) for each failure
                    storage_target: Where to store:
                        - "default": Aionvision's S3 bucket
                        - "custom": Your organization's configured S3 bucket

                Returns:
                    BatchDocumentUploadResults - list of DocumentUploadResult with helper methods:
                    - results.has_failures: True if any processing failed
                    - results.failed(): Get all failed results
                    - results.retryable(): Get retryable failures

                Raises:
                    ValidationError: If more than 10,000 files or unsupported type
                    QuotaExceededError: If upload quota is insufficient
                    UploadError: If upload fails
                    DocumentProcessingError: If any processing fails and raise_on_failure=True

                Example:
                    ```python
                    # Raises on any failure (default)
                    results = await client.documents.upload("/path/to/docs")
                    for r in results:
                        print(f"{r.filename}: {r.page_count} pages")

                    # Handle failures manually
                    results = await client.documents.upload(
                        "/path/to/docs",
                        raise_on_failure=False
                    )
                    if results.has_failures:
                        for r in results.failed():
                            print(f"{r.filename}: {r.processing_error}")
                    ```
        """
        ...
