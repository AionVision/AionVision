# Cloud Storage API

> Base URL: `https://api.aionvision.tech/api/v2`
> Authentication: `Authorization: Bearer {api_key}`

Connect Google Drive to import and export files directly. Uses OAuth 2.0 for secure access. Small imports are processed synchronously; large imports and all exports run as background jobs that you can poll for status.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /cloud-storage/auth/{provider} | Initiate OAuth flow, get authorization URL |
| GET | /cloud-storage/auth/{provider}/callback | OAuth redirect handler (browser flow) |
| POST | /cloud-storage/auth/{provider}/callback | Complete OAuth and create connection |
| GET | /cloud-storage/connections | List connected accounts |
| DELETE | /cloud-storage/connections/{connection_id} | Disconnect a cloud account |
| GET | /cloud-storage/connections/{connection_id}/picker-token | Get Google Picker session |
| POST | /cloud-storage/picker-proxy | Proxy Google Drive API calls |
| POST | /cloud-storage/import | Import files from cloud storage |
| POST | /cloud-storage/export | Export files to cloud storage |
| GET | /cloud-storage/jobs/{job_id} | Get import/export job status |

Currently supported provider: `"google_drive"`

---

## OAuth Flow

### Step 1 — POST /cloud-storage/auth/{provider}

Initiate the OAuth flow. Returns an authorization URL to redirect the user to.

**Request**
```http
POST /api/v2/cloud-storage/auth/google_drive
Authorization: Bearer aion_your_api_key_here
Content-Type: application/json
```

**Body**
```json
{
  "provider": "google_drive",
  "redirect_uri": "https://your-app.com/callback"
}
```

**Response** `200 OK`
```json
{
  "authorization_url": "https://accounts.google.com/o/oauth2/auth?...",
  "state": "csrf_state_token_abc123",
  "provider": "google_drive"
}
```

Redirect the user to `authorization_url`. Google will redirect back to your callback URL after authorization.

### Step 2 — POST /cloud-storage/auth/{provider}/callback

After the user authorizes, exchange the code for a connection.

**Request body**
```json
{
  "code": "authorization_code_from_google",
  "state": "csrf_state_token_abc123",
  "redirect_uri": "https://your-app.com/callback"
}
```

**Response** `200 OK`
```json
{
  "connection": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "provider": "google_drive",
    "provider_email": "user@gmail.com",
    "provider_display_name": "John Doe",
    "is_active": true,
    "created_at": "2025-01-15T10:30:00Z",
    "last_used_at": null
  },
  "is_new": true
}
```

> **Browser popup flow**: The `GET /callback` endpoint is the redirect target for browser-based OAuth. It returns an HTML page that uses `window.postMessage` to communicate the result back to the opener window.

---

## GET /cloud-storage/connections — List Connections

**Query parameters**: `?provider=google_drive&active_only=true`

**Response** `200 OK`
```json
{
  "connections": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "provider": "google_drive",
      "provider_email": "user@gmail.com",
      "provider_display_name": "John Doe",
      "is_active": true,
      "created_at": "2025-01-15T10:30:00Z",
      "last_used_at": "2025-01-15T11:00:00Z"
    }
  ],
  "total_count": 1
}
```

---

## DELETE /cloud-storage/connections/{connection_id} — Disconnect

Revokes OAuth tokens and removes the connection.

**Response** `200 OK`
```json
{"success": true, "message": "Connection disconnected successfully"}
```

---

## File Picker

The picker endpoints let you integrate Google's native file picker UI while keeping OAuth tokens server-side.

### GET /cloud-storage/connections/{connection_id}/picker-token

Returns credentials needed to initialize the Google Picker component.

**Response** `200 OK`
```json
{
  "session": {
    "session_id": "picker_sess_abc123",
    "access_token": "{google_access_token}",
    "app_id": "{google_app_id}",
    "developer_key": "{google_api_key}",
    "expires_at": "2025-01-15T11:30:00Z"
  }
}
```

