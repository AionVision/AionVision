# Colors API

> Base URL: `https://api.aionvision.tech/api/v2`
> Authentication: `Authorization: Bearer {api_key}`

Extract dominant colors from images, search your library by color, and browse color families.

**Color extraction is automatic.** When you upload an image, colors are extracted automatically — no extra API call needed. Simply retrieve the results with `GET /colors/images/{image_id}`. The extract endpoints below are only needed to re-run extraction with different settings (e.g., fewer colors or force refresh).

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /colors/images/{image_id} | Get color analysis for an image |
| POST | /colors/images/{image_id}/extract | Re-extract colors with custom settings |
| POST | /colors/batch/extract | Re-extract colors for multiple images |
| POST | /colors/search | Search images by color (hex, name, or family) |
| GET | /colors/families | List available color families |

---

## GET /colors/images/{image_id} — Get Color Analysis

**Response** `200 OK`
```json
{
  "image_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "color_analysis": {
    "version": "1.0",
    "dominant_colors": [
      {
        "rank": 1,
        "percentage": 35.2,
        "hex": "#C4A87C",
        "name": "Walnut",
        "family": "earth_tone",
        "rgb": {"r": 196, "g": 168, "b": 124},
        "hsl": {"h": 37, "s": 38, "l": 63},
        "lab": {"l": 70.1, "a": 3.2, "b": 25.8}
      },
      {
        "rank": 2,
        "percentage": 22.8,
        "hex": "#8B7355",
        "name": "Dark Tan",
        "family": "earth_tone",
        "rgb": {"r": 139, "g": 115, "b": 85},
        "hsl": {"h": 33, "s": 24, "l": 44},
        "lab": {"l": 49.5, "a": 5.1, "b": 19.3}
      }
    ],
    "analytics": {
      "temperature": {"value": "warm", "score": 0.82},
      "brightness": {"average": 58, "category": "medium"},
      "saturation": {"average": 31, "category": "medium"}
    },
    "extracted_at": "2025-01-15T14:22:00Z"
  }
}
```

`status` values: `"pending"`, `"processing"`, `"completed"`, `"failed"`

---

## POST /colors/images/{image_id}/extract — Re-extract Colors

Re-run color extraction with custom settings. Colors are already extracted automatically on upload — use this only to force a refresh or change the number of extracted colors.

**Query parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| force | boolean | Re-extract even if results already exist. Default: `false` |
| n_colors | integer | Number of colors to extract, 3–16. Default: `16` |

**Response** `200 OK` — same format as GET above.

```bash
curl -X POST "https://api.aionvision.tech/api/v2/colors/images/550e8400-e29b-41d4-a716-446655440000/extract?n_colors=8" \
  -H "Authorization: Bearer aion_your_api_key_here"
```
```python
result = await client.colors.extract("550e8400-...", n_colors=8)
```

---

## POST /colors/batch/extract — Batch Re-extraction

Re-run color extraction for multiple images with custom settings (max 200 per request). Colors are already extracted automatically on upload.

**Request body**
```json
{
  "image_ids": [
    "550e8400-e29b-41d4-a716-446655440000",
    "660f9500-f39c-52e5-b827-557766550111"
  ],
  "force": false,
  "n_colors": 16
}
```

**Response** `200 OK`
```json
{
  "queued_count": 2,
  "message": "2 images queued for color extraction"
}
```

Poll `GET /colors/images/{image_id}` for individual results.

---

## POST /colors/search — Search by Color

Find images that contain a specific color. At least one of `hex_code`, `color_name`, or `color_family` is required.

**Request**
```http
POST /api/v2/colors/search
Authorization: Bearer aion_your_api_key_here
Content-Type: application/json
```

**Body**
```json
{
  "hex_code": "#C4A87C",
  "color_name": "walnut",
  "color_family": "earth_tone",
  "delta_e_threshold": 15.0,
  "min_percentage": 5.0,
  "limit": 50,
  "offset": 0
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| hex_code | string | Hex color to match (e.g. `"#C4A87C"`) |
| color_name | string | Semantic color name (e.g. `"walnut"`, `"navy blue"`) |
| color_family | string | Color family name (see `GET /colors/families`) |
| delta_e_threshold | float | Color tolerance 0–100 (default: `15.0`). Lower = more precise |
| min_percentage | float | Minimum coverage % in image (default: `5.0`) |
| limit | integer | 1–200, default 50 |
| offset | integer | Default 0 |

**Response** `200 OK`
```json
{
  "results": [
    {
      "image_id": "550e8400-e29b-41d4-a716-446655440000",
      "thumbnail_url": "https://cdn.aionvision.tech/thumbnails/550e8400.jpg",
      "color_analysis": {
        "dominant_colors": [
          {
            "rank": 1,
            "percentage": 35.2,
            "hex": "#C4A87C",
            "name": "Walnut",
            "family": "earth_tone"
          }
        ]
      },
      "match_score": 4.2
    }
  ],
  "total_count": 128,
  "limit": 50,
  "offset": 0
}
```

`match_score` is the Delta-E color distance (lower = better match).

```bash
curl -X POST https://api.aionvision.tech/api/v2/colors/search \
  -H "Authorization: Bearer aion_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"hex_code": "#C4A87C", "delta_e_threshold": 10.0, "limit": 20}'
```
```python
results = await client.colors.search(hex_code="#C4A87C", limit=20)
for r in results.results:
    print(r.image_id, r.match_score)
```

---

## GET /colors/families — List Color Families

List all available color families with display names, descriptions, and example hex codes.

**Response** `200 OK`
```json
[
  {
    "name": "earth_tone",
    "display_name": "Earth Tones",
    "description": "Warm, natural colors inspired by earth and nature",
    "example_colors": ["#8B4513", "#A0522D", "#D2B48C", "#C4A87C"]
  },
  {
    "name": "neutral",
    "display_name": "Neutrals",
    "description": "Blacks, whites, grays — versatile foundation colors",
    "example_colors": ["#2C2C2C", "#808080", "#D3D3D3", "#F5F5F5"]
  },
  {
    "name": "metallic",
    "display_name": "Metallics",
    "description": "Gold, silver, bronze, copper",
    "example_colors": ["#FFD700", "#C0C0C0", "#CD7F32", "#B87333"]
  }
]
```

Use the `name` field (e.g. `"earth_tone"`) in the `color_family` parameter of `POST /colors/search`.

---

## Color Data Format

Each dominant color includes three color space representations:

| Field | Format | Description |
|-------|--------|-------------|
| `hex` | `"#RRGGBB"` | Web hex code |
| `rgb` | `{"r": 0-255, "g": 0-255, "b": 0-255}` | RGB channels |
| `hsl` | `{"h": 0-360, "s": 0-100, "l": 0-100}` | Hue/Saturation/Lightness |
| `lab` | `{"l": float, "a": float, "b": float}` | Perceptual CIE LAB space |
| `percentage` | `float` | Coverage % of this color in the image |
| `family` | `string` | Color family name |

---

## See Also

- [Files API](files.md) — manage uploaded images
- SDK: `client.colors` — `extract()`, `search()`, `search_all()`, `list_families()`, `batch_extract()`
