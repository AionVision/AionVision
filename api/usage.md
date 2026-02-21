# Usage API

> Base URL: `https://api.aionvision.tech/api/v2`
> Authentication: `Authorization: Bearer {api_key}`

Monitor API usage, credit consumption, and plan utilization. Use the summary endpoints for dashboards, `by-period` for time-series charts, and `check` before operations to guard against limit overruns.

**Rate limits**: 30 requests/min for most endpoints; 60/min for `POST /usage/check`.

## Endpoints

### Usage Summary

| Method | Path | Description |
|--------|------|-------------|
| GET | /usage/summary | Aggregated stats for a date range |
| GET | /usage/details | Individual usage event records |
| GET | /usage/by-period | Time-series data grouped by hour/day/month |
| GET | /usage/top-endpoints | Most-used endpoints ranked by request count |

### Credit Usage

| Method | Path | Description |
|--------|------|-------------|
| POST | /usage/check | Pre-flight check: can an operation proceed? |
| GET | /usage/breakdown | Credit breakdown by verification level and operation |
| GET | /usage/plan | Plan utilization, projections, and recommendations |

### Token Usage

| Method | Path | Description |
|--------|------|-------------|
| GET | /usage/tokens/monthly | Monthly token totals by operation type |
| GET | /usage/tokens/files | Per-file token usage |
| GET | /usage/tokens/conversations | Per-chat-session token usage |

---

## GET /usage/summary — Usage Summary

Get aggregated request counts, performance metrics, and plan limits for a date range. Requires VIEW permission.

**Query parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| start_date | string | ISO 8601 start date |
| end_date | string | ISO 8601 end date |
| period | string | Predefined period: `day`, `week`, `month` (default: `month`) |
| api_key_id | string | Filter by a specific API key |

**Response** `200 OK`
```json
{
  "period": {
    "start": "2025-01-01T00:00:00Z",
    "end": "2025-01-31T23:59:59Z"
  },
  "usage": {
    "verify_count": 120,
    "describe_count": 3500,
    "batch_count": 45,
    "total_requests": 3665,
    "successful_requests": 3600,
    "failed_requests": 65
  },
  "performance": {
    "avg_response_time_ms": 245.5
  },
  "limits": {
    "monthly_limit": 100000,
    "used_this_month": 3665,
    "remaining": 96335,
    "percentage_used": 3.67
  },
  "plan": {
    "name": "Professional",
    "requests_limit": 100000,
    "requests_used": 3665,
    "requests_remaining": 96335,
    "usage_percentage": 3.67,
    "renewal_date": "2025-01-31T23:59:59Z"
  },
  "total_credits": 4200
}
```

```bash
curl "https://api.aionvision.tech/api/v2/usage/summary?period=month" \
  -H "Authorization: Bearer aion_your_api_key_here"
```
```python
summary = await client.usage.summary(period="month")
print(f"Used: {summary.usage.total_requests} / {summary.limits.monthly_limit}")
```

---

## GET /usage/by-period — Time-Series Data

Get usage data grouped by time period for charts. Returns an array of data points.

**Query parameters**: `?period_type=day&start_date=ISO&end_date=ISO&api_key_id=uuid`

`period_type` options: `"hour"`, `"day"` (default), `"month"`

**Response** `200 OK`
```json
{
  "period_type": "day",
  "start_date": "2025-01-01T00:00:00Z",
  "end_date": "2025-01-31T23:59:59Z",
  "data": [
    {"timestamp": "2025-01-01T00:00:00Z", "value": 125, "label": "2025-01-01"},
    {"timestamp": "2025-01-02T00:00:00Z", "value": 143, "label": "2025-01-02"}
  ]
}
```

---

## GET /usage/details — Usage Event Records

Paginated list of individual usage events. Useful for audit trails and detailed analysis. Requires VIEW permission.

**Query parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| start_date | string | ISO 8601 start date |
| end_date | string | ISO 8601 end date |
| api_key_id | string | Filter by API key |
| operation_type | string | Filter by operation type (e.g. `describe`, `verify`) |
| page | integer | Page number, default 1 |
| page_size | integer | 1–100, default 50 |

**Response** `200 OK`
```json
{
  "events": [
    {
      "id": "evt_abc123",
      "timestamp": "2025-01-15T14:30:00Z",
      "operation_type": "upload",
      "endpoint": "/api/v2/user-files/upload/confirm",
      "method": "POST",
      "status_code": 200,
      "response_time_ms": 312,
      "error_code": null,
      "api_key_id": "key_xyz789"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 50,
    "total_count": 3665,
    "total_pages": 74
  }
}
```

---

## POST /usage/check — Pre-flight Credit Check

Check whether an operation would exceed limits before attempting it. Rate limited: 60/min.

