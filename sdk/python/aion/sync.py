from __future__ import annotations
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Iterator, Optional, Union
from .client import AionVision
from .config import ClientConfig
from .types.settings import S3ConfigStatus, S3ValidationResult
from .types import DescriptionFailedEvent, DescriptionProgressEvent, DescriptionStatus, FileCompleteEvent, UploadProgressEvent
from .types.callbacks import DocumentFileCompleteEvent, DocumentProcessingFailedEvent, DocumentProcessingProgressEvent, DocumentUploadProgressEvent
from .types.audit import AuditLogEntry, AuditLogList
from .types.batch import BatchItemResult, BatchResults, BatchStatusResult
from .types.chat import ChatImageList, ChatMessage, ChatResponse, ChatSession, ChatSessionDetail, ImageReference, PlanActionResponse, SessionList
from .types.colors import BatchColorExtractionResult, ColorExtractionResult, ColorFamilyInfo, ColorSearchResponse, ColorSearchResult
from .types.common import StorageTarget
from .types.files import BatchDeleteFilesResponse, DeleteFileResult, FileList, UpdateFileResult, UserFile, UserFileDetails
from .types.tenant import TenantLimits, TenantMember, TenantSettings
from .types.agent_operations import DocumentAnalysisResult, OrganizeResult, SynthesizeResult
from .types.agent_search import DocumentSearchAgentResult, ImageSearchAgentResult
from .types.documents import BatchDocumentUploadResults, DocumentBatchConfirmResult, DocumentBatchDeleteResponse, DocumentBatchPrepareResult, DocumentBatchStatusResult, DocumentChunksResponse, DocumentConfirmResult, DocumentDetails, DocumentItem, DocumentList, DocumentPresignedUploadResult, DocumentQuotaCheck, DocumentSearchResponse, DocumentStatusResult, DocumentUploadResult
from .types.folders import DeleteFolderResult, Folder, FolderBreadcrumbs, FolderContents, FolderTree, MoveFilesResult
from .types.links import CreateLinkResult, LinkDeleteResult, LinkDetails, LinkItem, LinkList, LinkUpdateResult, RecrawlLinkResult
from .types.callbacks import CloudStorageJobProgressEvent
from .types.cloud_storage import CloudFileInput, CloudStorageConnection, CloudStorageJob, CompleteAuthResult, ConnectionList, DisconnectResult, ExportResult, ImportResult, InitiateAuthResult
from .types.upload import BatchConfirmResult, BatchPrepareResult, BatchUploadResults, ConfirmResult, FileInfo, PresignedUrlInfo, QuotaInfo, UploadBatchStatusResult, UploadConfirmation, UploadResult


class SyncChatSession:
    """

        Synchronous chat session wrapper.

        Note: Streaming is not available in sync mode.

        Can be used as a context manager for automatic cleanup:
            with SyncAionVision(api_key="aion_...") as client:
                with client.chat_session() as session:
                    response = session.send("Find damaged poles")
                    print(response.content)
                # Session automatically closed

        Or manually:
            with SyncAionVision(api_key="aion_...") as client:
                session = client.chat_session()
                response = session.send("Find damaged poles")
                print(response.content)
                client.close_session(session.session_id)
    """

    def __init__(self, async_client: AionVision, session: ChatSession, loop: asyncio.AbstractEventLoop, auto_close: bool = True):
        """
        Initialize the sync chat session wrapper.

                Args:
                    async_client: The underlying async client
                    session: The ChatSession object
                    loop: The event loop to use for running coroutines
                    auto_close: Whether to close session on context exit (default: True)
        """
        ...

    def __enter__(self) -> SyncChatSession:
        """Context manager entry - returns self."""
        ...

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[Any]) -> None:
        """
        Context manager exit - closes the session if auto_close is True.

                Cleanup errors are suppressed to prevent masking exceptions from the with block.
        """
        ...

    def close(self) -> None:
        """
        Close this chat session.

                Safe to call multiple times. Errors are suppressed to prevent
                masking exceptions from the with block when called from __exit__.
        """
        ...

    @property
    def session_id(self) -> str:
        """Get the session ID."""
        ...

    @property
    def session(self) -> ChatSession:
        """Get the underlying ChatSession object."""
        ...

    @property
    def is_closed(self) -> bool:
        """
        Check if the session has been closed or is no longer usable.

                Returns True if:
                - The session was explicitly closed, OR
                - The parent client's event loop was closed
        """
        ...

    def send(self, message: str, *, force_detailed_analysis: bool = False) -> ChatResponse:
        """

                Send a message and get a complete response.

                Note: Streaming is not available in sync mode.

                Args:
                    message: User message text
                    force_detailed_analysis: Force high-resolution VLM analysis

                Returns:
                    ChatResponse with text, images, metadata

                Raises:
                    RuntimeError: If the session or client has been closed
        """
        ...

    def update_images(self, image_ids: list[str]) -> dict[str, Any]:
        """

                Update the images associated with this session.

                Args:
                    image_ids: List of image IDs to associate with the session

                Returns:
                    Response dict with status
        """
        ...

    def update_documents(self, document_ids: list[str]) -> dict[str, Any]:
        """

                Update the documents associated with this session.

                Args:
                    document_ids: List of document IDs to associate with the session

                Returns:
                    Response dict with status
        """
        ...

    def get_messages(self, limit: Optional[int] = None) -> list[ChatMessage]:
        """

                Get messages from this session.

                Args:
                    limit: Maximum number of messages to return

                Returns:
                    List of ChatMessage objects
        """
        ...


