# Uploads API

> Base URL: `https://api.aionvision.tech/api/v2`
> Authentication: `Authorization: Bearer {api_key}`

Upload images and documents to Aionvision. Use the **streaming endpoints** — they handle files in one request with no extra steps.

**Supported formats** — Images: JPEG, PNG, WebP, GIF · Documents: PDF, DOCX, TXT, MD

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /user-files/upload/stream | Stream upload single file (recommended) |
| POST | /user-files/upload/stream-batch | Stream upload multiple files (recommended) |
| GET | /uploads/quota-check | Check upload quota before starting |
| POST | /uploads/check-duplicates | Check for duplicate file hashes |
| GET | /uploads/status/{image_id} | Get single upload status |
| GET | /uploads/sessions/{session_id}/status | Get session progress |
| GET | /uploads/sessions/{session_id}/results | Get paginated session results |
| POST | /uploads/sessions/{session_id}/cancel | Cancel upload session |
| GET | /uploads/sessions | List upload sessions |

---

## POST /user-files/upload/stream — Stream Upload (Recommended)

Upload a single file directly. Files are processed in-memory while uploading to storage in parallel. Best for files up to 100MB.

**Request**
```http
POST /api/v2/user-files/upload/stream
Authorization: Bearer aion_your_api_key_here
Content-Type: multipart/form-data
```

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | file | Yes | File to upload (max 100MB) |
| title | string | No | Custom title (max 255 chars) |
| tags | string | No | Comma-separated tags (e.g. `"safety,inspection"`). Max 40 tags, each max 50 characters. |
| auto_describe | boolean | No | Enable AI description. Default: `true` |
| skip_duplicates | boolean | No | Skip if file hash already exists. Default: `false` |
| storage_target | string | No | `"default"` or `"custom"`. Default: `"default"` |

**Response** `200 OK`
```json
{
  "image_id": "550e8400-e29b-41d4-a716-446655440000",
  "object_key": "uploads/550e8400-e29b-41d4-a716-446655440000/photo.jpg",
  "upload_method": "STREAMING",
  "status": "completed",
  "processing_time_ms": 1250.5,
  "s3_upload_completed": true,
  "variants_queued": true,
  "description_queued": true,
  "skipped": false,
  "skipped_existing_image_id": null,
  "storage_target": "default",
  "media_type": "image",
  "document_type": null,
  "text_extraction_status": null
}
```

`status` values: `"completed"`, `"processing"`, `"skipped"`. When `skip_duplicates=true` and the file already exists, `skipped=true` and `skipped_existing_image_id` contains the existing file's ID.

**Example**
```bash
# cURL
curl -X POST https://api.aionvision.tech/api/v2/user-files/upload/stream \
  -H "Authorization: Bearer aion_your_api_key_here" \
  -F "file=@photo.jpg" \
  -F "title=Site Inspection" \
  -F "tags=inspection,site"
```
```python
# Python SDK equivalent
async with AionVision(api_key="aion_...") as client:
    result = await client.upload_one("photo.jpg", title="Site Inspection", tags=["inspection", "site"])
    print(result.image_id)
```

---

## POST /user-files/upload/stream-batch — Batch Stream Upload (Recommended)

Upload multiple files in a single request with server-managed concurrency.

**Request**
```http
POST /api/v2/user-files/upload/stream-batch
Authorization: Bearer aion_your_api_key_here
Content-Type: multipart/form-data
```

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| files | file[] | Yes | Files to upload. Tier limits: FREE: 10, STARTER: 50, PROFESSIONAL: 100, ENTERPRISE: 200 |
| auto_describe | boolean | No | Enable AI descriptions. Default: `true` |
| skip_duplicates | boolean | No | Skip existing files by hash. Default: `false` |
| tags | string | No | Comma-separated tags applied to all files. Max 40 tags, each max 50 characters. |
| storage_target | string | No | `"default"` or `"custom"` |

