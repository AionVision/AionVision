"""Shared file utilities for resource modules."""

from __future__ import annotations

from pathlib import Path
from typing import Union

from ..exceptions import UploadError


def is_in_hidden_directory(file_path: Path, base_path: Path) -> bool:
    """
    Check if a file is inside a hidden directory.

    Args:
        file_path: The file path to check
        base_path: The base directory being scanned

    Returns:
        True if any parent directory (relative to base) starts with '.'
    """
    ...


def expand_paths(
    paths: list[Union[str, Path, bytes]],
    supported_extensions: set[str],
    *,
    recursive: bool = True,
    include_hidden: bool = False,
) -> list[Union[str, Path, bytes]]:
    """
    Expand directory paths to individual file paths.

    Directories are expanded to include all files with supported extensions.
    Regular files and bytes are passed through unchanged.

    Args:
        paths: List of file paths, directory paths, or bytes
        supported_extensions: Set of allowed file extensions (e.g. {'.jpg', '.png'})
        recursive: Search directories recursively (default: True)
        include_hidden: Include hidden files and files in hidden directories (default: False)

    Returns:
        Flat list of file paths (directories expanded to their contents)

    Raises:
        UploadError: If permission is denied when reading a directory
    """
    ...
