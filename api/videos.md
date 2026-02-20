# Videos API

> Video upload and AI-powered scene detection is coming soon.

Video features including chunked multipart upload, real-time progress tracking, and automatic scene extraction with AI analysis are currently in development and not yet available via the API.

This page will be updated with full endpoint documentation when the feature launches.

<!--
HIDDEN: Video API documentation — uncomment to restore when video features are enabled.

> Base URL: `https://api.aionvision.tech/api/v2`
> Authentication: `Authorization: Bearer {api_key}`

Upload large video files using a chunked multipart upload flow, track progress in real time, and retrieve AI-detected scenes after processing. Videos are not available via the streaming upload endpoint — use this dedicated chunked flow instead.

**Supported formats**: MP4, MOV (QuickTime), M4V, WebM, AVI · **Max size**: 10GB · **Chunk size**: 10MB per chunk · **Max chunks**: 10,000

> **Note**: This resource is documented on the website but was previously missing from this docs repo.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /video-uploads/initiate | Start multipart upload, get presigned chunk URLs |
| POST | /video-uploads/chunks/confirm | Confirm an uploaded chunk |
| POST | /video-uploads/complete | Finalize upload and trigger AI analysis |
| GET | /video-uploads/progress/{media_id} | Get real-time upload progress |
| POST | /video-uploads/chunks/retry | Get new presigned URL for a failed chunk |
| POST | /video-uploads/abort | Cancel upload and clean up S3 resources |
| GET | /videos/{video_id}/scenes | List detected video scenes |
| GET | /video-scenes/{scene_id}/thumbnail | Get scene thumbnail image |

---

## Upload Flow

Chunked video upload requires 4 steps: **initiate** → **upload chunks to S3** → **confirm each chunk** → **complete**.

### Step 1 — POST /video-uploads/initiate

**Request**
```http
POST /api/v2/video-uploads/initiate
Authorization: Bearer aion_your_api_key_here
Content-Type: application/json
```

**Body**
```json
{
  "filename": "inspection.mp4",
  "content_type": "video/mp4",
  "size_bytes": 524288000,
  "title": "Site Inspection Video",
  "tags": ["inspection", "site-a"]
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| filename | string | Yes | 1–255 characters |
| content_type | string | Yes | `video/mp4`, `video/quicktime`, `video/x-m4v`, `video/webm`, `video/x-msvideo` |
| size_bytes | integer | Yes | 1 byte to 10,737,418,240 (10GB) |
| title | string | No | Max 255 characters |
| tags | string[] | No | Max 20 tags, each 1–50 chars (letters, numbers, spaces, `-`, `_`) |
| metadata | object | No | Arbitrary key-value metadata |

**Response** `201 Created`
```json
{
  "media_id": "550e8400-e29b-41d4-a716-446655440000",
  "upload_id": "multipart_upload_abc123",
  "total_chunks": 50,
  "chunk_size_bytes": 10485760,
  "storage_path": "tenants/abc/videos/550e8400.mp4",
  "chunks": [
    {
      "chunk_number": 1,
      "size_bytes": 10485760,
      "upload_url": "https://s3.amazonaws.com/bucket/chunk-1...",
      "upload_method": "PUT",
      "expires_at": "2025-01-15T10:40:00Z"
    }
  ],
  "expires_at": "2025-01-15T10:40:00Z",
  "concurrent_upload_limit": 5,
  "retry_attempts": 3
}
```

### Step 2 — Upload each chunk to S3

```bash
# Upload chunk 1 to its presigned URL
curl -X PUT "{chunk.upload_url}" \
  --data-binary @chunk_1.bin \
  --header "Content-Type: application/octet-stream"
