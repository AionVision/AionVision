from __future__ import annotations
import asyncio
import logging
import mimetypes
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional, Union
from ..config import ClientConfig
from ..exceptions import AionvisionError, AionvisionTimeoutError, DescriptionError, QuotaExceededError, UploadError, ValidationError
from ..types.callbacks import DescriptionFailedEvent, DescriptionProgressEvent, FileCompleteEvent, UploadProgressEvent
from ..types.common import DescriptionStatus as DescriptionStatusEnum, StorageTarget
from ..types.describe import DescriptionFailure, DescriptionStatus
from ..types.upload import BatchConfirmResult, BatchPrepareResult, BatchUploadResults, ConfirmResult, FileInfo, PresignedUrlInfo, QuotaInfo, UploadBatchStatusResult, UploadConfirmation, UploadResult
logger = logging.getLogger(__name__)
SUPPORTED_CONTENT_TYPES = {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}
BATCH_CHUNK_SIZE = 100
MAX_BATCH_FILES = 10000
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}


class UploadResource:
    """

        Upload operations for the Aionvision SDK.

        Provides both high-level convenience methods (upload, upload_batch)
        and low-level methods for fine-grained control.
    """

    def __init__(self, http: HTTPClient, config: ClientConfig) -> None:
        """

                Initialize the upload resource.

                Args:
                    http: HTTP client for API communication
                    config: Client configuration
        """
        ...

    async def upload_one(self, file: Union[str, Path, bytes], *, filename: Optional[str] = None, wait_for_descriptions: bool = True, raise_on_failure: bool = True, description_timeout: Optional[float] = None, storage_target: Union[StorageTarget, str] = StorageTarget.DEFAULT) -> UploadResult:
        """

                Upload a single file with automatic AI description.

                This is the preferred method for single file uploads. Returns an
                UploadResult directly (not wrapped in BatchUploadResults).

                Args:
                    file: File path or bytes to upload
                    filename: Override filename (required if file is bytes)
                    wait_for_descriptions: Wait for AI description to complete
                    raise_on_failure: Raise DescriptionError if description fails
                        (default: True). Set to False to handle failures manually.
                    description_timeout: Override default polling timeout
                    storage_target: Where to store:
                        - StorageTarget.DEFAULT: Aionvision's S3 bucket
                        - StorageTarget.CUSTOM: Your organization's configured S3 bucket

                Returns:
                    UploadResult with image_id, description, tags, etc.

                Raises:
                    ValidationError: If file type is unsupported
                    QuotaExceededError: If upload quota is insufficient
                    UploadError: If upload fails
                    DescriptionError: If description fails and raise_on_failure=True

                Example:
                    ```python
                    # Simple usage - raises on description failure
                    result = await client.upload_one("photo.jpg")
                    print(result.description)

                    # Handle failures manually
                    result = await client.upload_one(
                        "photo.jpg",
                        raise_on_failure=False
                    )
                    if result.is_failed:
                        print(f"Failed: {result.description_error}")
                    ```
        """
        ...

    async def upload(self, files: Union[str, Path, bytes, list[Union[str, Path, bytes]]], *, filename: Optional[str] = None, filenames: Optional[list[str]] = None, recursive: bool = True, include_hidden: bool = False, wait_for_descriptions: bool = True, raise_on_failure: bool = True, description_timeout: Optional[float] = None, on_progress: Optional[Callable[[UploadProgressEvent], None]] = None, on_file_complete: Optional[Callable[[FileCompleteEvent], None]] = None, on_description_progress: Optional[Callable[[DescriptionProgressEvent], None]] = None, on_description_failed: Optional[Callable[[DescriptionFailedEvent], None]] = None, storage_target: Union[StorageTarget, str] = StorageTarget.DEFAULT) -> BatchUploadResults:
        """

                Upload one or more files with automatic AI description.

                Supports single files, directories, or lists of files/directories.
                Directories are automatically expanded to include all supported image
                files (jpg, jpeg, png, webp, gif). Always returns BatchUploadResults.

                For single file uploads, prefer upload_one() which returns UploadResult directly.

                Args:
                    files: File path, bytes, directory, or list of any of these
                    filename: Override filename (for single bytes upload)
                    filenames: Override filenames (for multiple uploads)
                    recursive: Search directories recursively (default: True)
                    include_hidden: Include hidden files starting with . (default: False)
                    wait_for_descriptions: Wait for AI descriptions to complete
                    raise_on_failure: Raise DescriptionError if any description fails
                        (default: True). Set to False to handle failures via
                        results.has_failures and results.failed().
                    description_timeout: Override default polling timeout
                    on_progress: Callback(UploadProgressEvent) for file preparation progress
                    on_file_complete: Callback(FileCompleteEvent) per completed upload
                    on_description_progress: Callback(DescriptionProgressEvent) during polling
                    on_description_failed: Callback(DescriptionFailedEvent) for each failure
                    storage_target: Where to store:
                        - StorageTarget.DEFAULT: Aionvision's S3 bucket
                        - StorageTarget.CUSTOM: Your organization's configured S3 bucket

                Returns:
                    BatchUploadResults - list of UploadResult with helper methods:
                    - results.has_failures: True if any descriptions failed
                    - results.failed(): Get all failed results
                    - results.retryable(): Get retryable failures

                Raises:
                    ValidationError: If more than 10,000 files or unsupported type
                    QuotaExceededError: If upload quota is insufficient
                    UploadError: If upload fails
                    DescriptionError: If any description fails and raise_on_failure=True

                Example:
                    ```python
                    # Raises on any failure (default)
                    results = await client.upload("/path/to/photos")
                    for r in results:
                        print(r.description)

                    # Handle failures manually
                    results = await client.upload(
                        "/path/to/photos",
                        raise_on_failure=False
                    )
                    if results.has_failures:
                        for r in results.failed():
                            print(f"{r.filename}: {r.description_error}")
                    ```
        """
        ...

    async def upload_batch(self, files: Union[str, Path, list[Union[str, Path, bytes]]], *, filenames: Optional[list[str]] = None, recursive: bool = True, include_hidden: bool = False, wait_for_descriptions: bool = True, raise_on_failure: bool = True, description_timeout: Optional[float] = None, on_progress: Optional[Callable[[UploadProgressEvent], None]] = None, on_file_complete: Optional[Callable[[FileCompleteEvent], None]] = None, on_description_progress: Optional[Callable[[DescriptionProgressEvent], None]] = None, on_description_failed: Optional[Callable[[DescriptionFailedEvent], None]] = None, intent: str = 'describe', verification_level: str = 'standard', storage_target: str = 'default') -> BatchUploadResults:
        """

                Upload multiple files in parallel with optimized batch workflow.

                Supports uploading files, directories, or a mix of both. Directories
                are automatically expanded to include all supported image files
                (jpg, jpeg, png, webp, gif). Supports up to 10,000 files by
                automatically chunking into 100-file batches.

                Concurrency is controlled by the backend configuration (not user-configurable).

                Args:
                    files: File path, directory path, or list of paths (up to 10,000 files)
                    filenames: Override filenames (required if files are bytes)
                    recursive: Search directories recursively (default: True)
                    include_hidden: Include hidden files starting with . (default: False)
                    wait_for_descriptions: Wait for all AI descriptions
                    raise_on_failure: Raise DescriptionError if any description fails
                        (default: True). Set to False to handle failures manually.
                    description_timeout: Override polling timeout
                    on_progress: Callback(UploadProgressEvent) for file preparation progress
                    on_file_complete: Callback(FileCompleteEvent) per completed file
                    on_description_progress: Callback(DescriptionProgressEvent) during polling
                    on_description_failed: Callback(DescriptionFailedEvent) for each failure
                    intent: Processing intent (describe, verify, rules)
                    verification_level: AI verification level
                    storage_target: Where to store files:
                        - "default": Aionvision's S3 bucket (default)
                        - "custom": Your organization's configured S3 bucket

                Returns:
                    BatchUploadResults with helper methods for checking failures:
                    - results.has_failures: True if any descriptions failed
                    - results.failed(): Get all failed results
                    - results.retryable(): Get retryable failures

                Raises:
                    ValidationError: If more than 10,000 files are provided after expansion
                    QuotaExceededError: If quota is insufficient
                    UploadError: If batch preparation or uploads fail
                    DescriptionError: If any description fails and raise_on_failure=True

                Example:
                    ```python
                    # Raises on any failure (default)
                    results = await client.uploads.upload_batch("/path/to/photos")
                    for result in results:
                        print(result.description)

                    # Handle failures manually
                    results = await client.uploads.upload_batch(
                        "/path/to/photos",
                        raise_on_failure=False
                    )
                    if results.has_failures:
                        for result in results.failed():
                            print(f"{result.filename}: {result.description_error}")
                    ```
        """
        ...

    async def check_quota(self, file_count: int = 1) -> QuotaInfo:
        """

                Check if upload quota allows the operation.

                Args:
                    file_count: Number of files to upload

                Returns:
                    QuotaInfo with quota status and availability
        """
        ...

    async def request_presigned_url(self, filename: str, content_type: str, size_bytes: int, *, purpose: str = 'image_analysis', idempotency_key: Optional[str] = None, storage_target: str = 'default') -> PresignedUrlInfo:
        """

                Get a presigned URL for direct S3 upload.

                Args:
                    filename: Original filename
                    content_type: MIME type of the file
                    size_bytes: File size in bytes
                    purpose: Upload purpose (default: image_analysis)
                    idempotency_key: Optional key for retry handling
                    storage_target: Where to store the file:
                        - "default": Aionvision's S3 bucket (default)
                        - "custom": Your organization's configured S3 bucket

                Returns:
                    PresignedUrlInfo with upload URL and metadata
        """
        ...

    async def confirm_upload(self, object_key: str, size_bytes: int, *, checksum: Optional[str] = None) -> ConfirmResult:
        """

                Confirm upload completion and trigger auto-describe.

                Args:
                    object_key: S3 object key of uploaded file
                    size_bytes: Actual uploaded file size
                    checksum: Optional file checksum for verification

                Returns:
                    ConfirmResult with upload ID and status
        """
        ...

    async def wait_for_description(self, image_id: str, *, timeout: Optional[float] = None, poll_interval: Optional[float] = None) -> DescriptionStatus:
        """

                Poll until description is ready.

                Args:
                    image_id: Image identifier
                    timeout: Maximum wait time (default: from config)
                    poll_interval: Polling interval (default: from config)

                Returns:
                    DescriptionStatus with description data

                Raises:
                    AionvisionTimeoutError: If timeout is exceeded
                    DescriptionError: If description generation fails
        """
        ...

    async def batch_prepare(self, files: list[FileInfo], *, intent: str = 'describe', verification_level: str = 'standard', additional_params: Optional[dict[str, Any]] = None) -> BatchPrepareResult:
        """

                Prepare batch upload with presigned URLs for all files.

                Args:
                    files: List of file information
                    intent: Processing intent (describe, verify, rules)
                    verification_level: AI verification level
                    additional_params: Additional processing parameters

                Returns:
                    BatchPrepareResult with batch ID and presigned URLs
        """
        ...

    async def batch_confirm(self, batch_id: str, confirmations: list[UploadConfirmation], *, auto_process: bool = True) -> BatchConfirmResult:
        """

                Confirm batch uploads and trigger processing.

                Args:
                    batch_id: Batch identifier from prepare step
                    confirmations: Upload confirmation for each file
                    auto_process: Automatically trigger processing

                Returns:
                    BatchConfirmResult with status and stored images
        """
        ...

    async def get_batch_status(self, batch_id: str) -> UploadBatchStatusResult:
        """

                Get status of an upload batch.

                Args:
                    batch_id: Batch identifier from batch_prepare

                Returns:
                    UploadBatchStatusResult with overall status and progress
        """
        ...
