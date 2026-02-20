from __future__ import annotations
import logging
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any, Optional
logger = logging.getLogger(__name__)
from ..config import ClientConfig
from ..exceptions import ChatError
from ..types.chat import ChatImageList, ChatMessage, ChatResponse, ChatSession, ChatSessionDetail, ChatToken, ImageReference, PlanActionResponse, SessionList
from ..types.common import ChatTokenType


@dataclass
class ChatSessionConfig:
    """Configuration for a chat session context."""
    title: Optional[str] = None
    image_ids: Optional[list[str]] = None
    use_all_images: bool = True
    auto_close: bool = True


class ChatSessionContext:
    """

        Explicit session lifecycle management via context manager.

        Provides a clean, explicit way to manage chat sessions with
        proper resource cleanup.

        Usage:
            ```python
            async with client.chat_session() as session:
                response = await session.send("Find damaged poles")
                followup = await session.send("Tell me more")
            # Session automatically closed on exit
            ```

        Attributes:
            session_id: The underlying session ID
            session: The ChatSession object with session details
    """

    def __init__(self, chat: ChatResource, config: ChatSessionConfig) -> None:
        """

                Initialize the session context.

                Args:
                    chat: The ChatResource to use
                    config: Session configuration
        """
        ...

    @property
    def session_id(self) -> str:
        """Get the session ID."""
        ...

    @property
    def session(self) -> ChatSession:
        """Get the session object."""
        ...

    async def __aenter__(self) -> ChatSessionContext:
        """Create the session on context entry."""
        ...

    async def __aexit__(self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[Any]) -> None:
        """Close the session on context exit if auto_close is True."""
        ...

    async def send(self, message: str, *, force_detailed_analysis: bool = False) -> ChatResponse:
        """

                Send a message in this session and get a complete response.

                For streaming responses, use send_stream() instead.

                Args:
                    message: User message text
                    force_detailed_analysis: Force high-resolution VLM analysis

                Returns:
                    ChatResponse with text, images, metadata

                Example:
                    ```python
                    async with client.chat_session() as session:
                        response = await session.send("Find damaged poles")
                        print(response.content)
                    ```
        """
        ...

    async def send_stream(self, message: str, *, force_detailed_analysis: bool = False) -> AsyncIterator[ChatToken]:
        """

                Send a message and stream response tokens as they arrive.

                For complete responses, use send() instead.

                Args:
                    message: User message text
                    force_detailed_analysis: Force high-resolution VLM analysis

                Yields:
                    ChatToken objects with type, content, and data

                Example:
                    ```python
                    async with client.chat_session() as session:
                        async for token in session.send_stream("Find damaged poles"):
                            if token.type == ChatTokenType.TOKEN:
                                print(token.content, end="", flush=True)
                    ```
        """
        ...

    async def update_images(self, image_ids: list[str]) -> dict[str, Any]:
        """Update selected images for this session's context."""
        ...

    async def update_documents(self, document_ids: list[str]) -> dict[str, Any]:
        """Update selected documents for this session's context."""
        ...

    async def approve_plan(self, plan_id: str) -> PlanActionResponse:
        """Approve an execution plan in this session."""
        ...

    async def cancel_plan(self, plan_id: str) -> PlanActionResponse:
        """Cancel a pending execution plan in this session."""
        ...

    async def get_messages(self, *, limit: Optional[int] = None) -> list[ChatMessage]:
        """Get messages from this session."""
        ...


