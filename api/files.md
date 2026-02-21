# Files API

> Base URL: `https://api.aionvision.tech/api/v2`
> Authentication: `Authorization: Bearer {api_key}`

Manage uploaded images, documents, and saved website links. Supports full-text search, tag and date filtering, folder organization, and batch operations. Files are soft-deleted with a 30-day recovery window.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /user-files/upload/initiate | Initiate presigned URL upload (max 50MB) |
| POST | /user-files/upload/confirm | Confirm presigned URL upload |
| POST | /user-files/upload/stream | Stream upload single file |
| POST | /user-files/upload/stream-batch | Stream upload multiple files |
| GET | /user-files | List files with search and filtering |
| GET | /user-files/{file_id} | Get file details |
| GET | /user-files/{file_id}/variant/{variant_type} | Get image variant (302 redirect) |
| GET | /user-files/{file_id}/download | Download original file (302 redirect) |
| PATCH | /user-files/{file_id} | Update title and tags |
| DELETE | /user-files/{file_id} | Soft-delete file |
| POST | /user-files/batch-delete | Delete multiple files |
| POST | /user-files/{file_id}/trigger-variants | Re-trigger variant generation |
| POST | /user-files/links | Save a website link |
| POST | /user-files/{link_id}/recrawl | Recrawl a saved link |

---

## GET /user-files — List Files

List files with full-text search, filtering, and pagination.

**Request**
```http
GET /api/v2/user-files?search=damage+report&limit=20
Authorization: Bearer aion_your_api_key_here
```

**Query Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| search | string | Full-text search across descriptions and visible text |
| search_mode | string | `"all"` (default), `"metadata"`, or `"visible_text"` |
| tags | string | Comma-separated tag filter (e.g. `"safety,inspection"`) |
| media_types | string | Comma-separated: `"image"`, `"document"`, `"link"` <!-- "video" coming soon --> |
| folder_id | string | Filter by folder UUID |
| has_description | boolean | Filter by description status |
| ids | string | Comma-separated file UUIDs (max 500) |
| date_from | string | ISO 8601 timestamp |
| date_to | string | ISO 8601 timestamp |
| sort_by | string | `"content_created_at"` (default), `"created_at"`, `"title"`, `"size_bytes"` |
| sort_order | string | `"desc"` (default) or `"asc"` |
| limit | integer | 1–100, default 20 |
| offset | integer | Default 0 |

**Response** `200 OK`
```json
{
  "files": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Site Photo A",
      "filename": "site_photo.jpg",
      "thumbnail_url": "https://cdn.aionvision.tech/thumbs/...",
      "upload_description": "Damaged concrete pillar with visible cracks...",
      "visible_text": "WARNING: STRUCTURAL DAMAGE",
      "tags": ["damage", "concrete"],
      "size_bytes": 2048576,
      "created_at": "2025-01-15T10:30:00Z",
      "content_created_at": "2025-01-14T08:00:00Z",
      "has_full_description": true,
      "dimensions": {"width": 4000, "height": 3000},
      "format": "jpeg",
      "variant_status": "completed",
      "medium_url": "https://cdn.aionvision.tech/medium/...",
      "blur_hash": "L6PZfSi_.AyE_3t7t7R**0o#DgR4",
      "description_status": "completed",
      "confidence_score": 0.95,
      "media_type": "image"
    }
  ],
  "total_count": 150,
  "has_more": true
}
```

Additional fields by `media_type`:
<!-- - `"video"`: `video_metadata`, `video_analysis_status`, `scene_count` (coming soon) -->
- `"document"`: `document_type`, `page_count`, `text_extraction_status`, `chunk_count`
- `"link"`: `source_url`, `domain`, `og_metadata`, `favicon_url`, `crawl_status`

**Example**
```bash
curl "https://api.aionvision.tech/api/v2/user-files?search=damaged+equipment&media_types=image&limit=50" \
  -H "Authorization: Bearer aion_your_api_key_here"
```
```python
async with AionVision(api_key="aion_...") as client:
    files = await client.files.list(search="damaged equipment", media_types=["image"])
```

---

## GET /user-files/{file_id} — Get File Details

Get full file metadata including processing history and all variant URLs. Accepts full UUID or 8-character prefix.

