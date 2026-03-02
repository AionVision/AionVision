from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class MemberRole(str, Enum):
    """Role of a tenant member."""
    OWNER = 'owner'
    ADMIN = 'admin'
    EDITOR = 'editor'
    VIEWER = 'viewer'


@dataclass(frozen=True)
class TenantSettings:
    """

        Tenant settings and information.

        Contains configuration, subscription, and usage information for a tenant.
    """
    id: str
    name: str
    owner_user_id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    webhook_url: Optional[str]
    allowed_vlm_providers: list[str]
    allowed_domains: list[str]
    max_monthly_credits: int
    max_requests_per_minute: int
    custom_config: dict[str, Any]
    subscription_tier: str
    subscription_expires_at: Optional[datetime]
    current_month_credits: int
    current_month_cost: float
    total_credits: int
    total_cost: float

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> TenantSettings:
        """Create TenantSettings from API response."""
        ...


@dataclass(frozen=True)
class TenantLimits:
    """

        Tenant limits and usage information.

        Provides current limits, usage, and remaining quota for various resources.
    """
    limits: dict[str, int]
    usage: dict[str, int]
    remaining: dict[str, int]

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> TenantLimits:
        """Create TenantLimits from API response."""
        ...

    def get_limit(self, name: str) -> Optional[int]:
        """Get a specific limit value."""
        ...

    def get_usage(self, name: str) -> Optional[int]:
        """Get current usage for a limit."""
        ...

    def get_remaining(self, name: str) -> Optional[int]:
        """Get remaining quota for a limit."""
        ...


@dataclass(frozen=True)
class TenantMember:
    """

        Tenant member information.

        Represents a user who belongs to a tenant organization.
    """
    id: str
    email: str
    name: str
    role: str
    joined_at: datetime
    last_active_at: Optional[datetime] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> TenantMember:
        """Create TenantMember from API response."""
        ...

    @property
    def role_enum(self) -> MemberRole:
        """Get role as MemberRole enum."""
        ...
