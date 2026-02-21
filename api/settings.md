# Settings API

> Base URL: `https://api.aionvision.tech/api/v2`
> Authentication: Session authentication required

User preferences, tenant configuration, team membership, custom S3 storage, and audit logs. All settings endpoints require session authentication. Permission requirements vary by endpoint as noted below.

## Endpoints

### User Settings

| Method | Path | Description | Permission |
|--------|------|-------------|------------|
| GET | /user/profile | Get current user profile | Any |
| PATCH | /user/profile | Update name and preferences | Any |
| POST | /user/change-password | Change password | Any (rate limited: 3/hr) |
| POST | /user/change-email | Request email change | Any (rate limited: 3/day) |
| GET | /user/sessions | List active sessions | Any |
| DELETE | /user/sessions/{session_id} | Revoke a session | Any |
| POST | /user/revoke-all-sessions | Revoke all other sessions | Any |
| POST | /user/set-initial-password | Set password for OAuth users | Any |
| POST | /user/account/delete | Permanently delete account | Any (rate limited: 3/day) |

### Tenant Settings

| Method | Path | Description | Permission |
|--------|------|-------------|------------|
| GET | /tenant/settings | Get tenant configuration | VIEW |
| PATCH | /tenant/settings | Update tenant settings | ADMIN |
| GET | /tenant/limits | Get usage limits and quota | VIEW |
| GET | /tenant/members | List tenant members | VIEW |
| POST | /tenant/members/invite | Invite a new member | OWNER |
| PATCH | /tenant/members/{user_id}/role | Change member role | OWNER |
| DELETE | /tenant/members/{user_id} | Remove a member | OWNER |

### Custom S3 (BYOB)

| Method | Path | Description | Permission |
|--------|------|-------------|------------|
| POST | /tenant/s3-config | Configure custom S3 bucket | ADMIN |
| GET | /tenant/s3-config | Get S3 config status | VIEW |
| POST | /tenant/s3-config/validate | Test S3 credentials | ADMIN |
| DELETE | /tenant/s3-config | Remove S3 configuration | ADMIN |

### Audit Logs

| Method | Path | Description | Permission |
|--------|------|-------------|------------|
| GET | /tenant/audit-logs | List audit events (paginated) | ADMIN |
| GET | /tenant/audit-logs/{log_id} | Get a single audit event | ADMIN |

---

## User Profile

### GET /user/profile

**Response** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "is_active": true,
  "email_verified": true,
  "created_at": "2025-01-01T00:00:00Z",
  "last_login_at": "2025-06-10T14:22:00Z",
  "preferences": {
    "timezone": "America/New_York",
    "theme": "dark",
    "language": "en",
    "notifications": {"email": true, "browser": false}
  }
}
```

### PATCH /user/profile

```json
{
  "name": "Jane Doe",
  "preferences": {
    "timezone": "Europe/London",
    "theme": "light",
    "language": "en",
    "notifications": {"email": true, "browser": true}
  }
}
```

Returns updated profile object.

### POST /user/change-password

Rate limited: 3 requests per hour.

```json
{
  "current_password": "OldPassword123!",
  "new_password": "NewSecurePassword456!"
}
```

**Response** `200 OK`
```json
{
  "message": "Password changed successfully",
  "session_rotation_required": true,
  "rotation_endpoint": "/api/v2/auth/session/rotate-session"
}
```

### POST /user/set-initial-password

For users who signed up via OAuth (Google, GitHub) and want to add password authentication. Returns `400` if a password is already set.

Send the password directly as a JSON string body:
```
"SecurePassword123!"
```

**Response** `200 OK`
```json
{"success": true, "auth_provider": "both"}
```

### POST /user/account/delete

Permanently delete the authenticated user's account. Deletes all owned tenants (cascading to API keys, members, etc.), cancels active Stripe subscriptions, and creates an audit record. Rate limited: 3 attempts per day.

**Request body**
```json
{
  "confirmation": "delete my account"
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| confirmation | string | Must be exactly `"delete my account"` |

**Response** `200 OK`
```json
{"message": "Account deleted successfully"}
```

**Errors**
- `400` — Confirmation text doesn't match
- `404` — User not found

---

## Tenant Settings

### GET /tenant/settings

Returns full tenant configuration including subscription and usage summary. Requires VIEW permission.

**Response** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Acme Corp",
  "owner_user_id": "660e8400-e29b-41d4-a716-446655440000",
  "created_at": "2025-01-01T00:00:00Z",
  "is_active": true,
  "allowed_vlm_providers": ["openai", "anthropic", "google"],
  "subscription_tier": "professional",
  "subscription_expires_at": "2026-01-01T00:00:00Z",
  "max_monthly_credits": 10000,
  "max_requests_per_minute": 100,
  "current_month_credits": 2500,
  "current_month_cost": 45.00,
  "total_credits": 15000,
  "total_cost": 270.00
}
```

### PATCH /tenant/settings

Requires ADMIN role. Rate limited: 10/min. `max_monthly_credits` and `max_requests_per_minute` are billing-controlled and cannot be set here.

```json
{
  "name": "Acme Corporation",
  "allowed_vlm_providers": ["openai", "anthropic"],
  "custom_config": {"default_model": "gpt-4o"}
}
```

### GET /tenant/limits

Returns limits, current usage, and remaining quota.

**Response** `200 OK`
```json
{
  "limits": {
    "monthly_verifications": 1000,
    "api_calls_per_minute": 100
  },
  "usage": {
    "monthly_verifications": 250,
    "api_calls_per_minute": 45
  },
  "remaining": {
    "monthly_verifications": 750,
    "api_calls_per_minute": 55
  }
}
```

---

## Team Management

### POST /tenant/members/invite

Invite a new member. Creates a user account if the email doesn't exist. Requires OWNER permission. Rate limited: 5/min.

```json
{"email": "newmember@example.com", "role": "editor"}
```

Valid roles: `"viewer"`, `"editor"`, `"admin"` (cannot invite as `"owner"`)

**Response** `200 OK`
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440000",
  "email": "newmember@example.com",
  "name": "newmember@example.com",
  "role": "editor",
  "joined_at": "2025-06-15T10:30:00Z"
}
```