**Response** `200 OK`
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "total_files": 3,
  "accepted_files": 3,
  "rejected_files": 0,
  "status": "completed",
  "immediate_results": [
    {
      "image_id": "660e8400-e29b-41d4-a716-446655440001",
      "filename": "photo1.jpg",
      "object_key": "uploads/660e8400-e29b-41d4-a716-446655440001/photo1.jpg",
      "status": "completed",
      "processing_time_ms": 1250.5,
      "skipped": false,
      "skipped_existing_image_id": null,
      "error": null,
      "storage_target": "default",
      "media_type": "image",
      "document_type": null,
      "text_extraction_status": null
    }
  ],
  "status_url": "/api/v2/uploads/sessions/{session_id}/status",
  "websocket_channel": "batch.{session_id}",
  "rejections": null
}
```

`immediate_results` is only present for batches of 5 or fewer files. For larger batches, poll `status_url` or subscribe to `websocket_channel`.

**Example**
```bash
curl -X POST https://api.aionvision.tech/api/v2/user-files/upload/stream-batch \
  -H "Authorization: Bearer aion_your_api_key_here" \
  -F "files=@photo1.jpg" \
  -F "files=@photo2.jpg" \
  -F "files=@photo3.jpg"
```
```python
# Python SDK equivalent
async with AionVision(api_key="aion_...") as client:
    results = await client.upload(["photo1.jpg", "photo2.jpg", "photo3.jpg"])
    for result in results:
        print(result.image_id, result.status)
```

---

## GET /uploads/quota-check — Check Quota

Check available quota before starting an upload to prevent failures. Also useful as a general balance check to see remaining quota.

**Request**
```http
GET /api/v2/uploads/quota-check?file_count=10
Authorization: Bearer aion_your_api_key_here
```

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file_count | integer | **Yes** | Number of files you plan to upload. Use `file_count=1` for a general balance check. |

> **Tip:** The API requires `file_count` — calling without it returns a `422` validation error. To simply check your remaining quota without a specific upload in mind, pass `file_count=1`. The Python SDK's `client.uploads.check_quota()` defaults to `file_count=1` for this reason.

**Response** `200 OK`
```json
{
  "can_proceed": true,
  "requested": 10,
  "available": 990,
  "monthly_limit": 1000,
  "current_usage": 10,
  "prepaid_credits": 0,
  "max_batch_size": 20,
  "max_concurrent_uploads": 10,
  "message": null
}
```

| Field | Type | Description |
|-------|------|-------------|
| can_proceed | boolean | Whether the upload can proceed with the requested file count |
| requested | integer | Number of files requested (echoes `file_count`) |
| available | integer | Remaining uploads (included + prepaid credits) |
| monthly_limit | integer | Total monthly upload limit for the plan |
| current_usage | integer | Credits used this billing period |
| prepaid_credits | integer | Top-up credits available beyond the monthly plan (0 if tier doesn't support prepaid) |
| max_batch_size | integer | Maximum files per batch for the caller's subscription tier |
| max_concurrent_uploads | integer | Maximum concurrent uploads allowed |
| message | string or null | User-friendly explanation when `can_proceed` is `false` |

When `can_proceed: false`, the `message` field explains the limit and how to resolve it.

**Example — General balance check**
```bash
curl "https://api.aionvision.tech/api/v2/uploads/quota-check?file_count=1" \
  -H "Authorization: Bearer aion_your_api_key_here"
