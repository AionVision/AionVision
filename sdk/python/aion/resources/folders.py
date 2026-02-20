from __future__ import annotations
from typing import Any, Optional
from ..config import ClientConfig
from ..exceptions import ValidationError
from ..types.folders import DeleteFolderResult, Folder, FolderBreadcrumbs, FolderContents, FolderTree, MoveFilesResult
MAX_FOLDER_NAME_LENGTH = 255
FORBIDDEN_NAME_CHARS = frozenset('/\\\x00')
VALID_DELETE_MODES = {'move_to_parent', 'delete_all'}
MAX_MOVE_FILES_BATCH = 100


class FoldersResource:
    """

        Folder operations for the Aionvision SDK.

        Provides methods to create and manage folders for organizing
        files into a hierarchical structure.
    """

    def __init__(self, http: HTTPClient, config: ClientConfig) -> None:
        """

                Initialize the folders resource.

                Args:
                    http: HTTP client for API communication
                    config: Client configuration
        """
        ...

    async def tree(self) -> FolderTree:
        """

                Get the complete folder tree.

                Returns:
                    FolderTree with all folders

                Example:
                    ```python
                    tree = await client.folders.tree()
                    for folder in tree.folders:
                        print(f"{'  ' * folder.depth}{folder.name}")
                    ```
        """
        ...

    async def get(self, folder_id: str, *, limit: int = 50, offset: int = 0) -> FolderContents:
        """

                Get folder contents including subfolders and file info.

                Args:
                    folder_id: Unique folder identifier
                    limit: Number of files to return (1-100, default 50)
                    offset: Pagination offset (>= 0)

                Returns:
                    FolderContents with folder metadata, breadcrumbs, subfolders, and file info

                Raises:
                    ValidationError: If parameters are invalid
                    ResourceNotFoundError: If folder does not exist

                Example:
                    ```python
                    contents = await client.folders.get(folder_id)
                    print(f"Folder: {contents.folder.name}")
                    for sub in contents.subfolders:
                        print(f"  Subfolder: {sub.name}")
                    ```
        """
        ...

    async def get_breadcrumbs(self, folder_id: str) -> FolderBreadcrumbs:
        """

                Get the breadcrumb path for a folder.

                Args:
                    folder_id: Unique folder identifier

                Returns:
                    FolderBreadcrumbs with path from root to this folder

                Raises:
                    ValidationError: If folder_id is empty
                    ResourceNotFoundError: If folder does not exist

                Example:
                    ```python
                    result = await client.folders.get_breadcrumbs(folder_id)
                    path = " > ".join(bc.name for bc in result.breadcrumbs)
                    print(f"Path: {path}")
                    ```
        """
        ...

    async def create(self, name: str, *, parent_id: Optional[str] = None) -> Folder:
        """

                Create a new folder.

                Args:
                    name: Folder name (1-255 characters, no /, \\, or null bytes)
                    parent_id: Parent folder ID (None for root-level)

                Returns:
                    Folder with the created folder details

                Raises:
                    ValidationError: If name is invalid or parent_id is empty string

                Example:
                    ```python
                    folder = await client.folders.create("Photos")
                    subfolder = await client.folders.create(
                        "Vacation", parent_id=folder.id
                    )
                    ```
        """
        ...

    async def rename(self, folder_id: str, name: str) -> Folder:
        """

                Rename a folder.

                Args:
                    folder_id: Unique folder identifier
                    name: New folder name (1-255 characters)

                Returns:
                    Folder with updated details

                Raises:
                    ValidationError: If folder_id is empty or name is invalid
                    ResourceNotFoundError: If folder does not exist

                Example:
                    ```python
                    updated = await client.folders.rename(folder_id, "New Name")
                    print(f"Renamed to: {updated.name}")
                    ```
        """
        ...

    async def move(self, folder_id: str, *, new_parent_id: Optional[str] = None) -> Folder:
        """

                Move a folder to a new parent.

                Args:
                    folder_id: Unique folder identifier
                    new_parent_id: New parent folder ID (None to move to root)

                Returns:
                    Folder with updated details

                Raises:
                    ValidationError: If folder_id is empty
                    ResourceNotFoundError: If folder does not exist

                Example:
                    ```python
                    moved = await client.folders.move(
                        folder_id, new_parent_id=target_folder_id
                    )
                    ```
        """
        ...

    async def delete(self, folder_id: str, *, mode: str = 'move_to_parent') -> DeleteFolderResult:
        """

                Delete a folder.

                Args:
                    folder_id: Unique folder identifier
                    mode: Deletion mode - 'move_to_parent' (default) moves contents
                          to parent folder, 'delete_all' deletes folder and all contents

                Returns:
                    DeleteFolderResult with deletion details

                Raises:
                    ValidationError: If folder_id is empty or mode is invalid
                    ResourceNotFoundError: If folder does not exist

                Example:
                    ```python
                    result = await client.folders.delete(folder_id)
                    print(f"Files affected: {result.files_affected}")

                    # Delete everything
                    result = await client.folders.delete(
                        folder_id, mode="delete_all"
                    )
                    ```
        """
        ...

    async def move_files(self, file_ids: list[str], *, folder_id: Optional[str] = None) -> MoveFilesResult:
        """

                Move files to a folder.

                Args:
                    file_ids: List of file IDs to move (1-100, no duplicates)
                    folder_id: Target folder ID (None to move to root)

                Returns:
                    MoveFilesResult with move operation details

                Raises:
                    ValidationError: If file_ids is invalid

                Example:
                    ```python
                    result = await client.folders.move_files(
                        ["file1", "file2"], folder_id=target_folder_id
                    )
                    print(f"Moved {result.moved}/{result.total_requested}")
                    ```
        """
        ...
