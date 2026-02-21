# Aionvision API & Python SDK Documentation

Aionvision is a Vision AI platform that provides AI-powered image description, document processing, semantic search, agentic chat, and file management. This repository contains the public API specification and Python SDK reference for building applications with Aionvision.

## Installation

The SDK is distributed via a private package index authenticated with your API key.

```bash
pip install aion --extra-index-url https://aion:YOUR_API_KEY@api.aionvision.tech/api/v2/sdk/simple/
```

Replace `YOUR_API_KEY` with your Aionvision API key (format: `aion_...`). Create one from your [Dashboard](https://aionvision.tech/dashboard) under API Keys.

Optional extras:
```bash
pip install "aion[dotenv]" --extra-index-url https://aion:YOUR_API_KEY@api.aionvision.tech/api/v2/sdk/simple/    # .env file support
pip install "aion[tracing]" --extra-index-url https://aion:YOUR_API_KEY@api.aionvision.tech/api/v2/sdk/simple/   # OpenTelemetry tracing
```

To avoid repeating the URL, add it to your pip config:
```ini
# ~/.pip/pip.conf (Linux/macOS) or %APPDATA%\pip\pip.ini (Windows)
[global]
extra-index-url = https://aion:YOUR_API_KEY@api.aionvision.tech/api/v2/sdk/simple/
```

Then simply run `pip install aion`.

## Quick Start

### Async Client (recommended)

```python
import asyncio
from aion import AionVision

async def main():
    async with AionVision(api_key="aion_...") as client:
        # Upload an image with automatic AI description
        result = await client.upload_one("photo.jpg")
        print(result.description)

        # Chat with your image library
        async with client.chat_session() as session:
            response = await session.send("Find damaged poles")
            print(response.content)

asyncio.run(main())
```

### Sync Client

```python
from aion import SyncAionVision

with SyncAionVision(api_key="aion_...") as client:
    result = client.upload_one("photo.jpg")
    print(result.description)

    with client.chat_session() as session:
        response = session.send("Find damaged poles")
        print(response.content)
```

### Environment Variables

```python
from aion import AionVision, load_dotenv

load_dotenv()  # Load from .env file
async with AionVision.from_env() as client:
    result = await client.upload_one("photo.jpg")
```

| Variable | Description | Default |
|----------|-------------|---------|
| `AIONVISION_API_KEY` | API key (required) | - |
| `AIONVISION_BASE_URL` | API base URL | `https://api.aionvision.tech/api/v2` |
| `AIONVISION_TIMEOUT` | Request timeout (seconds) | `300` |
| `AIONVISION_MAX_RETRIES` | Max retry attempts | `3` |
| `AIONVISION_RETRY_DELAY` | Initial retry delay (seconds) | `1.0` |
| `AIONVISION_POLLING_INTERVAL` | Polling interval (seconds) | `2.0` |
| `AIONVISION_POLLING_TIMEOUT` | Polling timeout (seconds) | `360.0` |
| `AIONVISION_TENANT_ID` | Tenant ID for multi-tenant | - |
| `AIONVISION_PROXY_URL` | Proxy URL | - |
| `AIONVISION_ENABLE_TRACING` | Enable OpenTelemetry tracing | `false` |

## Features

### Image Upload & AI Description
Upload images and get AI-generated descriptions, tags, and metadata automatically.
- Single upload: `client.upload_one("photo.jpg")`
- Batch upload: `client.upload("/path/to/photos")` — directories only expand supported image files (JPEG, PNG, WebP, GIF); non-image files are skipped. Use `client.documents.upload()` for documents.
- Progress callbacks for tracking
- Custom storage targets (default or your own S3 bucket)

See: [examples/uploading_images.py](examples/uploading_images.py)

### Document Processing
Upload PDFs, DOCX, TXT, and Markdown documents for text extraction and semantic search.
- `client.documents.upload_one("report.pdf")`
- `client.documents.search("safety procedures")`

See: [examples/uploading_documents.py](examples/uploading_documents.py), [examples/documents.py](examples/documents.py)

### Agentic Chat
AI-powered chat with your image and document library. The chat system uses specialized agents to search, analyze, and synthesize information.
- `client.chat_session()` - managed sessions
- `session.send("query")` - complete responses
- `session.send_stream("query")` - streaming tokens

See: [examples/agentic_chat.py](examples/agentic_chat.py)

### Semantic Search
Search images and documents using natural language queries via AI agents. **Standalone search agents are the most token-efficient way to search** — use these directly instead of agentic chat when you don't need multi-turn conversation.
- `client.agent_search.images("damaged poles")`
- `client.agent_search.documents("safety procedures")`

See: [examples/semantic_search.py](examples/semantic_search.py)

### Standalone Agent Operations
Run AI agents directly without chat sessions.
- `client.agent_operations.synthesize("Write a report", document_ids=[...])`
- `client.agent_operations.analyze_documents("Find key issues", document_ids=[...])`
- `client.agent_operations.organize("Sort by severity", image_ids=[...])`

See: [examples/standalone_agents.py](examples/standalone_agents.py)

### Pipelines
Chain multiple agent operations in a single workflow with typed data flow.

```python
result = await (
    client.pipeline()
    .search_images("damaged utility poles")
    .organize("Sort by damage severity")
    .run()
)
```

See: [examples/pipelines.py](examples/pipelines.py)

### File Management
List, search, filter, update, and delete uploaded files.

See: [examples/file_management.py](examples/file_management.py)

### Link Management
Create bookmarked links with automatic Open Graph metadata crawling.

See: [examples/links.py](examples/links.py)

### Folder Management
Organize files into hierarchical folders.

See: [examples/folders.py](examples/folders.py)

### Color Analysis & Search
Colors are extracted automatically on upload. Retrieve dominant colors and search by color properties.

See: [examples/colors.py](examples/colors.py)

### Cloud Storage Integration
Connect Google Drive, OneDrive, or Dropbox to import/export files.

See: [examples/cloud_storage.py](examples/cloud_storage.py)

## Authentication

All API requests require an API key passed as a Bearer token:

```
Authorization: Bearer aion_your_api_key_here
```

API keys are prefixed with `aion_` and must be at least 20 characters after the prefix.

For multi-tenant deployments, include the tenant ID header:
```
X-Tenant-ID: your-tenant-id
```

## Error Handling

The SDK provides a typed exception hierarchy:

```python
from aion.exceptions import (
    AionvisionError,        # Base exception for all SDK errors
    AuthenticationError,     # Invalid or missing API key (401)
    RateLimitError,          # Rate limit exceeded (429) - has retry_after
    ValidationError,         # Request validation failed (400/422)
    QuotaExceededError,      # Upload quota exceeded - has partial_results
    ResourceNotFoundError,   # Resource not found (404)
    AionvisionTimeoutError,  # Operation timed out - has last_result
    ServerError,             # Server error (5xx)
    AionvisionPermissionError, # Insufficient permissions (403)
    UploadError,             # Upload failed - has session_id, partial_results
    DescriptionError,        # Description generation failed
    DocumentProcessingError, # Document processing failed
    ChatError,               # Chat operation failed
    BatchError,              # Batch operation failed
    AionvisionConnectionError, # Network connection failed
    CircuitBreakerError,     # Circuit breaker open
    CloudStorageError,       # Cloud storage operation failed
    SSEStreamError,          # SSE streaming failed
)
```

Exceptions are also accessible as class attributes: `AionVision.AuthenticationError`, `AionVision.RateLimitError`, etc.

See: [examples/error_handling.py](examples/error_handling.py)

## Result Types Quick Reference

Every SDK method returns a typed dataclass. Here are the fields for the most commonly used result types. For the complete definitions, see the type stubs in [`sdk/python/aion/types/`](sdk/python/aion/types/).

### Upload Results

**`UploadResult`** (from `client.upload_one()`):
| Field | Type | Description |
|-------|------|-------------|
| `image_id` | `str` | Unique image identifier |
| `filename` | `str` | Uploaded filename |
| `object_key` | `str` | S3/storage object key |
| `description` | `str \| None` | AI-generated description |
| `tags` | `list[str] \| None` | AI-generated tags |
| `visible_text` | `str \| None` | OCR-extracted text from image |
| `confidence_score` | `float \| None` | AI confidence score (0-1) |
| `description_status` | `DescriptionStatus` | Enum: `"pending"`, `"queued"`, `"processing"`, `"completed"`, `"failed"`, `"skipped"` |
| `thumbnail_url` | `str \| None` | Thumbnail URL |
| `created_at` | `datetime \| None` | Upload timestamp |
| `description_error` | `str \| None` | Error message if failed |
| `description_error_type` | `str \| None` | Error classification (e.g. `"timeout"`, `"vlm_error"`) |
| `description_is_retryable` | `bool \| None` | Whether a failed description can be retried |
| `is_failed` | `bool` (property) | Whether description generation failed |
| `is_completed` | `bool` (property) | Whether description generation completed successfully |
| `is_pending` | `bool` (property) | Whether description is still pending/processing |

**`BatchUploadResults`** (from `client.upload()`):

Extends `list[UploadResult]` — iterate directly, no `.results` attribute.

```python
results = await client.upload(["a.jpg", "b.jpg"])
len(results)                # number of uploads
results[0].image_id         # access individual results
for r in results: ...       # iterate directly
```

| Property/Method | Type | Description |
|-----------------|------|-------------|
| `has_failures` | `bool` | True if any descriptions failed |
| `succeeded_count` | `int` | Number of successful descriptions |
| `failed_count` | `int` | Number of failed descriptions |
| `pending_count` | `int` | Number still pending |
| `succeeded()` | `list[UploadResult]` | All successful results |
| `failed()` | `list[UploadResult]` | All failed results |
| `pending()` | `list[UploadResult]` | All results still pending |
| `retryable()` | `list[UploadResult]` | Failed results that can be retried |
| `raise_on_failures()` | `BatchUploadResults` | Raise `DescriptionError` if any failed; returns self for chaining |
| `summary()` | `str` | Human-readable summary, e.g. `"3 succeeded, 1 failed (1 retryable)"` |

### File Results

**`FileList`** (from `client.files.list()`):
| Field | Type | Description |
|-------|------|-------------|
| `files` | `list[UserFile]` | List of file summaries |
| `total_count` | `int` | Total matching files (not just this page) |
| `has_more` | `bool` | Whether more pages exist |

**`UserFile`** (items in `FileList.files`):
| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Unique file identifier |
| `size_bytes` | `int` | File size in bytes |
| `has_full_description` | `bool` | Whether full AI descriptions exist |
| `title` | `str \| None` | User-set or auto-generated title |
| `filename` | `str \| None` | Display filename |
| `thumbnail_url` | `str \| None` | Thumbnail URL |
| `upload_description` | `str \| None` | AI description |
| `visible_text` | `str \| None` | OCR-extracted text from image |
| `tags` | `list[str] \| None` | Tags |
| `created_at` | `datetime \| None` | Upload timestamp |
| `content_created_at` | `datetime \| None` | Actual content creation date (from EXIF metadata) |
| `dimensions` | `dict[str, int] \| None` | Image dimensions `{width, height}`. May be `{}` (empty dict) if dimension extraction has not completed; not all images will have dimensions populated. |
| `format` | `str \| None` | Image format (jpeg, png, etc.) |
| `variant_status` | `str \| None` | Variant generation status (pending/processing/completed/failed) |
| `variant_count` | `int \| None` | Number of generated variants |
| `medium_url` | `str \| None` | Medium variant URL |
| `full_url` | `str \| None` | Full-size variant URL |
| `blur_hash` | `str \| None` | BlurHash string for blur-up placeholder loading |
| `description_status` | `str \| None` | AI description generation status |
| `description_error` | `str \| None` | Error message if description failed |
| `content_type` | `str \| None` | MIME type (image/jpeg, application/pdf, etc.) |
| `media_type` | `str \| None` | Computed type: `"image"`, `"document"`, or `"link"` |
<!-- VIDEO FIELDS (coming soon):
| `video_metadata` | `dict \| None` | Video-specific metadata (duration, resolution, codecs) |
| `video_analysis_status` | `str \| None` | Video analysis job status |
| `video_analysis_job_id` | `str \| None` | Video analysis job ID |
| `scene_count` | `int \| None` | Number of scenes detected in video |
| `has_audio_transcript` | `bool \| None` | Whether audio transcript exists |
| `video_url` | `str \| None` | URL to original playable video (videos only) |
-->

**`UserFileDetails`** (from `client.files.get()`):

Separate dataclass (not a subclass of `UserFile`). Full fields:
| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Unique file identifier |
| `object_key` | `str` | S3/storage object key |
| `size_bytes` | `int` | File size in bytes |
| `content_type` | `str` | MIME type of the file |
| `hash` | `str` | File hash |
| `title` | `str \| None` | Title |
| `tags` | `list[str] \| None` | Tags |
| `dimensions` | `dict[str, int] \| None` | Image dimensions `{width, height}`. May be `{}` (empty dict) if dimension extraction has not completed; not all images will have dimensions populated. |
| `format` | `str \| None` | Image format (jpeg, png, etc.) |
| `full_url` | `str \| None` | Full-size variant URL (1024px; None if variants not yet generated) |
| `thumbnail_url` | `str \| None` | Thumbnail URL |
| `medium_url` | `str \| None` | Medium-size variant URL |
| `original_url` | `str \| None` | URL to original file (always available as fallback) |
| `upload_description` | `str \| None` | AI description |
| `visible_text` | `str \| None` | OCR-extracted text |
| `description_generated_at` | `datetime \| None` | When AI description was generated |
| `full_descriptions` | `list[FullDescription] \| None` | Detailed AI descriptions (plural, not `full_description`) |
| `processing_history` | `list[ProcessingHistory] \| None` | Processing operations |
| `created_at` | `datetime \| None` | Upload timestamp |
| `updated_at` | `datetime \| None` | Last update timestamp |
| `content_created_at` | `datetime \| None` | Actual content creation date (from EXIF metadata) |
| `upload_method` | `str \| None` | Upload method used (`"DIRECT"` or `"POST"`) |
| `original_filename` | `str \| None` | Original uploaded filename |
| `variant_status` | `str \| None` | Variant generation status (pending/processing/completed/failed) |
| `variant_count` | `int \| None` | Number of generated variants |
| `blur_hash` | `str \| None` | BlurHash string for blur-up placeholder loading |
| `description_status` | `str \| None` | AI description generation status (pending/processing/completed/failed) |

**`FullDescription`** (items in `UserFileDetails.full_descriptions`):

Detailed AI-generated descriptions for a file. Populated after auto-describe on upload completes.
| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Unique description identifier |
| `description` | `str` | Full AI-generated description text |
| `visible_text` | `str \| None` | OCR-extracted text from the image |
| `confidence_score` | `float \| None` | AI confidence score (0-1) |
| `processing_time_ms` | `int \| None` | Time taken to generate description |
| `created_at` | `datetime \| None` | When the description was created |

**`ProcessingHistory`** (items in `UserFileDetails.processing_history`):

History of processing operations on a file. Populated after describe, verify, or rules operations.
| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Unique history entry identifier |
| `operation_type` | `str` | Type of operation (`"describe"`, `"verify"`, `"rules"`) |
| `status` | `str` | Processing status |
| `created_at` | `datetime \| None` | When the operation started |
| `completed_at` | `datetime \| None` | When the operation completed |
| `error_message` | `str \| None` | Error message if operation failed |

### Chat Results

**`SessionList`** (from `client.chats.list_sessions()`):
| Field | Type | Description |
|-------|------|-------------|
| `items` | `list[ChatSession]` | List of sessions (not `.sessions`) |
| `total` | `int` | Total session count |
| `has_more` | `bool` | Whether more exist |

**`ChatSession`** (items in `SessionList.items`):
| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Session identifier |
| `title` | `str` | Session title |
| `total_messages` | `int` | Message count |
| `total_tokens` | `int` | Total tokens used |
| `remaining_tokens` | `int` | Tokens remaining in quota |
| `remaining_messages` | `int` | Messages remaining in quota |
| `is_active` | `bool` | Whether session is active |
| `use_all_images` | `bool` | Whether using all images as context |
| `selected_image_count` | `int` | Number of selected images |
| `created_at` | `datetime \| None` | Creation timestamp |
| `updated_at` | `datetime \| None` | Last update timestamp |
| `last_message_at` | `datetime \| None` | When last message was sent |
| `last_message_preview` | `str \| None` | Preview of the last message |
| `last_user_message` | `str \| None` | Last message from the user |

**`ChatSessionDetail`** (from `client.chats.get_session()`):

Title and other session fields are nested: access via `detail.session.title`, not `detail.title`.
| Field | Type | Description |
|-------|------|-------------|
| `session` | `ChatSession` | Session info (`.session.title`, `.session.id`, etc.) |
| `messages` | `list[ChatMessage]` | Messages in the session |
| `selected_image_ids` | `list[str] \| None` | Selected image IDs |
| `current_search_result_ids` | `list[str] \| None` | IDs from last search operation |

**`ChatResponse`** (from `session.send()`):
| Field | Type | Description |
|-------|------|-------------|
| `message_id` | `str` | Unique message identifier |
| `session_id` | `str` | Session this message belongs to |
| `content` | `str` | Response text |
| `token_count` | `int` | Tokens used in response |
| `provider` | `str` | AI provider used |
| `model` | `str` | Model used |
| `processing_time_ms` | `int` | Time to generate response in ms |
| `images` | `list[ImageReference] \| None` | Referenced images |
| `metadata` | `dict \| None` | Additional response metadata (contains `result_refs`, etc.) |
| `resolved_content` | `str` (property) | Content with `[[…]]` markup replaced by plain text |
| `references` | `ParsedReferences` (property) | Parsed image/document/link references from content |
| `result_refs` | `dict` (property) | Parsed `ResultRefData` from metadata |

**`ChatMessage`** (items in `ChatSessionDetail.messages`):
| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Message identifier |
| `role` | `MessageRole` | Message role (`"user"`, `"assistant"`, `"system"`) |
| `content` | `str` | Message text content |
| `created_at` | `datetime \| None` | When the message was created |
| `token_count` | `int` | Number of tokens in message |
| `image_context` | `list[ImageReference] \| None` | Images referenced in message |
| `metadata` | `dict \| None` | Additional message metadata |
| `resolved_content` | `str` (property) | Content with `[[…]]` markup replaced by plain text |
| `references` | `ParsedReferences` (property) | Parsed references from content |
| `result_refs` | `dict` (property) | Parsed `ResultRefData` from metadata |

**`ImageReference`** (items in `ChatResponse.images` and `ChatMessage.image_context`):
| Field | Type | Description |
|-------|------|-------------|
| `image_id` | `str` | Image identifier |
| `filename` | `str` | Original filename |
| `thumbnail_url` | `str \| None` | Thumbnail URL |
| `description` | `str \| None` | Image description |
| `confidence` | `float \| None` | Confidence score |
| `title` | `str \| None` | Image title |
| `stored_url` | `str \| None` | Full image URL |

### Document Results

**`DocumentList`** (from `client.documents.list()`):
| Field | Type | Description |
|-------|------|-------------|
| `documents` | `list[DocumentItem]` | List of documents |
| `total_count` | `int` | Total matching documents |
| `page` | `int` | Current page number |
| `page_size` | `int` | Items per page |
| `has_more` | `bool` | Whether more pages exist |

**`DocumentSearchResponse`** (from `client.documents.search()`):
| Field | Type | Description |
|-------|------|-------------|
| `results` | `list[DocumentSearchResult]` | Matching chunks |
| `total_count` | `int` | Total matching chunks |
| `search_time_ms` | `int` | Time taken for search in milliseconds |
| `query` | `str` | The search query used |

**`DocumentSearchResult`** (items in search results):
| Field | Type | Description |
|-------|------|-------------|
| `document_filename` | `str` | Source document filename |
| `content` | `str` | Matching chunk text |
| `score` | `float` | Similarity score 0-1 (not `relevance_score`) |
| `document_id` | `str` | Parent document ID |
| `chunk_id` | `str` | Chunk identifier |
| `page_numbers` | `list[int] \| None` | Pages this chunk spans |
| `chunk_index` | `int \| None` | Position in document (0-based) |

### Quota Results

**`QuotaInfo`** (from `client.uploads.check_quota()`):
| Field | Type | Description |
|-------|------|-------------|
| `can_proceed` | `bool` | Whether upload can proceed (not `allowed`) |
| `requested` | `int` | Number of uploads requested |
| `available` | `int` | Uploads still available |
| `monthly_limit` | `int` | Total monthly limit |
| `current_usage` | `int` | Current month's usage |
| `message` | `str \| None` | Optional message about quota status |
| `max_batch_size` | `int \| None` | Maximum batch size allowed |

**`DocumentQuotaCheck`** (from `client.documents.quota_check()`):
| Field | Type | Description |
|-------|------|-------------|
| `can_proceed` | `bool` | Whether upload can proceed (not `allowed`) |
| `document_count` | `int` | Current document count |
| `document_limit` | `int` | Maximum allowed documents |
| `storage_used_bytes` | `int` | Storage currently used |
| `storage_limit_bytes` | `int` | Storage limit |
| `message` | `str` | Additional information about quota status |
| `documents_remaining` | `int` (property) | Number of documents that can still be uploaded |
| `storage_remaining_bytes` | `int` (property) | Bytes of storage remaining |

## API Reference

Human-readable REST API docs are in [`api/`](api/) organized by resource:

| Resource | Description |
|----------|-------------|
| [README](api/README.md) | Auth, rate limits, error format, all endpoints |
| [Uploads](api/uploads.md) | Stream and batch upload images, presigned URL flow |
| [Files](api/files.md) | List, search, filter, update, delete uploaded files |
| [Documents](api/documents.md) | Upload PDFs/DOCX, text extraction, semantic search |
<!-- | [Videos](api/videos.md) | Chunked multipart upload, progress tracking, scenes | (coming soon) -->
| [Chat](api/chat.md) | Multi-turn AI sessions, streaming SSE, plan approval |
| [Agents](api/agents.md) | Stateless AI ops: search, synthesize, organize, pipeline |
| [Folders](api/folders.md) | Hierarchical folder tree, CRUD, file movement |
| [Colors](api/colors.md) | Color analysis (automatic on upload), hex/name/family search |
| [Datasets](api/datasets.md) | Create datasets from batches, export CSV/COCO/YOLO |
| [Cloud Storage](api/cloud-storage.md) | Google Drive OAuth, import/export jobs |
| [API Keys](api/api-keys.md) | Create, rotate, and revoke API keys with scopes |
| [Settings](api/settings.md) | User profile, tenant config, team members, custom S3 |
| [Usage](api/usage.md) | Usage analytics, credit tracking, plan utilization |

The machine-readable OpenAPI 3.1 specification is at [openapi.json](openapi.json).

SDK type stubs with full method signatures are in [sdk/python/aion/](sdk/python/aion/).

## Supported File Formats

**Images:** JPEG, PNG, WebP, GIF
**Documents:** PDF, DOCX, TXT, MD

## Rate Limits

The API enforces rate limits per API key. When exceeded, a `RateLimitError` is raised with:
- `retry_after`: Seconds to wait before retrying
- `limit`: Maximum requests allowed in the window
- `remaining`: Requests remaining (0 when rate limited)
- `reset`: Unix timestamp when the window resets

The SDK automatically retries transient errors with exponential backoff (configurable via `max_retries` and `retry_delay`).

## Repository Structure

```
api/                            # Human-readable REST API docs (one file per resource)
openapi.json                    # Full OpenAPI 3.1 specification
sdk/python/aion/                # Python SDK type stubs
  client.py                     # AionVision async client
  sync.py                       # SyncAionVision sync client
  config.py                     # ClientConfig
  exceptions.py                 # Exception hierarchy
  pipeline.py                   # Pipeline builder
  resources/                    # Resource classes (one per API domain)
  types/                        # Type definitions (dataclasses)
examples/                       # Runnable example scripts
llms.txt                        # AI agent context file
CLAUDE.md                       # Detailed AI coding assistant instructions
```
