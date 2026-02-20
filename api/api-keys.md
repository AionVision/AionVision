# API Keys API

> Base URL: `https://api.aionvision.tech/api/v2`
> Authentication: Session authentication required (not API key auth)

Create, manage, and rotate API keys with fine-grained scopes. API keys (format: `aion_...`) are used for programmatic access to all other API endpoints. This API itself requires active session authentication — ADMIN role for create/update/delete, VIEW permission for list/get.

> **Note**: The full API key value is only returned once at creation time. Store it securely — it cannot be retrieved again.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api-keys | Create a new API key (ADMIN) |
| GET | /api-keys | List all tenant API keys (VIEW) |
| GET | /api-keys/{api_key_id} | Get API key details (VIEW) |
| PUT | /api-keys/{api_key_id} | Update name/description/metadata (ADMIN) |
| DELETE | /api-keys/{api_key_id} | Revoke an API key (ADMIN) |

---

## POST /api-keys — Create API Key

**Request**
```http
POST /api/v2/api-keys
Authorization: Bearer {session_token}
Content-Type: application/json
```

**Body**
```json
{
  "name": "Production API Key",
  "description": "Key for production application",
  "scopes": ["read", "write"],
  "metadata": {"environment": "production", "team": "backend"},
  "expires_at": "2026-07-01T00:00:00Z"
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | 1–255 characters |
| description | string | No | Max 500 characters |
| scopes | string[] | No | If empty, inherits creator's permissions (capped at admin) |
| metadata | object | No | Arbitrary key-value pairs for tracking |
| expires_at | string | No | ISO 8601 expiration (must be in future). Omit for no expiration. |

**Response** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "api_key": "aion_1234567890abcdef...",
  "name": "Production API Key",
  "description": "Key for production application",
  "key_prefix": "aion_live_1234",
  "created_at": "2025-01-15T10:30:00Z",
  "expires_at": "2026-07-01T00:00:00Z",
  "is_active": true,
  "scopes": ["read", "write"],
  "metadata": {"environment": "production", "team": "backend"}
}
```

`api_key` is only present in the creation response. Subsequent gets return `key_prefix` only.

---

## GET /api-keys — List API Keys

**Response** `200 OK`
```json
{
  "api_keys": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Production API Key",
      "key_prefix": "aion_live_1234",
      "created_at": "2025-01-15T10:30:00Z",
      "last_used_at": "2025-01-15T09:00:00Z",
      "expires_at": "2026-07-01T00:00:00Z",
      "is_active": true,
      "scopes": ["read", "write"],
      "metadata": {"environment": "production"},
      "usage_count": 142
    }
  ],
  "total": 1
}
```

---

## PUT /api-keys/{api_key_id} — Update API Key

Update name, description, or metadata only. Scopes, `is_active`, and `expires_at` cannot be changed after creation.

**Request body** (all fields optional)
```json
{
  "name": "Updated Production Key",
  "description": "Updated description",
  "metadata": {"environment": "production", "version": "2.0"}
}
```

**Response** `200 OK` — returns updated key object (without full `api_key` value).

---

## DELETE /api-keys/{api_key_id} — Revoke API Key

Keys are deactivated (not physically deleted). Returns `204 No Content`.

```bash
curl -X DELETE https://api.aionvision.tech/api/v2/api-keys/550e8400-... \
  -H "Authorization: Bearer {session_token}"
```

---

## Scopes Reference

### Role-based scopes

| Scope | Equivalent role | Access |
|-------|----------------|--------|
| `read` | VIEWER | Read-only access |
| `write` | EDITOR | Read/write access |
| `admin` | ADMIN | Administrative access |

### Resource-specific scopes

| Scope | Access |
|-------|--------|
| `rules:read` | Read access to rules |
| `rules:write` | Write access to rules |
| `rules:delete` | Delete access to rules |
| `api_keys:read` | View API keys |
| `api_keys:write` | Manage API keys |
| `usage:read` | View usage statistics |
| `verifications:read` | View verification results |
| `verifications:write` | Create verifications |
| `tenants:read` | View tenant information |

If no scopes are specified at creation, the key inherits the creator's permissions (capped at admin level). Invalid scope names are rejected with `400 Bad Request`.

---

## See Also

- [Settings API](settings.md) — tenant and user settings management
- [Usage API](usage.md) — filter usage by `api_key_id`
- SDK: `client.api_keys` — `create()`, `list()`, `get()`, `update()`, `revoke()`
