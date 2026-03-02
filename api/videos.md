# Videos API

> Base URL: `https://api.aionvision.tech/api/v2`
> Authentication: `Authorization: Bearer {api_key}`

Upload large video files using a chunked multipart upload flow, track progress in real time, and retrieve AI-detected scenes after processing. Videos use a dedicated chunked upload flow — the streaming upload endpoint (`/uploads`) does not support video files.

**Supported formats**: MP4, MOV (QuickTime), M4V, WebM, AVI · **Max chunks**: 10,000 · **Max duration**: 2 hours (7,200 seconds)

> **Tier limits** — Maximum file size and chunk size vary by subscription tier. The actual chunk size is returned in the initiate response.
>
> | Tier | Max file size | Chunk size | Concurrent uploads | Max retries |
> |------|--------------|------------|--------------------|-------------|
> | Free | 1 GB | 10 MB | 2 | 1 |
> | Starter | 2 GB | 15 MB | 3 | 2 |
> | Professional | 4 GB | 20 MB | 5 | 3 |
> | Enterprise / Custom | 4 GB | 25 MB | 10 | 5 |

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /video-uploads/initiate | Start multipart upload, get presigned chunk URLs |
| POST | /video-uploads/batch/initiate | Start multipart uploads for up to 10 videos at once |
| POST | /video-uploads/chunks/confirm | Confirm a successfully uploaded chunk |
| POST | /video-uploads/complete | Finalize upload and trigger AI analysis |
| GET | /video-uploads/progress/{media_id} | Get real-time upload progress |
| POST | /video-uploads/chunks/retry | Get a new presigned URL for a failed chunk |
| POST | /video-uploads/abort | Cancel upload and clean up resources |
| GET | /video-analysis/jobs/{analysis_job_id} | Get analysis job status by job ID |
| GET | /video-analysis/status/{media_id} | Get latest analysis status for a video |
| POST | /video-analysis/jobs/{analysis_job_id}/retry | Retry a failed or cancelled analysis job |
| POST | /video-analysis/queue | Manually queue a video for analysis |
| GET | /videos/{video_id}/scenes | List AI-detected scenes with metadata |
| GET | /video-scenes/{scene_id}/thumbnail | Get scene thumbnail image |

---

## Upload Flow

Chunked video upload requires four steps: **initiate** → **upload chunks** → **confirm each chunk** → **complete**.

### Step 1 — POST /video-uploads/initiate

Start a multipart upload session and receive presigned URLs for each chunk.

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
| `filename` | string | Yes | 1–255 characters |
| `content_type` | string | Yes | One of: `video/mp4`, `video/quicktime`, `video/x-m4v`, `video/webm`, `video/x-msvideo` |
| `size_bytes` | integer | Yes | 1 byte to 4,294,967,296 (4 GB) |
| `title` | string | No | Max 255 characters |
| `tags` | string[] | No | Max 20 tags, each 1–50 chars (letters, numbers, spaces, `-`, `_`) |
| `metadata` | object | No | Arbitrary string key-value pairs |

**Response** `201 Created`
```json
{
  "media_id": "550e8400-e29b-41d4-a716-446655440000",
  "upload_id": "multipart_upload_abc123",
  "total_chunks": 50,
  "chunk_size_bytes": 10485760,
  "storage_path": "videos/550e8400-e29b-41d4-a716-446655440000.mp4",
  "chunks": [
    {
      "chunk_number": 1,
      "size_bytes": 10485760,
      "upload_url": "https://storage.example.com/presigned-upload-url...",
      "upload_method": "PUT",
      "expires_at": "2026-02-23T11:40:00Z"
    }
  ],
  "expires_at": "2026-02-23T11:40:00Z",
  "concurrent_upload_limit": 5,
  "retry_attempts": 3
}
```

