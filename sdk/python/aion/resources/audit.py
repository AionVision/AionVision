from __future__ import annotations
from datetime import datetime
from typing import Any, Optional
from ..config import ClientConfig
from ..types.audit import AuditLogEntry, AuditLogList


class AuditResource:
    """

        Audit log operations for the Aionvision SDK.

        Provides methods to query and retrieve audit logs for security
        monitoring and compliance. Requires ADMIN role on the tenant.
    """

    def __init__(self, http: HTTPClient, config: ClientConfig) -> None:
        """

                Initialize the audit resource.

                Args:
                    http: HTTP client for API communication
                    config: Client configuration
        """
        ...

    async def list(self, *, event_type: Optional[str] = None, severity: Optional[str] = None, user_id: Optional[str] = None, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None, result: Optional[str] = None, limit: int = 50, offset: int = 0) -> AuditLogList:
        """

                List audit log entries with filtering.

                Returns a paginated list of audit events. Use filters to narrow
                results by event type, severity, user, date range, or result.

                Requires ADMIN role on the tenant.

                Args:
                    event_type: Filter by event type (e.g., "auth.login", "api_key.created")
                    severity: Filter by severity (info, warning, error, critical)
                    user_id: Filter by user ID
                    date_from: Filter from date (inclusive)
                    date_to: Filter to date (inclusive)
                    result: Filter by result (success, failure, denied)
                    limit: Number of entries to return (1-100, default: 50)
                    offset: Offset for pagination

                Returns:
                    AuditLogList with entries, total_count, and has_more flag

                Raises:
                    PermissionError: If user doesn't have ADMIN role

                Example:
                    ```python
                    # Get recent audit logs
                    logs = await client.audit.list(limit=10)
                    for entry in logs.entries:
                        print(f"{entry.event_timestamp}: {entry.event_type} - {entry.result}")

                    # Filter by event type
                    login_logs = await client.audit.list(event_type="auth.login")

                    # Filter by date range
                    from datetime import datetime, timedelta
                    logs = await client.audit.list(
                        date_from=datetime.now() - timedelta(days=7),
                        severity="error"
                    )

                    # Paginate through results
                    offset = 0
                    while True:
                        page = await client.audit.list(offset=offset)
                        for entry in page.entries:
                            process(entry)
                        if not page.has_more:
                            break
                        offset += len(page.entries)
                    ```
        """
        ...

    async def get(self, log_id: str) -> AuditLogEntry:
        """

                Get a single audit log entry.

                Requires ADMIN role on the tenant.

                Args:
                    log_id: Audit log entry ID

                Returns:
                    AuditLogEntry with full details

                Raises:
                    ResourceNotFoundError: If log entry doesn't exist
                    PermissionError: If user doesn't have ADMIN role

                Example:
                    ```python
                    entry = await client.audit.get("log-uuid-here")
                    print(f"Event: {entry.event_type}")
                    print(f"User: {entry.user_id}")
                    print(f"IP: {entry.ip_address}")
                    if entry.metadata:
                        print(f"Details: {entry.metadata}")
                    ```
        """
        ...
