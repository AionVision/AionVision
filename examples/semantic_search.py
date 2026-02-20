"""
Semantic Search: Image and document search using AI agents.

Demonstrates:
- Image search with natural language queries
- Document search across uploaded documents
- Accessing search results and metadata
"""

import asyncio

from aion import AionVision


async def search_images():
    """Search images using natural language."""

    async with AionVision.from_env() as client:

        # Search for images matching a description
        result = await client.agent_search.images("damaged utility poles")
        print(f"Found {result.count} images")
        print(f"Summary: {result.summary}")

        for item in result.results:
            print(f"  Image: {item.image_id}")
            print(f"  Score: {item.score}")
            print(f"  Description: {item.description[:80]}...")
            print()


async def search_documents():
    """Search across uploaded documents."""

    async with AionVision.from_env() as client:

        # Search document content
        result = await client.agent_search.documents("safety procedures")
        print(f"Found {result.count} relevant chunks")
        print(f"Summary: {result.summary}")

        for chunk in result.results:
            print(f"  Document: {chunk.document_filename}")
            print(f"  Content: {chunk.text[:100]}...")
            print()

        # Search with document type filter
        result = await client.agent_search.documents(
            "budget allocations",
            document_types=["pdf", "xlsx"],
        )


async def search_via_chat():
    """Use chat for more conversational search."""

    async with AionVision.from_env() as client:

        async with client.chat_session() as session:
            # The chat system uses search agents behind the scenes
            response = await session.send("Find all images of damaged poles")
            print(response.content)

            # Referenced images are included in the response
            if response.images:
                print(f"\nReferenced {len(response.images)} images:")
                for img in response.images:
                    print(f"  {img.image_id}: {(img.description or '')[:50]}...")


if __name__ == "__main__":
    asyncio.run(search_images())
