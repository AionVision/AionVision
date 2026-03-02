from __future__ import annotations
import re
from collections.abc import AsyncIterator
from datetime import datetime
from typing import Any, Optional
from ..config import ClientConfig
from ..exceptions import ValidationError
from ..types.files import BatchDeleteFilesResponse
from ..types.links import CreateLinkResult, LinkDeleteResult, LinkDetails, LinkItem, LinkList, LinkUpdateResult, RecrawlLinkResult
MAX_URL_LENGTH = 2048
MAX_TITLE_LENGTH = 500
MAX_TAGS = 40
MAX_TAG_LENGTH = 50
DEFAULT_CRAWL_TIMEOUT = 60.0
DEFAULT_POLL_INTERVAL = 1.0


class LinksResource:
    """

        Link operations for the Aionvision SDK.

        Provides methods to create and manage links (bookmarks) with
        automatic Open Graph metadata extraction.
    """

    def __init__(self, http: HTTPClient, config: ClientConfig) -> None:
        """

                Initialize the links resource.

                Args:
                    http: HTTP client for API communication
                    config: Client configuration
        """
        ...

    async def create(self, url: str, *, title: Optional[str] = None, tags: Optional[list[str]] = None, folder_id: Optional[str] = None, auto_crawl: bool = True) -> CreateLinkResult:
        """

                Create a new link (bookmark).

                Saves a URL and optionally crawls it for Open Graph metadata
                (title, description, image, etc.).

                Args:
                    url: URL to save (must start with http:// or https://)
                    title: Optional title (uses OG metadata title if not provided)
                    tags: Optional list of tags (max 40 tags, each max 50 chars)
                    folder_id: Optional folder to place the link in
                    auto_crawl: Automatically crawl for metadata (default: True)

                Returns:
                    CreateLinkResult with link details and crawl status

                Raises:
                    ValidationError: If URL, title, or tags are invalid

                Example:
                    ```python
                    # Save a link with auto-crawl
                    link = await client.links.create(
                        url="https://example.com/article",
                        title="Important Article",
                        tags=["reference", "2024"]
                    )

                    print(f"Created link: {link.id}")
                    print(f"Domain: {link.domain}")
                    print(f"Status: {link.crawl_status}")

                    if link.og_metadata:
                        print(f"Title: {link.og_metadata.title}")
                        print(f"Description: {link.og_metadata.description}")
                    ```
        """
        ...

    async def recrawl(self, link_id: str) -> RecrawlLinkResult:
        """

                Recrawl a link to refresh its metadata.

                Triggers a new crawl of the URL to update Open Graph metadata.
                Rate limited to once per hour per link.

                Args:
                    link_id: Unique link identifier

                Returns:
                    RecrawlLinkResult with status and updated metadata

                Raises:
                    ValidationError: If link_id is empty
                    RateLimitError: If recrawl requested within 1 hour of last crawl

                Example:
                    ```python
                    try:
                        result = await client.links.recrawl(link_id)
                        print(f"Recrawl status: {result.status}")
                        if result.og_metadata:
                            print(f"New title: {result.og_metadata.title}")
                    except RateLimitError as e:
                        print(f"Rate limited. Retry after: {e.retry_after}s")
                    ```
        """
        ...

    async def get(self, link_id: str) -> LinkDetails:
        """

                Get detailed information about a link.

                Args:
                    link_id: Unique link identifier (UUID)

                Returns:
                    LinkDetails with full link information including OG metadata

                Raises:
                    ValidationError: If link_id is empty
                    ResourceNotFoundError: If link does not exist

                Example:
                    ```python
                    details = await client.links.get(link_id)
                    print(f"Title: {details.og_metadata.title}")
                    print(f"Domain: {details.domain}")
                    ```
        """
        ...

    async def list(self, *, search: Optional[str] = None, tags: Optional[list[str]] = None, folder_id: Optional[str] = None, crawl_status: Optional[str] = None, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None, limit: int = 20, offset: int = 0, sort_by: str = 'created_at', sort_order: str = 'desc') -> LinkList:
        """

                List links with optional filtering and pagination.

                Args:
                    search: Search query for titles and URLs
                    tags: Filter by tags (links must have all specified tags)
                    folder_id: Filter by folder
                    crawl_status: Filter by crawl status
                    date_from: Filter links created after this date
                    date_to: Filter links created before this date
                    limit: Number of links to return (1-100, default 20)
                    offset: Pagination offset
                    sort_by: Sort field - 'created_at', 'title'
                    sort_order: Sort direction - 'asc' or 'desc'

                Returns:
                    LinkList with links, total_count, and has_more

                Raises:
                    ValidationError: If parameters are invalid

                Example:
                    ```python
                    # List recent links
                    page = await client.links.list(limit=10)
                    for link in page.links:
                        print(f"{link.domain}: {link.title}")

                    # Search and filter
                    page = await client.links.list(
                        search="python",
                        tags=["reference"],
                        sort_order="asc"
                    )
                    ```
        """
        ...

    async def list_all(self, *, search: Optional[str] = None, tags: Optional[list[str]] = None, folder_id: Optional[str] = None, crawl_status: Optional[str] = None, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None, sort_by: str = 'created_at', sort_order: str = 'desc', page_size: int = 50) -> AsyncIterator[LinkItem]:
        """

                Iterate through all links with automatic pagination.

                This is an async generator that handles pagination automatically,
                yielding one LinkItem at a time.

                Args:
                    search: Search query for titles and URLs
                    tags: Filter by tags
                    folder_id: Filter by folder
                    crawl_status: Filter by crawl status
                    date_from: Filter links created after this date
                    date_to: Filter links created before this date
                    sort_by: Sort field - 'created_at', 'title'
                    sort_order: Sort direction - 'asc' or 'desc'
                    page_size: Number of links per page (default 50)

                Yields:
                    LinkItem objects one at a time

                Example:
                    ```python
                    async for link in client.links.list_all(tags=["research"]):
                        print(f"{link.domain}: {link.title}")
                    ```
        """
        ...

    async def update(self, link_id: str, *, title: Optional[str] = None, tags: Optional[list[str]] = None) -> LinkUpdateResult:
        """

                Update link metadata (title and/or tags).

                Args:
                    link_id: Unique link identifier
                    title: New title (max 500 characters)
                    tags: New tags (max 40 tags, each max 50 chars)

                Returns:
                    LinkUpdateResult with updated metadata

                Raises:
                    ValidationError: If neither title nor tags provided, or if values invalid
                    ResourceNotFoundError: If link does not exist

                Example:
                    ```python
                    updated = await client.links.update(
                        link_id,
                        title="My Article",
                        tags=["research", "python"]
                    )
                    print(f"Updated: {updated.title}")
                    ```
        """
        ...

    async def delete(self, link_id: str) -> LinkDeleteResult:
        """

                Delete a link.

                Args:
                    link_id: Unique link identifier

                Returns:
                    LinkDeleteResult with deletion confirmation

                Raises:
                    ValidationError: If link_id is empty
                    ResourceNotFoundError: If link does not exist

                Example:
                    ```python
                    result = await client.links.delete(link_id)
                    print(f"Deleted link: {result.id}")
                    ```
        """
        ...

    async def batch_delete(self, link_ids: list[str]) -> BatchDeleteFilesResponse:
        """

                Delete multiple links in a single batch operation.

                Args:
                    link_ids: List of link identifiers (max 100)

                Returns:
                    BatchDeleteFilesResponse with deleted, skipped, failed lists

                Raises:
                    ValidationError: If list is empty, has duplicates, or exceeds 100

                Example:
                    ```python
                    result = await client.links.batch_delete([link1_id, link2_id])
                    print(f"Deleted: {result.summary['deleted']}")
                    print(f"Failed: {result.summary['failed']}")
                    ```
        """
        ...

    async def wait_for_crawl(self, link_id: str, *, timeout: Optional[float] = None, poll_interval: Optional[float] = None) -> LinkDetails:
        """

                Wait for link crawl to complete.

                Polls the link status until crawl completes or fails.

                Args:
                    link_id: Link identifier
                    timeout: Maximum wait time in seconds (default: 60)
                    poll_interval: Time between polls in seconds (default: 1)

                Returns:
                    LinkDetails with final crawl status

                Raises:
                    ValidationError: If link_id is empty
                    AionvisionTimeoutError: If timeout exceeded

                Example:
                    ```python
                    link = await client.links.create("https://example.com", auto_crawl=True)
                    details = await client.links.wait_for_crawl(link.id, timeout=30)
                    print(f"Crawl complete: {details.og_metadata.title}")
                    ```
        """
        ...

    async def create_and_wait(self, url: str, *, title: Optional[str] = None, tags: Optional[list[str]] = None, folder_id: Optional[str] = None, timeout: Optional[float] = None) -> LinkDetails:
        """

                Create a link and wait for crawl to complete.

                Convenience method combining create() and wait_for_crawl().

                Args:
                    url: URL to save
                    title: Optional title
                    tags: Optional tags
                    folder_id: Optional folder
                    timeout: Maximum wait time for crawl (default: 60s)

                Returns:
                    LinkDetails with completed crawl status and metadata

                Example:
                    ```python
                    link = await client.links.create_and_wait(
                        "https://example.com/article",
                        tags=["research"]
                    )
                    print(f"Title: {link.og_metadata.title}")
                    print(f"Description: {link.og_metadata.description}")
                    ```
        """
        ...
