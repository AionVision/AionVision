"""
Sync Client: Synchronous wrapper for non-async environments.

Demonstrates:
- Using SyncAionVision for Django, Flask, CLI tools, data pipelines
- All major operations in sync mode
- Important: sync client is NOT thread-safe

Note: Streaming chat is NOT available in sync mode.
Use the async AionVision client for streaming capabilities.
"""

from aion import SyncAionVision


def upload_example():
    """Upload images using sync client."""

    with SyncAionVision(api_key="aion_your_api_key") as client:

        # Single upload
        result = client.upload_one("photo.jpg")
        print(f"Image ID: {result.image_id}")
        print(f"Description: {result.description}")

        # Batch upload
        results = client.upload("/path/to/photos")
        for r in results:
            print(f"  {r.filename}: {r.description[:50]}...")


def chat_example():
    """Chat using sync client."""

    with SyncAionVision(api_key="aion_your_api_key") as client:

        with client.chat_session() as session:
            response = session.send("Find damaged poles")
            print(response.content)

            followup = session.send("Tell me more about the worst ones")
            print(followup.content)


def file_management_example():
    """File management using sync client."""

    with SyncAionVision(api_key="aion_your_api_key") as client:

        # List files
        file_list = client.files.list(search="infrastructure")
        for f in file_list.files:
            print(f"  {f.id}: {f.title}")

        # Get file details
        details = client.files.get(file_id="image-uuid")
        print(f"Description: {details.upload_description}")
        for desc in details.full_descriptions or []:
            print(f"Full description: {desc.description}")


def document_example():
    """Document operations using sync client."""

    with SyncAionVision(api_key="aion_your_api_key") as client:

        # Upload a document
        result = client.documents.upload_one("report.pdf")
        print(f"Document: {result.document_id}")

        # Search documents
        results = client.documents.search("safety procedures")
        for r in results.results:
            print(f"  {r.document_filename}: {r.content[:80]}...")


def from_env_example():
    """Create sync client from environment variables."""

    with SyncAionVision.from_env() as client:
        result = client.upload_one("photo.jpg")
        print(result.description)


if __name__ == "__main__":
    upload_example()
