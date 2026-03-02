"""
Cloud Storage: Connect, import, and export with cloud providers.

Demonstrates:
- Connecting cloud storage accounts (Google Drive, OneDrive, Dropbox)
- Importing files from cloud storage
- Exporting files to cloud storage
- Monitoring import/export job progress
"""

import asyncio

from aion import AionVision
from aion.types.cloud_storage import CloudFileInput


async def connect_cloud_storage():
    """Connect a cloud storage provider via OAuth."""

    async with AionVision.from_env() as client:

        # Initiate OAuth flow
        auth = await client.cloud_storage.initiate_auth(provider="google_drive")
        print(f"Authorize at: {auth.authorization_url}")
        # User completes OAuth in browser, gets callback code

        # Complete OAuth flow
        result = await client.cloud_storage.complete_auth(
            provider="google_drive",
            code="oauth-callback-code",
            state=auth.state,
        )
        print(f"Connected: {result.connection.id}")


async def list_connections():
    """List connected cloud storage accounts."""

    async with AionVision.from_env() as client:

        connections = await client.cloud_storage.list_connections()
        for conn in connections.connections:
            print(f"  {conn.provider}: {conn.provider_email} (active={conn.is_active})")


async def import_files():
    """Import files from cloud storage."""

    async with AionVision.from_env() as client:

        # Import specific files and wait for completion
        job = await client.cloud_storage.import_and_wait(
            connection_id="connection-uuid",
            files=[
                CloudFileInput(id="drive-file-id-1", name="photo1.jpg"),
                CloudFileInput(id="drive-file-id-2", name="photo2.jpg"),
            ],
        )
        print(f"Imported {job.completed_files} files")
        print(f"Status: {job.status}")

        # Or start import without waiting
        job = await client.cloud_storage.start_import(
            connection_id="connection-uuid",
            files=[CloudFileInput(id="file-id", name="photo.jpg")],
        )
        print(f"Job ID: {job.job_id}")

        # Check job status later
        status = await client.cloud_storage.get_job(job.job_id)
        print(f"Status: {status.status}")


async def export_files():
    """Export files to cloud storage."""

    async with AionVision.from_env() as client:

        # Export files and wait for completion
        job = await client.cloud_storage.export_and_wait(
            connection_id="connection-uuid",
            image_ids=["image-id-1", "image-id-2"],
            folder_name="/Aionvision Exports",
        )
        print(f"Exported {job.completed_files} files")


if __name__ == "__main__":
    asyncio.run(list_connections())