**Request body**
```json
{
  "verification_level": "standard",
  "item_count": 1
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| verification_level | string | `quick`, `standard`, `thorough`, `critical`. Default: `standard` |
| item_count | integer | Number of items to process. Default: 1 |

**Response** `200 OK`
```json
{
  "can_proceed": true,
  "current_usage": 3665,
  "monthly_limit": 100000,
  "required_credits": 2,
  "available_credits": 96335,
  "reset_date": "2025-02-01",
  "message": null
}
```

When limit would be exceeded:
```json
{
  "can_proceed": false,
  "current_usage": 99999,
  "monthly_limit": 100000,
  "required_credits": 2,
  "available_credits": 1,
  "reset_date": "2025-02-01",
  "message": "Operation requires 2 credits, but only 1 available"
}
```

```python
check = await client.usage.check(verification_level="thorough", item_count=10)
if not check.can_proceed:
    raise RuntimeError(check.message)
```

---

## GET /usage/breakdown — Credit Breakdown

Detailed credit usage for the current month, broken down by verification level and operation type.

**Response** `200 OK`
```json
{
  "current_month": "2025-01",
  "total_credits_used": 4200,
  "monthly_limit": 100000,
  "remaining_credits": 95800,
  "usage_percentage": 4.2,
  "by_verification_level": {
    "quick": 500,
    "standard": 2400,
    "thorough": 800,
    "critical": 500
  },
  "by_operation_type": {
    "describe": 3000,
    "verify": 600,
    "batch_describe": 500,
    "batch_verify": 100
  },
  "reset_date": "2025-02-01T00:00:00+00:00"
}
```

---

## GET /usage/plan — Plan Utilization

Comprehensive plan details with projections and optimization recommendations. Accepts `?period=month&include_projections=true`.

**Response** `200 OK` (abbreviated)
```json
{
  "billing_period": {
    "start_date": "2025-01-01T00:00:00Z",
    "end_date": "2025-01-31T23:59:59Z",
    "days_remaining": 16,
    "renewal_date": "2025-02-01T00:00:00Z"
  },
  "plan_details": {
    "plan_name": "Professional",
    "monthly_requests_limit": 100000,
    "requests_used": 3665,
    "requests_remaining": 96335,
    "usage_percentage": 3.67,
    "features": {
      "verification_levels": ["quick", "standard", "thorough", "critical"],
      "rule_sets_limit": 50,
      "batch_processing": true
    }
  },
  "projections": {
    "projected_monthly_requests": 7500,
    "will_exceed_limit": false,
    "trending": "stable"
  },
  "optimization_recommendations": {
    "suggestions": [
      {
        "type": "verification_level",
        "message": "Consider using 'quick' verification for non-critical items to save credits",
        "potential_request_savings": 500
      }
    ]
  }
}
```

---

## Token Usage

### GET /usage/tokens/monthly

Monthly token totals broken down by operation (describe, chat, verify) including cache metrics.

**Query parameters**: `?year=2025&month=1`

**Response** `200 OK`
```json
{
  "year": 2025,
  "month": 1,
  "describe_input_tokens": 125000,
  "describe_output_tokens": 45000,
  "describe_operations": 3500,
  "chat_input_tokens": 85000,
  "chat_output_tokens": 32000,
  "chat_messages": 420,
  "verify_input_tokens": 18000,
  "verify_output_tokens": 6500,
  "verify_operations": 120,
  "total_input_tokens": 228000,
  "total_output_tokens": 83500,
  "total_tokens": 311500,
  "total_cache_read_tokens": 85000,
  "total_cache_creation_tokens": 22000
}
```

### GET /usage/tokens/files

Per-file token usage for processed images. Query parameters: `?limit=50&offset=0`

```json
{
  "files": [
    {
      "image_id": "img_abc123",
      "filename": "product-photo.jpg",
      "input_tokens": 1200,
      "output_tokens": 450,
      "total_tokens": 1650,
      "created_at": "2025-01-15T14:30:00Z"
    }
  ],
  "total_count": 3500,
  "total_input_tokens": 125000,
  "total_output_tokens": 45000
}
```

### GET /usage/tokens/conversations

Per-chat-session token usage. Query parameters: `?limit=50&offset=0`

```json
{
  "conversations": [
    {
      "session_id": "sess_abc123",
      "title": "Product Analysis Discussion",
      "input_tokens": 5200,
      "output_tokens": 3100,
      "total_tokens": 8300,
      "message_count": 12,
      "created_at": "2025-01-15T10:00:00Z"
    }
  ],
  "total_count": 420
}
```

---

## See Also

- [Settings API](settings.md) — `GET /tenant/limits` for quota snapshot
- [API Keys API](api-keys.md) — filter usage by `api_key_id`
- SDK: `client.usage` — `summary()`, `check()`, `breakdown()`, `plan()`