class _SyncResourceBase:
    """Base class for sync resource wrappers with loop validation."""

    def __init__(self, async_resource, loop: asyncio.AbstractEventLoop):
        ...


class SyncFilesResource(_SyncResourceBase):
    """Synchronous wrapper for file operations."""

    def list(self, *, search: Optional[str] = None, search_mode: str = 'all', tags: Optional[list[str]] = None, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None, has_description: Optional[bool] = None, ids: Optional[list[str]] = None, limit: int = 20, offset: int = 0, sort_by: str = 'content_created_at', sort_order: str = 'desc') -> FileList:
        """List files with search/filter/pagination."""
        ...

    def list_all(self, *, search: Optional[str] = None, search_mode: str = 'all', tags: Optional[list[str]] = None, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None, has_description: Optional[bool] = None, sort_by: str = 'content_created_at', sort_order: str = 'desc', page_size: int = 50) -> Iterator[UserFile]:
        """
        Iterate through all files with automatic pagination.

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
                    for file in client.files.list_all(search="damaged"):
                        print(f"{file.title}: {file.upload_description}")
                    ```
        """
        ...

    def get(self, file_id: str) -> UserFileDetails:
        """Get detailed file info."""
        ...

    def update(self, file_id: str, *, title: Optional[str] = None, tags: Optional[list[str]] = None) -> UpdateFileResult:
        """Update file title and/or tags."""
        ...

    def delete(self, file_id: str) -> DeleteFileResult:
        """Delete a file."""
        ...

    def batch_delete(self, file_ids: list[str]) -> BatchDeleteFilesResponse:
        """Delete multiple files."""
        ...

    def get_variant(self, file_id: str, variant_type: str = 'medium_750') -> str:
        """Get URL for a file variant."""
        ...

    def download(self, file_id: str) -> bytes:
        """Download the original file."""
        ...

    def trigger_variant_generation(self, file_id: str) -> dict[str, Any]:
        """Trigger generation of file variants."""
        ...


class SyncChatResource(_SyncResourceBase):
    """Synchronous wrapper for chat operations."""

    def create_session(self, *, title: Optional[str] = None, image_ids: Optional[list[str]] = None, use_all_images: bool = True) -> ChatSession:
        """Create a new chat session."""
        ...

    def send(self, message: str, *, session_id: str, force_detailed_analysis: bool = False) -> ChatResponse:
        """Send a message and get a complete response."""
        ...

    def close_session(self, session_id: str) -> dict[str, Any]:
        """Close a chat session."""
        ...

    def get_session(self, session_id: str, *, include_messages: bool = True, message_limit: Optional[int] = None) -> ChatSessionDetail:
        """Get session details."""
        ...

    def list_sessions(self, *, limit: int = 20, offset: int = 0, active_only: bool = False) -> SessionList:
        """List chat sessions."""
        ...

    def iter_sessions(self, *, page_size: int = 20, active_only: bool = False) -> Iterator[ChatSession]:
        """Iterate through all chat sessions with automatic pagination."""
        ...

    def get_messages(self, session_id: str, *, limit: Optional[int] = None) -> list[ChatMessage]:
        """Get messages from a session."""
        ...

    def update_images(self, session_id: str, image_ids: list[str]) -> dict[str, Any]:
        """Update images in a session."""
        ...

    def update_documents(self, session_id: str, document_ids: list[str]) -> dict[str, Any]:
        """Update documents in a session."""
        ...

    def update_mode(self, session_id: str, use_all_images: bool) -> dict[str, Any]:
        """Update session mode (use all images vs specific)."""
        ...

    def rename_session(self, session_id: str, title: str) -> dict[str, Any]:
        """Rename a session."""
        ...

    def export_session(self, session_id: str, *, format: str = 'markdown', include_metadata: bool = False) -> bytes:
        """Export session as markdown or other format."""
        ...

    def approve_plan(self, session_id: str, plan_id: str) -> PlanActionResponse:
        """Approve an execution plan."""
        ...

    def cancel_plan(self, session_id: str, plan_id: str) -> PlanActionResponse:
        """Cancel a pending execution plan."""
        ...

    def get_all_images(self, *, limit: int = 1000, offset: int = 0) -> ChatImageList:
        """Get all images available for chat."""
        ...

    def search_images(self, query: str, *, limit: int = 50, offset: int = 0) -> list[ImageReference]:
        """Search images by description."""
        ...


class SyncColorsResource(_SyncResourceBase):
    """Synchronous wrapper for color operations."""

    def extract(self, image_id: str, *, force: bool = False, n_colors: int = 16) -> ColorExtractionResult:
        """Extract dominant colors from an image (up to 16 colors)."""
        ...

    def get(self, image_id: str) -> ColorExtractionResult:
        """Get existing color extraction results."""
        ...

    def search(self, *, hex_code: Optional[str] = None, color_name: Optional[str] = None, color_family: Optional[str] = None, delta_e_threshold: float = 15.0, min_percentage: float = 5.0, limit: int = 50, offset: int = 0) -> ColorSearchResponse:
        """Search images by color."""
        ...

    def search_all(self, *, hex_code: Optional[str] = None, color_name: Optional[str] = None, color_family: Optional[str] = None, delta_e_threshold: float = 15.0, min_percentage: float = 5.0, page_size: int = 50) -> Iterator[ColorSearchResult]:
        """Iterate through all color search results with automatic pagination."""
        ...

    def list_families(self) -> list[ColorFamilyInfo]:
        """List available color families."""
        ...

    def batch_extract(self, image_ids: list[str], *, force: bool = False, n_colors: int = 16) -> BatchColorExtractionResult:
        """Batch extract colors from multiple images (up to 16 colors)."""
        ...


