# Aionvision SDK Reference for AI Coding Assistants

This file provides a comprehensive reference for the Aionvision Python SDK (`aionvision` on PyPI, imported as `aion`). Use this alongside the type stubs in `sdk/python/aion/` and the OpenAPI spec in `openapi.json`.

## Architecture Overview

- **Async client**: `AionVision` (recommended for production)
- **Sync client**: `SyncAionVision` (for Django, Flask, CLI, data pipelines)
- **Resource pattern**: `client.<resource>.<method>()` (e.g., `client.files.list()`)
- **Type stubs**: Full signatures in `sdk/python/aion/` - refer to these for exact parameter names and types
- **OpenAPI spec**: `openapi.json` - 210 endpoints, 295 schemas

## Client Initialization

```python
from aion import AionVision, SyncAionVision

# Async - explicit API key
async with AionVision(
    api_key="aion_...",
    base_url="https://api.aionvision.tech/api/v2",  # default
    timeout=300.0,           # request timeout seconds
    max_retries=3,           # retry transient errors
    retry_delay=1.0,         # initial backoff delay
    polling_interval=2.0,    # polling interval
    polling_timeout=360.0,   # max polling wait
    tenant_id=None,          # optional multi-tenant
    proxy_url=None,          # optional proxy
    enable_tracing=False,    # OpenTelemetry tracing
) as client:
    ...

# Async - from environment (AIONVISION_API_KEY)
async with AionVision.from_env() as client:
    ...

# Sync
with SyncAionVision(api_key="aion_...") as client:
    ...  # same API, no await
```

## Resource Reference

### client.uploads (UploadResource)

| Method | Description |
|--------|-------------|
| `upload_one(file, *, filename, wait_for_descriptions=True, raise_on_failure=True, description_timeout, storage_target) -> UploadResult` | Upload single image |
| `upload(files, *, filename, filenames, recursive=True, include_hidden=False, wait_for_descriptions=True, raise_on_failure=True, description_timeout, on_progress, on_file_complete, on_description_progress, on_description_failed, storage_target) -> BatchUploadResults` | Upload one or more images. **Directories only expand image files (JPEG, PNG, WebP, GIF)** — non-image files are silently skipped. Use `client.documents.upload()` for PDFs/DOCX. |
| `upload_batch(files, *, filenames, recursive=True, include_hidden=False, wait_for_descriptions=True, raise_on_failure=True, description_timeout, on_progress, on_file_complete, on_description_progress, on_description_failed, intent="describe", verification_level="standard", storage_target="default") -> BatchUploadResults` | Lower-level batch upload with intent and verification_level params |
| `check_quota(file_count=1) -> QuotaInfo` | Check remaining upload quota |
| `request_presigned_url(filename, content_type, size_bytes, *, purpose="image_analysis", idempotency_key, storage_target="default") -> PresignedUrlInfo` | Get presigned upload URL |
| `confirm_upload(object_key, size_bytes, *, checksum) -> ConfirmResult` | Confirm an upload |
| `wait_for_description(image_id, *, timeout, poll_interval) -> DescriptionStatus` | Poll for description completion |
| `batch_prepare(files, *, intent, verification_level, additional_params) -> BatchPrepareResult` | Prepare batch upload |
| `batch_confirm(batch_id, confirmations, *, auto_process=True) -> BatchConfirmResult` | Confirm batch upload |
| `get_batch_status(batch_id) -> UploadBatchStatusResult` | Check batch status |

### client.chats (ChatResource)

