# Agents API

> Base URL: `https://api.aionvision.tech/api/v2`
> Authentication: `Authorization: Bearer {api_key}`

Direct, stateless access to AI agents without requiring chat sessions. Each call executes a single operation and returns self-contained results — ideal for programmatic integrations, automated pipelines, and custom interfaces. The AI iteratively refines results until satisfactory, with usage tracking on every response.

> **Tip:** Standalone search agents are the most token-efficient way to search your data. If you only need to find images or documents without multi-turn conversation, use these endpoints directly instead of [agentic chat](chat.md) to save on token usage.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /agents/search/images | AI-powered image search |
| POST | /agents/search/documents | AI-powered document search |
| POST | /agents/synthesize | Generate a report from images/documents |
| POST | /agents/analyze/documents | Deep document analysis and comparison |
| POST | /agents/organize | Organize files into folders using AI |
| POST | /agents/pipeline | Multi-step agent pipeline with data wiring |

---

## POST /agents/search/images — Image Search

Search images using natural language with intelligent reasoning and multi-match boosting.

**Request**
```http
POST /api/v2/agents/search/images
Authorization: Bearer aion_your_api_key_here
Content-Type: application/json
```

**Body**
```json
{
  "query": "damaged utility poles in residential areas",
  "limit": 50,
  "folder_id": "550e8400-e29b-41d4-a716-446655440000",
  "image_ids": ["550e8400-e29b-41d4-a716-446655440001"]
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| query | string | Natural language query, 1–2000 chars (required) |
| limit | integer | Advisory max results, 1–500, default 50 |
| folder_id | string | Optional — restrict to a specific folder |
| image_ids | string[] | Optional — search within specific images |

**Response** `200 OK`
```json
{
  "success": true,
  "results": [
    {
      "image_id": "550e8400-e29b-41d4-a716-446655440000",
      "score": 0.92,
      "filename": "pole_damage_01.jpg",
      "title": "Utility Pole Assessment",
      "description": "Damaged wooden utility pole with visible crack...",
      "thumbnail_url": "https://cdn.aionvision.tech/thumbs/...",
      "features": [
        {"name": "utility_pole", "items": [{"count": 1, "confidence": 0.95}]},
        {"name": "damage", "items": [{"count": 1, "confidence": 0.88}]}
      ]
    }
  ],
  "count": 15,
  "summary": "Found 15 images of damaged utility poles",
  "execution_time_ms": 1250,
  "iterations": 2,
  "token_usage": {"input": 450, "output": 280}
}
```

```bash
curl -X POST https://api.aionvision.tech/api/v2/agents/search/images \
  -H "Authorization: Bearer aion_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"query": "damaged utility poles", "limit": 20}'
```
```python
async with AionVision(api_key="aion_...") as client:
    result = await client.agent_search.images("damaged utility poles", limit=20)
    for img in result.results:
        print(img.image_id, img.score)