class SyncBatchResource(_SyncResourceBase):
    """Synchronous wrapper for batch operations."""

    def get_status(self, batch_id: str) -> BatchStatusResult:
        """Get batch operation status."""
        ...

    def get_results(self, batch_id: str, *, include_failed: bool = True, offset: int = 0, limit: int = 100) -> BatchResults:
        """Get batch results with pagination."""
        ...

    def get_all_results(self, batch_id: str, *, include_failed: bool = True, page_size: int = 100) -> Iterator[BatchItemResult]:
        """Iterate through all batch results with automatic pagination."""
        ...

    def cancel(self, batch_id: str) -> None:
        """Cancel a batch operation."""
        ...

    def wait_for_completion(self, batch_id: str, *, timeout: Optional[float] = None, poll_interval: Optional[float] = None, on_progress: Optional[Callable[[BatchStatusResult], None]] = None) -> BatchStatusResult:
        """
        Wait for batch to complete.

                Args:
                    batch_id: The batch ID to wait for
                    timeout: Maximum time to wait (seconds)
                    poll_interval: Time between status checks (seconds)
                    on_progress: Callback invoked with status on each poll
        """
        ...


class SyncSettingsResource(_SyncResourceBase):
    """Synchronous wrapper for settings operations."""

    def configure_custom_s3(self, access_key_id: str, secret_access_key: str, bucket_name: str, region: str) -> S3ConfigStatus:
        """Configure custom S3 storage."""
        ...

    def get_custom_s3_status(self) -> S3ConfigStatus:
        """Get current S3 configuration status."""
        ...

    def remove_custom_s3(self) -> dict[str, Any]:
        """Remove custom S3 configuration."""
        ...

    def validate_custom_s3(self) -> S3ValidationResult:
        """Validate custom S3 credentials."""
        ...


class SyncTenantResource(_SyncResourceBase):
    """Synchronous wrapper for tenant operations."""

    def get_settings(self) -> TenantSettings:
        """Get tenant settings."""
        ...

    def update_settings(self, *, name: Optional[str] = None, webhook_url: Optional[str] = None, allowed_vlm_providers: Optional[list[str]] = None, allowed_domains: Optional[list[str]] = None, max_monthly_credits: Optional[int] = None, max_requests_per_minute: Optional[int] = None, custom_config: Optional[dict[str, Any]] = None) -> TenantSettings:
        """Update tenant settings."""
        ...

    def get_limits(self) -> TenantLimits:
        """Get usage limits."""
        ...

    def list_members(self) -> list[TenantMember]:
        """List tenant members."""
        ...

    def invite_member(self, email: str, *, role: str = 'viewer') -> TenantMember:
        """Invite a new member."""
        ...

    def update_member_role(self, user_id: str, role: str) -> TenantMember:
        """Update a member's role."""
        ...

    def remove_member(self, user_id: str) -> dict[str, Any]:
        """Remove a member from the tenant."""
        ...


class SyncAuditResource(_SyncResourceBase):
    """Synchronous wrapper for audit operations."""

    def list(self, *, event_type: Optional[str] = None, severity: Optional[str] = None, user_id: Optional[str] = None, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None, result: Optional[str] = None, limit: int = 50, offset: int = 0) -> AuditLogList:
        """List audit logs."""
        ...

    def get(self, log_id: str) -> AuditLogEntry:
        """Get a single audit log entry."""
        ...


class SyncUploadResource(_SyncResourceBase):
    """Synchronous wrapper for low-level upload operations."""

    def check_quota(self, file_count: int = 1) -> QuotaInfo:
        """Check upload quota."""
        ...

    def request_presigned_url(self, filename: str, content_type: str, size_bytes: int, *, purpose: str = 'image_analysis', idempotency_key: Optional[str] = None, storage_target: str = 'default') -> PresignedUrlInfo:
        """Request a presigned URL for upload."""
        ...

    def confirm_upload(self, object_key: str, size_bytes: int, *, checksum: Optional[str] = None) -> ConfirmResult:
        """Confirm an upload was successful."""
        ...

    def wait_for_description(self, image_id: str, *, timeout: Optional[float] = None, poll_interval: Optional[float] = None) -> DescriptionStatus:
        """Wait for description to complete."""
        ...

    def batch_prepare(self, files: list[FileInfo], *, intent: str = 'describe', verification_level: str = 'standard', additional_params: Optional[dict[str, Any]] = None) -> BatchPrepareResult:
        """Prepare a batch upload."""
        ...

    def batch_confirm(self, batch_id: str, confirmations: list[UploadConfirmation], *, auto_process: bool = True) -> BatchConfirmResult:
        """Confirm batch uploads."""
        ...

    def get_batch_status(self, batch_id: str) -> UploadBatchStatusResult:
        """Get batch upload status."""
        ...


class SyncAgentSearchResource(_SyncResourceBase):
    """Synchronous wrapper for agent search operations."""

    def images(self, query: str, *, limit: int = 50, folder_id: Optional[str] = None, image_ids: Optional[list[str]] = None) -> ImageSearchAgentResult:
        """Execute AI-powered image search."""
        ...

    def documents(self, query: str, *, limit: int = 50, document_types: Optional[list[str]] = None, document_ids: Optional[list[str]] = None) -> DocumentSearchAgentResult:
        """Execute AI-powered document search."""
        ...


