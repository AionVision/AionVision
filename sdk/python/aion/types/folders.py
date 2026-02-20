from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional


@dataclass(frozen=True)
class Folder:
    """

        A folder in the user's file hierarchy.

        Attributes:
            id: Unique folder identifier
            name: Folder name
            parent_id: Parent folder ID (None for root-level folders)
            depth: Nesting depth (0 for root-level)
            file_count: Number of files directly in this folder
            subfolder_count: Number of direct subfolders
            created_at: Creation timestamp
            updated_at: Last update timestamp
    """
    id: str
    name: str
    depth: int = 0
    parent_id: Optional[str] = None
    file_count: int = 0
    subfolder_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> Folder:
        """Create Folder from API response data."""
        ...


@dataclass(frozen=True)
class FolderBreadcrumb:
    """

        A breadcrumb entry in a folder's path.

        Attributes:
            id: Folder identifier
            name: Folder name
            depth: Nesting depth
    """
    id: str
    name: str
    depth: int = 0

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> FolderBreadcrumb:
        """Create FolderBreadcrumb from API response data."""
        ...


@dataclass(frozen=True)
class FolderTree:
    """

        Complete folder tree for the user.

        Attributes:
            folders: List of all folders
    """
    folders: list[Folder]

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> FolderTree:
        """Create FolderTree from API response data."""
        ...


@dataclass(frozen=True)
class FolderContents:
    """

        Contents of a folder including metadata and children.

        Attributes:
            folder: The folder itself (None if root)
            breadcrumbs: Path from root to this folder
            subfolders: Direct child folders
            total_files: Total number of files in this folder
            has_more_files: Whether more files exist beyond current page
    """
    breadcrumbs: list[FolderBreadcrumb]
    subfolders: list[Folder]
    total_files: int = 0
    has_more_files: bool = False
    folder: Optional[Folder] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> FolderContents:
        """Create FolderContents from API response data."""
        ...


@dataclass(frozen=True)
class FolderBreadcrumbs:
    """

        Breadcrumb path for a folder.

        Attributes:
            breadcrumbs: List of breadcrumb entries from root to folder
    """
    breadcrumbs: list[FolderBreadcrumb]

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> FolderBreadcrumbs:
        """Create FolderBreadcrumbs from API response data."""
        ...


@dataclass(frozen=True)
class DeleteFolderResult:
    """

        Result of folder deletion.

        Attributes:
            id: Deleted folder identifier
            files_affected: Number of files affected
            subfolders_affected: Number of subfolders affected
            mode: Deletion mode used ('move_to_parent' or 'delete_all')
    """
    id: str
    mode: str
    files_affected: int = 0
    subfolders_affected: int = 0

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DeleteFolderResult:
        """Create DeleteFolderResult from API response data."""
        ...


@dataclass(frozen=True)
class MoveFilesResult:
    """

        Result of moving files to a folder.

        Attributes:
            moved: Number of files successfully moved
            total_requested: Total number of files requested to move
    """
    moved: int
    total_requested: int

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> MoveFilesResult:
        """Create MoveFilesResult from API response data."""
        ...