| Method | Description |
|--------|-------------|
| `session(*, title, image_ids, use_all_images=True, auto_close=True) -> ChatSessionContext` | Create managed session (context manager) |
| `send(message, *, session_id, force_detailed_analysis=False) -> ChatResponse` | Send message (complete response) |
| `send_stream(message, *, session_id, force_detailed_analysis=False) -> AsyncIterator[ChatToken]` | Stream response tokens |
| `create_session(*, title, image_ids, use_all_images=True) -> ChatSession` | Create session manually |
| `get_session(session_id) -> ChatSessionDetail` | Get session details |
| `list_sessions(*, limit=20, offset=0, active_only=False) -> SessionList` | List sessions |
| `iter_sessions(*, page_size=20, active_only=False) -> AsyncIterator[ChatSession]` | Iterate all sessions (auto-pagination) |
| `get_messages(session_id) -> list[ChatMessage]` | Get session messages |
| `update_images(session_id, image_ids) -> dict` | Update session image context |
| `update_documents(session_id, document_ids) -> dict` | Update session document context |
| `close_session(session_id) -> dict` | Close a session |
| `rename_session(session_id, title) -> dict` | Rename session |
| `export_session(session_id, *, format="markdown") -> bytes` | Export session transcript |
| `search_images(query, *, limit=50) -> list[ImageReference]` | Search images for chat context |
| `get_all_images(*, limit=1000, offset=0) -> ChatImageList` | Get all user images available for chat context |
| `update_mode(session_id, use_all_images) -> dict` | Switch between all images / selected images mode |
| `approve_plan(session_id, plan_id) -> PlanActionResponse` | Approve an agent plan |
| `cancel_plan(session_id, plan_id) -> PlanActionResponse` | Cancel an agent plan |

**ChatSessionContext** (from `client.chat_session()`):

| Method | Description |
|--------|-------------|
| `send(message, *, force_detailed_analysis=False) -> ChatResponse` | Send message in session |
| `send_stream(message, *, force_detailed_analysis=False) -> AsyncIterator[ChatToken]` | Stream in session |
| `update_images(image_ids) -> dict` | Update image context |
| `update_documents(document_ids) -> dict` | Update document context |
| `approve_plan(plan_id) -> PlanActionResponse` | Approve plan |
| `cancel_plan(plan_id) -> PlanActionResponse` | Cancel plan |
| `get_messages(*, limit) -> list[ChatMessage]` | Get messages |

### client.files (FilesResource)

| Method | Description |
|--------|-------------|
| `list(*, search, search_mode, tags, date_from, date_to, has_description, ids, limit=20, offset=0, sort_by, sort_order) -> FileList` | List files with filtering |
| `list_all(*, search, tags, ..., page_size=50) -> AsyncIterator[UserFile]` | Iterate all files |
| `get(file_id) -> UserFileDetails` | Get file details |
| `update(file_id, *, title, tags) -> UpdateFileResult` | Update file metadata |
| `delete(file_id) -> DeleteFileResult` | Delete a file |
| `batch_delete(file_ids) -> BatchDeleteFilesResponse` | Delete multiple files |
| `get_variant(file_id, variant_type="medium_750") -> str` | Get image variant URL |
| `download(file_id) -> bytes` | Download file content |
| `trigger_variant_generation(file_id) -> dict` | Manually trigger image variant generation (retry failed or generate missing) |

### client.documents (DocumentsResource)

| Method | Description |
|--------|-------------|
| `upload_one(file, *, filename, wait_for_processing=True, raise_on_failure=True, processing_timeout, storage_target) -> DocumentUploadResult` | Upload single document |
| `upload(files, *, filenames, recursive=True, wait_for_processing=True, on_progress, on_file_complete, on_processing_progress, on_processing_failed, storage_target) -> BatchDocumentUploadResults` | Upload multiple documents |
| `list(*, page=1, page_size=20, status_filter) -> DocumentList` | List documents |
| `list_all(*, page_size=50, status_filter) -> AsyncIterator[DocumentItem]` | Iterate all documents |
| `get(document_id) -> DocumentDetails` | Get document details |
| `get_text(document_id) -> str` | Get full extracted text |
| `get_chunks(document_id, *, include_embeddings=False) -> DocumentChunksResponse` | Get document chunks |
| `download(document_id) -> str` | Get download URL |
| `search(query, *, limit=20, similarity_threshold=0.3, document_ids) -> DocumentSearchResponse` | Search documents |
| `delete(document_id) -> None` | Delete document |
| `batch_delete(document_ids) -> DocumentBatchDeleteResponse` | Delete multiple documents |
| `wait_for_processing(document_id, *, timeout) -> DocumentStatusResult` | Poll processing status |
| `request_upload(filename, content_type, size_bytes) -> DocumentPresignedUploadResult` | Low-level: get presigned URL |
| `confirm_upload(object_key, size_bytes, content_type) -> DocumentConfirmResult` | Low-level: confirm upload |
| `get_status(document_id) -> DocumentStatusResult` | Low-level: check status |
| `batch_status(batch_id) -> DocumentBatchStatusResult` | Get batch processing status |
| `quota_check(file_count=1) -> DocumentQuotaCheck` | Check quota |