class SyncAgentOperationsResource(_SyncResourceBase):
    """Synchronous wrapper for agent operations."""

    def synthesize(self, intent: str, *, image_ids: Optional[list[str]] = None, document_ids: Optional[list[str]] = None, auto_save: bool = False) -> SynthesizeResult:
        """Execute AI-powered report synthesis."""
        ...

    def analyze_documents(self, intent: str, document_ids: list[str]) -> DocumentAnalysisResult:
        """Execute AI-powered document analysis."""
        ...

    def organize(self, intent: str, *, image_ids: Optional[list[str]] = None, document_ids: Optional[list[str]] = None, parent_folder_id: Optional[str] = None) -> OrganizeResult:
        """Execute AI-driven file organization."""
        ...


class SyncDocumentsResource(_SyncResourceBase):
    """Synchronous wrapper for document operations."""

    def request_upload(self, filename: str, content_type: str, size_bytes: int, *, storage_target: str = 'default') -> DocumentPresignedUploadResult:
        """Request a presigned URL for document upload."""
        ...

    def confirm_upload(self, object_key: str, size_bytes: int, content_type: str, *, checksum: Optional[str] = None) -> DocumentConfirmResult:
        """Confirm a document upload after uploading to S3."""
        ...

    def get_status(self, document_id: str) -> DocumentStatusResult:
        """Get document processing status."""
        ...

    def quota_check(self, file_count: int = 1) -> DocumentQuotaCheck:
        """Check if upload quota allows for new document uploads."""
        ...

    def list(self, *, page: int = 1, page_size: int = 20, status_filter: Optional[str] = None) -> DocumentList:
        """List documents with pagination."""
        ...

    def list_all(self, *, page_size: int = 50, status_filter: Optional[str] = None) -> Iterator[DocumentItem]:
        """
        Iterate through all documents with automatic pagination.

                Args:
                    page_size: Items per page (1-100, default: 50)
                    status_filter: Filter by text_extraction_status

                Yields:
                    DocumentItem objects one at a time

                Example:
                    ```python
                    for doc in client.documents.list_all():
                        print(f"{doc.filename}: {doc.text_extraction_status}")
                    ```
        """
        ...

    def get(self, document_id: str) -> DocumentDetails:
        """Get detailed information about a document."""
        ...

    def get_text(self, document_id: str) -> str:
        """Get full extracted text from a document."""
        ...

    def get_chunks(self, document_id: str, *, include_embeddings: bool = False) -> DocumentChunksResponse:
        """Get all chunks for a document."""
        ...

    def download(self, document_id: str) -> str:
        """Get download URL for a document."""
        ...

    def search(self, query: str, *, limit: int = 20, similarity_threshold: float = 0.3, document_ids: Optional[list[str]] = None) -> DocumentSearchResponse:
        """Search documents using semantic similarity."""
        ...

    def delete(self, document_id: str) -> None:
        """Delete a document."""
        ...

    def batch_delete(self, document_ids: list[str]) -> DocumentBatchDeleteResponse:
        """Delete multiple documents in a single batch operation."""
        ...

    def batch_prepare(self, files: list[dict[str, Any]]) -> DocumentBatchPrepareResult:
        """Prepare batch upload for multiple documents."""
        ...

    def batch_confirm(self, batch_id: str, confirmations: list[dict[str, Any]]) -> DocumentBatchConfirmResult:
        """Confirm batch upload after uploading files to S3."""
        ...

    def batch_status(self, batch_id: str) -> DocumentBatchStatusResult:
        """Get processing status for a batch of documents."""
        ...

    def wait_for_processing(self, document_id: str, *, timeout: Optional[float] = None, poll_interval: Optional[float] = None) -> DocumentStatusResult:
        """Poll until document text extraction completes or fails."""
        ...

    def upload_one(self, file: Union[str, Path, bytes], *, filename: Optional[str] = None, wait_for_processing: bool = True, raise_on_failure: bool = True, processing_timeout: Optional[float] = None, storage_target: str = 'default') -> DocumentUploadResult:
        """Upload a single document with automatic text extraction."""
        ...

    def upload(self, files: Union[str, Path, bytes, list[Union[str, Path, bytes]]], *, filename: Optional[str] = None, filenames: Optional[list[str]] = None, recursive: bool = True, include_hidden: bool = False, wait_for_processing: bool = True, raise_on_failure: bool = True, processing_timeout: Optional[float] = None, on_progress: Optional[Callable[[DocumentUploadProgressEvent], None]] = None, on_file_complete: Optional[Callable[[DocumentFileCompleteEvent], None]] = None, on_processing_progress: Optional[Callable[[DocumentProcessingProgressEvent], None]] = None, on_processing_failed: Optional[Callable[[DocumentProcessingFailedEvent], None]] = None, storage_target: str = 'default') -> BatchDocumentUploadResults:
        """Upload one or more documents with automatic text extraction."""
        ...


