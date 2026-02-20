"""
Agentic Chat: Chat sessions, streaming, and follow-up conversations.

Demonstrates:
- Creating chat sessions with context manager
- Sending messages and getting responses
- Streaming responses token by token
- Follow-up conversations within a session
- Accessing referenced images in responses
"""

import asyncio

from aion import AionVision
from aion.types.common import ChatTokenType


async def basic_chat():
    """Basic chat with session management."""

    async with AionVision.from_env() as client:

        # Create a chat session (auto-managed)
        async with client.chat_session() as session:

            # Send a message and get a complete response
            response = await session.send("Find all damaged utility poles")
            print(f"Response: {response.content}")

            # Access referenced images
            if response.images:
                for img in response.images:
                    print(f"  Image: {img.image_id} - {(img.description or '')[:50]}...")

            # Follow-up in the same session (maintains context)
            followup = await session.send("Which ones look most severe?")
            print(f"Follow-up: {followup.content}")


async def streaming_chat():
    """Stream response tokens as they arrive."""

    async with AionVision.from_env() as client:

        async with client.chat_session() as session:

            # Stream tokens for real-time display
            async for token in session.send_stream("Describe my image collection"):
                if token.type == ChatTokenType.TOKEN:
                    print(token.content, end="", flush=True)
                elif token.type == ChatTokenType.COMPLETE:
                    print()  # Newline after streaming completes


async def chat_with_specific_images():
    """Chat about specific images."""

    async with AionVision.from_env() as client:

        # Create session with specific image context
        async with client.chat_session(
            title="Damage Assessment",
            image_ids=["image-id-1", "image-id-2"],
            use_all_images=False,
        ) as session:
            response = await session.send(
                "Compare these two images and describe the differences"
            )
            print(response.content)


async def manual_session_management():
    """Manual session management for more control."""

    async with AionVision.from_env() as client:

        # Create session manually
        session = await client.chats.create_session(title="Analysis")
        print(f"Session ID: {session.id}")

        # Send messages using the session ID
        response = await client.chat(
            "Find images with vegetation",
            session_id=session.id,
        )
        print(response.content)

        # List all sessions
        sessions = await client.chats.list_sessions()
        for s in sessions.items:
            print(f"  {s.id}: {s.title}")

        # Close session when done
        await client.chats.close_session(session.id)


async def force_detailed_analysis():
    """Force detailed analysis for complex queries."""

    async with AionVision.from_env() as client:

        async with client.chat_session() as session:
            # Force detailed analysis even for simple queries
            response = await session.send(
                "Show me infrastructure images",
                force_detailed_analysis=True,
            )
            print(response.content)


if __name__ == "__main__":
    asyncio.run(basic_chat())
