"""
Document Management: Full document lifecycle.

Demonstrates:
- Listing and searching documents
- Getting document details and text
- Getting document chunks for RAG
- Downloading documents
- Deleting documents
"""

import asyncio

from aion import AionVision


async def list_documents():
    """List and search documents."""

    async with AionVision.from_env() as client:

        # List documents with pagination
        doc_list = await client.documents.list(page=1, page_size=20)
        print(f"Total documents: {doc_list.total_count}")
        for doc in doc_list.documents:
            print(f"  {doc.id}: {doc.filename} ({doc.text_extraction_status})")

        # Iterate through all documents
        async for doc in client.documents.list_all():
            print(f"  {doc.filename}")


async def document_details():
    """Get detailed document information."""

    async with AionVision.from_env() as client:

        # Get document metadata
        doc = await client.documents.get("document-id")
        print(f"Title: {doc.title}")
        print(f"Filename: {doc.filename}")
        print(f"Pages: {doc.page_count}")
        print(f"Chunks: {doc.chunk_count}")
        print(f"Status: {doc.text_extraction_status}")

        # Get full extracted text
        text = await client.documents.get_text("document-id")
        print(f"Text length: {len(text)} chars")

        # Get chunks (useful for RAG pipelines)
        chunks_response = await client.documents.get_chunks("document-id")
        for chunk in chunks_response.chunks:
            print(f"  Chunk {chunk.chunk_index}: {chunk.content[:80]}...")

        # Get download URL
        download_url = await client.documents.download("document-id")
        print(f"Download: {download_url}")


async def search_documents():
    """Search across all documents."""

    async with AionVision.from_env() as client:

        results = await client.documents.search(
            query="safety inspection procedures",
            limit=10,
        )
        print(f"Found {results.total_count} results")
        for result in results.results:
            print(f"  {result.document_filename}")
            print(f"    Score: {result.score:.3f}")
            print(f"    Content: {result.content[:100]}...")


if __name__ == "__main__":
    asyncio.run(list_documents())
