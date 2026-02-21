from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
from .common import ChatTokenType, MessageRole


@dataclass(frozen=True)
class ImageReference:
    """

        Reference to an image in chat context.

        Attributes:
            image_id: Unique image identifier
            filename: Original filename
            thumbnail_url: URL to thumbnail
            description: Image description
            confidence: Description confidence score
            title: Image title
            stored_url: URL to full image
    """
    image_id: str
    filename: str
    thumbnail_url: Optional[str] = None
    description: Optional[str] = None
    confidence: Optional[float] = None
    title: Optional[str] = None
    stored_url: Optional[str] = None

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> ImageReference:
        """Create ImageReference from API response data."""
        ...


@dataclass(frozen=True)
class ChatMessage:
    """

        A message in a chat session.

        Attributes:
            id: Message identifier
            role: Message role (user, assistant, system)
            content: Message text content
            created_at: When the message was created
            token_count: Number of tokens in message
            image_context: Images referenced in message
            metadata: Additional message metadata
    """
    id: str
    role: MessageRole
    content: str
    created_at: Optional[datetime] = None
    token_count: int = 0
    image_context: Optional[list[ImageReference]] = None
    metadata: Optional[dict[str, Any]] = None

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> ChatMessage:
        """Create ChatMessage from API response data."""
        ...

    @property
    def resolved_content(self) -> str:
        """Content with all ``[[…]]`` markup replaced by plain text."""
        ...

    @property
    def references(self) -> Any:
        """
        Parsed references from the message content.

                Returns a :class:`~aion.types.references.ParsedReferences` instance.
        """
        ...

    @property
    def result_refs(self) -> dict[str, Any]:
        """Shortcut to ``result_refs`` from metadata, parsed as ``ResultRefData``."""
        ...

    def as_collection(self) -> 'FileCollection':
        """
        Build a :class:`FileCollection` from ``image_context``.

                Returns an empty collection when no images are present.
        """
        ...


@dataclass(frozen=True)
class ChatResponse:
    """

        Response from a chat message.

        Attributes:
            message_id: Unique message identifier
            session_id: Session this message belongs to
            content: Response text content
            token_count: Tokens used in response
            processing_time_ms: Time to generate response
            images: Images found or referenced
            metadata: Additional response metadata
    """
    message_id: str
    session_id: str
    content: str
    token_count: int = 0
    processing_time_ms: int = 0
    images: Optional[list[ImageReference]] = None
    metadata: Optional[dict[str, Any]] = None

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...

    @classmethod
    def from_api_response(cls, data: dict[str, Any], session_id: str = '') -> ChatResponse:
        """Create ChatResponse from API response data."""
        ...

    @property
    def resolved_content(self) -> str:
        """Content with all ``[[…]]`` markup replaced by plain text."""
        ...

    @property
    def references(self) -> Any:
        """
        Parsed references from the response content.

                Returns a :class:`~aion.types.references.ParsedReferences` instance.
        """
        ...

    @property
    def result_refs(self) -> dict[str, Any]:
        """Shortcut to ``result_refs`` from metadata, parsed as ``ResultRefData``."""
        ...

    def as_collection(self) -> 'FileCollection':
        """
        Build a :class:`FileCollection` from ``images``.

                Returns an empty collection when no images are present.
        """
        ...


@dataclass(frozen=True)
class ChatToken:
    """

        A single token or event in a streaming chat response.

        Attributes:
            type: Event type (token, status, image_results, complete, error, etc.)
            content: Text content (for token events)
            data: Full event data
    """
    type: ChatTokenType
    content: Optional[str] = None
    data: Optional[dict[str, Any]] = None

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...

    @classmethod
    def from_sse_event(cls, event_type: str, event_data: dict[str, Any]) -> ChatToken:
        """Create ChatToken from SSE event."""
        ...

    @property
    def resolved_content(self) -> Optional[str]:
        """
        Content with markup replaced (only for COMPLETE tokens).

                Returns *None* for non-complete tokens.
        """
        ...

    @property
    def references(self) -> Any:
        """
        Parsed references (only for COMPLETE tokens).

                Returns a :class:`~aion.types.references.ParsedReferences` instance,
                or *None* for non-complete tokens.
        """
        ...

    @property
    def result_refs(self) -> Optional[dict[str, Any]]:
        """Shortcut to ``result_refs`` (only for COMPLETE tokens)."""
        ...