### client.links (LinksResource)

| Method | Description |
|--------|-------------|
| `create(url, *, title, tags, folder_id, auto_crawl=True) -> CreateLinkResult` | Create a link |
| `create_and_wait(url, *, title, tags, folder_id, timeout) -> LinkDetails` | Create and wait for crawl |
| `get(link_id) -> LinkDetails` | Get link details |
| `list(*, search, tags, folder_id, crawl_status, date_from, date_to, limit=20, offset=0) -> LinkList` | List links |
| `list_all(*, search, tags, ..., page_size=50) -> AsyncIterator[LinkItem]` | Iterate all links |
| `update(link_id, *, title, tags) -> LinkUpdateResult` | Update link |
| `delete(link_id) -> LinkDeleteResult` | Delete link |
| `batch_delete(link_ids) -> BatchDeleteFilesResponse` | Delete multiple links |
| `recrawl(link_id) -> RecrawlLinkResult` | Refresh metadata |
| `wait_for_crawl(link_id, *, timeout) -> LinkDetails` | Wait for crawl to complete |

### client.folders (FoldersResource)

| Method | Description |
|--------|-------------|
| `tree() -> FolderTree` | Get folder tree |
| `get(folder_id, *, limit=50, offset=0) -> FolderContents` | Get folder contents |
| `get_breadcrumbs(folder_id) -> FolderBreadcrumbs` | Get breadcrumb path |
| `create(name, *, parent_id) -> Folder` | Create folder |
| `rename(folder_id, name) -> Folder` | Rename folder |
| `move(folder_id, *, new_parent_id) -> Folder` | Move folder |
| `delete(folder_id, *, mode="move_to_parent") -> DeleteFolderResult` | Delete folder |
| `move_files(file_ids, *, folder_id) -> MoveFilesResult` | Move files to folder |

### client.colors (ColorsResource)

| Method | Description |
|--------|-------------|
| `get(image_id) -> ColorExtractionResult` | Get colors (automatic on upload) |
| `extract(image_id, *, force=False, n_colors=16) -> ColorExtractionResult` | Re-extract with custom settings |
| `search(*, hex_code, color_name, color_family, delta_e_threshold=15.0, min_percentage=5.0, limit=50) -> ColorSearchResponse` | Search by color |
| `search_all(*, hex_code, color_name, color_family, ...) -> AsyncIterator[ColorSearchResult]` | Iterate color search |
| `list_families() -> list[ColorFamilyInfo]` | List color families |
| `batch_extract(image_ids, *, force=False, n_colors=16) -> BatchColorExtractionResult` | Batch re-extraction |

### client.agent_search (AgentSearchResource)

> **Tip:** Use standalone search agents instead of agentic chat when you only need to search — they consume significantly fewer tokens by skipping session overhead and conversational context.

| Method | Description |
|--------|-------------|
| `images(query, *, limit=50, folder_id, image_ids) -> ImageSearchAgentResult` | AI image search |
| `documents(query, *, limit=50, document_types, document_ids) -> DocumentSearchAgentResult` | AI document search |

### client.agent_operations (AgentOperationsResource)

| Method | Description |
|--------|-------------|
| `synthesize(intent, *, image_ids, document_ids, auto_save=False) -> SynthesizeResult` | Generate synthesis/report |
| `analyze_documents(intent, document_ids) -> DocumentAnalysisResult` | Analyze documents |
| `organize(intent, *, image_ids, document_ids, parent_folder_id) -> OrganizeResult` | Organize files into folders |

### client.batch (BatchResource)

| Method | Description |
|--------|-------------|
| `get_status(batch_id) -> BatchStatusResult` | Check batch progress |
| `get_results(batch_id, *, include_failed=True, offset=0, limit=100) -> BatchResults` | Get batch results |
| `get_all_results(batch_id, *, page_size=100) -> AsyncIterator[BatchItemResult]` | Iterate all results |
| `cancel(batch_id) -> None` | Cancel batch |
| `wait_for_completion(batch_id, *, timeout, on_progress) -> BatchStatusResult` | Poll until complete |