```
```python
# Python SDK (file_count defaults to 1)
quota = await client.uploads.check_quota()
print(f"Available: {quota.available} / {quota.monthly_limit}")
```

---

## POST /uploads/check-duplicates — Check for Duplicates

Check whether files already exist for this tenant using SHA-256 file hashes. Use this before uploading to skip re-uploading already-stored files. Up to 250 hashes per request.

**Request body**
```json
{
  "hashes": [
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| hashes | string[] | SHA-256 hashes to check (1–250 items, required) |

**Response** `200 OK`
```json
{
  "duplicates": ["e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"],
  "unique": ["a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"]
}
```

`duplicates` — hashes that already exist for this tenant. `unique` — hashes not yet stored. When `skip_duplicates=true` is set on stream uploads, the server performs this check automatically; call this endpoint manually when you need the decision ahead of time.

---

## GET /uploads/sessions/{session_id}/status — Session Progress

Poll the progress of an ongoing batch upload session.

**Response** `200 OK`
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "total_files": 20,
  "completed_files": 15,
  "failed_files": 1,
  "skipped_files": 2,
  "pending_files": 2,
  "progress_percentage": 90.0,
  "created_at": "2025-01-15T10:30:00Z",
  "recent_completions": [
    {
      "filename": "photo1.jpg",
      "image_id": "660e8400-e29b-41d4-a716-446655440001",
      "status": "completed",
      "description": "A site inspection showing..."
    }
  ],
  "recent_errors": [
    {
      "filename": "bad-photo.jpg",
      "error": "Processing failed: invalid format",
      "retryable": true
    }
  ],
  "results_url": "/api/v2/uploads/sessions/{session_id}/results",
  "websocket_channel": "batch.{session_id}"
}
```

`status` values: `"pending"`, `"uploading"`, `"processing"`, `"completed"`, `"failed"`, `"expired"`, `"cancelled"`

---

## GET /uploads/sessions/{session_id}/results — Session Results

Get paginated results from an upload session.

**Query parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| include_failed | boolean | `true` | Include failed files in results |
| offset | integer | 0 | Number of results to skip |
| limit | integer | 100 | Results per page (1–500) |

**Response** `200 OK`
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "results": [
    {
      "image_id": "660e8400-e29b-41d4-a716-446655440001",
      "filename": "photo1.jpg",
      "object_key": "uploads/660e8400-e29b-41d4-a716-446655440001/photo1.jpg",
      "status": "completed",
      "description": "Site inspection showing...",
      "visible_text": null,
      "tags": ["inspection"],
      "processing_time_ms": 1250.5,
      "error_message": null,
      "thumbnail_url": "https://cdn.aionvision.tech/thumbs/...",
      "created_at": "2025-01-15T10:30:05Z"
    }
  ],
  "total_count": 20,
  "offset": 0,
  "limit": 100,
  "has_more": false,
  "summary": {"total_files": 20, "completed": 18, "failed": 1, "skipped": 1}
}
```

`status` values per result: `"completed"`, `"failed"`, `"skipped"`

---

## GET /uploads/stuck-uploads — Find Stuck Uploads

Find uploads that have been in non-terminal states longer than expected. Useful for identifying files that may need manual intervention or retry.

**Query parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `stuck_minutes` | integer | 30 | Minutes before an upload is considered stuck |
| `limit` | integer | 100 | Maximum results to return (1–500) |

**Response** `200 OK`
```json
{
  "stuck_count": 2,
  "images": [
    {
      "image_id": "550e8400-e29b-41d4-a716-446655440000",
      "tenant_id": "660f9500-f39c-52e5-b827-557766550111",
      "batch_id": "770a0600-e29b-41d4-a716-446655440002",
      "unified_status": "processing",
      "component_statuses": {
        "upload_status": "completed",
        "variant_status": "processing",
        "description_status": "pending"
      },
      "error_message": null,
      "last_error_at": null,
      "created_at": "2025-01-15T10:00:00Z",
      "last_updated_at": "2025-01-15T10:05:00Z",
      "completed_at": null,
      "retry_count": 0,
      "processing_duration_seconds": 1920.5,
      "is_stuck": true,
      "is_terminal": false
    }
  ]
}
```

---

## See Also

- [Files API](files.md) — list and manage uploaded files
- [Documents API](documents.md) — document-specific upload workflow
- [Videos API](videos.md) — chunked video upload, AI analysis, scene detection
- SDK: `client.uploads` — `upload_one()`, `upload()`, `check_quota()`