```

Save the `ETag` response header from S3 — you'll need it for confirmation.

### Step 3 — POST /video-uploads/chunks/confirm

Call this after successfully uploading each chunk.

```json
{
  "media_id": "550e8400-e29b-41d4-a716-446655440000",
  "upload_id": "multipart_upload_abc123",
  "chunk_number": 1,
  "etag": "abc123def456",
  "size_bytes": 10485760
}
```

**Response** `200 OK`
```json
{
  "chunk_number": 1,
  "status": "completed",
  "chunks_completed": 1,
  "total_chunks": 50,
  "progress_percent": 2.0,
  "estimated_time_remaining": 245
}
```

### Step 4 — POST /video-uploads/complete

Finalize the upload after all chunks are confirmed.

```json
{
  "media_id": "550e8400-e29b-41d4-a716-446655440000",
  "upload_id": "multipart_upload_abc123",
  "auto_analyze": true,
  "analysis_provider": "google",
  "analysis_type": "full_vlm"
}
```

| Parameter | Description |
|-----------|-------------|
| `auto_analyze` | Default: `true` — queue AI analysis after upload |
| `analysis_provider` | `"google"` (default), `"openai"`, or `"anthropic"` |
| `analysis_type` | `"full_vlm"` (default), `"frame_sample"`, `"scene_detection"`, `"transcript"` |

**Response** `200 OK`
```json
{
  "media_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "processing_status": "queued",
  "metadata": {
    "duration_seconds": 120.5,
    "resolution": "1920x1080",
    "width": 1920,
    "height": 1080,
    "frame_rate": 30.0,
    "video_codec": "h264",
    "audio_codec": "aac",
    "file_size_bytes": 524288000
  },
  "video_url": "https://cdn.aionvision.tech/videos/...",
  "thumbnail_url": "https://cdn.aionvision.tech/thumbnails/...",
  "analysis_job_id": "990c2800-c62f-85b8-eb5a-880099880444",
  "created_at": "2025-01-15T10:30:00Z"
}
```

**Python SDK — complete upload loop**
```python
import asyncio

async def upload_video(path: str):
    async with AionVision(api_key="aion_...") as client:
        # Initiate
        session = await client.uploads.initiate_video(path)

        # Upload chunks in parallel (up to concurrent_upload_limit)
        chunk_size = session.chunk_size_bytes
        with open(path, "rb") as f:
            for i, chunk_info in enumerate(session.chunks):
                chunk_data = f.read(chunk_size)
                etag = await upload_chunk_to_s3(chunk_info.upload_url, chunk_data)
                await client.uploads.confirm_video_chunk(
                    media_id=session.media_id,
                    upload_id=session.upload_id,
                    chunk_number=i + 1,
                    etag=etag,
                    size_bytes=len(chunk_data)
                )

        # Complete
        result = await client.uploads.complete_video(
            media_id=session.media_id,
            upload_id=session.upload_id
        )
        return result.media_id
```

---

## GET /video-uploads/progress/{media_id} — Track Progress

**Response** `200 OK`
```json
{
  "media_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "uploading",
  "chunks_completed": 25,
  "total_chunks": 50,
  "bytes_uploaded": 262144000,
  "total_bytes": 524288000,
  "progress_percent": 50.0,
  "estimated_time_remaining": 120,
  "current_chunk": 26,
  "failed_chunks": [],
  "last_updated": "2025-01-15T10:35:00Z"
}
```

`status` values: `"uploading"`, `"processing"`, `"completed"`, `"failed"`, `"aborted"`

---

## Error Recovery

### POST /video-uploads/chunks/retry

Get a new presigned URL for a failed chunk.

```json
{
  "media_id": "550e8400-e29b-41d4-a716-446655440000",
  "upload_id": "multipart_upload_abc123",
  "chunk_number": 5
}
```

**Response**: `{"chunk_number": 5, "upload_url": "...", "retry_attempt": 1, "max_retries": 3}`

### POST /video-uploads/abort

Cancel an in-progress upload and clean up S3 resources.

```json
{
  "media_id": "550e8400-e29b-41d4-a716-446655440000",
  "upload_id": "multipart_upload_abc123",
  "reason": "User cancelled"
}
```

**Response**: `{"status": "aborted", "cleaned_up": true, "chunks_removed": 25}`

---

## GET /videos/{video_id}/scenes — List Scenes

After AI analysis completes, retrieve detected scenes with timestamps and descriptions.

**Response** `200 OK`
```json
{
  "video_id": "550e8400-e29b-41d4-a716-446655440000",
  "count": 3,
  "scenes": [
    {
      "scene_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "scene_index": 0,
      "start_time": 0.0,
      "end_time": 45.0,
      "time_range_formatted": "0:00-0:45",
      "description": "Exterior view of the building entrance",
      "tags": ["exterior", "entrance"],
      "visible_text": "Building A - Main Entrance",
      "confidence_score": 0.92,
      "thumbnail_url": "/api/v2/video-scenes/a1b2c3d4-e5f6-7890-abcd-ef1234567890/thumbnail",
      "created_at": "2025-01-15T10:45:00Z"
    }
  ]
}
```

## GET /video-scenes/{scene_id}/thumbnail

Returns the JPEG scene thumbnail (generated at scene midpoint). Cached with 1-year `Cache-Control`.

```
Content-Type: image/jpeg
Cache-Control: public, max-age=31536000
```

---

## See Also

- [Files API](files.md) — list uploaded videos (`?media_types=video`) and manage metadata
- [Uploads API](uploads.md) — streaming upload for images and documents
-->
