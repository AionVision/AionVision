"""Type definitions for video upload, analysis, and scene operations."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class VideoUploadStatus(str, Enum):
    """Status of a video upload."""

    UPLOADING = "uploading"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    ABORTED = "aborted"


class VideoAnalysisStatus(str, Enum):
    """Status of a video analysis job."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# =============================================================================
# UPLOAD TYPES
# =============================================================================


@dataclass(frozen=True)
class VideoChunkInfo:
    """Information for uploading a single video chunk.

    Attributes:
        chunk_number: One-based chunk number
        size_bytes: Expected size of this chunk in bytes
        upload_url: Presigned URL for uploading this chunk
        expires_at: When the presigned URL expires
        upload_method: HTTP method to use (typically PUT)
    """

    chunk_number: int
    size_bytes: int
    upload_url: str
    expires_at: Optional[datetime] = None
    upload_method: str = "PUT"

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> VideoChunkInfo:
        """Create from API response data."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


@dataclass(frozen=True)
class VideoUploadSession:
    """Session created when initiating a video upload.

    Attributes:
        media_id: Unique identifier for the video
        upload_id: Unique identifier for this upload session
        chunks: List of chunk upload information
        total_chunks: Total number of chunks
        chunk_size_bytes: Size of each chunk in bytes
        expires_at: When the upload session expires
        storage_path: Storage path for the video
        concurrent_upload_limit: Max concurrent chunk uploads allowed
        retry_attempts: Max retry attempts per chunk
    """

    media_id: str
    upload_id: str
    chunks: list[VideoChunkInfo] = field(default_factory=list)
    total_chunks: int = 0
    chunk_size_bytes: int = 0
    expires_at: Optional[datetime] = None
    storage_path: Optional[str] = None
    concurrent_upload_limit: int = 3
    retry_attempts: int = 3

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> VideoUploadSession:
        """Create from API response data."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


@dataclass(frozen=True)
class ChunkConfirmResult:
    """Result of confirming a chunk upload.

    Attributes:
        chunk_number: The confirmed chunk number
        status: Confirmation status
        chunks_completed: Total chunks completed so far
        total_chunks: Total chunks expected
        progress_percent: Upload progress as percentage
        estimated_time_remaining: Estimated seconds remaining
    """

    chunk_number: int
    status: str = "confirmed"
    chunks_completed: int = 0
    total_chunks: int = 0
    progress_percent: float = 0.0
    estimated_time_remaining: Optional[float] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> ChunkConfirmResult:
        """Create from API response data."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


@dataclass(frozen=True)
class VideoMetadata:
    """Technical metadata extracted from a video file.

    Attributes:
        duration_seconds: Video duration in seconds
        resolution: Resolution string (e.g. "1920x1080")
        width: Frame width in pixels
        height: Frame height in pixels
        frame_rate: Frames per second
        video_codec: Video codec name
        audio_codec: Audio codec name
        bitrate_kbps: Bitrate in kilobits per second
        file_size_bytes: File size in bytes
        format_name: Container format name
    """

    duration_seconds: Optional[float] = None
    resolution: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    frame_rate: Optional[float] = None
    video_codec: Optional[str] = None
    audio_codec: Optional[str] = None
    bitrate_kbps: Optional[int] = None
    file_size_bytes: Optional[int] = None
    format_name: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> VideoMetadata:
        """Create from API response data."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


@dataclass(frozen=True)
class VideoUploadResult:
    """Result of completing a video upload.

    Attributes:
        media_id: Unique identifier for the video
        status: Upload status
        metadata: Technical video metadata
        thumbnail_url: URL for the video thumbnail
        video_url: URL for the video file
        analysis_job_id: ID of the auto-started analysis job (if any)
        processing_status: Current processing status
        created_at: When the video was created
    """

    media_id: str
    status: str = "completed"
    metadata: Optional[VideoMetadata] = None
    thumbnail_url: Optional[str] = None
    video_url: Optional[str] = None
    analysis_job_id: Optional[str] = None
    processing_status: Optional[str] = None
    created_at: Optional[datetime] = None

    @property
    def is_completed(self) -> bool:
        """Whether the upload is completed."""
        ...

    @property
    def is_analyzing(self) -> bool:
        """Whether analysis is in progress."""
        ...

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> VideoUploadResult:
        """Create from API response data."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


@dataclass(frozen=True)
class VideoUploadProgress:
    """Progress information for an in-flight video upload.

    Attributes:
        media_id: Video identifier
        upload_id: Upload session identifier
        status: Current upload status
        chunks_completed: Number of chunks uploaded
        total_chunks: Total chunks expected
        bytes_uploaded: Bytes uploaded so far
        total_bytes: Total bytes expected
        progress_percent: Upload progress percentage
        failed_chunks: List of failed chunk numbers
        estimated_time_remaining: Estimated seconds remaining
    """

    media_id: str
    upload_id: str
    status: str = "uploading"
    chunks_completed: int = 0
    total_chunks: int = 0
    bytes_uploaded: int = 0
    total_bytes: int = 0
    progress_percent: float = 0.0
    failed_chunks: list[int] = field(default_factory=list)
    estimated_time_remaining: Optional[float] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> VideoUploadProgress:
        """Create from API response data."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