### client.settings (SettingsResource)

| Method | Description |
|--------|-------------|
| `configure_custom_s3(access_key_id, secret_access_key, bucket_name, region) -> S3ConfigStatus` | Configure custom S3 |
| `get_custom_s3_status() -> S3ConfigStatus` | Check S3 config |
| `remove_custom_s3() -> dict` | Remove S3 config |
| `validate_custom_s3() -> S3ValidationResult` | Validate S3 credentials |

### client.tenant (TenantResource)

| Method | Description |
|--------|-------------|
| `get_settings() -> TenantSettings` | Get tenant settings |
| `update_settings(*, name, webhook_url, allowed_vlm_providers, ...) -> TenantSettings` | Update settings (ADMIN) |
| `get_limits() -> TenantLimits` | Get usage limits |
| `list_members() -> list[TenantMember]` | List members |
| `invite_member(email, *, role="viewer") -> TenantMember` | Invite member (OWNER) |
| `update_member_role(user_id, role) -> TenantMember` | Change role (OWNER) |
| `remove_member(user_id) -> dict` | Remove member (OWNER) |

### client.audit (AuditResource)

| Method | Description |
|--------|-------------|
| `list(*, event_type, severity, user_id, date_from, date_to, result, limit=50, offset=0) -> AuditLogList` | List audit logs (ADMIN) |
| `get(log_id) -> AuditLogEntry` | Get audit entry |

### client.cloud_storage (CloudStorageResource)

| Method | Description |
|--------|-------------|
| `initiate_auth(provider, *, redirect_uri) -> InitiateAuthResult` | Start OAuth flow |
| `complete_auth(provider, *, code, state, redirect_uri) -> CompleteAuthResult` | Complete OAuth |
| `list_connections(*, provider, active_only=True) -> ConnectionList` | List connections |
| `disconnect(connection_id) -> DisconnectResult` | Disconnect account |
| `start_import(connection_id, files, *, auto_describe=True, tags) -> ImportResult` | Start file import |
| `start_export(connection_id, image_ids, *, folder_id, folder_name) -> ExportResult` | Start file export |
| `get_job(job_id) -> CloudStorageJob` | Check job status |
| `wait_for_job(job_id, *, timeout, on_progress) -> CloudStorageJob` | Wait for job |
| `import_and_wait(connection_id, files, *, timeout, on_progress) -> CloudStorageJob` | Import and wait |
| `export_and_wait(connection_id, image_ids, *, timeout, on_progress) -> CloudStorageJob` | Export and wait |

### Pipeline (from client.pipeline())

```python
pipeline = client.pipeline()

# Seed data
pipeline.with_images(image_ids)
pipeline.with_documents(document_ids)

# Search steps
pipeline.search_images(query)
pipeline.search_documents(query)
pipeline.search_links(query)

# Analysis steps
pipeline.analyze(intent, *, depends_on)
pipeline.analyze_documents(intent, *, depends_on)
pipeline.analyze_links(intent, *, depends_on)

# Operation steps
pipeline.synthesize(intent, *, depends_on)
pipeline.organize(intent, *, depends_on)
pipeline.cross_reference(intent, *, depends_on)

# Execute
result = await pipeline.run()  # -> PipelineResult
```

## Common Workflow Patterns

### Upload + Describe (most common)
```python
result = await client.upload_one("photo.jpg")
# result.image_id, result.description, result.tags, result.filename
```

### Batch Upload with Error Handling
```python
# Directory upload only includes image files (JPEG, PNG, WebP, GIF).
# Non-image files are silently skipped. Use client.documents.upload() for docs.
results = await client.upload("/photos", raise_on_failure=False)
for r in results:
    if r.is_failed:
        print(f"Failed: {r.filename}: {r.description_error}")
    else:
        print(f"OK: {r.filename}: {r.description[:50]}")
```

### Chat Session
```python
async with client.chat_session(title="Analysis") as session:
    response = await session.send("Find all damaged poles")
    print(response.content)
    for img in response.images:
        print(f"  Referenced: {img.image_id}")
```

