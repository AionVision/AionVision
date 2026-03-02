"""Video analysis resource for the Aionvision SDK."""

from __future__ import annotations

from typing import Callable, Optional

from ..config import ClientConfig
from ..exceptions import VideoAnalysisError
from ..types.video import (
    VideoAnalysisJobStatus,
    VideoAnalysisQueueResult,
    VideoAnalysisRetryResult,
)


class VideoAnalysisResource:
    """
    Access video analysis operations.

    Provides methods for managing video analysis jobs:
    - get_status() - Check analysis job status by job ID
    - get_status_by_media() - Check analysis status by media ID
    - retry() - Retry a failed analysis job
    - queue() - Queue a video for analysis
    - wait_for_completion() - Poll until analysis completes
    """

    def __init__(self, http: HTTPClient, config: ClientConfig) -> None:
        ...

    async def get_status(self, analysis_job_id: str) -> VideoAnalysisJobStatus:
        """
        Get the status of an analysis job.

        Args:
            analysis_job_id: The analysis job ID

        Returns:
            VideoAnalysisJobStatus with progress details

        Raises:
            ResourceNotFoundError: If the job is not found
        """
        ...

    async def get_status_by_media(self, media_id: str) -> VideoAnalysisJobStatus:
        """
        Get the analysis status for a video by its media ID.

        Args:
            media_id: The video (media) ID

        Returns:
            VideoAnalysisJobStatus with progress details

        Raises:
            ResourceNotFoundError: If the video or job is not found
        """
        ...

    async def retry(
        self,
        analysis_job_id: str,
        media_id: str,
        *,
        reason: Optional[str] = None,
    ) -> VideoAnalysisRetryResult:
        """
        Retry a failed analysis job.

        Args:
            analysis_job_id: The analysis job ID to retry
            media_id: The video (media) ID
            reason: Optional reason for the retry

        Returns:
            VideoAnalysisRetryResult with retry status

        Raises:
            VideoAnalysisError: If the retry fails
        """
        ...

    async def queue(
        self,
        media_id: str,
        *,
        analysis_type: str = "full_vlm",
        priority: str = "normal",
    ) -> VideoAnalysisQueueResult:
        """
        Queue a video for analysis.

        Args:
            media_id: The video (media) ID to analyze
            analysis_type: Type of analysis ("full_vlm", "frame_sample",
                "scene_detection", "transcript")
            priority: Processing priority ("normal", "high")

        Returns:
            VideoAnalysisQueueResult with queue position

        Raises:
            VideoAnalysisError: If queueing fails
        """
        ...

    async def wait_for_completion(
        self,
        analysis_job_id: str,
        *,
        timeout: Optional[float] = None,
        on_progress: Optional[Callable[[VideoAnalysisJobStatus], None]] = None,
    ) -> VideoAnalysisJobStatus:
        """
        Poll until video analysis completes or fails.

        Uses exponential backoff (1.5x factor, max 15s interval).

        Args:
            analysis_job_id: The analysis job ID to monitor
            timeout: Maximum wait time in seconds (default: config polling_timeout)
            on_progress: Optional callback fired on each poll with current status

        Returns:
            Final VideoAnalysisJobStatus

        Raises:
            AionvisionTimeoutError: If timeout is exceeded
            VideoAnalysisError: If analysis fails
        """
        ...
