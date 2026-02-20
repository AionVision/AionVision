from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional


@dataclass(frozen=True)
class CloudStorageConnection:
    """

        A cloud storage provider connection.

        Attributes:
            id: Unique connection identifier
            provider: Provider type (e.g. 'google_drive')
            is_active: Whether the connection is currently active
            provider_email: Email associated with the provider account
            provider_display_name: Display name from the provider
            created_at: When the connection was created
            last_used_at: When the connection was last used
    """
    id: str
    provider: str
    is_active: bool
    provider_email: Optional[str] = None
    provider_display_name: Optional[str] = None
    created_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> CloudStorageConnection:
        """Create CloudStorageConnection from API response data."""
        ...


@dataclass(frozen=True)
class InitiateAuthResult:
    """

        Result of initiating OAuth flow.

        Attributes:
            authorization_url: URL to redirect the user to for authorization
            state: State parameter for CSRF verification
            provider: Provider type
    """
    authorization_url: str
    state: str
    provider: str

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> InitiateAuthResult:
        """Create InitiateAuthResult from API response data."""
        ...


@dataclass(frozen=True)
class CompleteAuthResult:
    """

        Result of completing OAuth flow.

        Attributes:
            connection: The created or updated connection
            is_new: Whether this is a new connection (vs reconnection)
    """
    connection: CloudStorageConnection
    is_new: bool

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> CompleteAuthResult:
        """Create CompleteAuthResult from API response data."""
        ...


@dataclass(frozen=True)
class ConnectionList:
    """

        List of cloud storage connections.

        Attributes:
            connections: List of connections
            total_count: Total number of connections
    """
    connections: list[CloudStorageConnection]
    total_count: int

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> ConnectionList:
        """Create ConnectionList from API response data."""
        ...


@dataclass(frozen=True)
class DisconnectResult:
    """

        Result of disconnecting a cloud storage account.

        Attributes:
            success: Whether the disconnection succeeded
            message: Confirmation message
    """
    success: bool
    message: str

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DisconnectResult:
        """Create DisconnectResult from API response data."""
        ...


@dataclass(frozen=True)
class CloudFileInput:
    """

        Input for a cloud file to import.

        Not a response type - used to construct import requests.

        Attributes:
            id: Cloud provider file ID
            name: File name
            mime_type: MIME type of the file
            size_bytes: File size in bytes
    """
    id: str
    name: str
    mime_type: Optional[str] = None
    size_bytes: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to API request dictionary."""
        ...


@dataclass(frozen=True)
class ImportResult:
    """

        Result of a cloud storage import request.

        Attributes:
            total_files: Number of files in the import
            is_async: Whether the import is running asynchronously
            message: Status message
            image_ids: List of image IDs (for synchronous imports)
            job_id: Job ID for tracking (for async imports)
            status: Job status (for async imports)
    """
    total_files: int
    is_async: bool
    message: str
    image_ids: Optional[list[str]] = None
    job_id: Optional[str] = None
    status: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> ImportResult:
        """Create ImportResult from API response data."""
        ...


@dataclass(frozen=True)
class ExportResult:
    """

        Result of a cloud storage export request.

        Attributes:
            is_async: Whether the export is running asynchronously
            message: Status message
            cloud_file_ids: List of cloud file IDs (for synchronous exports)
            job_id: Job ID for tracking (for async exports)
            job_status: Job status (for async exports)
    """
    is_async: bool
    message: str
    cloud_file_ids: Optional[list[str]] = None
    job_id: Optional[str] = None
    job_status: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> ExportResult:
        """Create ExportResult from API response data."""
        ...


@dataclass(frozen=True)
class CloudStorageJob:
    """

        Status of a cloud storage import/export job.

        Attributes:
            job_id: Unique job identifier
            type: Job type ('import' or 'export')
            status: Job status (pending, in_progress, completed, partial, failed, cancelled)
            connection_id: Associated connection ID
            provider: Cloud storage provider
            total_files: Total number of files in the job
            completed_files: Number of files completed
            failed_files: Number of files that failed
            error: Error message if job failed
            created_at: When the job was created
            updated_at: When the job was last updated
            completed_at: When the job completed
    """
    job_id: str
    type: str
    status: str
    connection_id: str
    provider: str
    total_files: int
    completed_files: int
    failed_files: int
    error: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    @property
    def is_terminal(self) -> bool:
        """Whether the job has reached a final state."""
        ...

    @property
    def is_successful(self) -> bool:
        """Whether the job completed successfully (fully or partially)."""
        ...

    @property
    def progress_percent(self) -> float:
        """Calculate job progress as a percentage (0-100)."""
        ...

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> CloudStorageJob:
        """Create CloudStorageJob from API response data."""
        ...