class ChatResource:
    """

        Chat operations for the Aionvision SDK.

        Provides methods for managing chat sessions and sending messages
        with optional streaming support.

        For the best experience, use the session() context manager:
            ```python
            async with client.chats.session() as session:
                response = await session.send("Find damaged poles")
                followup = await session.send("Tell me more")
            ```
    """

    def __init__(self, http: HTTPClient, config: ClientConfig) -> None:
        """

                Initialize the chat resource.

                Args:
                    http: HTTP client for API communication
                    config: Client configuration
        """
        ...

    def session(self, *, title: Optional[str] = None, image_ids: Optional[list[str]] = None, use_all_images: bool = True, auto_close: bool = True) -> ChatSessionContext:
        """

                Create a chat session context manager.

                This is the preferred way to use chat - sessions are explicitly
                managed and automatically cleaned up.

                Args:
                    title: Optional session title
                    image_ids: Initial image IDs for context
                    use_all_images: Use all user's images as context
                    auto_close: Automatically close session on exit (default: True)

                Returns:
                    ChatSessionContext for use with 'async with'

                Example:
                    ```python
                    async with client.chats.session() as session:
                        response = await session.send("Find damaged poles")
                        followup = await session.send("Tell me more")
                    # Session automatically closed

                    # Keep session open for later use
                    async with client.chats.session(auto_close=False) as session:
                        response = await session.send("Hello")
                        session_id = session.session_id  # Save for later
                    ```
        """
        ...

    async def send(self, message: str, *, session_id: str, force_detailed_analysis: bool = False) -> ChatResponse:
        """

                Send a message to the agentic chat system and get a complete response.

                Requires an explicit session_id. Use session() for automatic
                session management, or create_session() for manual control.

                For streaming responses, use send_stream() instead.

                Args:
                    message: User message text
                    session_id: Session identifier (required)
                    force_detailed_analysis: Force high-resolution VLM analysis

                Returns:
                    ChatResponse with text, images, metadata

                Example:
                    ```python
                    # Using session context (recommended)
                    async with client.chats.session() as session:
                        response = await session.send("Find damaged poles")
                        print(response.content)

                    # Using explicit session management
                    session = await client.chats.create_session()
                    response = await client.chats.send(
                        "Find damaged poles",
                        session_id=session.id
                    )
                    ```
        """
        ...

    async def send_stream(self, message: str, *, session_id: str, force_detailed_analysis: bool = False) -> AsyncIterator[ChatToken]:
        """

                Send a message and stream response tokens as they arrive.

                Requires an explicit session_id. Use session() for automatic
                session management, or create_session() for manual control.

                For complete responses, use send() instead.

                Args:
                    message: User message text
                    session_id: Session identifier (required)
                    force_detailed_analysis: Force high-resolution VLM analysis

                Yields:
                    ChatToken objects with type, content, and data

                Example:
                    ```python
                    async with client.chats.session() as session:
                        async for token in session.send_stream("Find damaged poles"):
                            if token.type == ChatTokenType.TOKEN:
                                print(token.content, end="", flush=True)
                            elif token.type == ChatTokenType.COMPLETE:
                                print(f"\nDone in {token.data.get('processing_time_ms')}ms")
                    ```
        """
        ...

    async def create_session(self, *, title: Optional[str] = None, image_ids: Optional[list[str]] = None, use_all_images: bool = True) -> ChatSession:
        """

                Create a new chat session.

                Args:
                    title: Optional session title
                    image_ids: Initial image IDs for context
                    use_all_images: Use all user's images as context

                Returns:
                    ChatSession with session details
        """
        ...

    async def get_session(self, session_id: str, *, include_messages: bool = True, message_limit: Optional[int] = None) -> ChatSessionDetail:
        """

                Get session details with message history.

                Args:
                    session_id: Session identifier
                    include_messages: Include message history
                    message_limit: Maximum messages to return (default: API uses 1000)

                Returns:
                    ChatSessionDetail with session and messages
        """
        ...

    async def list_sessions(self, *, limit: int = 20, offset: int = 0, active_only: bool = False) -> SessionList:
        """

                List user's chat sessions.

                Args:
                    limit: Maximum sessions to return
                    offset: Pagination offset
                    active_only: Only return active sessions

                Returns:
                    SessionList with sessions and pagination info
        """
        ...

    async def iter_sessions(self, *, page_size: int = 20, active_only: bool = False) -> AsyncIterator[ChatSession]:
        """

                Iterate through all chat sessions with automatic pagination.

                Args:
                    page_size: Number of sessions per page (default 20)
                    active_only: Only return active sessions

                Yields:
                    ChatSession objects one at a time

                Example:
                    ```python
                    async for session in client.chats.iter_sessions():
                        print(f"Session: {session.title}")
                    ```
        """
        ...

    async def get_messages(self, session_id: str, *, limit: Optional[int] = None) -> list[ChatMessage]:
        """

                Get messages from a chat session.

                Args:
                    session_id: Session identifier
                    limit: Maximum messages to return (default: all)

                Returns:
                    List of ChatMessage objects

                Example:
                    ```python
                    messages = await client.chats.get_messages("abc123...")
                    for msg in messages:
                        print(f"{msg.role}: {msg.content}")
                    ```
        """
        ...

    async def update_images(self, session_id: str, image_ids: list[str]) -> dict[str, Any]:
        """

                Update selected images for session context.

                Args:
                    session_id: Session identifier
                    image_ids: Image IDs to use as context

                Returns:
                    Update result
        """
        ...

    async def update_documents(self, session_id: str, document_ids: list[str]) -> dict[str, Any]:
        """

                Update selected documents for session context.

                Args:
                    session_id: Session identifier
                    document_ids: Document IDs to use as context

                Returns:
                    Update result
        """
        ...

    async def update_mode(self, session_id: str, use_all_images: bool) -> dict[str, Any]:
        """

                Switch between all images / selected images mode.

                Args:
                    session_id: Session identifier
                    use_all_images: Whether to use all images

                Returns:
                    Update result
        """
        ...

    async def approve_plan(self, session_id: str, plan_id: str) -> PlanActionResponse:
        """

                Approve an execution plan for a chat session.

                When a streaming response includes a plan_pending_approval event,
                use this method to approve the plan and start execution.

                Args:
                    session_id: Session identifier
                    plan_id: Plan identifier from the plan_pending_approval event

                Returns:
                    PlanActionResponse with execution results or accepted status

                Example:
                    ```python
                    async for token in client.chats.send_stream("Organize my images", session_id=sid):
                        if token.type == ChatTokenType.PLAN_PENDING_APPROVAL:
                            plan_id = token.data["plan_id"]
                            result = await client.chats.approve_plan(sid, plan_id)
                    ```
        """
        ...

    async def cancel_plan(self, session_id: str, plan_id: str) -> PlanActionResponse:
        """

                Cancel a pending execution plan.

                Args:
                    session_id: Session identifier
                    plan_id: Plan identifier from the plan_pending_approval event

                Returns:
                    PlanActionResponse confirming cancellation
        """
        ...

    async def close_session(self, session_id: str) -> dict[str, Any]:
        """

                Close a chat session.

                Args:
                    session_id: Session identifier

                Returns:
                    Close result
        """
        ...

    async def rename_session(self, session_id: str, title: str) -> dict[str, Any]:
        """

                Rename a chat session.

                Args:
                    session_id: Session identifier
                    title: New title for the session (max 255 characters)

                Returns:
                    Updated session info with new title

                Raises:
                    ValidationError: If title exceeds 255 characters

                Example:
                    ```python
                    result = await client.chats.rename_session(
                        session_id="abc123...",
                        title="Discussion about utility poles"
                    )
                    print(f"New title: {result.get('title')}")
                    ```
        """
        ...

    async def export_session(self, session_id: str, *, format: str = 'markdown', include_metadata: bool = False) -> bytes:
        """

                Export chat session in specified format.

                Args:
                    session_id: Session identifier
                    format: Export format - 'json', 'markdown', or 'text'
                    include_metadata: Include message metadata in export

                Returns:
                    Exported content as bytes

                Raises:
                    ValidationError: If format is invalid

                Example:
                    ```python
                    content = await client.chats.export_session(
                        session_id="abc123...",
                        format="markdown"
                    )
                    with open("chat_export.md", "wb") as f:
                        f.write(content)
                    ```
        """
        ...

    async def get_all_images(self, *, limit: int = 1000, offset: int = 0) -> ChatImageList:
        """

                Get all user images available for chat context.

                Args:
                    limit: Maximum images to return (default 1000)
                    offset: Pagination offset

                Returns:
                    ChatImageList with images and pagination info

                Example:
                    ```python
                    result = await client.chats.get_all_images(limit=100)
                    for image_id in result.image_ids:
                        print(f"Image ID: {image_id}")
                    ```
        """
        ...

    async def search_images(self, query: str, *, limit: int = 50, offset: int = 0) -> list[ImageReference]:
        """

                Search images using natural language.

                Args:
                    query: Search query
                    limit: Maximum results (default 50)
                    offset: Pagination offset

                Returns:
                    List of matching images
        """
        ...
