"""
Folder Management: Create, organize, and manage folders.

Demonstrates:
- Creating folders and subfolders
- Listing folder contents
- Moving files between folders
- Folder tree navigation
- Deleting folders
"""

import asyncio

from aion import AionVision


async def manage_folders():
    """Create and manage folders."""

    async with AionVision.from_env() as client:

        # Create a folder
        folder = await client.folders.create("Infrastructure Photos")
        print(f"Created folder: {folder.id} - {folder.name}")

        # Create a subfolder
        subfolder = await client.folders.create(
            "Damaged Poles",
            parent_id=folder.id,
        )

        # Get folder contents
        contents = await client.folders.get(folder.id)
        print(f"Files: {contents.total_files}")
        print(f"Subfolders: {len(contents.subfolders)}")

        # Get folder tree (hierarchical view)
        tree = await client.folders.tree()
        for node in tree.folders:
            print(f"{'  ' * node.depth}{node.name}")

        # Get breadcrumb path
        breadcrumbs = await client.folders.get_breadcrumbs(subfolder.id)
        path = " > ".join(b.name for b in breadcrumbs.breadcrumbs)
        print(f"Path: {path}")

        # Move files to a folder
        result = await client.folders.move_files(
            file_ids=["image-id-1", "image-id-2"],
            folder_id=subfolder.id,
        )
        print(f"Moved {result.moved} files")

        # Rename a folder
        await client.folders.rename(folder.id, "Site Photos")

        # Delete a folder
        result = await client.folders.delete(subfolder.id)
        print(f"Files affected: {result.files_affected}")


if __name__ == "__main__":
    asyncio.run(manage_folders())
