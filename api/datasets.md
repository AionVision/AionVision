# Datasets API

> Base URL: `https://api.aionvision.tech/api/v2`
> Authentication: `Authorization: Bearer {api_key}`

Create and export structured datasets from batch processing results. Once a batch completes, create a dataset from its results to preserve them, enable sharing, and export them into standard ML training formats (CSV, COCO, YOLO, Pascal VOC).

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /datasets | Create a dataset from a completed batch |
| GET | /datasets | List all datasets |
| GET | /datasets/{dataset_id} | Get dataset details |
| POST | /datasets/{dataset_id}/export | Export dataset to a file |
| GET | /datasets/statistics/summary | Aggregated dataset statistics |

---

## POST /datasets — Create Dataset

Create a dataset from the results of a completed batch operation.

**Request**
```http
POST /api/v2/datasets
Authorization: Bearer aion_your_api_key_here
Content-Type: application/json
```

**Body**
```json
{
  "batch_id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Safety Equipment Dataset Q1 2024",
  "description": "Workplace safety equipment detection results",
  "format_config": {
    "csv_delimiter": ",",
    "include_timestamps": true
  }
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| batch_id | string | Yes | UUID of the completed batch |
| name | string | Yes | Dataset name |
| description | string | No | Optional description |
| format_config | object | No | Format-specific configuration |

**Response** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Safety Equipment Dataset Q1 2024",
  "description": "Workplace safety equipment detection results",
  "batch_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z",
  "batch_status": "completed",
  "total_items": 500,
  "successful_items": 487,
  "export_count": 0,
  "supported_formats": ["csv", "coco", "yolo", "pascal_voc"],
  "latest_export": null
}
```

`status` values: `"pending"`, `"processing"`, `"ready"`, `"failed"`

```bash
curl -X POST https://api.aionvision.tech/api/v2/datasets \
  -H "Authorization: Bearer aion_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"batch_id": "550e8400-...", "name": "Safety Equipment Dataset Q1 2024"}'
```
```python
async with AionVision(api_key="aion_...") as client:
    dataset = await client.datasets.create(
        batch_id="550e8400-...",
        name="Safety Equipment Dataset Q1 2024"
    )
```

---

## GET /datasets — List Datasets

**Query parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| status | string | Filter: `pending`, `processing`, `ready`, `failed` |
| limit | integer | Max results, default 100 |
| offset | integer | Pagination offset, default 0 |

**Response** `200 OK`
```json
{
  "datasets": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Safety Equipment Dataset Q1 2024",
      "batch_id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "ready",
      "created_at": "2025-01-15T10:30:00Z",
      "total_items": 500,
      "successful_items": 487,
      "export_count": 3,
      "supported_formats": ["csv", "coco", "yolo", "pascal_voc"],
      "latest_export": {
        "export_id": "export_001",
        "format": "csv",
        "created_at": "2025-01-20T15:00:00Z"
      }
    }
  ],
  "total_count": 1,
  "limit": 100,
  "offset": 0,
  "has_more": false
}
```

---

## POST /datasets/{dataset_id}/export — Export Dataset

Export a dataset to a downloadable file. Synchronous — returns a download URL immediately.

**Request body**
```json
{
  "format": "csv",
  "options": {
    "delimiter": ","
  },
  "include_failed_items": false
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| format | string | Yes | `"csv"`, `"coco"`, `"yolo"`, or `"pascal_voc"` |
| options | object | No | Format-specific settings (e.g. CSV delimiter) |
| include_failed_items | boolean | No | Include failed batch items. Default: `false` |

**Response** `200 OK`
```json
{
  "export_id": "550e8400-e29b-41d4-a716-446655440000",
  "dataset_id": "660f9500-e29b-41d4-a716-446655440000",
  "format": "csv",
  "status": "completed",
  "record_count": 487,
  "download_url": "https://api.aionvision.tech/exports/dataset_550e8400.csv",
  "file_size_bytes": 245678,
  "content_type": "text/csv",
  "exported_at": "2025-01-15T10:30:00Z"
}
```

**Export format details**

| Format | Use case | Content type |
|--------|----------|--------------|
| `csv` | Spreadsheet analysis, general export | `text/csv` |
| `coco` | Object detection model training (MS COCO format) | `application/json` |
| `yolo` | YOLO model training (annotation files) | `application/zip` |
| `pascal_voc` | Pascal VOC format (XML annotations) | `application/zip` |

```bash
curl -X POST https://api.aionvision.tech/api/v2/datasets/550e8400-.../export \
  -H "Authorization: Bearer aion_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"format": "coco"}'
```
```python
export = await client.datasets.export(dataset_id="550e8400-...", format="coco")
print(export.download_url)
```

---

## GET /datasets/statistics/summary — Statistics

Get aggregated statistics across all datasets. Accepts `?days=30` query parameter.

**Response** `200 OK`
```json
{
  "dataset_statistics": {
    "total_datasets": 15,
    "avg_items_per_dataset": 500.0,
    "total_items": 7500,
    "by_status": {
      "ready": 12,
      "pending": 1,
      "processing": 2
    }
  },
  "export_statistics": {
    "total_exports": 45,
    "total_data_volume": 125000000,
    "by_format": {
      "csv": {"count": 25, "total_size": 75000000, "avg_export_time_seconds": 2.5},
      "coco": {"count": 15, "total_size": 40000000, "avg_export_time_seconds": 4.1},
      "yolo": {"count": 5, "total_size": 10000000, "avg_export_time_seconds": 1.8}
    }
  },
  "popular_formats": [
    {"format": "csv", "usage_count": 25},
    {"format": "coco", "usage_count": 15}
  ],
  "period": {
    "since": "2025-01-07T00:00:00Z",
    "until": "2025-02-07T00:00:00Z"
  }
}
```

---

## See Also

- [Files API](files.md) — manage uploaded images used in batches
- SDK: `client.datasets` — `create()`, `list()`, `get()`, `export()`