```

---

## POST /agents/search/documents — Document Search

Search document chunks by semantic similarity with intelligent reasoning.

**Request body**
```json
{
  "query": "safety inspection procedures for electrical equipment",
  "limit": 50,
  "document_types": ["pdf", "docx"],
  "document_ids": ["550e8400-e29b-41d4-a716-446655440001"]
}
```

**Response** `200 OK`
```json
{
  "success": true,
  "results": [
    {
      "chunk_id": "chunk_550e8400",
      "document_id": "doc_550e8400",
      "document_filename": "safety_manual.pdf",
      "text": "Electrical equipment inspections must be conducted quarterly...",
      "score": 0.89,
      "page_numbers": [12, 13],
      "chunk_index": 5
    }
  ],
  "count": 8,
  "summary": "Found 8 relevant sections across 2 documents",
  "execution_time_ms": 980,
  "iterations": 1,
  "token_usage": {"input": 320, "output": 180}
}
```

---

## POST /agents/synthesize — Synthesize Report

Generate a report or narrative summary from images and documents.

**Request body**
```json
{
  "intent": "Write a report comparing Q3 and Q4 spending patterns",
  "image_ids": ["550e8400-e29b-41d4-a716-446655440000"],
  "document_ids": ["660f9500-e29b-41d4-a716-446655440000"],
  "auto_save": false
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| intent | string | What to synthesize, 1–2000 chars (required) |
| image_ids | string[] | Optional — images to include |
| document_ids | string[] | Optional — documents to include |
| auto_save | boolean | Save report as a new document. Default: `false` |

**Response** `200 OK`
```json
{
  "success": true,
  "report": "# Q3 vs Q4 Spending Analysis\n\n## Overview\n\nBased on the provided documents...",
  "summary": "Comparative analysis of Q3 and Q4 spending across 3 categories",
  "saved_document_id": null,
  "execution_time_ms": 4200,
  "iterations": 3,
  "token_usage": {"input": 1250, "output": 890}
}
```

```python
result = await client.agent_operations.synthesize(
    intent="Summarize key findings across all inspection reports",
    document_ids=["doc_1", "doc_2"]
)
print(result.report)
```

---

## POST /agents/analyze/documents — Analyze Documents

Deep analysis of one or more documents: summarize, compare, or categorize.

**Request body**
```json
{
  "intent": "Compare these two contracts, highlight key differences",
  "document_ids": [
    "550e8400-e29b-41d4-a716-446655440000",
    "660f9500-e29b-41d4-a716-446655440000"
  ]
}
```

**Response** `200 OK`
```json
{
  "success": true,
  "analysis": "# Contract Comparison\n\n## Key Differences\n\n1. **Term Length**: Contract A is 12 months...",
  "summary": "Compared 2 contracts with 5 key differences",
  "chunk_references": [
    {
      "chunk_id": "chunk_abc123",
      "document_id": "550e8400-e29b-41d4-a716-446655440000",
      "document_filename": "contract_a.pdf",
      "page_numbers": [3, 4]
    }
  ],
  "execution_time_ms": 3800,
  "token_usage": {"input": 980, "output": 720}
}
```

---

## POST /agents/organize — Organize Files

Automatically categorize and organize files into folders using AI-driven analysis.

**Request body**
```json
{
  "intent": "Sort these files by project and document type",
  "image_ids": ["550e8400-e29b-41d4-a716-446655440000"],
  "document_ids": ["770a0600-e29b-41d4-a716-446655440000"],
  "parent_folder_id": "880b1700-e29b-41d4-a716-446655440000"
}
```

**Response** `200 OK`
```json
{
  "success": true,
  "summary": "Created 2 folders and organized 3 files by project type",
  "actions": [
    {"action": "create_and_move_files", "folder_name": "Site Inspections", "file_count": 2},
    {"action": "create_and_move_files", "folder_name": "Contracts", "file_count": 1}
  ],
  "folders_created": 2,
  "files_moved": 3,
  "execution_time_ms": 2100,
  "token_usage": {"input": 680, "output": 420}
}
```

---

## POST /agents/pipeline — Multi-Step Pipeline

Chain multiple agent steps into a single server-side execution. Steps are auto-wired by data type, or you can declare explicit dependencies with `depends_on` for parallel fan-in patterns.

**Request body**
```json
{
  "steps": [
    {"agent": "image_search", "intent": "find damaged utility poles"},
    {"agent": "folder", "intent": "sort by damage severity"}
  ],
  "image_ids": null,
  "document_ids": null
}
```

Available agents: `image_search`, `document_search`, `link_search`, `analysis`, `document_analysis`, `link_analysis`, `assistant`, `folder`, `cross_reference`, `analytics`, `chat`

**DAG example with parallel execution**
```json
{
  "steps": [
    {"agent": "image_search", "intent": "utility poles"},
    {"agent": "document_search", "intent": "inspection reports"},
    {"agent": "assistant", "intent": "Cross-reference findings", "depends_on": [0, 1]}
  ]
}
```

Steps 0 and 1 execute in parallel (wave 1); step 2 waits for both (wave 2).

**Response** `200 OK`
```json
{
  "success": true,
  "nodes": [
    {
      "node_id": "a1b2c3d4",
      "agent": "image_search",
      "status": "completed",
      "summary": "Found 23 images of damaged utility poles",
      "execution_time_ms": 1450
    },
    {
      "node_id": "e5f6g7h8",
      "agent": "folder",
      "status": "completed",
      "summary": "Created 3 folders and organized 23 files",
      "execution_time_ms": 2100
    }
  ],
  "execution_time_ms": 3680,
  "total_waves": 2,
  "errors": [],
  "token_usage": {"input": 850, "output": 520}
}
```

```python
result = await client.pipeline() \
    .search_images("damaged utility poles") \
    .organize("sort by damage severity") \
    .run()
```

---

## See Also

- [Chat API](chat.md) — interactive stateful sessions using the same agents
- [Documents API](documents.md) — upload documents for agent analysis
- [Folders API](folders.md) — manually manage folders
- SDK: `client.agent_search`, `client.agent_operations`, `client.pipeline()`