**Response** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Site Photo A",
  "tags": ["damage", "concrete"],
  "size_bytes": 2048576,
  "dimensions": {"width": 4000, "height": 3000},
  "full_url": "https://cdn.aionvision.tech/large/...",
  "thumbnail_url": "https://cdn.aionvision.tech/thumbs/...",
  "medium_url": "https://cdn.aionvision.tech/medium/...",
  "original_url": "https://cdn.aionvision.tech/originals/...",
  "variant_status": "completed",
  "variant_count": 5,
  "upload_description": "Damaged concrete pillar...",
  "visible_text": "WARNING: STRUCTURAL DAMAGE",
  "full_descriptions": [
    {
      "id": "770a0600-e29b-41d4-a716-446655440000",
      "description": "Image shows a concrete pillar with visible cracks...",
      "confidence_score": 0.92,
      "processing_time_ms": 1850,
      "created_at": "2025-01-15T10:32:00Z"
    }
  ],
  "processing_history": [
    {
      "operation_type": "describe",
      "status": "completed",
      "created_at": "2025-01-15T10:30:05Z",
      "completed_at": "2025-01-15T10:32:00Z"
    }
  ],
  "description_status": "completed",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:35:00Z",
  "media_type": "image"
}
```

---

## PATCH /user-files/{file_id} — Update Metadata

Update file title and/or tags. Both fields are optional.

**Request**
```http
PATCH /api/v2/user-files/550e8400-e29b-41d4-a716-446655440000
Authorization: Bearer aion_your_api_key_here
Content-Type: application/json
```

**Body**
```json
{
  "title": "Updated Photo Title",
  "tags": ["updated", "reviewed"]
}
```

| Field | Constraints |
|-------|-------------|
| title | Optional, max 255 characters |
| tags | Optional, max 40 tags, each max 50 characters |

**Response** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Updated Photo Title",
  "tags": ["updated", "reviewed"],
  "updated_at": "2025-01-15T11:00:00Z"
}
```

---

## DELETE /user-files/{file_id} — Delete File

Soft-delete a file and its variants. Recoverable within 30 days via the dashboard.

**Response** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "deleted_at": "2025-01-15T11:00:00Z",
  "message": "File deleted successfully"
}
```

---

## POST /user-files/batch-delete — Batch Delete

Delete 1–100 files in one request. Returns per-file success/failure.

**Request body**
```json
{
  "file_ids": [
    "550e8400-e29b-41d4-a716-446655440000",
    "660f9500-f39c-52e5-b827-557766550111"
  ]
}
```

**Response** `200 OK`
```json
{
  "deleted": [
    {"id": "550e8400-e29b-41d4-a716-446655440000", "status": "deleted", "deleted_at": "2025-01-15T11:00:00Z"}
  ],
  "skipped": [],
  "failed": [
    {"id": "660f9500-f39c-52e5-b827-557766550111", "status": "failed", "message": "File not found"}
  ],
  "summary": {"total": 2, "deleted": 1, "skipped": 0, "failed": 1}
}
```

---

## Image Variants

`GET /user-files/{file_id}/variant/{variant_type}` returns a `302` redirect to a presigned S3 URL (expires in 1 hour).

| Variant | Size |
|---------|------|
| `original` | Original uploaded file |
| `tiny_64` | 64px max dimension |
| `small_256` | 256px max dimension |
| `medium_750` | 750px (recommended) |
| `large_1024` | 1024px max dimension |

---

## Website Links

Save URLs for reference. Links are automatically crawled to extract Open Graph metadata, favicon, and page content for AI search.

### POST /user-files/links

```json
{
  "url": "https://github.com/example/repo",
  "title": "My Favorite Repo",
  "tags": ["development", "reference"],
  "folder_id": "550e8400-e29b-41d4-a716-446655440000",
  "auto_crawl": true
}
```

**Response** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "source_url": "https://github.com/example/repo",
  "domain": "github.com",
  "crawl_status": "queued",
  "created_at": "2025-01-15T10:30:00Z"
}
```

Links appear in `GET /user-files` with `media_type: "link"`. Filter with `?media_types=link`. Recrawl with `POST /user-files/{link_id}/recrawl` (rate limited to once per hour).

---

## See Also

- [Uploads API](uploads.md) — upload new files
- [Folders API](folders.md) — organize files into folders
- SDK: `client.files` — `list()`, `get()`, `update()`, `delete()`, `batch_delete()`
