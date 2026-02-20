from __future__ import annotations
import warnings
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any, Callable, Optional, Union
from .config import ClientConfig
from .resources.agent_operations import AgentOperationsResource
from .resources.agent_search import AgentSearchResource
from .resources.cloud_storage import CloudStorageResource
from .resources.audit import AuditResource
from .resources.batch import BatchResource
from .resources.chat import ChatResource, ChatSessionContext
from .resources.colors import ColorsResource
from .resources.describe import DescribeResource
from .resources.documents import DocumentsResource
from .resources.files import FilesResource
from .resources.folders import FoldersResource
from .resources.links import LinksResource
from .resources.settings import SettingsResource
from .resources.tenant import TenantResource
from .resources.upload import UploadResource
from .resources.verify import VerifyResource
from .types.batch import BatchStatusResult
from .types.callbacks import DescriptionFailedEvent, DescriptionProgressEvent, FileCompleteEvent, UploadProgressEvent
from .types.chat import ChatResponse, ChatToken
from .types.common import StorageTarget
from .types.describe import DescriptionResult
from .types.upload import BatchUploadResults, UploadResult
from .types.verify import VerificationResult


class AionVision:
    """

        Async Python SDK for the Aionvision Vision AI API.

        Provides simple, single-line operations for:
        - Uploading images with automatic AI descriptions
        - Batch uploading multiple files
        - Agentic chat with your image library

        Usage:
            ```python
            async with AionVision(api_key="aion_...") as client:
                # Single file upload
                result = await client.upload_one("photo.jpg")
                print(result.description)

                # Multiple files
                results = await client.upload("/path/to/photos")
                for r in results:
                    print(r.description)

                # Chat with explicit session
                async with client.chat_session() as session:
                    response = await session.send("Find damaged poles")
            ```

        Attributes:
            uploads: Access to low-level upload operations
            chats: Access to chat session management
    """
    from .exceptions import AionvisionConnectionError, AionvisionError, AionvisionPermissionError, AionvisionTimeoutError, AuthenticationError, BatchError, ChatError, CircuitBreakerError, CloudStorageError, DescriptionError, DocumentProcessingError, QuotaExceededError, RateLimitError, ResourceNotFoundError, ServerError, SSEStreamError, UploadError, ValidationError
    from .types import DescriptionStatus
    from .types.agent_operations import ChunkReference, DocumentAnalysisResult, FolderActionDetail, OrganizeResult, SynthesizeResult
    from .types.agent_search import DocumentChunkResultItem, DocumentSearchAgentResult, ImageSearchAgentResult, ImageSearchResultItem, ResultRefData
    from .types.audit import AuditEventType, AuditLogEntry, AuditLogList, AuditResult, AuditSeverity
    from .types.batch import BatchImageInput, BatchItemResult, BatchItemStatus, BatchResults, BatchResultsPagination, BatchResultsSummary, BatchStatus, BatchStatusResult, BatchSubmissionResult, BatchVerifyInput
    from .types.callbacks import DescriptionFailedEvent, DescriptionProgressEvent, DocumentFileCompleteEvent, DocumentProcessingFailedEvent, DocumentProcessingProgressEvent, DocumentUploadProgressEvent, FileCompleteEvent, UploadProgressEvent
    from .types.chat import ChatImageList, ChatMessage, ChatResponse, ChatSession, ChatSessionDetail, ChatToken, ImageReference, SessionList
    from .types.references import DocumentRef, ImageRef, LinkRef, ParsedReferences
    from .types.colors import HSL, LAB, RGB, BatchColorExtractionResult, ColorAnalysis, ColorAnalytics, ColorBrightness, ColorExtractionResult, ColorExtractionStatus, ColorFamily, ColorFamilyInfo, ColorSaturation, ColorSearchResponse, ColorSearchResult, ColorTemperature, DominantColor
    from .types.common import ChatTokenType, DescriptionStatus, MessageRole, StorageTarget, VerificationLevel, VerificationLevelLiteral
    from .types.describe import DescriptionErrorType, DescriptionFailure, DescriptionResult
    from .types.documents import BatchDocumentUploadResults, DocumentBatchConfirmItem, DocumentBatchConfirmResult, DocumentBatchDeleteResponse, DocumentBatchFileInfo, DocumentBatchPrepareResult, DocumentBatchStatusItem, DocumentBatchStatusResult, DocumentChunk, DocumentChunksResponse, DocumentConfirmResult, DocumentDeleteResult, DocumentDetails, DocumentItem, DocumentList, DocumentPresignedUploadResult, DocumentProcessingErrorType, DocumentProcessingFailure, DocumentProcessingStatus, DocumentQuotaCheck, DocumentSearchResponse, DocumentSearchResult, DocumentStatusResult, DocumentUploadResult
    from .types.files import BatchDeleteFileResult, BatchDeleteFilesResponse, DeleteFileResult, FileList, FullDescription, ProcessingHistory, UpdateFileResult, UserFile, UserFileDetails
    from .types.links import CreateLinkResult, LinkCrawlStatus, LinkDeleteResult, LinkDetails, LinkItem, LinkList, LinkOGMetadata, LinkUpdateResult, RecrawlLinkResult
    from .types.cloud_storage import CloudFileInput, CloudStorageConnection, CloudStorageJob, CompleteAuthResult, ConnectionList, DisconnectResult, ExportResult, ImportResult, InitiateAuthResult
    from .types.tenant import MemberRole, TenantLimits, TenantMember, TenantSettings
    from .types.upload import BatchConfirmResult, BatchPrepareResult, BatchUploadResults, ConfirmResult, FileInfo, PresignedUrlInfo, QuotaInfo, UploadBatchStatusResult, UploadConfirmation, UploadResult
    from .types.verify import VerificationIssue, VerificationResult

    def __init__(self, api_key: str, *, base_url: str = 'https://api.aionvision.tech/api/v2', timeout: float = 300.0, max_retries: int = 3, retry_delay: float = 1.0, polling_interval: float = 2.0, polling_timeout: float = 360.0, tenant_id: Optional[str] = None, proxy_url: Optional[str] = None, enable_tracing: bool = False) -> None:
        """

                Initialize the Aionvision client.

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
    def from_env(cls, **overrides) -> AionVision:
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
                    AionVision client instance

                Raises:
                    ValueError: If API key not provided and not in environment

                Example:
                    ```python
                    # Uses AIONVISION_API_KEY from environment
                    async with AionVision.from_env() as client:
                        result = await client.upload_one("photo.jpg")

                    # Override specific values
                    async with AionVision.from_env(timeout=60.0) as client:
                        result = await client.upload_one("photo.jpg")
                    ```
        """
        ...

    async def __aenter__(self) -> AionVision:
        """Async context manager entry - initializes HTTP client."""
        ...

    async def __aexit__(self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[Any]) -> None:
        """Async context manager exit - ensures cleanup."""
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

    def chat_session(self, *, title: Optional[str] = None, image_ids: Optional[list[str]] = None, use_all_images: bool = True, auto_close: bool = True) -> ChatSessionContext:
        """

                Create a chat session context manager.

                This is the preferred way to use chat - sessions are explicitly
                managed and automatically cleaned up.

                Args:
                    title: Optional session title
                    image_ids: Initial image IDs for context
                    use_all_images: Use all user's images as context
                    auto_close: Automatically close session on exit (default: True)

                Returns:
                    ChatSessionContext for use with 'async with'

                Example:
                    ```python
                    async with client.chat_session() as session:
                        response = await session.send("Find damaged poles")
                        print(response.content)

                        followup = await session.send("Tell me more")
                        print(followup.content)
                    # Session automatically closed on exit
                    ```
        """
        ...

    async def chat(self, message: str, *, session_id: str, force_detailed_analysis: bool = False) -> ChatResponse:
        """

                Send a message to the agentic chat system and get a complete response.

                Requires an explicit session_id. For automatic session management,
                use chat_session() instead. For streaming responses, use chat_stream().

                Args:
                    message: User message text
                    session_id: Session identifier (required)
                    force_detailed_analysis: If True, force detailed analysis even if not needed

                Returns:
                    ChatResponse with text, images, metadata

                Example:
                    ```python
                    # Recommended: Use chat_session() context manager
                    async with client.chat_session() as session:
                        response = await session.send("Find damaged poles")
                        print(response.content)

                    # Or with explicit session management
                    session = await client.chats.create_session()
                    response = await client.chat("Show me damaged poles", session_id=session.id)
                    print(response.content)
                    ```
        """
        ...

    async def chat_stream(self, message: str, *, session_id: str, force_detailed_analysis: bool = False) -> AsyncIterator[ChatToken]:
        """

                Send a message and stream response tokens as they arrive.

                Requires an explicit session_id. For automatic session management,
                use chat_session() instead. For complete responses, use chat().

                Args:
                    message: User message text
                    session_id: Session identifier (required)
                    force_detailed_analysis: If True, force detailed analysis even if not needed

                Yields:
                    ChatToken objects with type, content, and data

                Example:
                    ```python
                    async with client.chat_session() as session:
                        async for token in session.send_stream("Find damaged poles"):
                            if token.type == ChatTokenType.TOKEN:
                                print(token.content, end="", flush=True)
                    ```
        """
        ...

    async def describe(self, image: Optional[Union[str, Path, bytes, list[Union[str, Path, bytes]]]] = None, *, object_key: Optional[str] = None, object_keys: Optional[list[str]] = None, verification_level: str = 'standard', include_metadata: bool = True, include_tags: bool = True, providers: Optional[list[str]] = None, prompt: Optional[str] = None, rule_set_id: Optional[str] = None, rules: Optional[list[dict[str, Any]]] = None, max_parallel: int = 5, timeout_per_item: int = 30, on_progress: Optional[Callable[[BatchStatusResult], None]] = None) -> Union[DescriptionResult, list[DescriptionResult]]:
        """

                Generate AI description for one or more images.

                .. deprecated::
                    This method is deprecated. Use :meth:`upload` instead, which handles
                    file upload and description in a single operation. The standalone
                    describe functionality will be removed in a future version.

                For single images, uses synchronous API. For multiple images,
                uses batch API with automatic polling.

                Args:
                    image: Single image (URL, file path, or bytes) or list of images
                    object_key: S3/Spaces object key for single previously uploaded image
                    object_keys: List of S3/Spaces object keys for batch processing
                    verification_level: quick | standard | thorough | critical
                    include_metadata: Include image metadata in response
                    include_tags: Whether to generate tags along with the description
                    providers: Specific VLM providers to use
                    prompt: Custom prompt for description focus
                    rule_set_id: UUID of rule set to apply during description
                    rules: Inline rules to apply during description
                    max_parallel: Maximum concurrent processing for batch (1-20, default: 5)
                    timeout_per_item: Seconds per item for batch (5-300, default: 30)
                    on_progress: Optional callback for batch progress updates

                Returns:
                    DescriptionResult for single image
                    List[DescriptionResult] for multiple images

                Example:
                    ```python
                    # Single image
                    result = await client.describe("photo.jpg")
                    print(result.description)

                    # Multiple images (batch)
                    results = await client.describe(["img1.jpg", "img2.jpg"])
                    for r in results:
                        print(r.description)

                    # From previously uploaded files
                    results = await client.describe(object_keys=["key1", "key2"])
                    ```
        """
        ...

    async def verify(self, image: Optional[Union[str, Path, bytes]] = None, content: str = '', *, images: Optional[list[Union[str, Path, bytes]]] = None, contents: Optional[list[str]] = None, object_key: Optional[str] = None, object_keys: Optional[list[str]] = None, mode: str = 'response', verification_level: str = 'standard', use_consensus: bool = True, providers: Optional[list[str]] = None, rule_set_id: Optional[str] = None, rules: Optional[list[dict[str, Any]]] = None, max_parallel: int = 5, timeout_per_item: int = 30, on_progress: Optional[Callable[[BatchStatusResult], None]] = None) -> Union[VerificationResult, list[VerificationResult]]:
        """

                Verify if content accurately describes one or more images.

                .. deprecated::
                    This method is deprecated. Verification functionality is being removed
                    as a standalone operation. Use :meth:`upload` for image processing.
                    This method will be removed in a future version.

                For single images, uses synchronous API. For multiple images,
                uses batch API with automatic polling.

                Single mode:
                    verify(image="img.jpg", content="A red car")

                Batch mode:
                    verify(images=["img1.jpg", "img2.jpg"], contents=["A red car", "A blue truck"])

                Args:
                    image: Single image (URL, file path, or bytes)
                    content: Text content to verify against single image
                    images: List of images for batch verification
                    contents: List of contents to verify (must match images length)
                    object_key: S3/Spaces object key for single previously uploaded image
                    object_keys: List of S3/Spaces object keys for batch verification
                    mode: "response" (full VLM response) or "claim" (specific claim)
                    verification_level: quick | standard | thorough | critical
                    use_consensus: Use multi-provider consensus
                    providers: Specific VLM providers to use for verification
                    rule_set_id: UUID of rule set to apply during verification
                    rules: Inline rules to apply during verification
                    max_parallel: Maximum concurrent processing for batch (1-20, default: 5)
                    timeout_per_item: Seconds per item for batch (5-300, default: 30)
                    on_progress: Optional callback for batch progress updates

                Returns:
                    VerificationResult for single image
                    List[VerificationResult] for multiple images

                Example:
                    ```python
                    # Single verification
                    result = await client.verify("photo.jpg", "A red sports car")
                    print(f"Verified: {result.is_verified}")

                    # Batch verification
                    results = await client.verify(
                        images=["img1.jpg", "img2.jpg"],
                        contents=["A red car", "A blue truck"]
                    )
                    for r in results:
                        print(f"Verified: {r.is_verified}, Risk: {r.risk_level}")
                    ```
        """
        ...

    @property
    def uploads(self) -> UploadResource:
        """

                Access upload operations.

                Provides low-level methods for fine-grained control:
                - check_quota()
                - request_presigned_url()
                - confirm_upload()
                - wait_for_description()
                - batch_prepare()
                - batch_confirm()
        """
        ...

    @property
    def chats(self) -> ChatResource:
        """

                Access chat operations.

                Provides methods for session management:
                - create_session()
                - get_session()
                - list_sessions()
                - update_images()
                - close_session()
                - search_images()
        """
        ...

    @property
    def descriptions(self) -> DescribeResource:
        """

                Access description operations.

                .. deprecated::
                    This resource is deprecated. Use :meth:`upload` instead, which handles
                    file upload and description in a single operation. The standalone
                    describe functionality will be removed in a future version.

                Provides methods for generating descriptions.
        """
        ...

    @property
    def verifications(self) -> VerifyResource:
        """

                Access verification operations.

                .. deprecated::
                    This resource is deprecated. Verification functionality is being removed
                    as a standalone operation. Use :meth:`upload` for image processing.
                    This resource will be removed in a future version.

                Provides methods for content verification and hallucination detection.
        """
        ...

    @property
    def files(self) -> FilesResource:
        """

                Access file operations.

                Provides methods for listing, retrieving, updating, and deleting files:
                - list() - List files with search/filter/pagination
                - get() - Get detailed file info with descriptions
                - update() - Update file title and tags
                - delete() - Soft-delete a file
                - batch_delete() - Delete multiple files in one operation

                Example:
                    ```python
                    files = await client.files.list(search="damaged pole")
                    details = await client.files.get(file_id="...")
                    ```
        """
        ...

    @property
    def batch(self) -> BatchResource:
        """

                Access batch operation management.

                Provides methods for monitoring and managing batch operations:
                - get_status() - Check batch progress
                - get_results() - Retrieve batch results with pagination
                - cancel() - Cancel a pending/processing batch
                - wait_for_completion() - Poll until batch completes

                Example:
                    ```python
                    status = await client.batch.get_status(batch_id="...")
                    results = await client.batch.get_results(batch_id="...")
                    ```
        """
        ...

    @property
    def settings(self) -> SettingsResource:
        """

                Access settings operations.

                Provides methods for configuring organization-level settings:
                - configure_custom_s3() - Configure custom S3 bucket for uploads
                - get_custom_s3_status() - Check S3 configuration status
                - remove_custom_s3() - Remove custom S3 configuration
                - validate_custom_s3() - Validate S3 credentials are still working

                Example:
                    ```python
                    # Configure custom S3 bucket
                    status = await client.settings.configure_custom_s3(
                        access_key_id="AKIA...",
                        secret_access_key="...",
                        bucket_name="my-bucket",
                        region="us-east-1"
                    )

                    # Check configuration status
                    status = await client.settings.get_custom_s3_status()

                    # Use custom storage in uploads
                    result = await client.upload("photo.jpg", storage_target="custom")
                    ```
        """
        ...

    @property
    def tenant(self) -> TenantResource:
        """

                Access tenant management operations.

                Provides methods for managing tenant settings, limits, and members:
                - get_settings() - Get tenant configuration and usage
                - update_settings() - Update tenant settings (ADMIN)
                - get_limits() - Get usage limits and remaining quota
                - list_members() - List all tenant members
                - invite_member() - Invite new member (OWNER)
                - update_member_role() - Change member role (OWNER)
                - remove_member() - Remove member from tenant (OWNER)

                Example:
                    ```python
                    # Get tenant settings
                    settings = await client.tenant.get_settings()
                    print(f"Tenant: {settings.name}")
                    print(f"Tier: {settings.subscription_tier}")

                    # Check limits
                    limits = await client.tenant.get_limits()
                    print(f"Remaining: {limits.remaining}")

                    # List members
                    members = await client.tenant.list_members()
                    for m in members:
                        print(f"{m.name} ({m.role})")
                    ```
        """
        ...

    @property
    def audit(self) -> AuditResource:
        """

                Access audit log operations.

                Provides methods for querying and retrieving security audit logs:
                - list() - List audit logs with filtering and pagination
                - get() - Get a single audit log entry

                Requires ADMIN role on the tenant.

                Example:
                    ```python
                    # List recent audit logs
                    logs = await client.audit.list(limit=20)
                    for entry in logs.entries:
                        print(f"{entry.event_timestamp}: {entry.event_type}")

                    # Filter by event type
                    login_logs = await client.audit.list(event_type="auth.login")

                    # Get specific entry
                    entry = await client.audit.get("log-uuid")
                    ```
        """
        ...

    @property
    def colors(self) -> ColorsResource:
        """

                Access color extraction and search operations.

                Provides methods for extracting dominant colors from images and
                searching images by color properties:
                - extract() - Trigger color extraction for an image
                - get() - Get extracted colors for an image
                - search() - Search images by color (hex, name, or family)
                - list_families() - List available color families
                - batch_extract() - Queue batch extraction for multiple images

                Example:
                    ```python
                    # Extract colors from an image
                    result = await client.colors.extract(image_id)
                    if result.is_completed:
                        for color in result.color_analysis.dominant_colors:
                            print(f"{color.name}: {color.hex}")

                    # Search by color
                    results = await client.colors.search(hex_code="#C4A87C")
                    for r in results.results:
                        print(f"Found: {r.image_id}")

                    # Search by color family
                    earth_images = await client.colors.search(color_family="earth_tone")
                    ```
        """
        ...

    @property
    def agent_search(self) -> AgentSearchResource:
        """

                Access AI agent search operations directly.

                Provides programmatic access to search agents without chat sessions:
                - images(): Execute ImageSearchAgent
                - documents(): Execute DocumentSearchAgent

                Example:
                    ```python
                    # Image search
                    result = await client.agent_search.images("damaged poles")
                    print(f"Found {result.count} images: {result.summary}")

                    # Document search
                    result = await client.agent_search.documents(
                        "safety procedures",
                        document_types=["pdf"]
                    )
                    for chunk in result.results:
                        print(f"{chunk.document_filename}: {chunk.text[:100]}...")
                    ```
        """
        ...

    @property
    def agent_operations(self) -> AgentOperationsResource:
        """

                Access AI agent operations directly.

                Provides programmatic access to operation agents without chat sessions:
                - synthesize(): Execute SynthesisAgent
                - analyze_documents(): Execute DocumentAnalysisAgent
                - organize(): Execute FolderAgent

                Example:
                    ```python
                    result = await client.agent_operations.synthesize(
                        "Write a report on spending patterns",
                        document_ids=["doc-1", "doc-2"],
                    )
                    print(result.report)
                    ```
        """
        ...

    def pipeline(self) -> 'Pipeline':
        """

                Create a new pipeline builder for multi-step agent workflows.

                Pipelines chain agent operations with typed data flow.
                The server handles auto-wiring, parallel execution, and data routing.

                Example:
                    ```python
                    result = await (
                        client.pipeline()
                        .search_images("damaged utility poles")
                        .organize("Sort by damage severity")
                        .run()
                    )
                    print(result.final.summary)
                    ```

                Returns:
                    Pipeline builder instance. Call .run() to execute.
        """
        ...

    @property
    def documents(self) -> DocumentsResource:
        """

                Access document operations.

                Provides high-level convenience methods:
                - upload_one() - Upload single document with automatic text extraction
                - upload() - Upload multiple documents with directory support
                - wait_for_processing() - Poll until text extraction completes

                And low-level methods for fine-grained control:
                - request_upload() - Get presigned URL for upload
                - confirm_upload() - Confirm upload and start processing
                - get_status() - Check document processing status
                - quota_check() - Check upload quota
                - list() - List documents with pagination
                - list_all() - Iterate through all documents
                - get() - Get document details
                - get_text() - Get full extracted text
                - get_chunks() - Get document chunks
                - download() - Get download URL
                - search() - Semantic search across documents
                - delete() - Delete a document
                - batch_delete() - Delete multiple documents
                - batch_prepare() - Prepare batch upload
                - batch_confirm() - Confirm batch upload
                - batch_status() - Check batch processing status

                Example:
                    ```python
                    # Simple single document upload
                    result = await client.documents.upload_one("report.pdf")
                    print(f"Processed {result.page_count} pages, {result.chunk_count} chunks")

                    # Directory upload with progress
                    results = await client.documents.upload(
                        "/path/to/docs",
                        on_progress=lambda e: print(f"Uploaded: {e.filename}"),
                        on_processing_progress=lambda e: print(f"Processing: {e.completed_count}/{e.total_count}"),
                    )
                    print(f"{results.succeeded_count} documents processed")

                    # Search documents
                    results = await client.documents.search("safety procedures")
                    for chunk in results.results:
                        print(f"{chunk.document_filename}: {chunk.content[:100]}...")
                    ```
        """
        ...

    @property
    def links(self) -> LinksResource:
        """

                Access link (bookmark) operations.

                Provides methods to create, retrieve, update, and delete saved links
                with automatic Open Graph metadata extraction.

                Methods:
                - create() - Create a new link with auto metadata crawl
                - create_and_wait() - Create and wait for crawl to complete
                - get() - Get detailed link information
                - list() - List links with filtering and pagination
                - list_all() - Iterate through all links
                - update() - Update link title/tags
                - delete() - Delete a link
                - batch_delete() - Delete multiple links
                - recrawl() - Refresh link metadata
                - wait_for_crawl() - Wait for crawl to complete

                Example:
                    ```python
                    # Create and wait for metadata
                    link = await client.links.create_and_wait(
                        url="https://example.com/article",
                        tags=["research"]
                    )
                    print(f"Title: {link.og_metadata.title}")

                    # List all links
                    async for link in client.links.list_all():
                        print(f"{link.domain}: {link.title}")

                    # Update metadata
                    await client.links.update(link.id, title="My Article")

                    # Delete
                    await client.links.delete(link.id)
                    ```
        """
        ...

    @property
    def folders(self) -> FoldersResource:
        """Access folder management operations."""
        ...

    @property
    def cloud_storage(self) -> CloudStorageResource:
        """

                Access cloud storage operations.

                Provides methods for connecting cloud storage providers and
                importing/exporting files:
                - initiate_auth() - Start OAuth flow
                - complete_auth() - Complete OAuth flow
                - list_connections() - List connected accounts
                - disconnect() - Disconnect an account
                - start_import() - Import files from cloud storage
                - start_export() - Export files to cloud storage
                - get_job() - Check import/export job status
                - wait_for_job() - Wait for job completion
                - import_and_wait() - Import and wait for completion
                - export_and_wait() - Export and wait for completion

                Example:
                    ```python
                    # List connections
                    conns = await client.cloud_storage.list_connections()

                    # Import files and wait
                    job = await client.cloud_storage.import_and_wait(
                        connection_id=conn_id,
                        files=[CloudFileInput(id="...", name="photo.jpg")],
                    )
                    print(f"Imported {job.completed_files} files")
                    ```
        """
        ...