class SyncLinksResource(_SyncResourceBase):
    """Synchronous wrapper for link operations."""

    def create(self, url: str, *, title: Optional[str] = None, tags: Optional[list[str]] = None, folder_id: Optional[str] = None, auto_crawl: bool = True) -> CreateLinkResult:
        """Create a new link (bookmark)."""
        ...

    def recrawl(self, link_id: str) -> RecrawlLinkResult:
        """Recrawl a link to refresh its metadata."""
        ...

    def get(self, link_id: str) -> LinkDetails:
        """Get detailed information about a link."""
        ...

    def list(self, *, search: Optional[str] = None, tags: Optional[list[str]] = None, folder_id: Optional[str] = None, crawl_status: Optional[str] = None, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None, limit: int = 20, offset: int = 0, sort_by: str = 'created_at', sort_order: str = 'desc') -> LinkList:
        """List links with optional filtering and pagination."""
        ...

    def list_all(self, *, search: Optional[str] = None, tags: Optional[list[str]] = None, folder_id: Optional[str] = None, crawl_status: Optional[str] = None, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None, sort_by: str = 'created_at', sort_order: str = 'desc', page_size: int = 50) -> Iterator[LinkItem]:
        """
        Iterate through all links with automatic pagination.

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
                    for link in client.links.list_all(tags=["research"]):
                        print(f"{link.domain}: {link.title}")
                    ```
        """
        ...

    def update(self, link_id: str, *, title: Optional[str] = None, tags: Optional[list[str]] = None) -> LinkUpdateResult:
        """Update link metadata (title and/or tags)."""
        ...

    def delete(self, link_id: str) -> LinkDeleteResult:
        """Delete a link."""
        ...

    def batch_delete(self, link_ids: list[str]) -> BatchDeleteFilesResponse:
        """Delete multiple links in a single batch operation."""
        ...

    def wait_for_crawl(self, link_id: str, *, timeout: Optional[float] = None, poll_interval: Optional[float] = None) -> LinkDetails:
        """Wait for link crawl to complete."""
        ...

    def create_and_wait(self, url: str, *, title: Optional[str] = None, tags: Optional[list[str]] = None, folder_id: Optional[str] = None, timeout: Optional[float] = None) -> LinkDetails:
        """Create a link and wait for crawl to complete."""
        ...


class SyncCloudStorageResource(_SyncResourceBase):
    """Synchronous wrapper for cloud storage operations."""

    def initiate_auth(self, provider: str, *, redirect_uri: Optional[str] = None) -> InitiateAuthResult:
        """Initiate OAuth flow for a cloud storage provider."""
        ...

    def complete_auth(self, provider: str, *, code: str, state: str, redirect_uri: Optional[str] = None) -> CompleteAuthResult:
        """Complete OAuth flow and create a connection."""
        ...

    def list_connections(self, *, provider: Optional[str] = None, active_only: bool = True) -> ConnectionList:
        """List cloud storage connections."""
        ...

    def disconnect(self, connection_id: str) -> DisconnectResult:
        """Disconnect a cloud storage account."""
        ...

    def start_import(self, connection_id: str, files: list[Union[CloudFileInput, dict[str, Any]]], *, auto_describe: bool = True, tags: Optional[list[str]] = None, collection_id: Optional[str] = None) -> ImportResult:
        """Start importing files from cloud storage."""
        ...

    def start_export(self, connection_id: str, image_ids: list[str], *, folder_id: Optional[str] = None, folder_name: Optional[str] = None) -> ExportResult:
        """Start exporting files to cloud storage."""
        ...

    def get_job(self, job_id: str) -> CloudStorageJob:
        """Get the status of a cloud storage job."""
        ...

    def wait_for_job(self, job_id: str, *, timeout: Optional[float] = None, poll_interval: Optional[float] = None, on_progress: Optional[Callable[[CloudStorageJobProgressEvent], None]] = None) -> CloudStorageJob:
        """Wait for a cloud storage job to complete."""
        ...

    def import_and_wait(self, connection_id: str, files: list[Union[CloudFileInput, dict[str, Any]]], *, auto_describe: bool = True, tags: Optional[list[str]] = None, collection_id: Optional[str] = None, timeout: Optional[float] = None, poll_interval: Optional[float] = None, on_progress: Optional[Callable[[CloudStorageJobProgressEvent], None]] = None) -> CloudStorageJob:
        """Import files from cloud storage and wait for completion."""
        ...

    def export_and_wait(self, connection_id: str, image_ids: list[str], *, folder_id: Optional[str] = None, folder_name: Optional[str] = None, timeout: Optional[float] = None, poll_interval: Optional[float] = None, on_progress: Optional[Callable[[CloudStorageJobProgressEvent], None]] = None) -> CloudStorageJob:
        """Export files to cloud storage and wait for completion."""
        ...


class SyncFoldersResource(_SyncResourceBase):
    """Synchronous wrapper for folder operations."""

    def tree(self) -> FolderTree:
        """Get the complete folder tree."""
        ...

    def get(self, folder_id: str, *, limit: int = 50, offset: int = 0) -> FolderContents:
        """Get folder contents."""
        ...

    def get_breadcrumbs(self, folder_id: str) -> FolderBreadcrumbs:
        """Get the breadcrumb path for a folder."""
        ...

    def create(self, name: str, *, parent_id: Optional[str] = None) -> Folder:
        """Create a new folder."""
        ...

    def rename(self, folder_id: str, name: str) -> Folder:
        """Rename a folder."""
        ...

    def move(self, folder_id: str, *, new_parent_id: Optional[str] = None) -> Folder:
        """Move a folder to a new parent."""
        ...

    def delete(self, folder_id: str, *, mode: str = 'move_to_parent') -> DeleteFolderResult:
        """Delete a folder."""
        ...

    def move_files(self, file_ids: list[str], *, folder_id: Optional[str] = None) -> MoveFilesResult:
        """Move files to a folder."""
        ...


