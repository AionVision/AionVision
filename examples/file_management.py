"""
File Management: List, search, filter, update, and delete files.

Demonstrates:
- Listing files with pagination
- Searching files by description content
- Getting detailed file information
- Updating file metadata (title, tags)
- Deleting files (single and batch)
"""

import asyncio

from aion import AionVision


async def list_files():
    """List files with search, filtering, and pagination."""

    async with AionVision.from_env() as client:

        # List all files (paginated)
        file_list = await client.files.list()
        print(f"Total files: {file_list.total_count}")
        for f in file_list.files:
            print(f"  {f.id}: {f.title or f.filename}")

        # Search by description content
        file_list = await client.files.list(search="damaged pole")
        print(f"Found {file_list.total_count} files matching 'damaged pole'")

        # Paginate through results
        file_list = await client.files.list(
            limit=20,
            offset=0,
            sort_by="created_at",
            sort_order="desc",
        )


async def get_file_details():
    """Get detailed information about a file."""

    async with AionVision.from_env() as client:

        details = await client.files.get(file_id="image-uuid")
        print(f"ID: {details.id}")
        print(f"Filename: {details.original_filename}")
        print(f"Title: {details.title}")
        print(f"Tags: {details.tags}")
        print(f"Description: {details.upload_description}")
        print(f"Created: {details.created_at}")

        # Access full AI descriptions (list of FullDescription objects)
        for desc in details.full_descriptions or []:
            print(f"Full description: {desc.description}")


async def update_files():
    """Update file metadata."""

    async with AionVision.from_env() as client:

        # Update title
        result = await client.files.update(
            file_id="image-uuid",
            title="Damaged utility pole #42",
        )
        print(f"Updated: {result.id} at {result.updated_at}")

        # Update tags
        result = await client.files.update(
            file_id="image-uuid",
            tags=["infrastructure", "damage", "priority-high"],
        )


async def delete_files():
    """Delete files individually or in batch."""

    async with AionVision.from_env() as client:

        # Delete a single file (soft delete)
        result = await client.files.delete(file_id="image-uuid")
        print(f"Deleted: {result.message}")

        # Batch delete multiple files
        result = await client.files.batch_delete(
            file_ids=["id-1", "id-2", "id-3"]
        )
        print(f"Deleted: {result.summary['deleted']}/{result.summary['total']}")


if __name__ == "__main__":
    asyncio.run(list_files())
