"""
Quickstart: Authentication and first API calls.

Demonstrates:
- Creating an async client (AionVision)
- Creating a sync client (SyncAionVision)
- Using environment variables for configuration
- Uploading an image and reading the AI description
- Starting a chat session
"""

import asyncio

from aion import AionVision, SyncAionVision


# === Async Client ===

async def async_quickstart():
    """Async client usage (recommended for production)."""

    # Initialize with explicit API key
    async with AionVision(api_key="aion_your_api_key_here") as client:

        # Upload a single image - returns UploadResult with AI description
        result = await client.upload_one("photo.jpg")
        print(f"Image ID: {result.image_id}")
        print(f"Description: {result.description}")
        print(f"Tags: {result.tags}")

        # Chat with your image library
        async with client.chat_session() as session:
            response = await session.send("What images do I have?")
            print(response.content)


# === Sync Client ===

def sync_quickstart():
    """Sync client usage (for Django, Flask, CLI tools, data pipelines)."""

    with SyncAionVision(api_key="aion_your_api_key_here") as client:

        # Same API, no await needed
        result = client.upload_one("photo.jpg")
        print(f"Image ID: {result.image_id}")
        print(f"Description: {result.description}")

        with client.chat_session() as session:
            response = session.send("Describe my images")
            print(response.content)


# === Using Environment Variables ===

async def env_quickstart():
    """Create client from environment variables."""

    # Reads AIONVISION_API_KEY from environment
    async with AionVision.from_env() as client:
        result = await client.upload_one("photo.jpg")
        print(result.description)

    # Or load from .env file first
    from aion import load_dotenv

    load_dotenv()  # Loads .env file
    async with AionVision.from_env() as client:
        result = await client.upload_one("photo.jpg")
        print(result.description)


if __name__ == "__main__":
    asyncio.run(async_quickstart())