| Field | Type | Description |
|-------|------|-------------|
| `media_id` | UUID | Unique identifier for this video — use in all subsequent requests |
| `upload_id` | string | Multipart upload ID |
| `total_chunks` | integer | Number of chunks to upload |
| `chunk_size_bytes` | integer | Size of each chunk except the last |
| `storage_path` | string | Storage path where the video will be stored |
| `chunks` | array | Presigned upload instructions for each chunk |
| `chunks[].chunk_number` | integer | 1-indexed chunk number |
| `chunks[].size_bytes` | integer | Expected size of this chunk in bytes |
| `chunks[].upload_url` | string | Presigned URL — upload using PUT |
| `chunks[].upload_method` | string | Always `"PUT"` |
| `chunks[].expires_at` | string | ISO 8601 datetime when this URL expires |
| `expires_at` | string | When the entire upload session expires |
| `concurrent_upload_limit` | integer | Recommended maximum parallel chunk uploads |
| `retry_attempts` | integer | Recommended maximum retry attempts per chunk |

---

### Step 2 — Upload each chunk

Upload each chunk directly to its presigned URL using PUT. Save the `ETag` response header — you will need it in Step 3.

```bash
curl -X PUT "{chunk.upload_url}" \
  --data-binary @chunk_1.bin \
  -H "Content-Type: application/octet-stream"
```

---

### Step 3 — POST /video-uploads/chunks/confirm

Call this after successfully uploading each chunk.

