"""Video scenes resource for the Aionvision SDK."""

from __future__ import annotations

from ..config import ClientConfig
from ..types.video import VideoScene, VideoSceneList


class VideoScenesResource:
    """
    Access video scene data.

    Provides methods for retrieving scenes extracted from analyzed videos:
    - list() - Get all scenes for a video
    - get_thumbnail() - Download a scene thumbnail
    """

    def __init__(self, http: HTTPClient, config: ClientConfig) -> None:
        ...

    async def list(self, video_id: str) -> VideoSceneList:
        """
        List all scenes for a video.

        Args:
            video_id: The video (media) ID to get scenes for

        Returns:
            VideoSceneList with all extracted scenes

        Raises:
            ResourceNotFoundError: If the video is not found
        """
        ...

    async def get_thumbnail(self, scene_id: str) -> bytes:
        """
        Download a scene thumbnail image.

        Args:
            scene_id: The scene ID to get the thumbnail for

        Returns:
            Raw bytes of the thumbnail JPEG image

        Raises:
            ResourceNotFoundError: If the scene is not found
        """
        ...
