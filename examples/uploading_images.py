"""
Uploading Images: Single and batch upload with callbacks.

Demonstrates:
- Single file upload with upload_one()
- Batch upload with upload() (files, directories, byte data)
- Progress callbacks for tracking upload and description status
- Handling description failures
- Custom storage targets
"""

import asyncio
from pathlib import Path

from aion import AionVision
from aion.types.callbacks import (
    DescriptionFailedEvent,
    DescriptionProgressEvent,
    FileCompleteEvent,
    UploadProgressEvent,
)
from aion.types.common import StorageTarget


async def single_upload():
    """Upload a single image file."""

    async with AionVision.from_env() as client:

        # Simple upload - waits for AI description by default
        result = await client.upload_one("photo.jpg")
        print(f"Image ID: {result.image_id}")
        print(f"Description: {result.description}")
        print(f"Tags: {result.tags}")

        # Upload from bytes
        image_bytes = Path("photo.jpg").read_bytes()
        result = await client.upload_one(
            image_bytes,
            filename="my_photo.jpg",
        )
        print(f"Uploaded: {result.filename}")

        # Upload without waiting for description
        result = await client.upload_one(
            "photo.jpg",
            wait_for_descriptions=False,
        )
        print(f"Image ID: {result.image_id}")
        print(f"Description status: {result.description_status}")


async def batch_upload():
    """Upload multiple files at once."""

    async with AionVision.from_env() as client:

        # Upload a directory of images
        # Note: only image files (JPEG, PNG, WebP, GIF) are included.
        # Non-image files (PDFs, AVIF, etc.) are silently skipped.
        # Use client.documents.upload() for document files.
        results = await client.upload("/path/to/photos")
        print(f"Uploaded {len(results)} images")
        for r in results:
            print(f"  {r.filename}: {r.description[:80]}...")

        # Upload specific files
        results = await client.upload([
            "photo1.jpg",
            "photo2.png",
            "photo3.webp",
        ])

        # Upload a directory recursively (default)
        results = await client.upload(
            "/path/to/photos",
            recursive=True,          # default: True
            include_hidden=False,     # default: False
        )


async def upload_with_callbacks():
    """Track upload progress with callbacks."""

    def on_progress(event: UploadProgressEvent):
        print(f"Prepared: {event.filename} ({event.total_bytes} bytes)")

    def on_file_complete(event: FileCompleteEvent):
        print(f"Uploaded: {event.result.filename} -> {event.result.image_id}")

    def on_description_progress(event: DescriptionProgressEvent):
        print(f"Describing: {event.completed_count}/{event.total_count} complete")

    def on_description_failed(event: DescriptionFailedEvent):
        print(f"Failed: {event.result.image_id} - {event.error_message}")

    async with AionVision.from_env() as client:
        results = await client.upload(
            "/path/to/photos",
            on_progress=on_progress,
            on_file_complete=on_file_complete,
            on_description_progress=on_description_progress,
            on_description_failed=on_description_failed,
        )
        print(f"Completed: {len(results)} images")


async def handle_failures():
    """Handle description failures gracefully."""

    async with AionVision.from_env() as client:

        # By default, raises DescriptionError on failure
        # Set raise_on_failure=False to handle manually
        results = await client.upload(
            "/path/to/photos",
            raise_on_failure=False,
        )

        if results.has_failures:
            print(f"Failures: {len(results.failed())}")
            for r in results.failed():
                print(f"  {r.filename}: {r.description_error}")

            # Retryable failures can be re-attempted
            for r in results.retryable():
                print(f"  Retryable: {r.filename}")


async def custom_storage():
    """Upload to custom S3 bucket."""

    async with AionVision.from_env() as client:

        # Upload to your organization's configured S3 bucket
        result = await client.upload_one(
            "photo.jpg",
            storage_target=StorageTarget.CUSTOM,
        )
        print(f"Stored in custom bucket: {result.image_id}")


if __name__ == "__main__":
    asyncio.run(batch_upload())