@dataclass(frozen=True)
class ChatSession:
    """

        Basic chat session information.

        Attributes:
            id: Session identifier
            title: Session title
            total_messages: Number of messages in session
            total_tokens: Total tokens used
            remaining_tokens: Tokens remaining in quota
            remaining_messages: Messages remaining in quota
            is_active: Whether session is active
            use_all_images: Whether using all images as context
            selected_image_count: Number of selected images
            created_at: When session was created
            updated_at: When session was last updated
            last_message_at: When last message was sent
            last_message_preview: Preview of the last message
            last_user_message: Last message from the user
    """
    id: str
    title: str
    total_messages: int = 0
    total_tokens: int = 0
    remaining_tokens: int = 0
    remaining_messages: int = 0
    is_active: bool = True
    use_all_images: bool = True
    selected_image_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_message_at: Optional[datetime] = None
    last_message_preview: Optional[str] = None
    last_user_message: Optional[str] = None

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> ChatSession:
        """Create ChatSession from API response data."""
        ...


@dataclass(frozen=True)
class ChatSessionDetail:
    """

        Detailed chat session information including messages.

        Attributes:
            session: Basic session information
            messages: List of messages in the session
            selected_image_ids: IDs of selected images for context
            current_search_result_ids: IDs from last search
    """
    session: ChatSession
    messages: list[ChatMessage]
    selected_image_ids: Optional[list[str]] = None
    current_search_result_ids: Optional[list[str]] = None

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> ChatSessionDetail:
        """Create ChatSessionDetail from API response data."""
        ...

    def as_collection(self) -> 'FileCollection':
        """
        Build a :class:`FileCollection` from search result IDs or selected images.

                Uses ``current_search_result_ids`` if available, otherwise falls back
                to ``selected_image_ids``. Returns an empty collection when neither
                is present.
        """
        ...


@dataclass(frozen=True)
class SessionList:
    """

        List of chat sessions.

        Attributes:
            items: List of sessions
            total: Total number of sessions
            has_more: Whether there are more sessions
    """
    items: list[ChatSession]
    total: int = 0
    has_more: bool = False

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> SessionList:
        """Create SessionList from API response data."""
        ...


@dataclass(frozen=True)
class PlanActionResponse:
    """

        Response from approving or cancelling an execution plan.

        Attributes:
            success: Whether the action was successful
            plan_id: The plan identifier
            message: Human-readable result message
            action_taken: The action that was taken ("approve" or "cancel")
            results: Execution results (present for fast-path completions)
            agent_results: Detailed results from each agent execution
            pending_actions: Actions requiring further user confirmation
            status: Async status ("accepted" for 202 responses)
    """
    success: bool
    plan_id: str
    message: str
    action_taken: str
    results: Optional[dict[str, Any]] = None
    agent_results: Optional[list[dict[str, Any]]] = None
    pending_actions: Optional[list[dict[str, Any]]] = None
    status: Optional[str] = None

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> PlanActionResponse:
        """Create PlanActionResponse from API response data."""
        ...


@dataclass(frozen=True)
class ChatImageList:
    """

        Paginated list of image IDs available for chat context.

        Attributes:
            image_ids: List of image ID strings
            total_count: Total number of images available
            has_more: Whether there are more images beyond this page
    """
    image_ids: list[str]
    total_count: int
    has_more: bool

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        ...

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> ChatImageList:
        """Create ChatImageList from API response data."""
        ...

    def as_collection(self) -> 'FileCollection':
        """Build a :class:`FileCollection` from ``image_ids``."""
        ...
