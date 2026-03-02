"""
Link Management: Create, manage, and crawl bookmarked links.

Demonstrates:
- Creating links with automatic metadata crawling
- Listing and filtering links
- Updating link metadata
- Recrawling links for fresh metadata
- Deleting links
"""

import asyncio

from aion import AionVision


async def create_links():
    """Create links and wait for metadata crawl."""

    async with AionVision.from_env() as client:

        # Create a link and wait for OG metadata crawl
        link = await client.links.create_and_wait(
            url="https://example.com/article",
            tags=["research", "infrastructure"],
        )
        print(f"Link ID: {link.id}")
        print(f"Title: {link.og_metadata.title}")
        print(f"Description: {link.og_metadata.description}")
        print(f"Domain: {link.domain}")

        # Create without waiting
        result = await client.links.create(
            url="https://example.com/another",
            title="Custom Title",
        )
        print(f"Created: {result.id}")
        print(f"Crawl status: {result.crawl_status}")


async def manage_links():
    """List, update, and delete links."""

    async with AionVision.from_env() as client:

        # List all links with pagination
        link_list = await client.links.list(limit=20, offset=0)
        for link in link_list.links:
            print(f"  {link.id}: {link.title} ({link.domain})")

        # Iterate through all links
        async for link in client.links.list_all():
            print(f"  {link.url}")

        # Get link details
        details = await client.links.get("link-id")
        print(f"URL: {details.url}")
        print(f"Tags: {details.tags}")

        # Update link metadata
        await client.links.update(
            "link-id",
            title="Updated Title",
            tags=["updated", "tag"],
        )

        # Recrawl to refresh metadata
        result = await client.links.recrawl("link-id")
        print(f"Recrawl status: {result.status}")

        # Delete a link
        await client.links.delete("link-id")

        # Batch delete
        await client.links.batch_delete(["link-1", "link-2"])


if __name__ == "__main__":
    asyncio.run(create_links())
