"""
Uploading Documents: Document upload and processing.

Demonstrates:
- Single document upload with automatic text extraction
- Batch document upload from directories
- Progress tracking for processing
- Checking document processing status
- Supported formats: PDF, DOCX, TXT, MD
"""

import asyncio

from aion import AionVision
from aion.types.callbacks import (
    DocumentProcessingProgressEvent,
    DocumentUploadProgressEvent,
)


async def upload_single_document():
    """Upload a single document and wait for processing."""

    async with AionVision.from_env() as client:

        # Upload a PDF - waits for text extraction by default
        result = await client.documents.upload_one("report.pdf")
        print(f"Document ID: {result.document_id}")
        print(f"Pages: {result.page_count}")
        print(f"Chunks: {result.chunk_count}")
        print(f"Status: {result.text_extraction_status}")


async def upload_multiple_documents():
    """Upload multiple documents from a directory."""

    def on_upload(event: DocumentUploadProgressEvent):
        print(f"Uploading: {event.filename}")

    def on_processing(event: DocumentProcessingProgressEvent):
        print(f"Processing: {event.completed_count}/{event.total_count}")

    async with AionVision.from_env() as client:

        # Upload all documents in a directory
        results = await client.documents.upload(
            "/path/to/documents",
            on_progress=on_upload,
            on_processing_progress=on_processing,
        )
        print(f"Uploaded: {results.succeeded_count} documents")
        print(f"Failed: {results.failed_count} documents")

        # Upload specific files
        results = await client.documents.upload([
            "report.pdf",
            "spreadsheet.xlsx",
            "presentation.pptx",
        ])


async def manage_documents():
    """List, search, and manage documents."""

    async with AionVision.from_env() as client:

        # List all documents
        doc_list = await client.documents.list()
        for doc in doc_list.documents:
            print(f"{doc.filename} ({doc.text_extraction_status})")

        # Get document details
        details = await client.documents.get("document-id")
        print(f"Title: {details.title}")
        print(f"Pages: {details.page_count}")

        # Get extracted text
        text = await client.documents.get_text("document-id")
        print(f"Text: {text[:200]}...")

        # Get document chunks (for RAG)
        chunks = await client.documents.get_chunks("document-id")
        for chunk in chunks.chunks:
            print(f"Chunk {chunk.chunk_index}: {chunk.content[:100]}...")

        # Search across all documents
        results = await client.documents.search("safety procedures")
        for result in results.results:
            print(f"{result.document_filename}: {result.content[:100]}...")

        # Delete a document
        await client.documents.delete("document-id")


if __name__ == "__main__":
    asyncio.run(upload_single_document())