### POST /cloud-storage/picker-proxy

Proxy Google Drive API calls server-side using a picker session. Keeps access tokens out of frontend JavaScript.

**Request body**
```json
{
  "session_id": "picker_sess_abc123",
  "endpoint": "files/abc123",
  "params": {
    "fields": "id,name,mimeType,size"
  }
}
```

Allowed endpoint patterns: `files`, `files/{id}`, `files/{id}/export`, `about`

**Response** `200 OK` — proxied Google Drive API response.

---

## POST /cloud-storage/import — Import Files

Import files from a connected cloud storage account. Small imports (up to a few files) complete synchronously; large imports create a background job.

**Request body**
```json
{
  "connection_id": "550e8400-e29b-41d4-a716-446655440000",
  "files": [
    {
      "id": "gdrive_file_id_1",
      "name": "photo1.jpg",
      "mime_type": "image/jpeg",
      "size_bytes": 2048576
    }
  ],
  "auto_describe": true,
  "tags": ["imported", "drive"],
  "collection_id": "col_550e8400"
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| connection_id | string | Yes | Connected account UUID |
| files | array | Yes | Files to import (each needs at least `id` and `name`) |
| auto_describe | boolean | No | Run AI description on import. Default: `true` |
| tags | string[] | No | Tags to apply to imported files |
| collection_id | string | No | Target collection |

**Response** `200 OK`

Sync (small import):
```json
{
  "image_ids": ["img_001", "img_002"],
  "job_id": null,
  "status": null,
  "total_files": 2,
  "is_async": false,
  "message": "2 files imported successfully"
}
```

Async (large import):
```json
{
  "image_ids": null,
  "job_id": "job_550e8400",
  "status": "pending",
  "total_files": 50,
  "is_async": true,
  "message": "Import job created"
}
```

Poll `GET /cloud-storage/jobs/{job_id}` for async progress.

---

## POST /cloud-storage/export — Export Files

Upload images from Aionvision to a connected cloud storage account. Always async.

**Request body**
```json
{
  "connection_id": "550e8400-e29b-41d4-a716-446655440000",
  "image_ids": ["img_001", "img_002"],
  "folder_id": "gdrive_folder_id",
  "folder_name": "Aionvision Export"
}
```

**Response** `200 OK`
```json
{
  "job_id": "job_660f9500",
  "job_status": "pending",
  "is_async": true,
  "message": "Export job created"
}
```

---

## GET /cloud-storage/jobs/{job_id} — Job Status

Poll this endpoint to track import or export progress.

**Response** `200 OK`
```json
{
  "job": {
    "job_id": "job_550e8400",
    "type": "import",
    "status": "in_progress",
    "connection_id": "550e8400-e29b-41d4-a716-446655440000",
    "provider": "google_drive",
    "total_files": 50,
    "completed_files": 30,
    "failed_files": 2,
    "error": null,
    "created_at": "2025-01-15T10:30:00Z",
    "updated_at": "2025-01-15T10:35:00Z",
    "completed_at": null
  }
}
```

`status` values: `"pending"`, `"in_progress"`, `"completed"`, `"partial"`, `"failed"`, `"cancelled"`

> **Status mapping**: The API normalizes backend statuses — `"processing"` is returned as `"in_progress"`, and `"completed_with_errors"` is returned as `"partial"`.

```python
# Poll until done
job_id = import_response.job_id
while True:
    job = await client.cloud_storage.get_job(job_id)
    if job.status in ("completed", "partial", "failed"):
        break
    await asyncio.sleep(2)
```

---

## See Also

- [Files API](files.md) — manage files after they are imported
- [Settings API](settings.md) — configure custom S3 as an alternative to cloud storage
- SDK: `client.cloud_storage` — `connect()`, `import_files()`, `export_files()`, `get_job()`
