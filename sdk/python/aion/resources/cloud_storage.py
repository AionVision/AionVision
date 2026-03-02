from __future__ import annotations
from typing import Any, Callable, Optional, Union
from ..config import ClientConfig
from ..exceptions import CloudStorageError, ValidationError
from ..types.callbacks import CloudStorageJobProgressEvent
from ..types.cloud_storage import CloudFileInput, CloudStorageConnection, CloudStorageJob, CompleteAuthResult, ConnectionList, DisconnectResult, ExportResult, ImportResult, InitiateAuthResult


class CloudStorageResource:
    """

        Cloud storage operations for the Aionvision SDK.

        Provides methods for connecting cloud storage providers (Google Drive),
        importing files from cloud storage, and exporting files to cloud storage.
    """

    def __init__(self, http: HTTPClient, config: ClientConfig) -> None:
        ...

    async def initiate_auth(self, provider: str, *, redirect_uri: Optional[str] = None) -> InitiateAuthResult:
        """

                Initiate OAuth flow for a cloud storage provider.

                Returns an authorization URL to redirect the user to.

                Args:
                    provider: Provider type (e.g. 'google_drive')
                    redirect_uri: Custom redirect URI for the OAuth callback

                Returns:
                    InitiateAuthResult with authorization_url and state

                Raises:
                    ValidationError: If provider is empty
        """
        ...

    async def complete_auth(self, provider: str, *, code: str, state: str, redirect_uri: Optional[str] = None) -> CompleteAuthResult:
        """

                Complete OAuth flow and create a connection.

                Called after the user authorizes the application.

                Args:
                    provider: Provider type (e.g. 'google_drive')
                    code: Authorization code from the OAuth callback
                    state: State parameter for CSRF verification
                    redirect_uri: Redirect URI used during auth initiation

                Returns:
                    CompleteAuthResult with the connection and whether it's new

                Raises:
                    ValidationError: If required parameters are empty
        """
        ...

    async def list_connections(self, *, provider: Optional[str] = None, active_only: bool = True) -> ConnectionList:
        """

                List cloud storage connections.

                Args:
                    provider: Filter by provider type
                    active_only: Only return active connections (default: True)

                Returns:
                    ConnectionList with connections and total_count
        """
        ...

    async def disconnect(self, connection_id: str) -> DisconnectResult:
        """

                Disconnect a cloud storage account.

                Args:
                    connection_id: Connection identifier to disconnect

                Returns:
                    DisconnectResult with success status and message

                Raises:
                    ValidationError: If connection_id is empty
        """
        ...

    async def start_import(self, connection_id: str, files: list[Union[CloudFileInput, dict[str, Any]]], *, auto_describe: bool = True, tags: Optional[list[str]] = None, collection_id: Optional[str] = None) -> ImportResult:
        """

                Start importing files from cloud storage.

                Args:
                    connection_id: Connection to import from
                    files: List of files to import (CloudFileInput or dicts with id/name)
                    auto_describe: Automatically generate AI descriptions (default: True)
                    tags: Tags to apply to imported files
                    collection_id: Target collection for imported files

                Returns:
                    ImportResult with job_id for async imports or image_ids for sync

                Raises:
                    ValidationError: If connection_id is empty or files is empty
        """
        ...

    async def start_export(self, connection_id: str, image_ids: list[str], *, folder_id: Optional[str] = None, folder_name: Optional[str] = None) -> ExportResult:
        """

                Start exporting files to cloud storage.

                Args:
                    connection_id: Connection to export to
                    image_ids: List of image IDs to export
                    folder_id: Target folder ID in cloud storage
                    folder_name: Create a new folder with this name

                Returns:
                    ExportResult with job_id for async exports

                Raises:
                    ValidationError: If connection_id is empty or image_ids is empty
        """
        ...

    async def get_job(self, job_id: str) -> CloudStorageJob:
        """

                Get the status of a cloud storage job.

                Args:
                    job_id: Job identifier

                Returns:
                    CloudStorageJob with current status and progress

                Raises:
                    ValidationError: If job_id is empty
        """
        ...

    async def wait_for_job(self, job_id: str, *, timeout: Optional[float] = None, poll_interval: Optional[float] = None, on_progress: Optional[Callable[[CloudStorageJobProgressEvent], None]] = None) -> CloudStorageJob:
        """

                Wait for a cloud storage job to complete.

                Polls the job status until it reaches a terminal state.

                Args:
                    job_id: Job identifier
                    timeout: Maximum wait time in seconds (default: config polling_timeout)
                    poll_interval: Time between polls in seconds (default: config polling_interval)
                    on_progress: Optional callback fired on each poll with progress info

                Returns:
                    CloudStorageJob with final status

                Raises:
                    ValidationError: If job_id is empty
                    CloudStorageError: If the job failed completely
                    AionvisionTimeoutError: If timeout exceeded
        """
        ...

    async def import_and_wait(self, connection_id: str, files: list[Union[CloudFileInput, dict[str, Any]]], *, auto_describe: bool = True, tags: Optional[list[str]] = None, collection_id: Optional[str] = None, timeout: Optional[float] = None, poll_interval: Optional[float] = None, on_progress: Optional[Callable[[CloudStorageJobProgressEvent], None]] = None) -> CloudStorageJob:
        """

                Import files from cloud storage and wait for completion.

                Convenience method combining start_import() and wait_for_job().

                Args:
                    connection_id: Connection to import from
                    files: List of files to import
                    auto_describe: Automatically generate AI descriptions (default: True)
                    tags: Tags to apply to imported files
                    collection_id: Target collection for imported files
                    timeout: Maximum wait time in seconds
                    poll_interval: Time between polls in seconds
                    on_progress: Optional callback fired on each poll

                Returns:
                    CloudStorageJob with final status

                Raises:
                    CloudStorageError: If the job failed
                    AionvisionTimeoutError: If timeout exceeded
        """
        ...

    async def export_and_wait(self, connection_id: str, image_ids: list[str], *, folder_id: Optional[str] = None, folder_name: Optional[str] = None, timeout: Optional[float] = None, poll_interval: Optional[float] = None, on_progress: Optional[Callable[[CloudStorageJobProgressEvent], None]] = None) -> CloudStorageJob:
        """

                Export files to cloud storage and wait for completion.

                Convenience method combining start_export() and wait_for_job().

                Args:
                    connection_id: Connection to export to
                    image_ids: List of image IDs to export
                    folder_id: Target folder ID in cloud storage
                    folder_name: Create a new folder with this name
                    timeout: Maximum wait time in seconds
                    poll_interval: Time between polls in seconds
                    on_progress: Optional callback fired on each poll

                Returns:
                    CloudStorageJob with final status

                Raises:
                    CloudStorageError: If the job failed
                    AionvisionTimeoutError: If timeout exceeded
        """
        ...
