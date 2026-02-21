# Chat API

> Base URL: `https://api.aionvision.tech/api/v2`
> Authentication: `Authorization: Bearer {api_key}`

Create multi-turn AI chat sessions with access to your uploaded images and documents. The system uses specialized agents for search, analysis, document search, analytics, cross-referencing, and file organization. Both non-streaming and streaming (SSE) message endpoints are supported.

> **Tip:** If you only need to search images or documents without multi-turn conversation, use the [Agents API](agents.md) directly (e.g., `POST /agents/search/images`). Standalone search agents consume significantly fewer tokens by skipping session overhead and conversational context.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /chat/sessions | Create a new session |
| GET | /chat/sessions | List sessions |
| GET | /chat/sessions/{id} | Get session with message history |
| PATCH | /chat/sessions/{id}/title | Rename session |
| DELETE | /chat/sessions/{id} | Close session |
| POST | /chat/sessions/{id}/messages | Send message (non-streaming) |
| POST | /chat/sessions/{id}/messages/stream | Send message (streaming SSE) |
| PATCH | /chat/sessions/{id}/mode | Toggle all-images vs selected-images mode |
| PUT | /chat/sessions/{id}/images | Update image context |
| PUT | /chat/sessions/{id}/documents | Update document context |
| GET | /chat/images/all | List all available images for context |
| POST | /chat/images/search | Search images by natural language |
| POST | /chat/sessions/{id}/plans/{plan_id}/action | Approve or cancel an execution plan |
| GET | /chat/sessions/{id}/export | Export session (JSON, Markdown, or text) |

---

## POST /chat/sessions — Create Session

**Request**
```http
POST /api/v2/chat/sessions
Authorization: Bearer aion_your_api_key_here
Content-Type: application/json
```

**Body**
```json
{
  "title": "Equipment Analysis",
  "initial_image_ids": ["550e8400-e29b-41d4-a716-446655440000"],
  "use_all_images": true
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| title | string | Optional, max 255 chars |
| initial_image_ids | string[] | Optional, specific images to include (max 1000 if `use_all_images=false`) |
| use_all_images | boolean | Default: `true` — make all tenant images available |

**Response** `200 OK`
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Equipment Analysis",
  "created_at": "2025-01-15T10:30:00Z"
}
```

```python
async with AionVision(api_key="aion_...") as client:
    async with client.chat_session() as session:
        response = await session.send("What damage do you see?")
        print(response.content)
```

---

## POST /chat/sessions/{id}/messages — Send Message (Non-Streaming)

**Request body**
```json
{
  "message": "What safety issues do you see in these images?",
  "force_detailed_analysis": false,
  "expected_image_ids": ["550e8400-e29b-41d4-a716-446655440000"]
}
```

**Response** `200 OK`
```json
{
  "message_id": "550e8400-e29b-41d4-a716-446655440000",
  "content": "Based on my analysis of the images, I can see...",
  "token_count": 450,
  "provider": "anthropic",
  "model": "claude-sonnet-4-20250514",
  "processing_time_ms": 2500,
  "remaining_tokens": 94550,
  "remaining_messages": 97
}
```

---

## POST /chat/sessions/{id}/messages/stream — Send Message (Streaming)

Returns a Server-Sent Events stream. Connect with `Accept: text/event-stream`.

**Request body** (same as non-streaming)
```json
{
  "message": "What are the key safety requirements?",
  "force_detailed_analysis": false
}
```

**SSE Event stream**
```
event: connection
data: {"type": "connection", "message_id": "msg_001", "status": "connected"}

event: thinking
data: {"type": "thinking", "status": "processing"}

event: thinking_step
data: {"type": "thinking_step", "phase": "analysis", "agent_name": "AnalysisAgent", "message": "Examining images..."}

event: status
data: {"type": "status", "phase": "searching", "message": "Searching documents...", "agent_name": "SearchAgent"}

event: tool_invocation
data: {"type": "tool_invocation", "tool_name": "search_images", "agent_name": "SearchAgent"}

event: image_results
data: {"type": "image_results", "images": [...], "count": 5}

event: token
id: 1
data: {"type": "token", "content": "Based", "accumulated": "Based", "token_index": 0}

event: complete
data: {"type": "complete", "content": "Based on my analysis...", "resolved_content": "Based on my analysis...", "message_id": "550e8400-...", "agents_used": ["SearchAgent"], "has_results": true, "result_count": 5, "image_context": [...]}

event: ping
data: {"type": "ping"}
```

