"""
Uploading Videos: Single and batch upload with AI analysis.

Demonstrates:
- Single video upload with upload_one()
- Batch upload with upload() (files, directories)
- Progress callbacks for chunk upload and analysis
- Waiting for AI analysis to complete
- Retrieving AI-detected scenes
- Low-level chunked upload control
- Error handling with VideoUploadError and VideoAnalysisError
"""

import asyncio
from pathlib import Path

from aion import AionVision, VideoAnalysisError, VideoUploadError
from aion.types.callbacks import (
    VideoAnalysisProgressEvent,
    VideoChunkProgressEvent,
    VideoUploadCompleteEvent,
)


async def single_upload():
    """Upload a single video file."""

    async with AionVision.from_env() as client:

        # Simple upload — auto-starts AI analysis, does not wait for it
        result = await client.video_uploads.upload_one("footage.mp4")
        print(f"media_id: {result.media_id}")
        print(f"analysis_job_id: {result.analysis_job_id}")
        print(f"thumbnail_url: {result.thumbnail_url}")


async def upload_with_callbacks():
    """Upload a video with progress tracking and analysis wait."""

    def on_chunk(event: VideoChunkProgressEvent) -> None:
        print(
            f"  Chunk {event.chunk_number}/{event.total_chunks} "
            f"({event.progress_percent:.1f}%)"
        )

    def on_complete(event: VideoUploadCompleteEvent) -> None:
        print(f"  Upload complete: {event.media_id}")

    def on_analysis(event: VideoAnalysisProgressEvent) -> None:
        status = event.job_status
        print(
            f"  Analysis {event.progress_percent:.0f}%"
            + (f" — {status.current_step}" if status.current_step else "")
        )

    async with AionVision.from_env() as client:

        result = await client.video_uploads.upload_one(
            "footage.mp4",
            title="Inspection footage",
            tags=["inspection", "2024"],
            auto_analyze=True,
            wait_for_analysis=True,
            analysis_type="full_vlm",       # full AI scene analysis
            max_chunk_retries=3,
            on_chunk_progress=on_chunk,
            on_upload_complete=on_complete,
            on_analysis_progress=on_analysis,
        )

        print(f"media_id: {result.media_id}")
        print(f"thumbnail_url: {result.thumbnail_url}")
        print(f"video_url: {result.video_url}")


async def batch_upload():
    """Upload multiple video files."""

    async with AionVision.from_env() as client:

        # Upload a list of files
        results = await client.video_uploads.upload(
            ["clip1.mp4", "clip2.mov", "clip3.mp4"],
            tags=["batch"],
            auto_analyze=True,
        )
        for r in results:
            print(f"{r.media_id}: {r.status}")

        # Or upload an entire directory (expands .mp4, .mov, .m4v, .webm, .avi)
        dir_results = await client.video_uploads.upload("/videos/inspection")
        print(f"Uploaded {len(dir_results)} videos")


async def retrieve_scenes():
    """Retrieve AI-detected scenes from an analyzed video."""

    async with AionVision.from_env() as client:

        video_id = "550e8400-e29b-41d4-a716-446655440000"

        scenes = await client.video_scenes.list(video_id)
        print(f"Found {scenes.count} scenes")

        for scene in scenes.scenes:
            print(
                f"  Scene {scene.scene_index}: {scene.time_range_formatted}"
                f" — {scene.description}"
            )
            if scene.tags:
                print(f"    Tags: {', '.join(scene.tags)}")
            if scene.visible_text:
                print(f"    OCR: {scene.visible_text[:80]}")

        # Download a scene thumbnail
        if scenes.scenes:
            thumbnail_bytes = await client.video_scenes.get_thumbnail(
                scenes.scenes[0].scene_id
            )
            Path("scene_0.jpg").write_bytes(thumbnail_bytes)


async def poll_analysis():
    """Separately poll an analysis job that was started earlier."""

    async with AionVision.from_env() as client:

        analysis_job_id = "job-id-from-upload-result"

        # Check status once
        status = await client.video_analysis.get_status(analysis_job_id)
        print(f"status: {status.status}, progress: {status.progress_percent:.0f}%")

        # Or poll to completion
        if not status.is_terminal:
            final = await client.video_analysis.wait_for_completion(
                analysis_job_id,
                timeout=600.0,
                on_progress=lambda s: print(f"  {s.progress_percent:.0f}%"),
            )
            print(f"Final status: {final.status}")

        # Check by video ID instead of job ID
        status_by_media = await client.video_analysis.get_status_by_media(
            "550e8400-e29b-41d4-a716-446655440000"
        )
        print(f"Media analysis status: {status_by_media.status}")


async def retry_analysis():
    """Retry a failed analysis job."""

    async with AionVision.from_env() as client:

        result = await client.video_analysis.retry(
            analysis_job_id="failed-job-id",
            media_id="550e8400-e29b-41d4-a716-446655440000",
            reason="Retry after transient VLM error",
        )
        print(f"Retry submitted: {result.status}, attempt {result.retry_count}")


async def low_level_upload():
    """Low-level chunked upload for custom upload orchestration."""

    async with AionVision.from_env() as client:

        file_path = Path("large_video.mp4")
        file_size = file_path.stat().st_size

        # Step 1: Initiate
        session = await client.video_uploads.initiate(
            filename=file_path.name,
            content_type="video/mp4",
            size_bytes=file_size,
            title="Large inspection video",
        )
        print(f"media_id: {session.media_id}")
        print(f"total_chunks: {session.total_chunks}")
        print(f"chunk_size_bytes: {session.chunk_size_bytes}")

        # Step 2: Upload chunks and confirm each one
        # (upload_one() does this automatically — use low-level only for
        # custom concurrency, custom HTTP clients, or special retry logic)
        chunk_size = session.chunk_size_bytes
        with open(file_path, "rb") as f:
            for chunk_info in session.chunks:
                chunk_data = f.read(chunk_size)
                # ... upload chunk_data to chunk_info.upload_url via PUT ...
                # etag = response.headers["ETag"]
                # confirm = await client.video_uploads.confirm_chunk(
                #     session.media_id, session.upload_id,
                #     chunk_info.chunk_number, etag, len(chunk_data),
                # )

        # Step 3: Complete
        result = await client.video_uploads.complete(
            media_id=session.media_id,
            upload_id=session.upload_id,
            auto_analyze=True,
            analysis_type="full_vlm",
        )
        print(f"Upload complete: {result.status}")


async def error_handling():
    """Handle video-specific errors."""

    async with AionVision.from_env() as client:

        try:
            result = await client.video_uploads.upload_one(
                "footage.mp4",
                wait_for_analysis=True,
            )
        except VideoUploadError as e:
            # Upload failed at a specific stage
            print(f"Upload failed at stage '{e.details.get('stage')}'")
            if e.media_id:
                # Upload initiated but failed later — media_id exists
                print(f"media_id: {e.media_id}")
                print(f"Chunks uploaded before failure: {e.partial_chunks}")
        except VideoAnalysisError as e:
            # Upload succeeded but analysis failed
            print(f"Analysis failed: {e.message}")
            print(f"media_id: {e.media_id}")
            print(f"analysis_job_id: {e.analysis_job_id}")

            # Retry manually
            retry = await client.video_analysis.retry(
                analysis_job_id=e.analysis_job_id,
                media_id=e.media_id,
            )
            print(f"Retry status: {retry.status}")


if __name__ == "__main__":
    asyncio.run(single_upload())
