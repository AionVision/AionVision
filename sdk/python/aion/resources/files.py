from __future__ import annotations
from collections.abc import AsyncIterator
from datetime import datetime
from typing import Any, Optional
from ..config import ClientConfig
from ..exceptions import ValidationError
from ..types.files import BatchDeleteFilesResponse, DeleteFileResult, FileList, UpdateFileResult, UserFile, UserFileDetails


class FilesResource:
    """

        File operations for the Aionvision SDK.

        Provides methods to list, get, update, and delete user files
        along with their AI-generated descriptions and metadata.
    """

    def __init__(self, http: HTTPClient, config: ClientConfig) -> None:
        """

                Initialize the files resource.

                Args:
                    http: HTTP client for API communication
                    config: Client configuration
        """
        ...

    async def list(self, *, search: Optional[str] = None, search_mode: str = 'all', tags: Optional[list[str]] = None, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None, has_description: Optional[bool] = None, ids: Optional[list[str]] = None, limit: int = 20, offset: int = 0, sort_by: str = 'content_created_at', sort_order: str = 'desc') -> FileList:
        """

                List user files with optional filtering and pagination.

                Args:
                    search: Search query for titles and descriptions
                    search_mode: Search scope - 'all', 'metadata', or 'visible_text'
                    tags: Filter by tags (files must have all specified tags)
                    date_from: Filter files created after this date
                    date_to: Filter files created before this date
                    has_description: Filter by description status
                    ids: Filter by specific file IDs (max 500)
                    limit: Number of files to return (1-100, default 20)
                    offset: Pagination offset
                    sort_by: Sort field - 'created_at', 'content_created_at', 'title', 'size_bytes'
                    sort_order: Sort direction - 'asc' or 'desc'

                Returns:
                    FileList with files, total_count, and has_more

                Example:
                    ```python
                    # List recent files with search
                    files = await client.files.list(
                        search="damaged pole",
                        tags=["priority"],
                        limit=10
                    )
                    for f in files.files:
                        print(f"{f.title}: {f.upload_description}")
                    ```
        """
        ...

    async def list_all(self, *, search: Optional[str] = None, search_mode: str = 'all', tags: Optional[list[str]] = None, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None, has_description: Optional[bool] = None, sort_by: str = 'content_created_at', sort_order: str = 'desc', page_size: int = 50) -> AsyncIterator[UserFile]:
        """

                Iterate through all files with automatic pagination.

                This is a convenience method that handles pagination automatically.
                For manual pagination control, use list() instead.

                Args:
                    search: Search query for titles and descriptions
                    search_mode: Search scope - 'all', 'metadata', or 'visible_text'
                    tags: Filter by tags (files must have all specified tags)
                    date_from: Filter files created after this date
                    date_to: Filter files created before this date
                    has_description: Filter by description status
                    sort_by: Sort field - 'created_at', 'content_created_at', 'title', 'size_bytes'
                    sort_order: Sort direction - 'asc' or 'desc'
                    page_size: Number of files per page (1-100, default 50)

                Yields:
                    UserFile objects one at a time

                Example:
                    ```python
                    # Iterate through all files matching search
                    async for file in client.files.list_all(search="damaged"):
                        print(f"{file.title}: {file.upload_description}")

                    # Collect all into a list
                    all_files = [f async for f in client.files.list_all()]
                    ```
        """
        ...

    async def get(self, file_id: str) -> UserFileDetails:
        """

                Get detailed information about a file.

                Returns full file details including all descriptions, visible text,
                tags, processing history, and image variant URLs.

                Args:
                    file_id: Unique file identifier (UUID)

                Returns:
                    UserFileDetails with complete file information

                Example:
                    ```python
                    details = await client.files.get(file_id="abc123...")
                    print(f"Title: {details.title}")
                    print(f"Visible text: {details.visible_text}")
                    print(f"Tags: {details.tags}")

                    for desc in details.full_descriptions or []:
                        print(f"Description: {desc.description}")
                        print(f"Confidence: {desc.confidence_score}")
                    ```
        """
        ...

    async def update(self, file_id: str, *, title: Optional[str] = None, tags: Optional[list[str]] = None) -> UpdateFileResult:
        """

                Update file metadata (title and/or tags).

                At least one of title or tags must be provided.

                Args:
                    file_id: Unique file identifier (UUID)
                    title: New title for the file (max 255 characters)
                    tags: New tags for the file (max 40 tags, each max 50 chars)

                Returns:
                    UpdateFileResult with updated metadata

                Raises:
                    ValidationError: If neither title nor tags are provided,
                        or if validation fails

                Example:
                    ```python
                    result = await client.files.update(
                        file_id="abc123...",
                        title="Damaged Pole #42",
                        tags=["damage", "priority", "reviewed"]
                    )
                    print(f"Updated at: {result.updated_at}")
                    ```
        """
        ...

    async def delete(self, file_id: str) -> DeleteFileResult:
        """

                Soft-delete a file.

                The file can be recovered within 30 days after deletion.

                Args:
                    file_id: Unique file identifier (UUID)

                Returns:
                    DeleteFileResult with deletion confirmation

                Example:
                    ```python
                    result = await client.files.delete(file_id="abc123...")
                    print(f"Deleted: {result.message}")
                    ```
        """
        ...

    async def batch_delete(self, file_ids: list[str]) -> BatchDeleteFilesResponse:
        """

                Soft-delete multiple files in a single batch operation.

                Files can be recovered within 30 days after deletion.
                Files currently processing are skipped (not failed).

                Args:
                    file_ids: List of unique file identifiers (UUIDs), max 100

                Returns:
                    BatchDeleteFilesResponse with:
                    - deleted: Successfully deleted files
                    - skipped: Files skipped (e.g., currently processing)
                    - failed: Files that failed to delete
                    - summary: {total, deleted, skipped, failed}

                Raises:
                    ValidationError: If file_ids is empty, has duplicates, or exceeds 100

                Example:
                    ```python
                    result = await client.files.batch_delete(
                        file_ids=["id1", "id2", "id3"]
                    )
                    print(f"Deleted: {result.summary['deleted']}")
                    print(f"Skipped: {result.summary['skipped']}")
                    for file in result.deleted:
                        print(f"  {file.id}: {file.message}")
                    ```
        """
        ...

    async def get_variant(self, file_id: str, variant_type: str = 'medium_750') -> str:
        """

                Get redirect URL for an image variant.

                Args:
                    file_id: Unique file identifier (UUID)
                    variant_type: Variant size - one of:
                        - 'original': Original uploaded file
                        - 'tiny_64': 64px thumbnail
                        - 'small_256': 256px small
                        - 'medium_750': 750px medium (default)
                        - 'large_1024': 1024px large

                Returns:
                    Presigned URL to the image variant

                Raises:
                    ValidationError: If variant_type is invalid
                    ResourceNotFoundError: If file or variant not found

                Example:
                    ```python
                    url = await client.files.get_variant(file_id="abc123...", variant_type="large_1024")
                    # Use URL to display or download the image
                    ```
        """
        ...

    async def download(self, file_id: str) -> bytes:
        """

                Download the original file content.

                Args:
                    file_id: Unique file identifier (UUID)

                Returns:
                    File content as bytes

                Raises:
                    ResourceNotFoundError: If file not found

                Example:
                    ```python
                    content = await client.files.download(file_id="abc123...")
                    with open("downloaded.jpg", "wb") as f:
                        f.write(content)
                    ```
        """
        ...

    async def trigger_variant_generation(self, file_id: str) -> dict[str, Any]:
        """

                Manually trigger variant generation for an image.

                Useful for retrying failed variant generation or generating
                variants for files that were uploaded without auto-generation.

                Args:
                    file_id: Unique file identifier (UUID)

                Returns:
                    Status dict with job_id and message

                Raises:
                    ResourceNotFoundError: If file not found
                    ValidationError: If variants are already being generated

                Example:
                    ```python
                    result = await client.files.trigger_variant_generation(file_id="abc123...")
                    print(f"Job ID: {result.get('job_id')}")
                    print(f"Message: {result.get('message')}")
                    ```
        """
        ...