**Error events**
```
event: auth_error
data: {"type": "auth_error", "error": "Session not found"}

event: error
data: {"type": "error", "message": "Monthly chat limit reached (200/200).", "code": "USAGE_LIMIT_EXCEEDED"}

event: close
data: {"type": "close", "message_id": "msg_001"}
```

The `complete` event includes `resolved_content` — the response with all `[[ref:KEY]]`, `[[img:ID|filename]]`, `[[doc:ID|filename|p:N]]` markup replaced with human-readable text. Use this for CLI output or non-interactive contexts.

**Example with curl**
```bash
curl -X POST "https://api.aionvision.tech/api/v2/chat/sessions/550e8400-e29b-41d4-a716-446655440000/messages/stream" \
  -H "Authorization: Bearer aion_your_api_key_here" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"message": "Describe the damage you see"}'
```

```python
async with client.chat_session() as session:
    async for token in session.send_stream("Describe the damage"):
        print(token.content, end="", flush=True)
```

---

## GET /chat/sessions/{id} — Get Session with History

**Query parameters**: `?include_messages=true&message_limit=50`

**Response** `200 OK`
```json
{
  "session": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Equipment Analysis",
    "total_messages": 4,
    "remaining_tokens": 94000,
    "remaining_messages": 96,
    "is_active": true,
    "use_all_images": false,
    "selected_image_count": 2
  },
  "messages": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "role": "user",
      "content": "What damage do you see?",
      "token_count": 12,
      "created_at": "2025-01-15T10:31:00Z"
    },
    {
      "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
      "role": "assistant",
      "content": "I can see corrosion on...",
      "token_count": 450,
      "provider": "anthropic",
      "model": "claude-sonnet-4-20250514",
      "processing_time_ms": 1250,
      "image_context": [
        {
          "image_id": "550e8400-e29b-41d4-a716-446655440000",
          "description": "Steel beam with rust",
          "confidence": 0.95
        }
      ],
      "metadata": {"vision_used": true, "offers_detailed_analysis": false}
    }
  ],
  "selected_image_ids": ["550e8400-e29b-41d4-a716-446655440000"]
}
```

---

## Context Management

### PUT /chat/sessions/{id}/images

Update which images are available in chat context (max 1000).

```json
{"image_ids": ["550e8400-e29b-41d4-a716-446655440000", "660f9500-f39c-52e5-b827-557766550111"]}
```

### PUT /chat/sessions/{id}/documents

Update which documents are available in chat context (max 100).

```json
{"document_ids": ["550e8400-e29b-41d4-a716-446655440000"]}
```

### PATCH /chat/sessions/{id}/mode

Toggle between all-images and selected-images mode.

```json
{"use_all_images": true}
```

---

## Plan Approval

When a complex request requires multi-step agent operations, the streaming response may include a `plan_pending_approval` event. Approve or cancel it:

**POST /chat/sessions/{id}/plans/{plan_id}/action**
```json
{"action": "approve"}
```

- `200` — plan completed synchronously, `results` included in response
- `202 Accepted` — plan executing in background; subscribe to WebSocket events for progress
- `action` values: `"approve"` or `"cancel"`

---

## Export

**GET /chat/sessions/{id}/export**

Query params: `?format=markdown&include_metadata=false`

`format` options: `"json"`, `"markdown"` (default), `"text"`

Returns a file download with `Content-Disposition` header.

---

## See Also

- [Agents API](agents.md) — stateless AI operations without sessions
- [Documents API](documents.md) — upload documents for chat context
- [Files API](files.md) — manage images available in chat
- SDK: `client.chats` — `session()`, `send()`, `send_stream()`