### Streaming Chat
```python
async with client.chat_session() as session:
    async for token in session.send_stream("Describe my images"):
        if token.type == ChatTokenType.TOKEN:
            print(token.content, end="", flush=True)
```

### Document RAG Pipeline
```python
doc = await client.documents.upload_one("report.pdf")
chunks = await client.documents.get_chunks(doc.document_id)
results = await client.documents.search("key findings")
```

### Multi-Agent Pipeline
```python
result = await (
    client.pipeline()
    .search_images("utility poles")          # step 0
    .search_documents("maintenance records")  # step 1
    .cross_reference("Cross-reference findings", depends_on=[0, 1])  # step 2
    .run()
)
```

## Error Handling Patterns

```python
try:
    result = await client.upload_one("photo.jpg")
except AionVision.AuthenticationError:
    # Invalid API key
except AionVision.RateLimitError as e:
    # Wait e.retry_after seconds
except AionVision.QuotaExceededError as e:
    # e.partial_results may contain completed uploads
except AionVision.UploadError as e:
    # e.session_id for recovery, e.partial_results for completed chunks
except AionVision.AionvisionTimeoutError as e:
    # e.last_result contains last status before timeout
except AionVision.AionvisionError as e:
    # Base catch-all: e.code, e.message, e.details
```

## Key Types

See `sdk/python/aion/types/` for complete type definitions. Key types:

- **UploadResult**: image_id, filename, description, tags, description_status, is_failed, description_error, thumbnail_url
- **BatchUploadResults**: **extends `list[UploadResult]`** — iterate directly (`for r in results`), no `.results` attribute. Properties: has_failures (bool), succeeded_count (int), failed_count (int), pending_count (int). Methods: succeeded(), failed(), retryable(), pending(), raise_on_failures() -> self, summary() -> str
- **ChatResponse**: message_id, session_id, content (str), token_count, processing_time_ms, images (list[ImageReference] | None), metadata. Properties: resolved_content (str), references (ParsedReferences), result_refs (dict), as_collection() -> FileCollection
- **ChatToken**: type (TOKEN, COMPLETE, ERROR, STATUS, IMAGE_RESULTS, etc.), content, data
- **FileList**: files (list[UserFile]), total_count (int — not `.total`), has_more (bool)
- **UserFile**: id, title, filename, tags, upload_description, visible_text, created_at, content_created_at, size_bytes, has_full_description, thumbnail_url, medium_url, full_url, content_type, media_type, dimensions, format, variant_status, variant_count, blur_hash, description_status, description_error <!-- video fields coming soon: video_metadata, video_analysis_status, video_analysis_job_id, scene_count, has_audio_transcript, video_url -->
- **UserFileDetails**: id, object_key, title, original_filename, tags, upload_description, visible_text, full_descriptions (list[FullDescription] — plural, not `.full_description`), processing_history (list[ProcessingHistory]), full_url, medium_url, thumbnail_url, original_url, dimensions, format, size_bytes, content_type, hash, description_generated_at, created_at, updated_at, content_created_at, upload_method, variant_status, variant_count, blur_hash, description_status
- **FullDescription**: id, description, visible_text, confidence_score, processing_time_ms, created_at
- **SessionList**: items (list[ChatSession] — not `.sessions`), total (int), has_more (bool)
- **ChatSession**: id, title, total_messages, total_tokens, remaining_tokens, remaining_messages, is_active, use_all_images, selected_image_count, created_at, updated_at, last_message_at, last_message_preview, last_user_message
- **ChatSessionDetail**: session (ChatSession — title is nested: `detail.session.title`), messages (list[ChatMessage]), selected_image_ids, current_search_result_ids
- **QuotaInfo**: can_proceed (bool — not `.allowed`), requested, available, monthly_limit, current_usage, message
- **DocumentQuotaCheck**: can_proceed (bool — not `.allowed`), document_count, document_limit, storage_used_bytes, storage_limit_bytes
- **DocumentUploadResult**: document_id, filename, status, page_count, chunk_count
- **DocumentList**: documents (list[DocumentItem]), total_count (int — not `.total`), page, page_size, has_more (bool)
- **DocumentDetails**: id, title, filename, page_count, chunk_count, text_extraction_status, embedding_status
- **DocumentSearchResponse**: results (list[DocumentSearchResult]), total_count, search_time_ms, query
- **DocumentSearchResult**: chunk_id, document_id, document_filename, content, score (float 0-1 — not `.relevance_score`), chunk_index, page_numbers (list[int] — plural)
- **ImageSearchAgentResult**: count, summary, results (list of ImageSearchResultItem)
- **DocumentSearchAgentResult**: count, summary, results (list of DocumentChunkResultItem)
- **PipelineResult**: success, steps (list[StepResult]), execution_time_ms, total_waves, errors (list[str]), token_usage (dict | None). Properties: final (StepResult). Methods: step(index) -> StepResult
- **ColorExtractionResult**: is_completed, color_analysis (dominant_colors, analytics)
- **LinkDetails**: id, url, title, domain, tags, og_metadata, crawl_status
- **Folder**: id, name, parent_id, depth
- **AuditLogList**: entries (list[AuditLogEntry]), total_count (int), has_more (bool) — requires ADMIN role
- **AuditLogEntry**: id, event_type, event_timestamp, severity, action, result, user_id, ip_address, metadata
- **ChatImageList**: image_ids (list[str]), total_count (int), has_more (bool). Method: as_collection() -> FileCollection
- **StepResult**: agent, status ("completed"/"failed"/"skipped"), summary, outputs (dict), error, execution_time_ms
- **ParsedReferences**: images (list[ImageRef]), documents (list[DocumentRef]), links (list[LinkRef]), counts (dict). Property: has_references (bool)
- **ImageRef**: id_prefix, filename, full_id (resolved from image_context)
- **DocumentRef**: id_prefix, filename, full_id, page, page_range
- **LinkRef**: id_prefix, title, full_id, source_url, domain
- **AgentContract**: name, capability (AgentCapability), description, inputs (tuple[TypedInput]), outputs (tuple[TypedOutput]), example_intents, can_run_parallel, typical_duration_ms, can_chain_with
- **TypedInput**: name, data_type, required, description, content_type_hint
- **TypedOutput**: name, data_type, mergeable, description, content_type_hint

