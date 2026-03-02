from __future__ import annotations
from typing import Any, Optional
from ..config import ClientConfig
from ..types.tenant import TenantLimits, TenantMember, TenantSettings


class TenantResource:
    """

        Tenant management operations for the Aionvision SDK.

        Provides methods to manage tenant settings, limits, and members.
        These wrap the existing /tenant/* API endpoints.

        Note: Most member management operations require OWNER role.
    """

    def __init__(self, http: HTTPClient, config: ClientConfig) -> None:
        """

                Initialize the tenant resource.

                Args:
                    http: HTTP client for API communication
                    config: Client configuration
        """
        ...

    async def get_settings(self) -> TenantSettings:
        """

                Get current tenant settings.

                Returns configuration, subscription, and usage information.
                Requires VIEW permission on the tenant.

                Returns:
                    TenantSettings with current configuration

                Example:
                    ```python
                    settings = await client.tenant.get_settings()
                    print(f"Tenant: {settings.name}")
                    print(f"Tier: {settings.subscription_tier}")
                    print(f"Credits this month: {settings.current_month_credits}")
                    ```
        """
        ...

    async def update_settings(self, *, name: Optional[str] = None, webhook_url: Optional[str] = None, allowed_vlm_providers: Optional[list[str]] = None, allowed_domains: Optional[list[str]] = None, max_monthly_credits: Optional[int] = None, max_requests_per_minute: Optional[int] = None, custom_config: Optional[dict[str, Any]] = None) -> TenantSettings:
        """

                Update tenant settings.

                Only provided fields are updated; others remain unchanged.
                Requires ADMIN role on the tenant.

                Args:
                    name: Tenant/organization name
                    webhook_url: URL for event notifications
                    allowed_vlm_providers: List of allowed VLM providers
                    allowed_domains: Allowed domains for CORS
                    max_monthly_credits: Monthly credit limit
                    max_requests_per_minute: API rate limit
                    custom_config: Custom configuration JSON

                Returns:
                    Updated TenantSettings

                Raises:
                    PermissionError: If user doesn't have ADMIN role

                Example:
                    ```python
                    settings = await client.tenant.update_settings(
                        name="My Updated Company",
                        max_requests_per_minute=200
                    )
                    ```
        """
        ...

    async def get_limits(self) -> TenantLimits:
        """

                Get tenant usage limits and current usage.

                Returns limits, current usage, and remaining quota for various
                resources like monthly credits and API calls.

                Returns:
                    TenantLimits with limits, usage, and remaining quota

                Example:
                    ```python
                    limits = await client.tenant.get_limits()
                    print(f"Monthly credits remaining: {limits.remaining.get('monthly_credits')}")
                    ```
        """
        ...

    async def list_members(self) -> list[TenantMember]:
        """

                Get all tenant members.

                Returns list of users who have access to this tenant.
                Requires VIEW permission on the tenant.

                Returns:
                    List of TenantMember objects

                Example:
                    ```python
                    members = await client.tenant.list_members()
                    for member in members:
                        print(f"{member.name} ({member.email}) - {member.role}")
                    ```
        """
        ...

    async def invite_member(self, email: str, *, role: str = 'viewer') -> TenantMember:
        """

                Invite a user to join the tenant.

                Creates a new user account if the email doesn't exist.
                Requires OWNER role on the tenant.

                Args:
                    email: Email address of user to invite
                    role: Role to assign (viewer, editor, admin)

                Returns:
                    TenantMember for the invited user

                Raises:
                    PermissionError: If user doesn't have OWNER role
                    ValidationError: If email is invalid or user is already a member

                Example:
                    ```python
                    member = await client.tenant.invite_member(
                        "newuser@example.com",
                        role="editor"
                    )
                    print(f"Invited: {member.email}")
                    ```
        """
        ...

    async def update_member_role(self, user_id: str, role: str) -> TenantMember:
        """

                Update a tenant member's role.

                Requires OWNER role on the tenant.
                Cannot change the owner's role.

                Args:
                    user_id: User ID of the member to update
                    role: New role to assign (viewer, editor, admin)

                Returns:
                    Updated TenantMember

                Raises:
                    PermissionError: If user doesn't have OWNER role
                    ValidationError: If trying to change owner's role

                Example:
                    ```python
                    member = await client.tenant.update_member_role(
                        "user-uuid",
                        "admin"
                    )
                    print(f"Updated {member.email} to {member.role}")
                    ```
        """
        ...

    async def remove_member(self, user_id: str) -> dict[str, Any]:
        """

                Remove a member from the tenant.

                Requires OWNER role on the tenant.
                Cannot remove yourself or the owner.

                Args:
                    user_id: User ID of the member to remove

                Returns:
                    Dictionary with removal status

                Raises:
                    PermissionError: If user doesn't have OWNER role
                    ValidationError: If trying to remove owner or yourself

                Example:
                    ```python
                    result = await client.tenant.remove_member("user-uuid")
                    print(result["detail"])
                    ```
        """
        ...
