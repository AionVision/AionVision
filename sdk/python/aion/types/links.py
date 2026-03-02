from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class LinkCrawlStatus(str, Enum):
    """Status of link metadata crawling."""
    PENDING = 'pending'
    QUEUED = 'queued'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'


@dataclass(frozen=True)
class LinkOGMetadata:
    """

        Open Graph metadata extracted from a link.

        Attributes:
            title: Page title from og:title or <title>
            description: Page description from og:description or meta description
            image_url: Image URL from og:image
            site_name: Site name from og:site_name
            type: Content type from og:type
            locale: Locale from og:locale
    """
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    site_name: Optional[str] = None
    type: Optional[str] = None
    locale: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> LinkOGMetadata:
        """Create LinkOGMetadata from API response data."""
        ...


@dataclass(frozen=True)
class CreateLinkResult:
    """

        Result of link creation.

        Attributes:
            id: Unique link identifier
            url: The saved URL
            title: Link title (user-provided or from OG metadata)
            domain: Extracted domain from URL
            tags: User-provided tags
            folder_id: Folder containing the link
            crawl_status: Status of metadata crawling (pending/processing/completed/failed)
            og_metadata: Open Graph metadata (if crawled)
            created_at: Creation timestamp
    """
    id: str
    url: str
    domain: str
    crawl_status: str
    title: Optional[str] = None
    tags: Optional[list[str]] = None
    folder_id: Optional[str] = None
    og_metadata: Optional[LinkOGMetadata] = None
    created_at: Optional[datetime] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> CreateLinkResult:
        """Create CreateLinkResult from API response data."""
        ...


@dataclass(frozen=True)
class RecrawlLinkResult:
    """

        Result of link recrawl operation.

        Attributes:
            id: Link identifier
            status: Recrawl status (queued/completed/failed)
            message: Additional information
            og_metadata: Updated Open Graph metadata (if immediately available)
            next_allowed_recrawl: When the next recrawl is allowed (rate limited)
    """
    id: str
    status: str
    message: str = ''
    og_metadata: Optional[LinkOGMetadata] = None
    next_allowed_recrawl: Optional[datetime] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> RecrawlLinkResult:
        """Create RecrawlLinkResult from API response data."""
        ...


@dataclass(frozen=True)
class LinkItem:
    """

        Link summary for list responses (lightweight).

        Attributes:
            id: Unique link identifier
            url: The saved URL (source_url from API)
            domain: Extracted domain from URL
            title: Link title (user-provided or from OG metadata)
            tags: User-provided tags
            folder_id: Folder containing the link
            crawl_status: Status of metadata crawling
            og_metadata: Open Graph metadata (if crawled)
            favicon_url: Resolved favicon URL
            created_at: Creation timestamp
    """
    id: str
    url: str
    domain: str
    title: Optional[str] = None
    tags: Optional[list[str]] = None
    folder_id: Optional[str] = None
    crawl_status: Optional[str] = None
    og_metadata: Optional[LinkOGMetadata] = None
    favicon_url: Optional[str] = None
    created_at: Optional[datetime] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> LinkItem:
        """Create LinkItem from API response data."""
        ...


@dataclass(frozen=True)
class LinkDetails:
    """

        Full link details from get() endpoint.

        Attributes:
            id: Unique link identifier
            url: The saved URL (source_url from API)
            domain: Extracted domain from URL
            title: Link title (user-provided or from OG metadata)
            tags: User-provided tags
            folder_id: Folder containing the link
            crawl_status: Status of metadata crawling
            crawl_error: Error message if crawl failed
            crawled_at: Last crawl timestamp
            og_metadata: Open Graph metadata (if crawled)
            favicon_url: Resolved favicon URL
            extracted_images: Images found on the page
            extracted_images_count: Count of extracted images
            created_at: Creation timestamp
            updated_at: Last update timestamp
    """
    id: str
    url: str
    domain: str
    title: Optional[str] = None
    tags: Optional[list[str]] = None
    folder_id: Optional[str] = None
    crawl_status: Optional[str] = None
    crawl_error: Optional[str] = None
    crawled_at: Optional[datetime] = None
    og_metadata: Optional[LinkOGMetadata] = None
    favicon_url: Optional[str] = None
    extracted_images: Optional[list[dict[str, Any]]] = None
    extracted_images_count: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def is_crawl_complete(self) -> bool:
        """Check if crawl has completed successfully."""
        ...

    @property
    def is_crawl_failed(self) -> bool:
        """Check if crawl has failed."""
        ...

    @property
    def is_crawling(self) -> bool:
        """Check if crawl is still in progress."""
        ...

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> LinkDetails:
        """Create LinkDetails from API response data."""
        ...


@dataclass(frozen=True)
class LinkList:
    """

        Paginated list of links.

        Attributes:
            links: List of link summaries
            total_count: Total number of links matching query
            has_more: Whether more links exist beyond current page
    """
    links: list[LinkItem]
    total_count: int
    has_more: bool

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> LinkList:
        """Create LinkList from API response data."""
        ...


@dataclass(frozen=True)
class LinkUpdateResult:
    """

        Result of link update operation.

        Attributes:
            id: Link identifier
            title: Updated title
            tags: Updated tags
            updated_at: Update timestamp
    """
    id: str
    title: Optional[str] = None
    tags: Optional[list[str]] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> LinkUpdateResult:
        """Create LinkUpdateResult from API response data."""
        ...


@dataclass(frozen=True)
class LinkDeleteResult:
    """

        Result of link deletion.

        Attributes:
            id: Deleted link identifier
            deleted_at: Deletion timestamp
            message: Confirmation message
    """
    id: str
    deleted_at: Optional[datetime] = None
    message: str = ''

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> LinkDeleteResult:
        """Create LinkDeleteResult from API response data."""
        ...