## REST API Quick Reference

Base URL: `https://api.aionvision.tech/api/v2` · Auth: `Authorization: Bearer {aion_...}`

See [`api/`](api/) for full per-resource docs with request/response examples.

### Uploads
| Method | Path | Description |
|--------|------|-------------|
| POST | /user-files/upload/stream | Stream upload — recommended for all images/docs |
| POST | /user-files/upload/stream-batch | Upload multiple files in one multipart request |
| GET | /uploads/quota-check | Check remaining upload quota |
| GET | /uploads/sessions/{id}/status | Track upload session progress |
| POST | /user-files/upload/initiate | Get presigned URL (advanced; use for >100MB) |

### Files
| Method | Path | Description |
|--------|------|-------------|
| GET | /user-files | List files (filter by search, tags, date, folder) |
| GET | /user-files/{id} | Get file details and variants |
| PATCH | /user-files/{id} | Update title or tags |
| DELETE | /user-files/{id} | Soft-delete a file |
| POST | /user-files/batch-delete | Delete up to 100 files |
| POST | /user-files/links | Create a bookmarked link with OG crawl |

### Documents
| Method | Path | Description |
|--------|------|-------------|
| POST | /document-uploads/request-presigned-url | Step 1: get presigned upload URL |
| POST | /document-uploads/confirm | Step 2: confirm upload, trigger processing |
| GET | /document-uploads/{id}/status | Poll processing status |
| GET | /documents/{id}/chunks | Get text chunks |
| POST | /documents/search | Semantic search across documents |

<!-- ### Videos (coming soon)
| Method | Path | Description |
|--------|------|-------------|
| POST | /video-uploads/initiate | Start multipart upload, get presigned chunk URLs |
| POST | /video-uploads/chunks/confirm | Confirm each uploaded chunk |
| POST | /video-uploads/complete | Finalize upload, trigger AI analysis |
| GET | /video-uploads/progress/{id} | Track upload progress |
| GET | /videos/{id}/scenes | List detected scenes |
-->