class SyncAionVision:
    """

        Synchronous Python SDK for the Aionvision Vision AI API.

        For async code, use AionVision directly. This wrapper maintains a
        persistent event loop for efficient connection reuse.

        Warning:
            This client is NOT thread-safe. Do not share instances across threads.
            Each thread should create its own SyncAionVision instance.

        Usage:
            with SyncAionVision(api_key="aion_...") as client:
                # Upload a file
                result = client.upload_one("photo.jpg")
                print(result.description)

                # Chat about your images (with context manager)
                with client.chat_session() as session:
                    response = session.send("Find damaged poles")
                    print(response.content)
                # Session automatically closed

                # Or manually:
                session = client.chat_session()
                response = session.send("Find damaged poles")
                print(response.content)
                client.close_session(session.session_id)

        Note: Streaming is not available in sync mode.
    """
    from .exceptions import AionvisionConnectionError, AionvisionError, AionvisionPermissionError, AionvisionTimeoutError, AuthenticationError, BatchError, ChatError, CircuitBreakerError, CloudStorageError, DescriptionError, DocumentProcessingError, QuotaExceededError, RateLimitError, ResourceNotFoundError, ServerError, SSEStreamError, UploadError, ValidationError
    from .types import DescriptionStatus
    from .types.audit import AuditEventType, AuditLogEntry, AuditLogList, AuditResult, AuditSeverity
    from .types.batch import BatchImageInput, BatchItemResult, BatchItemStatus, BatchResults, BatchResultsPagination, BatchResultsSummary, BatchStatus, BatchStatusResult, BatchSubmissionResult, BatchVerifyInput
    from .types.callbacks import DescriptionFailedEvent, DescriptionProgressEvent, FileCompleteEvent, UploadProgressEvent
    from .types.chat import ChatImageList, ChatMessage, ChatResponse, ChatSession, ChatSessionDetail, ChatToken, ImageReference, PlanActionResponse, SessionList
    from .types.colors import HSL, LAB, RGB, BatchColorExtractionResult, ColorAnalysis, ColorAnalytics, ColorBrightness, ColorExtractionResult, ColorExtractionStatus, ColorFamily, ColorFamilyInfo, ColorSaturation, ColorSearchResponse, ColorSearchResult, ColorTemperature, DominantColor
    from .types.common import ChatTokenType, DescriptionStatus, MessageRole, StorageTarget, VerificationLevel, VerificationLevelLiteral
    from .types.describe import DescriptionErrorType, DescriptionFailure, DescriptionResult
    from .types.files import BatchDeleteFileResult, BatchDeleteFilesResponse, DeleteFileResult, FileList, FullDescription, ProcessingHistory, UpdateFileResult, UserFile, UserFileDetails
    from .types.tenant import MemberRole, TenantLimits, TenantMember, TenantSettings
    from .types.upload import BatchConfirmResult, BatchPrepareResult, BatchUploadResults, ConfirmResult, FileInfo, PresignedUrlInfo, QuotaInfo, UploadBatchStatusResult, UploadConfirmation, UploadResult
    from .types.verify import VerificationIssue, VerificationResult
    from .types.agent_search import DocumentChunkResultItem, DocumentSearchAgentResult, ImageSearchAgentResult, ImageSearchResultItem, ResultRefData
    from .types.documents import BatchDocumentUploadResults, DocumentBatchConfirmItem, DocumentBatchConfirmResult, DocumentBatchDeleteResponse, DocumentBatchFileInfo, DocumentBatchPrepareResult, DocumentBatchStatusItem, DocumentBatchStatusResult, DocumentChunk, DocumentChunksResponse, DocumentConfirmResult, DocumentDeleteResult, DocumentDetails, DocumentItem, DocumentList, DocumentPresignedUploadResult, DocumentProcessingErrorType, DocumentProcessingFailure, DocumentProcessingStatus, DocumentQuotaCheck, DocumentSearchResponse, DocumentSearchResult, DocumentStatusResult, DocumentUploadResult
    from .types.callbacks import DocumentFileCompleteEvent, DocumentProcessingFailedEvent, DocumentProcessingProgressEvent, DocumentUploadProgressEvent
    from .types.links import CreateLinkResult, LinkCrawlStatus, LinkDeleteResult, LinkDetails, LinkItem, LinkList, LinkOGMetadata, LinkUpdateResult, RecrawlLinkResult
    from .types.cloud_storage import CloudFileInput, CloudStorageConnection, CloudStorageJob, CompleteAuthResult, ConnectionList, DisconnectResult, ExportResult, ImportResult, InitiateAuthResult

    def __init__(self, api_key: str, *, base_url: str = 'https://api.aionvision.tech/api/v2', timeout: float = 300.0, max_retries: int = 3, retry_delay: float = 1.0, polling_interval: float = 2.0, polling_timeout: float = 360.0, tenant_id: Optional[str] = None, proxy_url: Optional[str] = None, enable_tracing: bool = False) -> None:
        """

                Initialize the synchronous Aionvision client.

                Args:
                    api_key: Your Aionvision API key (starts with aion_)
                    base_url: API base URL (default: production)
                    timeout: Request timeout in seconds
                    max_retries: Maximum retry attempts for transient failures
                    retry_delay: Initial delay between retries (exponential backoff)
                    polling_interval: Interval for polling operations (auto-describe)
                    polling_timeout: Maximum time to wait for polling operations
                    tenant_id: Optional tenant ID for multi-tenant deployments
                    proxy_url: Optional proxy URL for network requests
                    enable_tracing: Enable OpenTelemetry tracing

                Raises:
                    ValueError: If API key is invalid or missing
        """
        ...

    @classmethod
    def from_env(cls, **overrides) -> SyncAionVision:
        """

                Create client from environment variables.

                This is a convenience factory method that reads configuration from
                environment variables, allowing you to create a client without
                explicitly passing the API key.

                Environment variables:
                    AIONVISION_API_KEY: API key (required if not provided)
                    AIONVISION_BASE_URL: Base URL (optional)
                    AIONVISION_TIMEOUT: Request timeout in seconds (optional)
                    AIONVISION_MAX_RETRIES: Maximum retry attempts (optional)
                    AIONVISION_RETRY_DELAY: Initial retry delay in seconds (optional)
                    AIONVISION_POLLING_INTERVAL: Polling interval in seconds (optional)
                    AIONVISION_POLLING_TIMEOUT: Polling timeout in seconds (optional)
                    AIONVISION_TENANT_ID: Tenant ID for multi-tenant (optional)
                    AIONVISION_PROXY_URL: Proxy URL (optional)
                    AIONVISION_ENABLE_TRACING: Enable OpenTelemetry tracing (optional)

                Args:
                    **overrides: Override any configuration value (api_key, base_url,
                        timeout, max_retries, retry_delay, polling_interval, polling_timeout)

                Returns:
                    SyncAionVision client instance

                Raises:
                    ValueError: If API key not provided and not in environment

                Example:
                    ```python
                    # Uses AIONVISION_API_KEY from environment
                    with SyncAionVision.from_env() as client:
                        result = client.upload_one("photo.jpg")

                    # Override specific values
                    with SyncAionVision.from_env(timeout=60.0) as client:
                        result = client.upload_one("photo.jpg")
                    ```
        """
        ...

    def __enter__(self) -> SyncAionVision:
        """Context manager entry - initializes event loop and HTTP client."""
        ...

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[Any]) -> None:
        """
        Context manager exit - ensures cleanup.

                Cleanup errors do not mask exceptions from the with block.
                If an exception occurred in the with block, cleanup errors are suppressed.
                If no exception occurred, cleanup errors are raised normally.
        """
        ...

    def upload_one(self, file: Union[str, Path, bytes], *, filename: Optional[str] = None, wait_for_descriptions: bool = True, raise_on_failure: bool = True, description_timeout: Optional[float] = None, storage_target: Union[StorageTarget, str] = StorageTarget.DEFAULT) -> UploadResult:
        """

                Upload a single file with automatic AI description.

                Args:
                    file: File path or bytes to upload
                    filename: Override filename (required if file is bytes)
                    wait_for_descriptions: Wait for AI description to complete
                    raise_on_failure: Raise DescriptionError if description fails
                    description_timeout: Override default polling timeout
                    storage_target: Where to store (DEFAULT or CUSTOM)

                Returns:
                    UploadResult with image_id, description, tags, etc.

                Raises:
                    ValidationError: If file type is unsupported
                    QuotaExceededError: If upload quota is insufficient
                    UploadError: If upload fails
                    DescriptionError: If description fails and raise_on_failure=True
        """
        ...

    def upload(self, files: Union[str, Path, bytes, list[Union[str, Path, bytes]]], *, filename: Optional[str] = None, filenames: Optional[list[str]] = None, recursive: bool = True, include_hidden: bool = False, wait_for_descriptions: bool = True, raise_on_failure: bool = True, description_timeout: Optional[float] = None, on_progress: Optional[Callable[[UploadProgressEvent], None]] = None, on_file_complete: Optional[Callable[[FileCompleteEvent], None]] = None, on_description_progress: Optional[Callable[[DescriptionProgressEvent], None]] = None, on_description_failed: Optional[Callable[[DescriptionFailedEvent], None]] = None, storage_target: Union[StorageTarget, str] = StorageTarget.DEFAULT) -> BatchUploadResults:
        """

                Upload one or more files with automatic AI description.

                Note: Streaming is not available in sync mode. Use the async AionVision
                client for streaming capabilities.

                Args:
                    files: File path, bytes, directory, or list of any of these
                    filename: Override filename (for single bytes upload)
                    filenames: Override filenames (for multiple uploads)
                    recursive: Search directories recursively (default: True)
                    include_hidden: Include hidden files starting with .
                    wait_for_descriptions: Wait for AI descriptions to complete
                    raise_on_failure: Raise DescriptionError if any description fails
                    description_timeout: Override default polling timeout
                    on_progress: Callback for file preparation updates
                    on_file_complete: Callback when each file upload completes
                    on_description_progress: Callback for description polling progress
                    on_description_failed: Callback when a description fails
                    storage_target: Where to store (DEFAULT or CUSTOM)

                Returns:
                    BatchUploadResults - list of UploadResult with helper methods

                Raises:
                    ValidationError: If more than 10,000 files or unsupported type
                    QuotaExceededError: If upload quota is insufficient
                    UploadError: If upload fails
                    DescriptionError: If any description fails and raise_on_failure=True
        """
        ...

    def chat_session(self, *, title: Optional[str] = None, image_ids: Optional[list[str]] = None, use_all_images: bool = True, auto_close: bool = True) -> SyncChatSession:
        """

                Create a chat session.

                Can be used as a context manager for automatic cleanup, or
                call close_session() when done to clean up the session manually.

                Args:
                    title: Optional session title
                    image_ids: Initial image IDs for context
                    use_all_images: Use all user's images as context
                    auto_close: Automatically close session on context exit (default: True)

                Returns:
                    SyncChatSession for sending messages

                Example:
                    # As context manager (recommended):
                    with client.chat_session() as session:
                        response = session.send("Find damaged poles")
                        print(response.content)
                    # Session automatically closed

                    # Or manually:
                    session = client.chat_session(auto_close=False)
                    response = session.send("Find damaged poles")
                    print(response.content)
                    client.close_session(session.session_id)
        """
        ...

    def close_session(self, session_id: str) -> dict[str, Any]:
        """

                Close a chat session.

                Args:
                    session_id: The session ID to close

                Returns:
                    Close result dictionary
        """
        ...

    def chat(self, message: str, *, session_id: str, force_detailed_analysis: bool = False) -> ChatResponse:
        """

                Send a message to the agentic chat system.

                Requires an explicit session_id. For session management,
                use chat_session() instead.

                Args:
                    message: User message text
                    session_id: Session identifier (required)
                    force_detailed_analysis: Force high-resolution VLM analysis

                Returns:
                    ChatResponse with text, images, metadata
        """
        ...

    @property
    def async_client(self) -> AionVision:
        """

                Access the underlying async client for advanced operations.

                This provides access to the async resources if you need to use them
                with custom event loop management or for advanced operations.

                Warning: The async client is bound to this wrapper's event loop.
                Do not use it with asyncio.run() or in other event loops.

                Example:
                    async_files = client.async_client.files  # FilesResource (async)
                    result = client._run(async_files.list())

                Raises:
                    RuntimeError: If client context has not been entered
        """
        ...

    @property
    def files(self) -> SyncFilesResource:
        """

                Access file operations with native sync interface.

                This property matches the async client's API for portable code.

                Example:
                    files = client.files.list(search="damaged pole")
                    details = client.files.get(file_id="...")
        """
        ...

    @property
    def chats(self) -> SyncChatResource:
        """

                Access chat operations with native sync interface.

                This property matches the async client's API for portable code.

                Example:
                    sessions = client.chats.list_sessions()
                    session = client.chats.create_session()
        """
        ...

    @property
    def colors(self) -> SyncColorsResource:
        """

                Access color operations with native sync interface.

                This property matches the async client's API for portable code.

                Example:
                    result = client.colors.extract(image_id)
                    results = client.colors.search(color_family="earth_tone")
        """
        ...

    @property
    def batch(self) -> SyncBatchResource:
        """

                Access batch operations with native sync interface.

                This property matches the async client's API for portable code.

                Example:
                    status = client.batch.get_status(batch_id)
                    results = client.batch.get_results(batch_id)
        """
        ...

    @property
    def settings(self) -> SyncSettingsResource:
        """

                Access settings operations with native sync interface.

                This property matches the async client's API for portable code.

                Example:
                    status = client.settings.get_custom_s3_status()
        """
        ...

    @property
    def tenant(self) -> SyncTenantResource:
        """

                Access tenant operations with native sync interface.

                This property matches the async client's API for portable code.

                Example:
                    settings = client.tenant.get_settings()
                    limits = client.tenant.get_limits()
        """
        ...

    @property
    def audit(self) -> SyncAuditResource:
        """

                Access audit operations with native sync interface.

                This property matches the async client's API for portable code.

                Example:
                    logs = client.audit.list(limit=20)
                    entry = client.audit.get(log_id)
        """
        ...

    @property
    def uploads(self) -> SyncUploadResource:
        """

                Access low-level upload operations with native sync interface.

                This property matches the async client's API for portable code.

                Example:
                    quota = client.uploads.check_quota(5)
                    url_info = client.uploads.request_presigned_url(...)
        """
        ...

    @property
    def agent_search(self) -> SyncAgentSearchResource:
        """

                Access AI agent search operations with native sync interface.

                This property matches the async client's API for portable code.

                Example:
                    result = client.agent_search.images("damaged poles")
        """
        ...

    @property
    def agent_operations(self) -> SyncAgentOperationsResource:
        """

                Access AI agent operations with native sync interface.

                This property matches the async client's API for portable code.

                Example:
                    result = client.agent_operations.synthesize("Write a report", document_ids=["doc-1"])
        """
        ...

    @property
    def documents(self) -> SyncDocumentsResource:
        """

                Access document operations with native sync interface.

                This property matches the async client's API for portable code.

                Example:
                    docs = client.documents.list()
                    result = client.documents.upload_one("report.pdf")
        """
        ...

    @property
    def links(self) -> SyncLinksResource:
        """

                Access link (bookmark) operations with native sync interface.

                This property matches the async client's API for portable code.

                Example:
                    link = client.links.create("https://example.com")
                    all_links = client.links.list()
        """
        ...

    @property
    def folders(self) -> SyncFoldersResource:
        """Access folder management operations with native sync interface."""
        ...

    @property
    def cloud_storage(self) -> SyncCloudStorageResource:
        """

                Access cloud storage operations with native sync interface.

                This property matches the async client's API for portable code.

                Example:
                    conns = client.cloud_storage.list_connections()
                    job = client.cloud_storage.import_and_wait(conn_id, files)
        """
        ...