**Body**
```json
{
  "media_id": "550e8400-e29b-41d4-a716-446655440000",
  "upload_id": "multipart_upload_abc123",
  "chunk_number": 1,
  "etag": "abc123def456",
  "size_bytes": 10485760
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `media_id` | UUID | Yes | From initiate response |
| `upload_id` | string | Yes | From initiate response |
| `chunk_number` | integer | Yes | 1-indexed, 1–10,000 |
| `etag` | string | Yes | ETag returned in the upload response header |
| `size_bytes` | integer | Yes | Actual size of the uploaded chunk in bytes |

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

`estimated_time_remaining` is `null` if not yet calculable.

---

### Step 4 — POST /video-uploads/complete

Finalize the upload after all chunks have been confirmed. The API assembles the multipart upload, extracts video metadata, generates a thumbnail, and optionally queues AI analysis.

**Body**
```json
{
  "media_id": "550e8400-e29b-41d4-a716-446655440000",
  "upload_id": "multipart_upload_abc123",
  "duration_seconds": 120.5,
  "auto_analyze": true,
  "analysis_provider": "google",
  "analysis_type": "full_vlm"
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `media_id` | UUID | Yes | From initiate response |
| `upload_id` | string | Yes | From initiate response |
| `duration_seconds` | float | Yes | Video duration in seconds (client-measured). Used for billing: 1 credit per minute, minimum 1. Max: 7,200 (2 hours). |
| `auto_analyze` | boolean | No | Default: `true` — queue AI analysis after upload |
| `analysis_provider` | string | No | Default: `"google"`. One of: `"google"`, `"openai"`, `"anthropic"` |
| `analysis_model` | string | No | Default: `"gemini-3-flash-preview"`. Specific model to use for analysis |
| `analysis_type` | string | No | Default: `"full_vlm"`. One of: `"full_vlm"`, `"frame_sample"`, `"scene_detection"`, `"transcript"` |
| `duration_extraction_failed` | boolean | No | Default: `false`. Set to `true` if client-side duration extraction failed — the backend will reconcile using ffprobe |

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
    "bitrate_kbps": 8000,
    "file_size_bytes": 524288000,
    "format_name": "mp4"
  },
  "video_url": "https://cdn.aionvision.tech/videos/...",
  "thumbnail_url": "https://cdn.aionvision.tech/thumbnails/...",
  "analysis_job_id": "990c2800-c62f-85b8-eb5a-880099880444",
  "created_at": "2026-02-23T10:30:00Z"
}
```

`processing_status` values: `"pending"`, `"queued"`, `"processing"`, `"completed"`, `"failed"`. This endpoint returns `"queued"` immediately after the upload is assembled — metadata extraction and thumbnail generation happen asynchronously.

`thumbnail_url` and `analysis_job_id` are `null` if no thumbnail was generated or `auto_analyze` was `false`. `audio_codec` is `null` for videos with no audio track.

---

## GET /video-uploads/progress/{media_id} — Track Progress

Poll this endpoint during upload to get real-time progress.

**Response** `200 OK`
```json
{
  "media_id": "550e8400-e29b-41d4-a716-446655440000",
  "upload_id": "multipart_upload_abc123",
  "status": "uploading",
  "chunks_completed": 25,
  "total_chunks": 50,
  "bytes_uploaded": 262144000,
  "total_bytes": 524288000,
  "progress_percent": 50.0,
  "estimated_time_remaining": 120,
  "current_chunk": 26,
  "failed_chunks": [],
  "last_updated": "2026-02-23T10:35:00Z"
}
```

`status` values: `"uploading"`, `"processing"`, `"completed"`, `"failed"`, `"aborted"`

`estimated_time_remaining` and `current_chunk` are `null` if not yet calculable.

---

## Error Recovery

### POST /video-uploads/chunks/retry

Get a new presigned URL for a failed chunk. Retry limits are based on your subscription tier.

**Body**
```json
{
  "media_id": "550e8400-e29b-41d4-a716-446655440000",
  "upload_id": "multipart_upload_abc123",
  "chunk_number": 5
}
```

**Response** `200 OK`
```json
{
  "chunk_number": 5,
  "upload_url": "https://storage.example.com/presigned-retry-url...",
  "expires_at": "2026-02-23T11:40:00Z",
  "retry_attempt": 1,
  "max_retries": 3
}
```

---

### POST /video-uploads/abort

Cancel an in-progress upload and clean up all uploaded resources.

**Body**
```json
{
  "media_id": "550e8400-e29b-41d4-a716-446655440000",
  "upload_id": "multipart_upload_abc123",
  "reason": "User cancelled"
}
```

`reason` is optional, max 500 characters.

**Response** `200 OK`
```json
{
  "media_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "aborted",
  "cleaned_up": true,
  "chunks_removed": 25,
  "s3_cleanup": true
}
```

---

## Batch Upload

### POST /video-uploads/batch/initiate

Start upload sessions for up to 10 videos in a single request. Returns presigned chunk URLs for all videos so uploads can proceed in parallel. Each video then follows the same confirm and complete steps independently.

**Body**
```json
{
  "videos": [
    {
      "filename": "video1.mp4",
      "content_type": "video/mp4",
      "size_bytes": 104857600
    },
    {
      "filename": "video2.mp4",
      "content_type": "video/mp4",
      "size_bytes": 209715200
    }
  ],
  "processing_priority": "normal"
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `videos` | array | Yes | 1–10 video upload requests, each following the initiate request schema |
| `auto_process` | boolean | No | Default: `true` |
| `processing_priority` | string | No | Default: `"normal"`. One of: `"low"`, `"normal"`, `"high"` |

**Response** `201 Created`
```json
{
  "batch_id": "aabbccdd-1234-5678-abcd-000000000001",
  "videos": [ ],
  "total_videos": 2,
  "total_size_bytes": 314572800,
  "estimated_time_seconds": 30.0,
  "processing_priority": "normal"
}
```

`videos` is an array of initiate responses, one per video, in the same order as the request.

---

## Video Analysis

AI analysis runs automatically when `auto_analyze: true` is set in the complete request. These endpoints let you check job status, re-trigger analysis, or manually queue analysis for an already-uploaded video.

### GET /video-analysis/jobs/{analysis_job_id}

Get the status and progress of a video analysis job by its job ID. The `analysis_job_id` is returned by the complete endpoint when `auto_analyze` is `true`.

**Response** `200 OK`
```json
{
  "analysis_job_id": "990c2800-c62f-85b8-eb5a-880099880444",
  "media_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress_percent": 45,
  "current_step": "Extracting frames",
  "started_at": "2026-02-23T10:31:00Z",
  "completed_at": null,
  "error_message": null,
  "error_code": null,
  "retry_count": 0,
  "max_retries": 3,
  "estimated_completion_time": "2026-02-23T10:34:00Z"
}
```

`status` values: `"pending"`, `"uploading_to_vlm"`, `"processing"`, `"completed"`, `"failed"`, `"cancelled"`

`current_step`, `started_at`, `completed_at`, `error_message`, `error_code`, and `estimated_completion_time` are `null` when not applicable.

---

### GET /video-analysis/status/{media_id}

Get the latest analysis job status for a video by its media ID. Returns the most recently queued job for that video. Useful when you have the media ID but not the analysis job ID.

Same response schema as `GET /video-analysis/jobs/{analysis_job_id}`.

---

### POST /video-analysis/jobs/{analysis_job_id}/retry — `202 Accepted`

Retry a failed or cancelled analysis job. Resets the job to `"pending"` and re-queues it with high priority. Only jobs with status `"failed"` or `"cancelled"` can be retried.

**Body**
```json
{
  "media_id": "550e8400-e29b-41d4-a716-446655440000",
  "reason": "Provider timeout"
}
```

`reason` is optional, max 500 characters.

**Response** `202 Accepted`
```json
{
  "analysis_job_id": "990c2800-c62f-85b8-eb5a-880099880444",
  "media_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "retry_count": 1,
  "max_retries": 3,
  "message": "Analysis retry queued (attempt 1/3)"
}
```

---

### POST /video-analysis/queue — `202 Accepted`

Manually queue an already-uploaded video for analysis. Useful for re-analysis or when `auto_analyze` was `false` at upload time. If a job is already pending or processing for this video, the existing job is returned.

**Body**
```json
{
  "media_id": "550e8400-e29b-41d4-a716-446655440000",
  "analysis_type": "full_vlm",
  "priority": "normal"
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `media_id` | UUID | Yes | Video to analyze |
| `analysis_type` | string | No | Default: `"full_vlm"`. One of: `"full_vlm"`, `"frame_sample"`, `"scene_detection"` |
| `priority` | string | No | Default: `"normal"`. One of: `"low"`, `"normal"`, `"high"` |

**Response** `202 Accepted`
```json
{
  "analysis_job_id": "990c2800-c62f-85b8-eb5a-880099880444",
  "media_id": "550e8400-e29b-41d4-a716-446655440000",
  "queue_position": 3,
  "estimated_start_time": "2026-02-23T10:33:00Z",
  "message": "Video analysis job queued successfully"
}
```

`estimated_start_time` is `null` if the queue position cannot be estimated.

---

## GET /videos/{video_id}/scenes — List Scenes

After AI analysis completes, retrieve the detected scenes with timestamps, descriptions, and thumbnail URLs. Returns an empty `scenes` array if analysis has not completed yet.

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
      "embedding_status": "completed",
      "thumbnail_url": "/api/v2/video-scenes/a1b2c3d4-e5f6-7890-abcd-ef1234567890/thumbnail",
      "created_at": "2026-02-23T10:45:00Z"
    }
  ]
}
```

`visible_text`, `thumbnail_url`, and `created_at` are `null` if not available. `embedding_status` indicates whether semantic search embeddings have been generated for this scene (`"pending"` or `"completed"`).

---

## GET /video-scenes/{scene_id}/thumbnail

Returns the JPEG thumbnail for a scene, generated at the scene midpoint during analysis.

```
Content-Type: image/jpeg
Cache-Control: public, max-age=31536000
Content-Disposition: inline; filename="scene_{scene_id}.jpg"
```

Returns `404` if no thumbnail has been generated for the scene yet.

---

## See Also

- [Files API](files.md) — list uploaded videos with `?media_types=video`, access `video_metadata`, `video_analysis_status`, `scene_count`, and `video_url` fields
- [Uploads API](uploads.md) — streaming upload for images and documents (does not support video)