@dataclass(frozen=True)
class VideoAbortResult:
    """Result of aborting a video upload.

    Attributes:
        media_id: Video identifier
        status: Abort status
        cleaned_up: Whether cleanup was performed
        chunks_removed: Number of chunks cleaned up
        s3_cleanup: Whether storage objects were removed
    """

    media_id: str
    status: str = "aborted"
    cleaned_up: bool = False
    chunks_removed: int = 0
    s3_cleanup: bool = False

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> VideoAbortResult:
        """Create from API response data."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


@dataclass(frozen=True)
class ChunkRetryResult:
    """Result of requesting a retry URL for a failed chunk.

    Attributes:
        chunk_number: The chunk to retry
        upload_url: New presigned URL for retry
        expires_at: When the new URL expires
        retry_attempt: Current retry attempt number
        max_retries: Maximum retries allowed
    """

    chunk_number: int
    upload_url: str
    expires_at: Optional[datetime] = None
    retry_attempt: int = 0
    max_retries: int = 3

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> ChunkRetryResult:
        """Create from API response data."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


@dataclass(frozen=True)
class BatchVideoUploadSession:
    """Session created for a batch video upload.

    Attributes:
        batch_id: Unique batch identifier
        videos: List of individual upload sessions
        total_videos: Total number of videos in batch
        total_size_bytes: Total size of all videos
        estimated_time_seconds: Estimated processing time
        processing_priority: Priority level
    """

    batch_id: str
    videos: list[VideoUploadSession] = field(default_factory=list)
    total_videos: int = 0
    total_size_bytes: int = 0
    estimated_time_seconds: Optional[float] = None
    processing_priority: str = "normal"

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> BatchVideoUploadSession:
        """Create from API response data."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


# =============================================================================
# ANALYSIS TYPES
# =============================================================================


@dataclass(frozen=True)
class VideoAnalysisJobStatus:
    """Status of a video analysis job.

    Attributes:
        analysis_job_id: Unique job identifier
        media_id: Video identifier
        status: Current job status
        progress_percent: Analysis progress percentage
        current_step: Current processing step description
        started_at: When analysis started
        completed_at: When analysis completed
        error_message: Error message if failed
        error_code: Error code if failed
        retry_count: Number of retries attempted
        max_retries: Maximum retries allowed
        estimated_completion_time: Estimated completion timestamp
    """

    analysis_job_id: str
    media_id: str
    status: str = "pending"
    progress_percent: float = 0.0
    current_step: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    error_code: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    estimated_completion_time: Optional[datetime] = None

    @property
    def is_completed(self) -> bool:
        """Whether the analysis completed successfully."""
        ...

    @property
    def is_failed(self) -> bool:
        """Whether the analysis failed."""
        ...

    @property
    def is_pending(self) -> bool:
        """Whether the analysis is still pending."""
        ...

    @property
    def is_terminal(self) -> bool:
        """Whether the analysis has reached a terminal state (completed, failed, or cancelled)."""
        ...

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> VideoAnalysisJobStatus:
        """Create from API response data."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


@dataclass(frozen=True)
class VideoAnalysisRetryResult:
    """Result of retrying a video analysis job.

    Attributes:
        analysis_job_id: Job identifier
        media_id: Video identifier
        status: New job status after retry
        retry_count: Current retry count
        max_retries: Maximum retries allowed
        message: Human-readable status message
    """

    analysis_job_id: str
    media_id: str
    status: str = "pending"
    retry_count: int = 0
    max_retries: int = 3
    message: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> VideoAnalysisRetryResult:
        """Create from API response data."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


@dataclass(frozen=True)
class VideoAnalysisQueueResult:
    """Result of queuing a video for analysis.

    Attributes:
        analysis_job_id: Job identifier
        media_id: Video identifier
        queue_position: Position in the analysis queue
        estimated_start_time: Estimated time when analysis will start
        message: Human-readable status message
    """

    analysis_job_id: str
    media_id: str
    queue_position: Optional[int] = None
    estimated_start_time: Optional[datetime] = None
    message: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> VideoAnalysisQueueResult:
        """Create from API response data."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


# =============================================================================
# SCENE TYPES
# =============================================================================


@dataclass(frozen=True)
class VideoScene:
    """A single scene extracted from a video.

    Attributes:
        scene_id: Unique scene identifier
        scene_index: Zero-based index of the scene in the video
        start_time: Scene start time in seconds
        end_time: Scene end time in seconds
        time_range_formatted: Human-readable time range (e.g. "00:01:30-00:02:15")
        description: AI-generated description of the scene
        tags: Tags extracted from the scene
        visible_text: Text visible in the scene (OCR)
        confidence_score: Confidence score of the scene extraction
        embedding_status: Status of scene embedding generation
        thumbnail_url: URL for the scene thumbnail
        created_at: When the scene was created
    """

    scene_id: str
    scene_index: int = 0
    start_time: float = 0.0
    end_time: float = 0.0
    time_range_formatted: Optional[str] = None
    description: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    visible_text: Optional[str] = None
    confidence_score: Optional[float] = None
    embedding_status: Optional[str] = None
    thumbnail_url: Optional[str] = None
    created_at: Optional[datetime] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> VideoScene:
        """Create from API response data."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...


@dataclass(frozen=True)
class VideoSceneList:
    """List of scenes from a video.

    Attributes:
        scenes: List of video scenes
        count: Total number of scenes
        video_id: ID of the video these scenes belong to
    """

    scenes: list[VideoScene] = field(default_factory=list)
    count: int = 0
    video_id: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> VideoSceneList:
        """Create from API response data."""
        ...

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...