### PATCH /tenant/members/{user_id}/role

Change a member's role. Cannot change the owner's role. Rate limited: 10/min.

```json
{"role": "admin"}
```

### DELETE /tenant/members/{user_id}

Remove a member from the tenant. Cannot remove the owner or yourself. Rate limited: 5/min.

```json
{"detail": "Member removed successfully"}
```

---

## Custom S3 Storage (BYOB)

Store files in your own AWS S3 bucket. Credentials are encrypted at rest using AES-256. After configuration, all new uploads go to your bucket.

### POST /tenant/s3-config

Validates credentials by testing bucket access, then stores them encrypted. Requires ADMIN permission. Rate limited: 5/min.

```json
{
  "access_key_id": "YOUR_AWS_ACCESS_KEY_ID",
  "secret_access_key": "YOUR_AWS_SECRET_ACCESS_KEY",
  "bucket_name": "my-company-uploads",
  "region": "us-east-1"
}
```

**Response** `200 OK`
```json
{
  "configured": true,
  "bucket_name": "my-company-uploads",
  "region": "us-east-1",
  "configured_at": "2025-06-15T12:00:00Z",
  "is_validated": null,
  "error": null
}
```

### GET /tenant/s3-config

Returns configuration status without exposing credentials.

```json
{"configured": true, "bucket_name": "my-company-uploads", "region": "us-east-1", "is_validated": true}
```

### POST /tenant/s3-config/validate

Test that stored credentials still work. Safe health-check — does not modify configuration. Rate limited: 10/min.

```json
{"valid": true, "bucket_name": "my-company-uploads", "region": "us-east-1", "error": null}
```

### DELETE /tenant/s3-config

Removes S3 configuration. Future uploads go to the default Aionvision bucket. Rate limited: 5/min.

---

## Audit Logs

Query log of admin and security events for the tenant. Requires ADMIN role.

### GET /tenant/audit-logs

**Query parameters**: `?event_type=auth.login&severity=info&user_id=uuid&date_from=ISO&date_to=ISO&result=success&limit=50&offset=0`

**Response** `200 OK`
```json
{
  "entries": [
    {
      "id": "log_abc123",
      "event_type": "api_key.created",
      "event_timestamp": "2025-06-10T14:22:00Z",
      "severity": "info",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "action": "create",
      "result": "success",
      "ip_address": "192.168.1.1",
      "resource_type": "api_key",
      "resource_id": "key_xyz789",
      "metadata": {"key_name": "Production API Key"}
    }
  ],
  "total_count": 142,
  "has_more": true
}
```

---

## See Also

- [API Keys API](api-keys.md) — manage API keys for programmatic access
- [Usage API](usage.md) — usage analytics and quota tracking
- SDK: `client.settings` — `get_profile()`, `update_profile()`, `get_tenant()`, `invite_member()`
