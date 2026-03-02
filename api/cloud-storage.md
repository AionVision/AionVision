# Cloud Storage API

> Base URL: `https://api.aionvision.tech/api/v2`
> Authentication: `Authorization: Bearer {api_key}` for most endpoints. OAuth flow endpoints and picker endpoints require session authentication — see individual sections below.

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

> **Auth**: Session authentication required. API key auth is not supported — a user session is needed to associate the OAuth connection with a specific user.

**Request**
```http
POST /api/v2/cloud-storage/auth/google_drive
Cookie: session=your_session_token
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

> **Auth**: Session authentication required. API key auth is not supported.

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

> **API key scope**: `read` or `cloud_storage:read`

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

> **API key scope**: `write`, `admin`, or `cloud_storage:delete`

Revokes OAuth tokens and removes the connection.

**Response** `200 OK`
```json
{"success": true, "message": "Connection disconnected successfully"}
```

**Errors**
- `404` — Connection not found
- `403` — Not authorized to disconnect this connection

---

## File Picker

The picker endpoints let you integrate Google's native file picker UI while keeping OAuth tokens server-side.

### GET /cloud-storage/connections/{connection_id}/picker-token

> **Auth**: Session authentication required. API key auth is not supported — access tokens must be kept server-side and scoped to the authenticated user.

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

**Errors**
- `404` — Connection not found
- `403` — Not authorized for this connection
- `401` — OAuth token expired and requires re-authorization; response includes `"requires_reauth": true`

### POST /cloud-storage/picker-proxy

> **Auth**: Session authentication required. API key auth is not supported.

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

**Response** `200 OK`
```json
{
  "data": {
    "id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms",
    "name": "photo.jpg",
    "mimeType": "image/jpeg",
    "size": "2048576"
  }
}
```

The Google Drive API response is wrapped in a `data` field. The structure of `data` depends on which Drive endpoint was proxied.

**Errors**
- `401` — Picker session expired; obtain a new token via `GET /picker-token`
- `400` — Invalid or disallowed endpoint pattern
- `403` — Access denied by Google API
- `404` — Resource not found in Google Drive
- `502` — Failed to reach the Google API

---

## POST /cloud-storage/import — Import Files

> **API key scope**: `write` or `cloud_storage:write`

Import files from a connected cloud storage account. All imports are processed asynchronously via a background job. Placeholder image records are created immediately and returned in `image_ids` so you can reference the files right away; actual file transfer from cloud storage happens in the background.

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
```json
{
  "image_ids": ["550e8400-e29b-41d4-a716-446655440000", "660f9500-f39c-52e5-b827-557766550111"],
  "job_id": "job_550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "total_files": 2,
  "is_async": true,
  "message": "Importing 2 files"
}
```

`image_ids` contains placeholder UUIDs for the files being imported — these IDs are valid immediately and can be used to reference the files before transfer completes. `is_async` is always `true`. Poll `GET /cloud-storage/jobs/{job_id}` for progress.

**Errors**
- `404` — Connection not found
- `403` — Not authorized for this connection
- `429` — Usage limit exceeded
- `507` — Storage quota exceeded
- `400` — Invalid request (e.g. no files specified)

---

## POST /cloud-storage/export — Export Files

> **API key scope**: `write` or `cloud_storage:write`

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
  "cloud_file_ids": null,
  "job_id": "job_660f9500-e29b-41d4-a716-446655440000",
  "job_status": "pending",
  "is_async": true,
  "message": "Export job created"
}
```

`cloud_file_ids` is populated with cloud storage file IDs once the export completes; it is `null` while the job is still in progress. Poll `GET /cloud-storage/jobs/{job_id}` for progress.

**Errors**
- `404` — Connection not found
- `403` — Not authorized to export to this connection
- `400` — Invalid request

---

## GET /cloud-storage/jobs/{job_id} — Job Status

> **API key scope**: `read` or `cloud_storage:read`

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
