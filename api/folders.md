# Folders API

> Base URL: `https://api.aionvision.tech/api/v2`
> Authentication: `Authorization: Bearer {api_key}`

Organize files into a hierarchical folder structure. Supports nested folders, breadcrumb navigation, and bulk file movement. The AI agents can also create and organize folders automatically via the [Agents API](agents.md).

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /folders | List all folders as a flat list |
| GET | /folders/{folder_id} | Get folder contents (subfolders + file count) |
| GET | /folders/{folder_id}/breadcrumbs | Get ancestor chain for navigation |
| POST | /folders | Create a new folder |
| PATCH | /folders/{folder_id} | Rename a folder |
| POST | /folders/{folder_id}/move | Move folder to a new parent |
| DELETE | /folders/{folder_id} | Delete folder |
| POST | /folders/move-files | Move files into a folder |

---

## GET /folders — List Folders

Returns all folders as a flat list. Build the tree client-side using the `parent_id` field.

**Response** `200 OK`
```json
{
  "folders": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Project Photos",
      "parent_id": null,
      "depth": 0,
      "file_count": 25,
      "subfolder_count": 3,
      "created_at": "2025-01-15T10:00:00Z",
      "updated_at": "2025-01-15T10:30:00Z"
    },
    {
      "id": "660f9500-f39c-52e5-b827-557766550111",
      "name": "Site Inspections",
      "parent_id": "550e8400-e29b-41d4-a716-446655440000",
      "depth": 1,
      "file_count": 10,
      "subfolder_count": 0,
      "created_at": "2025-01-15T10:05:00Z",
      "updated_at": "2025-01-15T10:30:00Z"
    }
  ]
}
```

---

## GET /folders/{folder_id} — Get Folder Contents

Get subfolders, file count, and breadcrumbs for a specific folder.

**Query params**: `?limit=50&offset=0`

**Response** `200 OK`
```json
{
  "folder": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Project Photos",
    "parent_id": null,
    "depth": 0,
    "file_count": 25,
    "subfolder_count": 3
  },
  "breadcrumbs": [
    {"id": "550e8400-e29b-41d4-a716-446655440000", "name": "Project Photos", "depth": 0}
  ],
  "subfolders": [
    {
      "id": "660f9500-f39c-52e5-b827-557766550111",
      "name": "Site Inspections",
      "parent_id": "550e8400-e29b-41d4-a716-446655440000",
      "depth": 1,
      "file_count": 10
    }
  ],
  "total_files": 25,
  "has_more_files": false
}
```

To list the files inside a folder, use `GET /user-files?folder_id={folder_id}`.

---

## POST /folders — Create Folder

**Request**
```http
POST /api/v2/folders
Authorization: Bearer aion_your_api_key_here
Content-Type: application/json
```

**Body**
```json
{
  "name": "New Folder",
  "parent_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

`parent_id` is optional — omit or set to `null` for a root-level folder.

**Response** `201 Created`
```json
{
  "id": "770a0600-a40d-63f6-c938-668877660222",
  "name": "New Folder",
  "parent_id": "550e8400-e29b-41d4-a716-446655440000",
  "depth": 1,
  "file_count": 0,
  "subfolder_count": 0,
  "created_at": "2025-01-15T10:30:00Z"
}
```

```bash
curl -X POST https://api.aionvision.tech/api/v2/folders \
  -H "Authorization: Bearer aion_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"name": "Site Inspections", "parent_id": "550e8400-e29b-41d4-a716-446655440000"}'
```
```python
async with AionVision(api_key="aion_...") as client:
    folder = await client.folders.create("Site Inspections", parent_id="550e8400-...")
```

---

## PATCH /folders/{folder_id} — Rename

```json
{"name": "Renamed Folder"}
```

**Response** `200 OK` — returns updated folder object.

---

## POST /folders/{folder_id}/move — Move Folder

Move a folder to a different parent. Returns `422` if the move would create a circular reference.

```json
{"new_parent_id": "770a0600-a40d-63f6-c938-668877660222"}
```

Set `new_parent_id` to `null` to move to the root level.

**Response** `200 OK` — returns updated folder object with new `parent_id` and `depth`.

---

## DELETE /folders/{folder_id} — Delete Folder

**Query parameter**: `?mode=move_to_parent` (default) or `?mode=delete_all`

| Mode | Behavior |
|------|----------|
| `move_to_parent` | Files and subfolders move to the parent folder (safe) |
| `delete_all` | Everything inside is permanently deleted |

**Response** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "files_affected": 25,
  "subfolders_affected": 3,
  "mode": "move_to_parent"
}
```

---

## POST /folders/move-files — Move Files

Move up to 100 files into a folder in one request.

**Request body**
```json
{
  "file_ids": [
    "550e8400-e29b-41d4-a716-446655440000",
    "660f9500-f39c-52e5-b827-557766550111"
  ],
  "folder_id": "770a0600-a40d-63f6-c938-668877660222"
}
```

Set `folder_id` to `null` to move files to the root level.

**Response** `200 OK`
```json
{"moved": 2, "total_requested": 2}
```

```python
await client.folders.move_files(
    file_ids=["550e8400-...", "660f9500-..."],
    folder_id="770a0600-..."
)
```

---

## GET /folders/{folder_id}/breadcrumbs — Breadcrumbs

Get the ancestor chain from root to the specified folder.

**Response** `200 OK`
```json
{
  "breadcrumbs": [
    {"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890", "name": "Projects", "depth": 0},
    {"id": "b2c3d4e5-f6a7-8901-bcde-f12345678901", "name": "2024", "depth": 1},
    {"id": "c3d4e5f6-a7b8-9012-cdef-123456789012", "name": "Site A", "depth": 2}
  ]
}
```

---

## See Also

- [Files API](files.md) — `GET /user-files?folder_id={id}` to list files in a folder
- [Agents API](agents.md) — `POST /agents/organize` to auto-organize files with AI
- SDK: `client.folders` — `create()`, `rename()`, `move()`, `move_files()`, `delete()`
