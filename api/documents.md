# Documents API

> Base URL: `https://api.aionvision.tech/api/v2`
> Authentication: `Authorization: Bearer {api_key}`

Upload, process, and search documents with AI-powered text extraction and semantic indexing. Supported formats: PDF, DOCX, TXT, MD (max 50MB per file). Documents are processed through text extraction → content segmentation → search indexing and can be added to chat sessions for grounded AI responses.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /document-uploads/request-presigned-url | Generate presigned URL for upload |
| POST | /document-uploads/confirm | Confirm upload and trigger processing |
| GET | /document-uploads/{document_id}/status | Check processing status |
| GET | /document-uploads/quota-check | Check document quota |
| POST | /document-uploads/batch-prepare | Prepare batch upload (1-100 files) |
| POST | /document-uploads/batch-confirm | Confirm batch upload |
| GET | /document-uploads/batch/{batch_id}/status | Get batch status |
| GET | /documents | List documents |
| GET | /documents/{document_id} | Get document metadata |
| PATCH | /documents/{document_id} | Update title and tags |
| GET | /documents/{document_id}/text | Get extracted text |
| GET | /documents/{document_id}/chunks | Get document chunks |
| GET | /documents/{document_id}/download | Download original (302 redirect) |
| DELETE | /documents/{document_id} | Delete document |
| POST | /documents/batch-delete | Delete multiple documents |
| POST | /documents/search | Semantic search across documents |

---

## Document Upload Flow

Documents use a presigned URL workflow (3 steps): **request** → **upload to S3** → **confirm**.

### Step 1 — POST /document-uploads/request-presigned-url

**Request body**
```json
{
  "filename": "safety_manual.pdf",
  "content_type": "application/pdf",
  "size_bytes": 2048576,
  "storage_target": "default",
  "idempotency_key": "unique-retry-key-123"
}
```

Supported `content_type` values: `application/pdf`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`, `text/plain`, `text/markdown`

**Response** `200 OK`
```json
{
  "upload_url": "https://nyc3.digitaloceanspaces.com/bucket/presigned-url...",
  "upload_method": "PUT",
  "upload_headers": { "Content-Type": "application/pdf" },
  "object_key": "documents/{tenant_id}/{uuid}/safety_manual.pdf",
  "expires_at": "2025-01-15T10:40:00",
  "max_size_bytes": 52428800,
  "storage_target": "default"
}
```

### Step 2 — Upload to S3

```bash
curl -X PUT "{upload_url}" \
  -H "Content-Type: application/pdf" \
  --data-binary @safety_manual.pdf
```

### Step 3 — POST /document-uploads/confirm

```json
{
  "object_key": "documents/{tenant_id}/{uuid}/safety_manual.pdf",
  "size_bytes": 2048576,
  "content_type": "application/pdf",
  "checksum": "sha256:abc123def456..."
}
```

**Response** `201 Created`
```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "safety_manual.pdf",
  "document_type": "pdf",
  "status": "queued",
  "confirmed": true
}
```

**Python SDK equivalent**
```python
async with AionVision(api_key="aion_...") as client:
    result = await client.documents.upload_one("safety_manual.pdf")
    await client.documents.wait_for_processing(result.document_id)
```

---

## GET /document-uploads/{document_id}/status — Processing Status

Poll after confirming upload to track text extraction progress.

**Response** `200 OK`
```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "safety_manual.pdf",
  "document_type": "pdf",
  "text_extraction_status": "completed",
  "page_count": 15,
  "chunk_count": 42,
  "created_at": "2025-01-15T10:30:00Z",
  "processing_started_at": "2025-01-15T10:30:05Z",
  "completed_at": "2025-01-15T10:32:00Z"
}
```

`text_extraction_status` values: `"pending"`, `"processing"`, `"completed"`, `"failed"`

---

## GET /documents/{document_id}/chunks — Get Chunks

Retrieve the segmented chunks of a processed document.

**Query parameters**: `?include_embeddings=true` (default: false)

**Response** `200 OK`
```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "chunks": [
    {
      "chunk_id": "chunk_001",
      "chunk_index": 0,
      "content": "Safety inspections must be conducted quarterly...",
      "page_numbers": [12, 13],
      "heading_hierarchy": ["Chapter 3", "Inspections"],
      "similarity_score": 1.0,
      "metadata": {
        "token_count": 256,
        "chunk_type": "paragraph"
      }
    }
  ],
  "total_chunks": 42,
  "status_counts": {"completed": 42, "pending": 0, "failed": 0}
}
```

---

## POST /documents/search — Semantic Search

Search document content by meaning using AI embeddings. Returns matching chunks with similarity scores.

**Request**
```http
POST /api/v2/documents/search
Authorization: Bearer aion_your_api_key_here
Content-Type: application/json
```

**Body**
```json
{
  "query": "safety inspection requirements",
  "limit": 20,
  "similarity_threshold": 0.3,
  "document_ids": ["550e8400-e29b-41d4-a716-446655440000"]
}
```

`document_ids` is optional — omit to search all documents.

**Response** `200 OK`
```json
{
  "query": "safety inspection requirements",
  "results": [
    {
      "chunk_id": "chunk_001",
      "document_id": "550e8400-e29b-41d4-a716-446655440000",
      "document_filename": "safety_manual.pdf",
      "chunk_index": 5,
      "content": "Safety inspections must be conducted quarterly...",
      "page_numbers": [12, 13],
      "heading_hierarchy": ["Chapter 3", "Inspections", "Schedule"],
      "similarity_score": 0.87
    }
  ],
  "total_count": 15,
  "search_time_ms": 45
}
```

```bash
curl -X POST https://api.aionvision.tech/api/v2/documents/search \
  -H "Authorization: Bearer aion_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"query": "safety inspection requirements", "limit": 10}'
```

---

## Batch Upload

Upload 1–100 documents in parallel using presigned URLs.

### POST /document-uploads/batch-prepare

```json
{
  "files": [
    {"filename": "report1.pdf", "size_bytes": 1048576, "content_type": "application/pdf"},
    {"filename": "manual.docx", "size_bytes": 2097152, "content_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
  ]
}
```

Returns `batch_id` and `presigned_urls` array. Upload each file, then confirm with `POST /document-uploads/batch-confirm`.

---

## Document Management

| Operation | Endpoint | Notes |
|-----------|----------|-------|
| List | `GET /documents?page=1&page_size=20` | Filter by `status_filter`: `pending`, `processing`, `completed`, `failed` |
| Get | `GET /documents/{id}` | Returns metadata with page/chunk counts |
| Update | `PATCH /documents/{id}` | Update `title` (max 255) and `tags` (max 40) |
| Get text | `GET /documents/{id}/text` | Returns full extracted text string |
| Download | `GET /documents/{id}/download` | 302 redirect to presigned S3 URL (1 hour) |
| Delete | `DELETE /documents/{id}` | 204 No Content; 409 if currently processing |
| Batch delete | `POST /documents/batch-delete` | Max 100 per request |

---

## Limits

| Constraint | Value |
|------------|-------|
| Max file size | 50MB |
| Batch size | 1–100 documents |
| Presigned URL expiry | 10 minutes |
| Search query length | 1–1000 characters |
| Search results | 1–100 per query |
| Tags per document | Max 40 (each max 50 chars) |
| Batch delete | Max 100 per request |

---

## See Also

- [Chat API](chat.md) — add documents to chat sessions as context
- [Agents API](agents.md) — semantic document search via agents
- SDK: `client.documents` — `upload_one()`, `wait_for_processing()`, `search()`, `get_chunks()`
