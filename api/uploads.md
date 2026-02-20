# Uploads API

> Base URL: `https://api.aionvision.tech/api/v2`
> Authentication: `Authorization: Bearer {api_key}`

Upload images and documents to Aionvision. For most use cases, use the **streaming endpoints** — they handle files in one request with no extra steps. The presigned URL workflow is only needed for files over 100MB or browser-direct-to-S3 uploads.

**Supported formats** — Images: JPEG, PNG, WebP, GIF · Documents: PDF, DOCX, TXT, MD

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /user-files/upload/stream | Stream upload single file (recommended) |
| POST | /user-files/upload/stream-batch | Stream upload multiple files (recommended) |
| GET | /uploads/quota-check | Check upload quota before starting |
| POST | /uploads/check-duplicates | Check for duplicate file hashes |
| POST | /uploads/request-presigned-url | Generate presigned URL (advanced) |
| POST | /uploads/confirm | Confirm presigned upload (advanced) |
| POST | /uploads/batch-prepare | Prepare batch presigned upload (advanced, max 5) |
| POST | /uploads/batch-confirm | Confirm batch presigned upload (advanced) |
| GET | /uploads/batch/{batch_id}/status | Get batch status |
| GET | /uploads/status/{image_id} | Get single upload status |
| GET | /uploads/sessions/{session_id}/status | Get session progress |
| GET | /uploads/sessions/{session_id}/results | Get paginated session results |
| POST | /uploads/sessions/{session_id}/cancel | Cancel upload session |
| GET | /uploads/sessions | List upload sessions |

---

## POST /user-files/upload/stream — Stream Upload (Recommended)

Upload a single file directly. Files are processed in-memory while uploading to S3 in parallel. Best for files up to 100MB.

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
| tags | string | No | Comma-separated tags (e.g. `"safety,inspection"`) |
| auto_describe | boolean | No | Enable AI description. Default: `true` |
| skip_duplicates | boolean | No | Skip if file hash already exists. Default: `false` |
| storage_target | string | No | `"default"` or `"custom"`. Default: `"default"` |

**Response** `200 OK`
```json
{
  "image_id": "550e8400-e29b-41d4-a716-446655440000",
  "object_key": "uploads/{tenant_id}/{uuid}/photo.jpg",
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
| files | file[] | Yes | Files to upload. Tier limits: FREE: 10, STARTER: 20, PROFESSIONAL: 20, ENTERPRISE: 50 |
| auto_describe | boolean | No | Enable AI descriptions. Default: `true` |
| skip_duplicates | boolean | No | Skip existing files by hash. Default: `false` |
| tags | string | No | Comma-separated tags applied to all files |
| intent | string | No | `"describe"` (default), `"verify"`, or `"rules"` |
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
      "status": "completed",
      "processing_time_ms": 1250.5,
      "skipped": false,
      "error": null,
      "media_type": "image"
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

Check available quota before starting an upload to prevent failures.

**Request**
```http
GET /api/v2/uploads/quota-check?file_count=10
Authorization: Bearer aion_your_api_key_here
```

**Response** `200 OK`
```json
{
  "can_proceed": true,
  "requested": 10,
  "available": 990,
  "monthly_limit": 1000,
  "current_usage": 10,
  "message": null
}
```

When `can_proceed: false`, the `message` field explains the limit and how to resolve it.

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

## Presigned URL Workflow (Advanced)

Use only for files over 100MB or browser-direct-to-S3 uploads. Requires 3 steps: request → upload → confirm.

### POST /uploads/request-presigned-url

**Request body**
```json
{
  "filename": "large-photo.jpg",
  "content_type": "image/jpeg",
  "size_bytes": 52428800,
  "idempotency_key": "unique-retry-key-123",
  "storage_target": "default"
}
```

**Response** `200 OK`
```json
{
  "upload_url": "https://storage.example.com/bucket/presigned-upload-url...",
  "upload_method": "PUT",
  "upload_headers": { "Content-Type": "image/jpeg" },
  "object_key": "uploads/{tenant_id}/{uuid}/example.jpg",
  "expires_at": "2025-01-15T10:40:00",
  "max_size_bytes": 104857600,
  "storage_target": "default"
}
```

Then upload directly to `upload_url` with `upload_headers`, then call `POST /uploads/confirm` with the `object_key`.

---

## See Also

- [Files API](files.md) — list and manage uploaded files
- [Documents API](documents.md) — document-specific upload workflow
<!-- - [Videos API](videos.md) — chunked video upload (coming soon) -->
- SDK: `client.uploads` — `upload_one()`, `upload()`, `check_quota()`
