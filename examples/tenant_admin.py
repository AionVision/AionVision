"""
Tenant Administration: Settings, team members, audit logs, and custom S3 storage.

Demonstrates:
- Reading and updating tenant settings
- Managing team members (list, invite, role change, remove)
- Querying audit logs
- Configuring custom S3 storage
"""

import asyncio
from datetime import datetime, timedelta

from aion import AionVision


async def tenant_settings():
    """Read and update tenant configuration."""

    async with AionVision.from_env() as client:

        # Get current tenant settings
        settings = await client.tenant.get_settings()
        print(f"Tenant: {settings.name}")
        print(f"Tier: {settings.subscription_tier}")
        print(f"Credits this month: {settings.current_month_credits}")
        print(f"VLM providers: {settings.allowed_vlm_providers}")

        # Update settings (only provided fields are changed)
        updated = await client.tenant.update_settings(
            name="Acme Corporation",
            allowed_vlm_providers=["openai", "anthropic"],
        )
        print(f"Updated name: {updated.name}")

        # Check usage limits
        limits = await client.tenant.get_limits()
        print(f"Limits: {limits.limits}")
        print(f"Usage: {limits.usage}")
        print(f"Remaining: {limits.remaining}")


async def team_management():
    """Manage team members."""

    async with AionVision.from_env() as client:

        # List all members
        members = await client.tenant.list_members()
        for member in members:
            print(f"{member.name} ({member.email}) - {member.role}")

        # Invite a new member
        new_member = await client.tenant.invite_member(
            "colleague@example.com",
            role="editor",
        )
        print(f"Invited: {new_member.email} as {new_member.role}")

        # Change a member's role
        updated = await client.tenant.update_member_role(
            new_member.id,
            "admin",
        )
        print(f"Updated {updated.email} to {updated.role}")

        # Remove a member
        result = await client.tenant.remove_member(new_member.id)
        print(result["detail"])


async def audit_logs():
    """Query audit logs for security monitoring."""

    async with AionVision.from_env() as client:

        # Get recent audit logs
        logs = await client.audit.list(limit=10)
        print(f"Total events: {logs.total_count}")
        for entry in logs.entries:
            print(f"  {entry.event_timestamp}: {entry.event_type} - {entry.result}")

        # Filter by event type
        login_logs = await client.audit.list(event_type="auth.login")
        print(f"Login events: {login_logs.total_count}")

        # Filter by date range and severity
        recent_errors = await client.audit.list(
            date_from=datetime.now() - timedelta(days=7),
            severity="error",
        )
        for entry in recent_errors.entries:
            print(f"  {entry.event_type}: {entry.error_message}")

        # Get a single audit log entry
        if logs.entries:
            detail = await client.audit.get(logs.entries[0].id)
            print(f"Event: {detail.event_type}")
            print(f"IP: {detail.ip_address}")
            if detail.metadata:
                print(f"Metadata: {detail.metadata}")

        # Paginate through all results
        offset = 0
        while True:
            page = await client.audit.list(limit=50, offset=offset)
            for entry in page.entries:
                pass  # process entry
            if not page.has_more:
                break
            offset += len(page.entries)


async def custom_s3_storage():
    """Configure your own S3 bucket for file storage."""

    async with AionVision.from_env() as client:

        # Check current S3 configuration
        status = await client.settings.get_custom_s3_status()
        if status.configured:
            print(f"Using bucket: {status.bucket_name} in {status.region}")
        else:
            print("No custom S3 configured (using default Aionvision storage)")

        # Configure a custom S3 bucket
        config = await client.settings.configure_custom_s3(
            access_key_id="AKIAIOSFODNN7EXAMPLE",
            secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            bucket_name="my-company-uploads",
            region="us-east-1",
        )
        print(f"Configured: {config.bucket_name}")

        # Validate that credentials still work
        validation = await client.settings.validate_custom_s3()
        if validation.valid:
            print("S3 credentials are valid")
        else:
            print(f"Validation failed: {validation.error}")

        # Remove custom S3 (revert to default storage)
        result = await client.settings.remove_custom_s3()
        print(result["message"])


if __name__ == "__main__":
    asyncio.run(tenant_settings())
