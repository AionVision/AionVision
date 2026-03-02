from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class AuditEventType(str, Enum):
    """Audit event types."""
    AUTH_LOGIN = 'auth.login'
    AUTH_LOGOUT = 'auth.logout'
    AUTH_LOGIN_FAILED = 'auth.login_failed'
    AUTH_TOKEN_REFRESH = 'auth.token_refresh'
    AUTH_EMAIL_VERIFIED = 'auth.email_verified'
    AUTH_PASSWORD_CHANGED = 'auth.password_changed'
    AUTH_OAUTH_LOGIN = 'auth.oauth_login'
    PERMISSION_DENIED = 'permission.denied'
    PERMISSION_GRANTED = 'permission.granted'
    ROLE_CHANGED = 'role.changed'
    API_KEY_CREATED = 'api_key.created'
    API_KEY_DELETED = 'api_key.deleted'
    API_KEY_USED = 'api_key.used'
    API_KEY_FAILED = 'api_key.failed'
    TENANT_CREATED = 'tenant.created'
    TENANT_UPDATED = 'tenant.updated'
    TENANT_MEMBER_ADDED = 'tenant.member_added'
    TENANT_MEMBER_REMOVED = 'tenant.member_removed'
    TENANT_MEMBER_ROLE_CHANGED = 'tenant.member_role_changed'
    RULE_SET_CREATED = 'rule_set.created'
    RULE_SET_UPDATED = 'rule_set.updated'
    RULE_SET_DELETED = 'rule_set.deleted'
    RULE_SET_SHARED = 'rule_set.shared'
    RULE_SET_SHARE_REVOKED = 'rule_set.share_revoked'
    SECURITY_RATE_LIMIT_EXCEEDED = 'security.rate_limit_exceeded'
    SECURITY_INVALID_TOKEN = 'security.invalid_token'
    SECURITY_SUSPICIOUS_ACTIVITY = 'security.suspicious_activity'


class AuditSeverity(str, Enum):
    """Audit log severity levels."""
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    CRITICAL = 'critical'


class AuditResult(str, Enum):
    """Audit log result values."""
    SUCCESS = 'success'
    FAILURE = 'failure'
    DENIED = 'denied'


@dataclass(frozen=True)
class AuditLogEntry:
    """

        A single audit log entry.

        Represents a security-relevant event that occurred in the system.
    """
    id: str
    event_type: str
    event_timestamp: Optional[datetime]
    severity: str
    action: str
    result: str
    user_id: Optional[str] = None
    api_key_id: Optional[str] = None
    ip_address: Optional[str] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> AuditLogEntry:
        """Create AuditLogEntry from API response."""
        ...

    @property
    def event_type_enum(self) -> Optional[AuditEventType]:
        """Get event type as enum, or None if not a known type."""
        ...

    @property
    def severity_enum(self) -> AuditSeverity:
        """Get severity as enum."""
        ...

    @property
    def result_enum(self) -> AuditResult:
        """Get result as enum."""
        ...


@dataclass(frozen=True)
class AuditLogList:
    """

        Paginated list of audit log entries.

        Contains entries along with pagination information.
    """
    entries: list[AuditLogEntry]
    total_count: int
    has_more: bool

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> AuditLogList:
        """Create AuditLogList from API response."""
        ...
