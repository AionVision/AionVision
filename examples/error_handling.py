"""
Error Handling: Exception handling patterns for the SDK.

Demonstrates:
- Catching specific exception types
- Handling rate limits with retry-after
- Authentication errors
- Quota exceeded with partial results
- Upload failures with session recovery
- Timeout handling
"""

import asyncio

from aion import AionVision
from aion.exceptions import (
    AionvisionConnectionError,
    AionvisionError,
    AionvisionTimeoutError,
    AuthenticationError,
    ChatError,
    DescriptionError,
    QuotaExceededError,
    RateLimitError,
    ResourceNotFoundError,
    UploadError,
    ValidationError,
)


async def basic_error_handling():
    """Basic error handling pattern."""

    try:
        async with AionVision(api_key="aion_your_key") as client:
            result = await client.upload_one("photo.jpg")
            print(result.description)

    except AuthenticationError:
        print("Invalid API key. Check your AIONVISION_API_KEY.")

    except ValidationError as e:
        print(f"Validation error: {e.message}")
        print(f"Details: {e.details}")

    except QuotaExceededError as e:
        print(f"Quota exceeded: {e.message}")
        print(f"Details: available={e.details.get('available')}, limit={e.details.get('limit')}")

    except RateLimitError as e:
        print(f"Rate limited. Retry after {e.retry_after}s")
        print(f"Limit: {e.limit}, Remaining: {e.remaining}")

    except AionvisionError as e:
        # Catch-all for any SDK error
        print(f"Error [{e.code}]: {e.message}")


async def upload_error_handling():
    """Handle upload-specific errors."""

    async with AionVision.from_env() as client:
        try:
            results = await client.upload("/path/to/photos")

        except UploadError as e:
            print(f"Upload failed: {e.message}")
            print(f"Stage: {e.details.get('stage')}")

            # If upload had partial results, access them
            if e.partial_results:
                print(f"Partial results: {len(e.partial_results)} succeeded")
                for r in e.partial_results:
                    print(f"  {r.filename}: {r.image_id}")

            # Session ID can be used for manual recovery
            if e.session_id:
                print(f"Session ID for recovery: {e.session_id}")

        except DescriptionError as e:
            print(f"Description failed: {e.message}")
            print(f"Image ID: {e.details.get('image_id')}")

        except QuotaExceededError as e:
            print(f"Quota exceeded: {e.message}")
            # Partial results from completed chunks
            if e.partial_results:
                print(f"Got {len(e.partial_results)} results before quota limit")


async def chat_error_handling():
    """Handle chat-specific errors."""

    async with AionVision.from_env() as client:
        try:
            async with client.chat_session() as session:
                response = await session.send("Find damaged poles")
                print(response.content)

        except ChatError as e:
            print(f"Chat error: {e.message}")
            print(f"Session: {e.details.get('session_id')}")

        except ResourceNotFoundError as e:
            print(f"Not found: {e.message}")


async def timeout_handling():
    """Handle timeout errors."""

    async with AionVision.from_env() as client:
        try:
            result = await client.upload_one(
                "large_image.jpg",
                description_timeout=30.0,  # Custom timeout
            )
        except AionvisionTimeoutError as e:
            print(f"Timed out: {e.message}")
            # Access the last result received before timeout
            if e.last_result:
                print(f"Last status: {e.last_result}")


async def connection_error_handling():
    """Handle network connection errors."""

    try:
        async with AionVision(api_key="aion_your_key") as client:
            result = await client.upload_one("photo.jpg")

    except AionvisionConnectionError:
        print("Cannot connect to API. Check your network.")


async def using_class_exceptions():
    """Use exception classes from the client class directly."""

    async with AionVision.from_env() as client:
        try:
            result = await client.upload_one("photo.jpg")
        except AionVision.AuthenticationError:
            print("Auth failed")
        except AionVision.RateLimitError as e:
            print(f"Rate limited, retry after {e.retry_after}s")
        except AionVision.AionvisionError as e:
            print(f"Error: {e.message}")


if __name__ == "__main__":
    asyncio.run(basic_error_handling())
