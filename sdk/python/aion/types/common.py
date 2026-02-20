from __future__ import annotations
from enum import Enum
from typing import Literal


class VerificationLevel(str, Enum):
    """Verification level for AI operations."""
    QUICK = 'quick'
    STANDARD = 'standard'
    THOROUGH = 'thorough'
    CRITICAL = 'critical'


class DescriptionStatus(str, Enum):
    """Status of description generation for an image."""
    PENDING = 'pending'
    QUEUED = 'queued'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'
    SKIPPED = 'skipped'


class ChatTokenType(str, Enum):
    """Type of chat streaming token/event."""
    TOKEN = 'token'
    STATUS = 'status'
    IMAGE_RESULTS = 'image_results'
    COMPLETE = 'complete'
    ERROR = 'error'
    RECONNECTING = 'reconnecting'
    PLAN_PENDING_APPROVAL = 'plan_pending_approval'
    THINKING = 'thinking'
    THINKING_STEP = 'thinking_step'
    TOOL_INVOCATION = 'tool_invocation'
    TOOL_RESULT = 'tool_result'
    CONNECTION = 'connection'
    PING = 'ping'
    CLOSE = 'close'
    AUTH_ERROR = 'auth_error'


class StorageTarget(str, Enum):
    """Target storage location for uploads."""
    DEFAULT = 'default'
    CUSTOM = 'custom'


class MessageRole(str, Enum):
    """Role of a message in a chat conversation."""
    USER = 'user'
    ASSISTANT = 'assistant'
    SYSTEM = 'system'


class CloudStorageProvider(str, Enum):
    """Cloud storage provider type."""
    GOOGLE_DRIVE = 'google_drive'


class CloudStorageJobStatus(str, Enum):
    """Status of a cloud storage import/export job."""
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    PARTIAL = 'partial'
    FAILED = 'failed'
    CANCELLED = 'cancelled'


class CloudStorageJobType(str, Enum):
    """Type of cloud storage job."""
    IMPORT = 'import'
    EXPORT = 'export'
VerificationLevelLiteral = Literal['quick', 'standard', 'thorough', 'critical']