### Chat
| Method | Path | Description |
|--------|------|-------------|
| POST | /chat/sessions | Create session |
| POST | /chat/sessions/{id}/messages | Send message (non-streaming) |
| POST | /chat/sessions/{id}/messages/stream | Send message (streaming SSE) |
| GET | /chat/sessions/{id} | Get session with message history |
| POST | /chat/sessions/{id}/plans/{plan_id}/action | Approve or cancel execution plan |

### Agents
| Method | Path | Description |
|--------|------|-------------|
| POST | /agents/search/images | AI image search with natural language |
| POST | /agents/search/documents | AI document search |
| POST | /agents/synthesize | Generate report from images/documents |
| POST | /agents/analyze/documents | Deep document analysis and comparison |
| POST | /agents/organize | Auto-organize files into folders |
| POST | /agents/pipeline | Multi-step agent pipeline with DAG support |

### Folders
| Method | Path | Description |
|--------|------|-------------|
| GET | /folders | List all folders (flat, build tree client-side) |
| POST | /folders | Create folder |
| PATCH | /folders/{id} | Rename folder |
| POST | /folders/{id}/move | Move folder to new parent |
| DELETE | /folders/{id} | Delete folder (move_to_parent or delete_all) |
| POST | /folders/move-files | Move files into a folder |

### Colors
| Method | Path | Description |
|--------|------|-------------|
| GET | /colors/images/{id} | Get color analysis for an image |
| POST | /colors/images/{id}/extract | Extract/re-extract colors |
| POST | /colors/batch/extract | Queue batch extraction |
| POST | /colors/search | Search images by hex, name, or family |
| GET | /colors/families | List available color families |

### Datasets
| Method | Path | Description |
|--------|------|-------------|
| POST | /datasets | Create dataset from completed batch |
| GET | /datasets | List datasets |
| GET | /datasets/{id} | Get dataset details |
| POST | /datasets/{id}/export | Export to CSV, COCO, YOLO, or Pascal VOC |
| GET | /datasets/statistics/summary | Aggregated export statistics |

### Cloud Storage
| Method | Path | Description |
|--------|------|-------------|
| POST | /cloud-storage/auth/{provider} | Initiate OAuth flow |
| POST | /cloud-storage/auth/{provider}/callback | Complete OAuth, create connection |
| GET | /cloud-storage/connections | List connected accounts |
| POST | /cloud-storage/import | Import files from Google Drive |
| POST | /cloud-storage/export | Export files to Google Drive |
| GET | /cloud-storage/jobs/{id} | Poll import/export job status |

### API Keys
| Method | Path | Description |
|--------|------|-------------|
| POST | /api-keys | Create API key (ADMIN, session auth) |
| GET | /api-keys | List API keys |
| PUT | /api-keys/{id} | Update name/description/metadata |
| DELETE | /api-keys/{id} | Revoke API key |

### Settings
| Method | Path | Description |
|--------|------|-------------|
| GET | /user/profile | Get user profile and preferences |
| PATCH | /user/profile | Update name and preferences |
| GET | /tenant/settings | Get tenant config and subscription info |
| POST | /tenant/members/invite | Invite team member |
| POST | /tenant/s3-config | Configure custom S3 (BYOB) |
| GET | /tenant/audit-logs | List audit events (ADMIN) |

### Usage
| Method | Path | Description |
|--------|------|-------------|
| GET | /usage/summary | Aggregated stats for a date range |
| GET | /usage/by-period | Time-series usage data for charts |
| POST | /usage/check | Pre-flight credit check before operations |
| GET | /usage/breakdown | Credit breakdown by level and operation type |
| GET | /usage/plan | Plan utilization and recommendations |
| GET | /usage/tokens/monthly | Monthly token totals by operation |

---

## Important Notes

- Always use context managers (`async with` / `with`) for client lifecycle
- The sync client (`SyncAionVision`) is NOT thread-safe
- Streaming (`send_stream`) is only available with the async client
- `upload_one()` returns `UploadResult` directly; `upload()` returns `BatchUploadResults`
- By default, upload methods wait for AI descriptions and raise on failure
- Set `raise_on_failure=False` to handle description failures manually
- Pipeline steps auto-wire data dependencies; use `depends_on` for DAG patterns
- The `StorageTarget.CUSTOM` option requires prior S3 configuration via `client.settings`
