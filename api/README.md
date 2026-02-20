# Aionvision API Reference

> **Base URL**: `https://api.aionvision.tech/api/v2`

Human-readable API documentation organized by resource. For the machine-readable OpenAPI 3.1 specification (193 endpoints, 283 schemas), see [../openapi.json](../openapi.json).

---

## Authentication

All API requests require a Bearer token in the `Authorization` header:

```http
Authorization: Bearer aion_your_api_key_here
```

API keys start with `aion_` and are generated from your dashboard at [aionvision.tech](https://aionvision.tech). Keys are tenant-scoped — one key per workspace.

```bash
# Example authenticated request
curl https://api.aionvision.tech/api/v2/user-files \
  -H "Authorization: Bearer aion_your_api_key_here"
```

---

## Resources

| Resource | Endpoints | Description |
|----------|-----------|-------------|
| [Uploads](uploads.md) | 18 | Stream and batch image/document upload |
| [Files](files.md) | 14 | List, search, and manage uploaded files |
| [Documents](documents.md) | 16 | Document processing, text extraction, semantic search |
<!-- | [Videos](videos.md) | 8 | Chunked video upload and scene extraction | -->
| [Chat](chat.md) | 14 | Agentic chat sessions with image/document context |
| [Agents](agents.md) | 6 | Stateless AI agent operations (search, synthesize, analyze) |
| [Folders](folders.md) | 8 | Hierarchical file organization |
| [Colors](colors.md) | 5 | Color analysis (automatic on upload) and color-based search |
| [Datasets](datasets.md) | 5 | Dataset creation and export (CSV, COCO, YOLO, Pascal VOC) |
| [Cloud Storage](cloud-storage.md) | 10 | Google Drive / cloud import and export |
| [API Keys](api-keys.md) | 5 | Manage API keys |
| [Settings](settings.md) | 12 | Tenant settings, custom S3, team management |
| [Usage](usage.md) | 8 | Usage analytics and quota information |

---

## Rate Limits

Rate limits are applied per API key. When exceeded, the API returns `429 Too Many Requests` with a `Retry-After` header indicating when to retry.

| Plan | Requests/minute | Batch size | Monthly uploads |
|------|----------------|------------|-----------------|
| FREE | 10 | 10 files | 1,000 |
| STARTER | 30 | 20 files | 10,000 |
| PROFESSIONAL | 100 | 20 files | 50,000 |
| ENTERPRISE | 500 | 50 files | Unlimited |

---

## Error Format

All errors follow a consistent JSON envelope:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": {
      "field": "limit",
      "issue": "Must be between 1 and 100"
    }
  },
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

Include the `request_id` when contacting support.

### HTTP Status Codes

| Status | Meaning |
|--------|---------|
| `200` | Success |
| `201` | Created |
| `204` | No content (DELETE) |
| `302` | Redirect (file downloads, variants) |
| `400` | Bad request — invalid syntax or parameters |
| `401` | Unauthorized — missing or invalid API key |
| `402` | Payment required — subscription issue |
| `403` | Forbidden — insufficient permissions |
| `404` | Not found |
| `409` | Conflict — duplicate or concurrent operation |
| `422` | Unprocessable — validation or business rule violation |
| `429` | Rate limited — check `Retry-After` header |
| `500` | Server error — retry with exponential backoff |
| `502` | AI provider error |
| `503` | Service temporarily unavailable |

### Common Error Codes

| Code | Description |
|------|-------------|
| `INVALID_API_KEY` | API key is invalid or malformed |
| `EXPIRED_API_KEY` | API key has expired |
| `RATE_LIMIT_ERROR` | Too many requests |
| `STORAGE_QUOTA_EXCEEDED` | Account storage limit reached |
| `USAGE_LIMIT_EXCEEDED` | Monthly processing limit reached |
| `MEMORY_LIMIT_EXCEEDED` | Server overloaded — retry after `Retry-After` |
| `IMAGE_PROCESSING_ERROR` | AI analysis failed — retry |
| `TIMEOUT` | Operation timed out — reduce batch size |

---

## Pagination

List endpoints use offset-based pagination:

```
?limit=20&offset=0
```

Responses include:

```json
{
  "items": [...],
  "total_count": 150,
  "has_more": true
}
```

---

## See Also

> **Coming soon**: Video upload and scene detection — see [Videos](videos.md).

- [SDK Reference](../sdk/python/aion/) — Python SDK stubs with full type signatures
- [Examples](../examples/) — Runnable Python examples for all major workflows
- [OpenAPI Spec](../openapi.json) — Full machine-readable specification
