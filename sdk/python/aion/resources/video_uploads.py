"""Video uploads resource for the Aionvision SDK."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Optional, Union

from ..config import ClientConfig
from ..exceptions import VideoUploadError
from ..types.callbacks import (
    VideoAnalysisProgressEvent,
    VideoChunkProgressEvent,
    VideoUploadCompleteEvent,
)
from ..types.video import (
    BatchVideoUploadSession,
    ChunkConfirmResult,
    ChunkRetryResult,
    VideoAbortResult,
    VideoUploadProgress,
    VideoUploadResult,
    VideoUploadSession,
)

SUPPORTED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".webm", ".avi"}


class VideoUploadsResource:
    """
    Access video upload operations.

    Provides low-level methods (1:1 with API):
    - initiate() - Start a chunked video upload
    - batch_initiate() - Start a batch video upload
    - confirm_chunk() - Confirm a chunk was uploaded
    - complete() - Complete the upload after all chunks
    - abort() - Abort an in-progress upload
    - get_progress() - Check upload progress
    - retry_chunk() - Get a new URL for a failed chunk

    And high-level convenience methods:
    - upload_one() - Upload a single video file with automatic chunking
    - upload() - Upload one or more video files

    Supported formats: .mp4, .mov, .m4v, .webm, .avi
    """

    def __init__(self, http: HTTPClient, config: ClientConfig) -> None:
        ...

    # =========================================================================
    # LOW-LEVEL METHODS (1:1 with API)
    # =========================================================================

    async def initiate(
        self,
        filename: str,
        content_type: str,
        size_bytes: int,
        *,
        title: Optional[str] = None,
        tags: Optional[list[str]] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> VideoUploadSession:
        """
        Initiate a chunked video upload.

        Args:
            filename: Name of the video file
            content_type: MIME type (e.g. "video/mp4")
            size_bytes: Total file size in bytes
            title: Optional title for the video
            tags: Optional tags
            metadata: Optional additional metadata

        Returns:
            VideoUploadSession with chunk upload URLs

        Raises:
            ValidationError: If file type is unsupported
            QuotaExceededError: If upload quota is insufficient
        """
        ...

    async def batch_initiate(
        self,
        videos: list[dict[str, Any]],
        *,
        auto_process: bool = True,
        processing_priority: str = "normal",
    ) -> BatchVideoUploadSession:
        """
        Initiate a batch video upload (up to 10 videos).

        Args:
            videos: List of video info dicts, each with filename, content_type, size_bytes
            auto_process: Whether to auto-start analysis after upload
            processing_priority: Processing priority ("normal", "high")

        Returns:
            BatchVideoUploadSession with per-video upload sessions
        """
        ...

    async def confirm_chunk(
        self,
        media_id: str,
        upload_id: str,
        chunk_number: int,
        etag: str,
        size_bytes: int,
    ) -> ChunkConfirmResult:
        """
        Confirm a chunk was successfully uploaded.

        Args:
            media_id: Video identifier
            upload_id: Upload session identifier
            chunk_number: One-based chunk number
            etag: ETag returned after upload
            size_bytes: Size of the uploaded chunk

        Returns:
            ChunkConfirmResult with progress information
        """
        ...

    async def complete(
        self,
        media_id: str,
        upload_id: str,
        *,
        duration_seconds: Optional[float] = None,
        duration_extraction_failed: Optional[bool] = None,
        auto_analyze: bool = True,
        analysis_type: str = "full_vlm",
        title: Optional[str] = None,
        tags: Optional[list[str]] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> VideoUploadResult:
        """
        Complete a video upload after all chunks are uploaded.

        Args:
            media_id: Video identifier
            upload_id: Upload session identifier
            duration_seconds: Video duration in seconds (extracted client-side).
                If None, sends 1.0 as fallback with duration_extraction_failed=True.
            duration_extraction_failed: Whether client-side duration extraction failed.
                Auto-set to True when duration_seconds is None.
            auto_analyze: Whether to auto-start analysis
            analysis_type: Analysis pipeline to run on completion
                (full_vlm, frame_sample, scene_detection, transcript)
            title: Optional title override
            tags: Optional tags override
            metadata: Optional metadata override

        Returns:
            VideoUploadResult with final status and metadata
        """
        ...

    async def abort(
        self,
        media_id: str,
        upload_id: str,
        *,
        reason: Optional[str] = None,
    ) -> VideoAbortResult:
        """
        Abort an in-progress video upload.

        Args:
            media_id: Video identifier
            upload_id: Upload session identifier
            reason: Optional abort reason

        Returns:
            VideoAbortResult with cleanup details
        """
        ...

    async def get_progress(self, media_id: str) -> VideoUploadProgress:
        """
        Get upload progress for a video.

        Args:
            media_id: Video identifier

        Returns:
            VideoUploadProgress with chunk-level progress
        """
        ...

    async def retry_chunk(
        self,
        media_id: str,
        upload_id: str,
        chunk_number: int,
    ) -> ChunkRetryResult:
        """
        Get a new presigned URL for retrying a failed chunk upload.

        Args:
            media_id: Video identifier
            upload_id: Upload session identifier
            chunk_number: One-based chunk number to retry

        Returns:
            ChunkRetryResult with new upload URL
        """
        ...

    # =========================================================================
    # HIGH-LEVEL CONVENIENCE METHODS
    # =========================================================================

    async def upload_one(
        self,
        file: Union[str, Path],
        *,
        title: Optional[str] = None,
        tags: Optional[list[str]] = None,
        auto_analyze: bool = True,
        wait_for_analysis: bool = False,
        analysis_timeout: Optional[float] = None,
        analysis_type: str = "full_vlm",
        max_chunk_concurrency: Optional[int] = None,
        max_chunk_retries: int = 3,
        on_chunk_progress: Optional[Callable[[VideoChunkProgressEvent], None]] = None,
        on_upload_complete: Optional[Callable[[VideoUploadCompleteEvent], None]] = None,
        on_analysis_progress: Optional[Callable[[VideoAnalysisProgressEvent], None]] = None,
    ) -> VideoUploadResult:
        """
        Upload a single video file with automatic chunking.

        Handles the full upload lifecycle: initiate, parallel chunk upload with
        retries, confirm, complete. Memory is bounded to approximately
        max_chunk_concurrency × chunk_size bytes.

        Args:
            file: Path to the video file
            title: Optional title for the video
            tags: Optional tags for the video
            auto_analyze: Whether to auto-start analysis after upload
            wait_for_analysis: Whether to wait for analysis to complete
            analysis_timeout: Timeout for analysis wait (default: config polling_timeout)
            analysis_type: Analysis pipeline to run on completion
                (full_vlm, frame_sample, scene_detection, transcript)
            max_chunk_concurrency: Max concurrent chunk uploads (default: from server)
            max_chunk_retries: Max retry attempts per chunk (default: 3)
            on_chunk_progress: Callback fired after each chunk upload
            on_upload_complete: Callback fired when upload completes
            on_analysis_progress: Callback fired during analysis polling

        Returns:
            VideoUploadResult with video metadata and status

        Raises:
            VideoUploadError: If upload fails at any stage
            VideoAnalysisError: If wait_for_analysis=True and analysis fails
            FileNotFoundError: If the file does not exist
        """
        ...

    async def upload(
        self,
        files: Union[str, Path, list[Union[str, Path]]],
        *,
        title: Optional[str] = None,
        tags: Optional[list[str]] = None,
        auto_analyze: bool = True,
        wait_for_analysis: bool = False,
        analysis_timeout: Optional[float] = None,
        analysis_type: str = "full_vlm",
        max_chunk_concurrency: Optional[int] = None,
        max_chunk_retries: int = 3,
        on_chunk_progress: Optional[Callable[[VideoChunkProgressEvent], None]] = None,
        on_upload_complete: Optional[Callable[[VideoUploadCompleteEvent], None]] = None,
        on_analysis_progress: Optional[Callable[[VideoAnalysisProgressEvent], None]] = None,
    ) -> list[VideoUploadResult]:
        """
        Upload one or more video files.

        Accepts a single path, list of paths, or directory path. Directories
        are expanded to find all supported video files (.mp4, .mov, .m4v, .webm, .avi).

        Args:
            files: File path, directory, or list of file paths
            title: Optional title (only applied for single-file uploads)
            tags: Optional tags
            auto_analyze: Whether to auto-start analysis
            wait_for_analysis: Whether to wait for analysis to complete
            analysis_timeout: Timeout for analysis wait
            analysis_type: Type of analysis
            max_chunk_concurrency: Max concurrent chunk uploads per video
            max_chunk_retries: Max retry attempts per chunk
            on_chunk_progress: Callback fired after each chunk upload
            on_upload_complete: Callback fired when each upload completes
            on_analysis_progress: Callback fired during analysis polling

        Returns:
            List of VideoUploadResult for each uploaded video
        """
        ...
