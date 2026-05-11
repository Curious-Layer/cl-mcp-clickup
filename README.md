**Manage tasks, projects, and team workflows in ClickUp through the Model Context Protocol.**

A Model Context Protocol (MCP) server that exposes ClickUp's API for managing workspaces, tasks, time tracking, and team collaboration.

---

## Overview

The CL ClickUp MCP Server provides stateless, multi-user access to the ClickUp API with server-side credential injection:

- Full workspace hierarchy management — spaces, folders, lists, and tasks
- Time tracking, goals, checklists, custom fields, tags, and views
- Team collaboration tools — comments, members, webhooks, docs, and chat

Perfect for:

- Automating task creation, updates, and assignment from AI workflows
- Querying and reporting across projects, sprints, and workspaces
- Integrating ClickUp data into custom pipelines and productivity tools

---

## Tools

### Utility

<details>
<summary><code>ping</code> → Health check for the MCP server</summary>

Verifies the server is running and reachable. No credentials required.

**Inputs:**

No inputs required.

**Output:**

```json
{
  "status": "ok",
  "server": "CL ClickUp MCP Server",
  "message": "Server is running successfully!",
  "api_base": "https://api.clickup.com/api/v2"
}
```

**Usage Example:**

```bash
POST /mcp/clickup/ping
```

</details>

---

### Authorization

<details>
<summary><code>get_authorized_user</code> → Get the authenticated user's profile</summary>

Returns the ClickUp user associated with the injected OAuth access token.

**Inputs:**

No inputs required.

**Output:**

```json
{
  "user": {
    "id": 1234567,
    "username": "jane_doe",
    "email": "jane@example.com",
    "color": "#7B68EE",
    "profilePicture": "https://..."
  }
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_authorized_user
```

</details>

---

<details>
<summary><code>get_authorized_teams</code> → List all accessible Workspaces</summary>

Returns all ClickUp Workspaces (teams) the authenticated user has access to.

**Inputs:**

No inputs required.

**Output:**

```json
{
  "teams": [
    {
      "id": "9876543",
      "name": "My Workspace",
      "color": "#536DFE",
      "members": [{ "user": { "id": 1234567, "username": "jane_doe" } }]
    }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_authorized_teams
```

</details>

---

### Spaces

<details>
<summary><code>get_spaces</code> → List all Spaces in a Workspace</summary>

Returns all Spaces within the specified Workspace, with optional filtering for archived spaces.

**Inputs:**

- `team_id` (string, required) → The ID of the Workspace (team).
- `archived` (boolean, optional) → Include archived spaces. Default: `false`.

**Output:**

```json
{
  "spaces": [
    {
      "id": "90110011",
      "name": "Engineering",
      "archived": false,
      "features": { "due_dates": { "enabled": true } }
    }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_spaces

{
  "team_id": "9876543"
}
```

</details>

---

<details>
<summary><code>get_space</code> → Get a specific Space</summary>

Returns full details for a single Space by its ID.

**Inputs:**

- `space_id` (string, required) → The ID of the Space.

**Output:**

```json
{
  "id": "90110011",
  "name": "Engineering",
  "archived": false,
  "multiple_assignees": true,
  "features": { "due_dates": { "enabled": true }, "time_tracking": { "enabled": true } }
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_space

{
  "space_id": "90110011"
}
```

</details>

---

<details>
<summary><code>create_space</code> → Create a new Space in a Workspace</summary>

Creates a Space with the specified name and feature configuration inside a Workspace.

**Inputs:**

- `team_id` (string, required) → The ID of the Workspace (team).
- `body` (string, required) → JSON string of the space definition.

**Body fields:**

- `name` (string, required) → Space name.
- `multiple_assignees` (boolean, optional) → Allow multiple assignees on tasks.
- `features` (object, optional) → Feature flags (e.g. `due_dates`, `time_tracking`).

**Output:**

```json
{
  "id": "90110099",
  "name": "New Space",
  "archived": false
}
```

**Usage Example:**

```bash
POST /mcp/clickup/create_space

{
  "team_id": "9876543",
  "body": "{\"name\": \"New Space\", \"multiple_assignees\": true}"
}
```

</details>

---

<details>
<summary><code>update_space</code> → Update an existing Space</summary>

Updates the name, settings, or feature flags of an existing Space.

**Inputs:**

- `space_id` (string, required) → The ID of the Space to update.
- `body` (string, required) → JSON string of fields to update.

**Body fields:**

- `name` (string, optional) → New Space name.
- `multiple_assignees` (boolean, optional) → Allow multiple assignees.
- `features` (object, optional) → Updated feature flags.

**Output:**

```json
{
  "id": "90110011",
  "name": "Engineering (Updated)",
  "archived": false
}
```

**Usage Example:**

```bash
POST /mcp/clickup/update_space

{
  "space_id": "90110011",
  "body": "{\"name\": \"Engineering (Updated)\"}"
}
```

</details>

---

<details>
<summary><code>delete_space</code> → Delete a Space</summary>

Permanently deletes a Space and all its contents.

**Inputs:**

- `space_id` (string, required) → The ID of the Space to delete.

**Output:**

```json
{
  "success": true
}
```

**Usage Example:**

```bash
POST /mcp/clickup/delete_space

{
  "space_id": "90110011"
}
```

</details>

---

### Folders

<details>
<summary><code>get_folders</code> → List all Folders in a Space</summary>

Returns all Folders within the specified Space.

**Inputs:**

- `space_id` (string, required) → The ID of the Space.
- `archived` (boolean, optional) → Include archived folders. Default: `false`.

**Output:**

```json
{
  "folders": [
    { "id": "78901234", "name": "Sprint 1", "task_count": "12", "lists": [] }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_folders

{
  "space_id": "90110011"
}
```

</details>

---

<details>
<summary><code>get_folder</code> → Get a specific Folder</summary>

Returns full details for a single Folder by its ID.

**Inputs:**

- `folder_id` (string, required) → The ID of the Folder.

**Output:**

```json
{
  "id": "78901234",
  "name": "Sprint 1",
  "task_count": "12",
  "lists": [{ "id": "56789012", "name": "Backlog" }]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_folder

{
  "folder_id": "78901234"
}
```

</details>

---

<details>
<summary><code>create_folder</code> → Create a new Folder in a Space</summary>

Creates a named Folder inside the specified Space.

**Inputs:**

- `space_id` (string, required) → The ID of the Space.
- `body` (string, required) → JSON string of the folder definition.

**Body fields:**

- `name` (string, required) → Folder name.

**Output:**

```json
{
  "id": "78901299",
  "name": "Sprint 2",
  "task_count": "0"
}
```

**Usage Example:**

```bash
POST /mcp/clickup/create_folder

{
  "space_id": "90110011",
  "body": "{\"name\": \"Sprint 2\"}"
}
```

</details>

---

<details>
<summary><code>update_folder</code> → Update an existing Folder</summary>

Renames or modifies an existing Folder.

**Inputs:**

- `folder_id` (string, required) → The ID of the Folder to update.
- `body` (string, required) → JSON string of fields to update.

**Body fields:**

- `name` (string, optional) → New Folder name.

**Output:**

```json
{
  "id": "78901234",
  "name": "Sprint 1 (Completed)"
}
```

**Usage Example:**

```bash
POST /mcp/clickup/update_folder

{
  "folder_id": "78901234",
  "body": "{\"name\": \"Sprint 1 (Completed)\"}"
}
```

</details>

---

<details>
<summary><code>delete_folder</code> → Delete a Folder</summary>

Permanently deletes a Folder and all its lists.

**Inputs:**

- `folder_id` (string, required) → The ID of the Folder to delete.

**Output:**

```json
{
  "success": true
}
```

**Usage Example:**

```bash
POST /mcp/clickup/delete_folder

{
  "folder_id": "78901234"
}
```

</details>

---

### Lists

<details>
<summary><code>get_lists</code> → List all Lists in a Folder</summary>

Returns all Lists within the specified Folder.

**Inputs:**

- `folder_id` (string, required) → The ID of the Folder.
- `archived` (boolean, optional) → Include archived lists. Default: `false`.

**Output:**

```json
{
  "lists": [
    { "id": "56789012", "name": "Backlog", "task_count": 8, "status": null }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_lists

{
  "folder_id": "78901234"
}
```

</details>

---

<details>
<summary><code>get_folderless_lists</code> → List all Lists not in a Folder</summary>

Returns Lists that belong directly to a Space (not inside any Folder).

**Inputs:**

- `space_id` (string, required) → The ID of the Space.
- `archived` (boolean, optional) → Include archived lists. Default: `false`.

**Output:**

```json
{
  "lists": [
    { "id": "56789099", "name": "Inbox", "task_count": 3 }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_folderless_lists

{
  "space_id": "90110011"
}
```

</details>

---

<details>
<summary><code>get_list</code> → Get a specific List</summary>

Returns full details for a single List by its ID.

**Inputs:**

- `list_id` (string, required) → The ID of the List.

**Output:**

```json
{
  "id": "56789012",
  "name": "Backlog",
  "task_count": 8,
  "due_date": null,
  "priority": null
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_list

{
  "list_id": "56789012"
}
```

</details>

---

<details>
<summary><code>create_list</code> → Create a new List in a Folder</summary>

Creates a named List inside the specified Folder.

**Inputs:**

- `folder_id` (string, required) → The ID of the Folder.
- `body` (string, required) → JSON string of the list definition.

**Body fields:**

- `name` (string, required) → List name.
- `content` (string, optional) → List description.
- `due_date` (integer, optional) → Due date as Unix timestamp in ms.
- `priority` (integer, optional) → Priority level (1–4).
- `assignee` (integer, optional) → Default assignee user ID.
- `status` (string, optional) → List status.

**Output:**

```json
{
  "id": "56789099",
  "name": "In Review"
}
```

**Usage Example:**

```bash
POST /mcp/clickup/create_list

{
  "folder_id": "78901234",
  "body": "{\"name\": \"In Review\", \"content\": \"Tasks under code review\"}"
}
```

</details>

---

<details>
<summary><code>create_folderless_list</code> → Create a List directly in a Space</summary>

Creates a List at the Space level, not inside any Folder.

**Inputs:**

- `space_id` (string, required) → The ID of the Space.
- `body` (string, required) → JSON string of the list definition (same fields as `create_list`).

**Output:**

```json
{
  "id": "56789100",
  "name": "General"
}
```

**Usage Example:**

```bash
POST /mcp/clickup/create_folderless_list

{
  "space_id": "90110011",
  "body": "{\"name\": \"General\"}"
}
```

</details>

---

<details>
<summary><code>update_list</code> → Update an existing List</summary>

Updates the name, description, due date, or other properties of a List.

**Inputs:**

- `list_id` (string, required) → The ID of the List to update.
- `body` (string, required) → JSON string of fields to update.

**Body fields:**

- `name` (string, optional) → New List name.
- `content` (string, optional) → Updated description.
- `due_date` (integer, optional) → New due date (Unix ms).
- `priority` (integer, optional) → Priority level (1–4).
- `assignee` (integer, optional) → Updated default assignee.
- `unset_status` (boolean, optional) → Clear the list status.

**Output:**

```json
{
  "id": "56789012",
  "name": "Backlog (Archived)"
}
```

**Usage Example:**

```bash
POST /mcp/clickup/update_list

{
  "list_id": "56789012",
  "body": "{\"name\": \"Backlog (Archived)\"}"
}
```

</details>

---

<details>
<summary><code>delete_list</code> → Delete a List</summary>

Permanently deletes a List and all its tasks.

**Inputs:**

- `list_id` (string, required) → The ID of the List to delete.

**Output:**

```json
{
  "success": true
}
```

**Usage Example:**

```bash
POST /mcp/clickup/delete_list

{
  "list_id": "56789012"
}
```

</details>

---

### Tasks

<details>
<summary><code>get_tasks</code> → List tasks in a List</summary>

Returns tasks in the specified List with optional pagination and filtering.

**Inputs:**

- `list_id` (string, required) → The ID of the List.
- `archived` (boolean, optional) → Include archived tasks. Default: `false`.
- `include_closed` (boolean, optional) → Include closed tasks. Default: `false`.
- `page` (integer, optional) → Page number (0-indexed). Default: `0`.
- `order_by` (string, optional) → Sort field: `id`, `created`, `updated`, `due_date`.
- `reverse` (boolean, optional) → Reverse the sort order.
- `subtasks` (boolean, optional) → Include subtasks.
- `statuses` (string, optional) → Comma-separated status names to filter by.
- `assignees` (string, optional) → Comma-separated assignee user IDs to filter by.
- `due_date_gt` (integer, optional) → Tasks with due date after this Unix ms timestamp.
- `due_date_lt` (integer, optional) → Tasks with due date before this Unix ms timestamp.
- `date_created_gt` (integer, optional) → Tasks created after this Unix ms timestamp.
- `date_created_lt` (integer, optional) → Tasks created before this Unix ms timestamp.
- `date_updated_gt` (integer, optional) → Tasks updated after this Unix ms timestamp.
- `date_updated_lt` (integer, optional) → Tasks updated before this Unix ms timestamp.

**Output:**

```json
{
  "tasks": [
    {
      "id": "abc123",
      "name": "Fix login bug",
      "status": { "status": "in progress", "color": "#4169E1" },
      "priority": { "id": "2", "priority": "high" },
      "assignees": [{ "id": 1234567, "username": "jane_doe" }],
      "due_date": "1717200000000"
    }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_tasks

{
  "list_id": "56789012",
  "include_closed": false,
  "order_by": "due_date"
}
```

</details>

---

<details>
<summary><code>get_task</code> → Get a specific task</summary>

Returns full details for a single task by its ID.

**Inputs:**

- `task_id` (string, required) → The ID of the task.
- `include_subtasks` (boolean, optional) → Include subtasks in response. Default: `false`.
- `include_markdown_description` (boolean, optional) → Return description as markdown. Default: `false`.

**Output:**

```json
{
  "id": "abc123",
  "name": "Fix login bug",
  "description": "Investigate session token expiry",
  "status": { "status": "in progress" },
  "priority": { "priority": "high" },
  "assignees": [{ "id": 1234567 }],
  "due_date": "1717200000000",
  "tags": [],
  "subtasks": []
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_task

{
  "task_id": "abc123",
  "include_subtasks": true
}
```

</details>

---

<details>
<summary><code>create_task</code> → Create a new task in a List</summary>

Creates a task with the specified properties inside a List.

**Inputs:**

- `list_id` (string, required) → The ID of the List.
- `body` (string, required) → JSON string of the task definition.

**Body fields:**

- `name` (string, required) → Task name.
- `description` (string, optional) → Task description (plain text).
- `markdown_description` (string, optional) → Task description in markdown.
- `assignees` (array of integers, optional) → List of assignee user IDs.
- `tags` (array of strings, optional) → Tag names to apply.
- `status` (string, optional) → Initial status name.
- `priority` (integer, optional) → Priority level: `1` Urgent, `2` High, `3` Normal, `4` Low.
- `due_date` (integer, optional) → Due date as Unix timestamp in ms.
- `due_date_time` (boolean, optional) → Whether due_date includes a time component.
- `time_estimate` (integer, optional) → Time estimate in milliseconds.
- `start_date` (integer, optional) → Start date as Unix timestamp in ms.
- `notify_all` (boolean, optional) → Notify all assignees.
- `parent` (string, optional) → Parent task ID (to create a subtask).

**Output:**

```json
{
  "id": "abc999",
  "name": "Implement dark mode",
  "status": { "status": "Open" },
  "priority": { "priority": "normal" },
  "assignees": []
}
```

**Usage Example:**

```bash
POST /mcp/clickup/create_task

{
  "list_id": "56789012",
  "body": "{\"name\": \"Implement dark mode\", \"priority\": 3, \"assignees\": [1234567]}"
}
```

</details>

---

<details>
<summary><code>update_task</code> → Update an existing task</summary>

Updates any combination of task fields including name, status, priority, assignees, and due date.

**Inputs:**

- `task_id` (string, required) → The ID of the task to update.
- `body` (string, required) → JSON string of fields to update.

**Body fields:**

- `name` (string, optional) → New task name.
- `description` (string, optional) → Updated description.
- `status` (string, optional) → New status name.
- `priority` (integer, optional) → New priority (1–4, or `null` to clear).
- `due_date` (integer, optional) → New due date (Unix ms, or `null` to clear).
- `assignees` (object, optional) → `{"add": [id], "rem": [id]}` to add/remove assignees.
- `archived` (boolean, optional) → Archive or unarchive the task.

**Output:**

```json
{
  "id": "abc123",
  "name": "Fix login bug",
  "status": { "status": "in review" },
  "priority": { "priority": "urgent" }
}
```

**Usage Example:**

```bash
POST /mcp/clickup/update_task

{
  "task_id": "abc123",
  "body": "{\"status\": \"in review\", \"priority\": 1}"
}
```

</details>

---

<details>
<summary><code>delete_task</code> → Delete a task</summary>

Permanently deletes a task.

**Inputs:**

- `task_id` (string, required) → The ID of the task to delete.

**Output:**

```json
{
  "success": true
}
```

**Usage Example:**

```bash
POST /mcp/clickup/delete_task

{
  "task_id": "abc123"
}
```

</details>

---

<details>
<summary><code>get_filtered_team_tasks</code> → List tasks across a Workspace with filters</summary>

Returns tasks across an entire Workspace with optional filtering by space, folder, list, status, assignee, and date ranges.

**Inputs:**

- `team_id` (string, required) → The ID of the Workspace (team).
- `page` (integer, optional) → Page number (0-indexed). Default: `0`.
- `order_by` (string, optional) → Sort field: `id`, `created`, `updated`, `due_date`.
- `reverse` (boolean, optional) → Reverse the sort order.
- `subtasks` (boolean, optional) → Include subtasks.
- `space_ids` (string, optional) → Comma-separated Space IDs to filter by.
- `project_ids` (string, optional) → Comma-separated Folder IDs to filter by.
- `list_ids` (string, optional) → Comma-separated List IDs to filter by.
- `statuses` (string, optional) → Comma-separated status names to filter by.
- `include_closed` (boolean, optional) → Include closed tasks. Default: `false`.
- `assignees` (string, optional) → Comma-separated assignee user IDs to filter by.
- `due_date_gt` (integer, optional) → Tasks with due date after this Unix ms timestamp.
- `due_date_lt` (integer, optional) → Tasks with due date before this Unix ms timestamp.
- `date_created_gt` (integer, optional) → Tasks created after this Unix ms timestamp.
- `date_created_lt` (integer, optional) → Tasks created before this Unix ms timestamp.
- `date_updated_gt` (integer, optional) → Tasks updated after this Unix ms timestamp.
- `date_updated_lt` (integer, optional) → Tasks updated before this Unix ms timestamp.

**Output:**

```json
{
  "tasks": [
    {
      "id": "abc123",
      "name": "Fix login bug",
      "list": { "id": "56789012", "name": "Backlog" },
      "folder": { "id": "78901234", "name": "Sprint 1" },
      "space": { "id": "90110011" }
    }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_filtered_team_tasks

{
  "team_id": "9876543",
  "statuses": "in progress,in review",
  "assignees": "1234567"
}
```

</details>

---

### Task Comments

<details>
<summary><code>get_task_comments</code> → List comments on a task</summary>

Returns all comments on the specified task, with optional pagination by date or comment ID.

**Inputs:**

- `task_id` (string, required) → The ID of the task.
- `start` (integer, optional) → Return comments after this Unix ms timestamp.
- `start_id` (string, optional) → Return comments after this comment ID.

**Output:**

```json
{
  "comments": [
    {
      "id": "55001122",
      "comment_text": "Looks good, merging tomorrow.",
      "user": { "id": 1234567, "username": "jane_doe" },
      "date": "1717200000000",
      "resolved": false
    }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_task_comments

{
  "task_id": "abc123"
}
```

</details>

---

<details>
<summary><code>create_task_comment</code> → Post a comment on a task</summary>

Adds a new comment to the specified task.

**Inputs:**

- `task_id` (string, required) → The ID of the task.
- `body` (string, required) → JSON string of the comment.

**Body fields:**

- `comment_text` (string, required) → The comment text.
- `assignee` (integer, optional) → Assign the comment to a user ID.
- `notify_all` (boolean, optional) → Notify all task watchers. Default: `false`.

**Output:**

```json
{
  "id": "55001199",
  "comment": [{ "text": "Looks good, merging tomorrow." }],
  "date": "1717200000000"
}
```

**Usage Example:**

```bash
POST /mcp/clickup/create_task_comment

{
  "task_id": "abc123",
  "body": "{\"comment_text\": \"Looks good, merging tomorrow.\", \"notify_all\": false}"
}
```

</details>

---

<details>
<summary><code>get_list_comments</code> → List comments on a List</summary>

Returns all comments posted on the specified List.

**Inputs:**

- `list_id` (string, required) → The ID of the list.
- `start` (integer, optional) → Return comments after this Unix ms timestamp.
- `start_id` (string, optional) → Return comments after this comment ID.

**Output:**

```json
{
  "comments": [
    {
      "id": "55001123",
      "comment_text": "This list needs triage.",
      "user": { "id": 1234567 },
      "date": "1717100000000"
    }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_list_comments

{
  "list_id": "56789012"
}
```

</details>

---

<details>
<summary><code>create_list_comment</code> → Post a comment on a List</summary>

Adds a new comment to the specified List.

**Inputs:**

- `list_id` (string, required) → The ID of the list.
- `body` (string, required) → JSON string of the comment.

**Body fields:**

- `comment_text` (string, required) → The comment text.
- `notify_all` (boolean, optional) → Notify all list members. Default: `false`.

**Output:**

```json
{
  "id": "55001200",
  "comment": [{ "text": "This list needs triage." }],
  "date": "1717100000000"
}
```

**Usage Example:**

```bash
POST /mcp/clickup/create_list_comment

{
  "list_id": "56789012",
  "body": "{\"comment_text\": \"This list needs triage.\"}"
}
```

</details>

---

<details>
<summary><code>update_comment</code> → Update an existing comment</summary>

Edits the text or resolved state of a comment.

**Inputs:**

- `comment_id` (string, required) → The ID of the comment to update.
- `body` (string, required) → JSON string of fields to update.

**Body fields:**

- `comment_text` (string, optional) → Updated comment text.
- `assignee` (integer, optional) → Updated assignee user ID.
- `resolved` (boolean, optional) → Mark or unmark as resolved.

**Output:**

```json
{
  "success": true
}
```

**Usage Example:**

```bash
POST /mcp/clickup/update_comment

{
  "comment_id": "55001122",
  "body": "{\"resolved\": true}"
}
```

</details>

---

<details>
<summary><code>delete_comment</code> → Delete a comment</summary>

Permanently deletes a comment.

**Inputs:**

- `comment_id` (string, required) → The ID of the comment to delete.

**Output:**

```json
{
  "success": true
}
```

**Usage Example:**

```bash
POST /mcp/clickup/delete_comment

{
  "comment_id": "55001122"
}
```

</details>

---

### Time Tracking

<details>
<summary><code>get_time_entries</code> → List time entries in a Workspace</summary>

Returns time entries within an optional date range, filterable by assignee.

**Inputs:**

- `team_id` (string, required) → The ID of the Workspace (team).
- `start_date` (integer, optional) → Start of range as Unix ms timestamp.
- `end_date` (integer, optional) → End of range as Unix ms timestamp.
- `assignee` (string, optional) → Filter by user ID.
- `include_task_tags` (boolean, optional) → Include task tags in response. Default: `false`.
- `include_location_names` (boolean, optional) → Include space/folder/list names. Default: `false`.

**Output:**

```json
{
  "data": [
    {
      "id": "1234567890",
      "task": { "id": "abc123", "name": "Fix login bug" },
      "duration": "3600000",
      "start": "1717100000000",
      "user": { "id": 1234567 }
    }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_time_entries

{
  "team_id": "9876543",
  "start_date": 1717100000000,
  "end_date": 1717200000000
}
```

</details>

---

<details>
<summary><code>get_single_time_entry</code> → Get a specific time entry</summary>

Returns full details for a single time entry.

**Inputs:**

- `team_id` (string, required) → The ID of the Workspace (team).
- `timer_id` (string, required) → The ID of the time entry.

**Output:**

```json
{
  "data": {
    "id": "1234567890",
    "task": { "id": "abc123" },
    "duration": "3600000",
    "start": "1717100000000",
    "end": "1717103600000"
  }
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_single_time_entry

{
  "team_id": "9876543",
  "timer_id": "1234567890"
}
```

</details>

---

<details>
<summary><code>create_time_entry</code> → Create a manual time entry</summary>

Logs time against a task with explicit start time and duration.

**Inputs:**

- `team_id` (string, required) → The ID of the Workspace (team).
- `body` (string, required) → JSON string of the time entry.

**Body fields:**

- `start` (integer, required) → Start time as Unix ms timestamp.
- `duration` (integer, required) → Duration in milliseconds.
- `tid` (string, optional) → Task ID to log time against.
- `description` (string, optional) → Note about the work done.
- `billable` (boolean, optional) → Mark as billable.

**Output:**

```json
{
  "data": {
    "id": "9876543210",
    "duration": "3600000",
    "start": "1717100000000"
  }
}
```

**Usage Example:**

```bash
POST /mcp/clickup/create_time_entry

{
  "team_id": "9876543",
  "body": "{\"tid\": \"abc123\", \"start\": 1717100000000, \"duration\": 3600000}"
}
```

</details>

---

<details>
<summary><code>update_time_entry</code> → Update a time entry</summary>

Modifies the start time, duration, task, or description of an existing time entry.

**Inputs:**

- `team_id` (string, required) → The ID of the Workspace (team).
- `timer_id` (string, required) → The ID of the time entry to update.
- `body` (string, required) → JSON string of fields to update.

**Body fields:**

- `start` (integer, optional) → Updated start time (Unix ms).
- `duration` (integer, optional) → Updated duration (ms).
- `description` (string, optional) → Updated description.
- `tid` (string, optional) → Updated task ID.
- `billable` (boolean, optional) → Updated billable flag.

**Output:**

```json
{
  "data": {
    "id": "1234567890",
    "duration": "7200000"
  }
}
```

**Usage Example:**

```bash
POST /mcp/clickup/update_time_entry

{
  "team_id": "9876543",
  "timer_id": "1234567890",
  "body": "{\"duration\": 7200000}"
}
```

</details>

---

<details>
<summary><code>delete_time_entry</code> → Delete a time entry</summary>

Permanently deletes a time entry.

**Inputs:**

- `team_id` (string, required) → The ID of the Workspace (team).
- `timer_id` (string, required) → The ID of the time entry to delete.

**Output:**

```json
{
  "data": []
}
```

**Usage Example:**

```bash
POST /mcp/clickup/delete_time_entry

{
  "team_id": "9876543",
  "timer_id": "1234567890"
}
```

</details>

---

<details>
<summary><code>start_time_entry</code> → Start a running timer</summary>

Starts a live timer optionally linked to a task.

**Inputs:**

- `team_id` (string, required) → The ID of the Workspace (team).
- `body` (string, required) → JSON string of the timer details.

**Body fields:**

- `tid` (string, optional) → Task ID to track time against.
- `description` (string, optional) → Note about what's being worked on.
- `billable` (boolean, optional) → Mark as billable.

**Output:**

```json
{
  "data": {
    "id": "9876543211",
    "start": "1717200000000",
    "task": { "id": "abc123" }
  }
}
```

**Usage Example:**

```bash
POST /mcp/clickup/start_time_entry

{
  "team_id": "9876543",
  "body": "{\"tid\": \"abc123\", \"description\": \"Working on login fix\"}"
}
```

</details>

---

<details>
<summary><code>stop_time_entry</code> → Stop the running timer</summary>

Stops the currently running timer for the authenticated user.

**Inputs:**

- `team_id` (string, required) → The ID of the Workspace (team).

**Output:**

```json
{
  "data": {
    "id": "9876543211",
    "start": "1717200000000",
    "end": "1717203600000",
    "duration": "3600000"
  }
}
```

**Usage Example:**

```bash
POST /mcp/clickup/stop_time_entry

{
  "team_id": "9876543"
}
```

</details>

---

<details>
<summary><code>get_running_time_entry</code> → Get the currently running timer</summary>

Returns the active timer for the authenticated user, if one is running.

**Inputs:**

- `team_id` (string, required) → The ID of the Workspace (team).

**Output:**

```json
{
  "data": {
    "id": "9876543211",
    "start": "1717200000000",
    "task": { "id": "abc123", "name": "Fix login bug" }
  }
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_running_time_entry

{
  "team_id": "9876543"
}
```

</details>

---

### Members

<details>
<summary><code>get_workspace_members</code> → List all members in a Workspace</summary>

Returns the Workspace details including all member profiles.

**Inputs:**

- `team_id` (string, required) → The ID of the Workspace (team).

**Output:**

```json
{
  "team": {
    "id": "9876543",
    "name": "My Workspace",
    "members": [
      { "user": { "id": 1234567, "username": "jane_doe", "email": "jane@example.com", "role": 2 } }
    ]
  }
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_workspace_members

{
  "team_id": "9876543"
}
```

</details>

---

<details>
<summary><code>get_task_members</code> → List members assigned to a task</summary>

Returns all users who are assignees or watchers of the specified task.

**Inputs:**

- `task_id` (string, required) → The ID of the task.

**Output:**

```json
{
  "members": [
    { "id": 1234567, "username": "jane_doe", "email": "jane@example.com" }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_task_members

{
  "task_id": "abc123"
}
```

</details>

---

<details>
<summary><code>get_list_members</code> → List members with access to a List</summary>

Returns all users who have access to the specified List.

**Inputs:**

- `list_id` (string, required) → The ID of the list.

**Output:**

```json
{
  "members": [
    { "id": 1234567, "username": "jane_doe", "email": "jane@example.com" }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_list_members

{
  "list_id": "56789012"
}
```

</details>

---

### Tags

<details>
<summary><code>get_space_tags</code> → List all tags in a Space</summary>

Returns all tags defined within the specified Space.

**Inputs:**

- `space_id` (string, required) → The ID of the Space.

**Output:**

```json
{
  "tags": [
    { "name": "bug", "tag_fg": "#FFFFFF", "tag_bg": "#FF0000" },
    { "name": "feature", "tag_fg": "#FFFFFF", "tag_bg": "#4169E1" }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_space_tags

{
  "space_id": "90110011"
}
```

</details>

---

<details>
<summary><code>create_space_tag</code> → Create a tag in a Space</summary>

Creates a new named tag with custom foreground and background colors.

**Inputs:**

- `space_id` (string, required) → The ID of the Space.
- `body` (string, required) → JSON string of the tag definition.

**Body fields:**

- `tag.name` (string, required) → Tag name.
- `tag.tag_fg` (string, optional) → Foreground color hex (e.g. `#FFFFFF`).
- `tag.tag_bg` (string, optional) → Background color hex (e.g. `#FF0000`).

**Output:**

```json
{
  "success": true
}
```

**Usage Example:**

```bash
POST /mcp/clickup/create_space_tag

{
  "space_id": "90110011",
  "body": "{\"tag\": {\"name\": \"urgent\", \"tag_fg\": \"#FFFFFF\", \"tag_bg\": \"#FF0000\"}}"
}
```

</details>

---

<details>
<summary><code>update_space_tag</code> → Update a tag in a Space</summary>

Updates the name or colors of an existing tag.

**Inputs:**

- `space_id` (string, required) → The ID of the Space.
- `tag_name` (string, required) → The current name of the tag to update.
- `body` (string, required) → JSON string of tag fields to update.

**Body fields:**

- `tag.name` (string, optional) → New tag name.
- `tag.tag_fg` (string, optional) → New foreground color hex.
- `tag.tag_bg` (string, optional) → New background color hex.

**Output:**

```json
{
  "success": true
}
```

**Usage Example:**

```bash
POST /mcp/clickup/update_space_tag

{
  "space_id": "90110011",
  "tag_name": "urgent",
  "body": "{\"tag\": {\"name\": \"critical\", \"tag_bg\": \"#CC0000\"}}"
}
```

</details>

---

<details>
<summary><code>delete_space_tag</code> → Delete a tag from a Space</summary>

Removes a tag from the Space and detaches it from all tasks.

**Inputs:**

- `space_id` (string, required) → The ID of the Space.
- `tag_name` (string, required) → The name of the tag to delete.

**Output:**

```json
{
  "success": true
}
```

**Usage Example:**

```bash
POST /mcp/clickup/delete_space_tag

{
  "space_id": "90110011",
  "tag_name": "critical"
}
```

</details>

---

<details>
<summary><code>add_tag_to_task</code> → Apply a tag to a task</summary>

Attaches an existing Space tag to the specified task.

**Inputs:**

- `task_id` (string, required) → The ID of the task.
- `tag_name` (string, required) → The name of the tag to apply.

**Output:**

```json
{
  "success": true
}
```

**Usage Example:**

```bash
POST /mcp/clickup/add_tag_to_task

{
  "task_id": "abc123",
  "tag_name": "bug"
}
```

</details>

---

<details>
<summary><code>remove_tag_from_task</code> → Remove a tag from a task</summary>

Detaches a tag from the specified task.

**Inputs:**

- `task_id` (string, required) → The ID of the task.
- `tag_name` (string, required) → The name of the tag to remove.

**Output:**

```json
{
  "success": true
}
```

**Usage Example:**

```bash
POST /mcp/clickup/remove_tag_from_task

{
  "task_id": "abc123",
  "tag_name": "bug"
}
```

</details>

---

### Goals

<details>
<summary><code>get_goals</code> → List all goals in a Workspace</summary>

Returns all goals in the Workspace, optionally including completed ones.

**Inputs:**

- `team_id` (string, required) → The ID of the Workspace (team).
- `include_completed` (boolean, optional) → Include completed goals. Default: `false`.

**Output:**

```json
{
  "goals": [
    {
      "id": "goal001",
      "name": "Q2 OKRs",
      "due_date": "1719792000000",
      "description": "Quarterly objectives",
      "percent_completed": 45,
      "owners": [{ "id": 1234567 }]
    }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_goals

{
  "team_id": "9876543",
  "include_completed": false
}
```

</details>

---

<details>
<summary><code>get_goal</code> → Get a specific goal</summary>

Returns full details for a single goal including key results.

**Inputs:**

- `goal_id` (string, required) → The ID of the goal.

**Output:**

```json
{
  "goal": {
    "id": "goal001",
    "name": "Q2 OKRs",
    "percent_completed": 45,
    "key_results": [],
    "owners": [{ "id": 1234567 }]
  }
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_goal

{
  "goal_id": "goal001"
}
```

</details>

---

<details>
<summary><code>create_goal</code> → Create a new goal</summary>

Creates a goal with a name, due date, owners, and optional color.

**Inputs:**

- `team_id` (string, required) → The ID of the Workspace (team).
- `body` (string, required) → JSON string of the goal definition.

**Body fields:**

- `name` (string, required) → Goal name.
- `due_date` (integer, required) → Due date as Unix ms timestamp.
- `description` (string, optional) → Goal description.
- `multiple_owners` (boolean, optional) → Allow multiple owners.
- `owners` (array of integers, optional) → List of owner user IDs.
- `color` (string, optional) → Goal color hex.

**Output:**

```json
{
  "goal": {
    "id": "goal002",
    "name": "Q3 OKRs",
    "due_date": "1727740800000"
  }
}
```

**Usage Example:**

```bash
POST /mcp/clickup/create_goal

{
  "team_id": "9876543",
  "body": "{\"name\": \"Q3 OKRs\", \"due_date\": 1727740800000, \"owners\": [1234567]}"
}
```

</details>

---

<details>
<summary><code>update_goal</code> → Update a goal</summary>

Updates the name, description, due date, or owners of a goal.

**Inputs:**

- `goal_id` (string, required) → The ID of the goal to update.
- `body` (string, required) → JSON string of fields to update.

**Body fields:**

- `name` (string, optional) → New goal name.
- `due_date` (integer, optional) → New due date (Unix ms).
- `description` (string, optional) → Updated description.
- `rem_owners` (array of integers, optional) → Owner user IDs to remove.
- `add_owners` (array of integers, optional) → Owner user IDs to add.
- `color` (string, optional) → Updated color hex.

**Output:**

```json
{
  "goal": {
    "id": "goal001",
    "name": "Q2 OKRs (Extended)",
    "percent_completed": 45
  }
}
```

**Usage Example:**

```bash
POST /mcp/clickup/update_goal

{
  "goal_id": "goal001",
  "body": "{\"name\": \"Q2 OKRs (Extended)\"}"
}
```

</details>

---

<details>
<summary><code>delete_goal</code> → Delete a goal</summary>

Permanently deletes a goal.

**Inputs:**

- `goal_id` (string, required) → The ID of the goal to delete.

**Output:**

```json
{
  "success": true
}
```

**Usage Example:**

```bash
POST /mcp/clickup/delete_goal

{
  "goal_id": "goal001"
}
```

</details>

---

### Checklists

<details>
<summary><code>create_checklist</code> → Create a checklist on a task</summary>

Adds a named checklist to the specified task.

**Inputs:**

- `task_id` (string, required) → The ID of the task.
- `body` (string, required) → JSON string of the checklist definition.

**Body fields:**

- `name` (string, required) → Checklist name.

**Output:**

```json
{
  "checklist": {
    "id": "chk001",
    "name": "Pre-launch QA",
    "task_id": "abc123",
    "items": []
  }
}
```

**Usage Example:**

```bash
POST /mcp/clickup/create_checklist

{
  "task_id": "abc123",
  "body": "{\"name\": \"Pre-launch QA\"}"
}
```

</details>

---

<details>
<summary><code>update_checklist</code> → Update a checklist</summary>

Renames a checklist or changes its position.

**Inputs:**

- `checklist_id` (string, required) → The ID of the checklist.
- `body` (string, required) → JSON string of fields to update.

**Body fields:**

- `name` (string, optional) → New checklist name.
- `position` (integer, optional) → Display position (0-indexed).

**Output:**

```json
{
  "checklist": {
    "id": "chk001",
    "name": "Pre-launch QA (Final)"
  }
}
```

**Usage Example:**

```bash
POST /mcp/clickup/update_checklist

{
  "checklist_id": "chk001",
  "body": "{\"name\": \"Pre-launch QA (Final)\"}"
}
```

</details>

---

<details>
<summary><code>delete_checklist</code> → Delete a checklist</summary>

Permanently deletes a checklist and all its items.

**Inputs:**

- `checklist_id` (string, required) → The ID of the checklist to delete.

**Output:**

```json
{
  "success": true
}
```

**Usage Example:**

```bash
POST /mcp/clickup/delete_checklist

{
  "checklist_id": "chk001"
}
```

</details>

---

<details>
<summary><code>create_checklist_item</code> → Add an item to a checklist</summary>

Adds a new item to the specified checklist with optional assignee.

**Inputs:**

- `checklist_id` (string, required) → The ID of the checklist.
- `body` (string, required) → JSON string of the checklist item.

**Body fields:**

- `name` (string, required) → Item text.
- `assignee` (integer, optional) → User ID to assign the item to.

**Output:**

```json
{
  "checklist": {
    "id": "chk001",
    "items": [
      { "id": "item001", "name": "Smoke test all pages", "resolved": false }
    ]
  }
}
```

**Usage Example:**

```bash
POST /mcp/clickup/create_checklist_item

{
  "checklist_id": "chk001",
  "body": "{\"name\": \"Smoke test all pages\", \"assignee\": 1234567}"
}
```

</details>

---

<details>
<summary><code>update_checklist_item</code> → Update a checklist item</summary>

Edits the text, assignee, or resolved state of a checklist item.

**Inputs:**

- `checklist_id` (string, required) → The ID of the checklist.
- `checklist_item_id` (string, required) → The ID of the checklist item.
- `body` (string, required) → JSON string of fields to update.

**Body fields:**

- `name` (string, optional) → Updated item text.
- `assignee` (integer, optional) → Updated assignee user ID.
- `resolved` (boolean, optional) → Mark as complete or incomplete.
- `parent` (string, optional) → Parent item ID (to nest items).

**Output:**

```json
{
  "checklist": {
    "id": "chk001",
    "items": [
      { "id": "item001", "name": "Smoke test all pages", "resolved": true }
    ]
  }
}
```

**Usage Example:**

```bash
POST /mcp/clickup/update_checklist_item

{
  "checklist_id": "chk001",
  "checklist_item_id": "item001",
  "body": "{\"resolved\": true}"
}
```

</details>

---

<details>
<summary><code>delete_checklist_item</code> → Delete a checklist item</summary>

Permanently removes an item from a checklist.

**Inputs:**

- `checklist_id` (string, required) → The ID of the checklist.
- `checklist_item_id` (string, required) → The ID of the checklist item to delete.

**Output:**

```json
{
  "success": true
}
```

**Usage Example:**

```bash
POST /mcp/clickup/delete_checklist_item

{
  "checklist_id": "chk001",
  "checklist_item_id": "item001"
}
```

</details>

---

### Custom Fields

<details>
<summary><code>get_accessible_custom_fields</code> → List custom fields for a List</summary>

Returns all custom fields accessible within the specified List.

**Inputs:**

- `list_id` (string, required) → The ID of the list.

**Output:**

```json
{
  "fields": [
    {
      "id": "field001",
      "name": "Story Points",
      "type": "number",
      "type_config": { "precision": 0 },
      "required": false
    }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_accessible_custom_fields

{
  "list_id": "56789012"
}
```

</details>

---

<details>
<summary><code>set_custom_field_value</code> → Set a custom field value on a task</summary>

Assigns a value to a specific custom field on a task. The value format depends on the field type.

**Inputs:**

- `task_id` (string, required) → The ID of the task.
- `field_id` (string, required) → The ID of the custom field.
- `body` (string, required) → JSON string containing the value.

**Body fields:**

- `value` (any, required) → The value to set. Type depends on the field: string for text, integer for number, boolean for checkbox, ISO date string for date fields.

**Output:**

```json
{
  "success": true
}
```

**Usage Example:**

```bash
POST /mcp/clickup/set_custom_field_value

{
  "task_id": "abc123",
  "field_id": "field001",
  "body": "{\"value\": 8}"
}
```

</details>

---

<details>
<summary><code>remove_custom_field_value</code> → Clear a custom field value from a task</summary>

Removes the value of a custom field from a task, resetting it to empty.

**Inputs:**

- `task_id` (string, required) → The ID of the task.
- `field_id` (string, required) → The ID of the custom field to clear.

**Output:**

```json
{
  "success": true
}
```

**Usage Example:**

```bash
POST /mcp/clickup/remove_custom_field_value

{
  "task_id": "abc123",
  "field_id": "field001"
}
```

</details>

---

### Views

<details>
<summary><code>get_team_views</code> → List views at the Workspace level</summary>

Returns all views defined at the top level of a Workspace.

**Inputs:**

- `team_id` (string, required) → The ID of the Workspace (team).

**Output:**

```json
{
  "views": [
    { "id": "view001", "name": "All Tasks", "type": "list" },
    { "id": "view002", "name": "Gantt", "type": "gantt" }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_team_views

{
  "team_id": "9876543"
}
```

</details>

---

<details>
<summary><code>get_space_views</code> → List views in a Space</summary>

Returns all views defined within the specified Space.

**Inputs:**

- `space_id` (string, required) → The ID of the Space.

**Output:**

```json
{
  "views": [
    { "id": "view003", "name": "Sprint Board", "type": "board" }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_space_views

{
  "space_id": "90110011"
}
```

</details>

---

<details>
<summary><code>get_folder_views</code> → List views in a Folder</summary>

Returns all views defined within the specified Folder.

**Inputs:**

- `folder_id` (string, required) → The ID of the Folder.

**Output:**

```json
{
  "views": [
    { "id": "view004", "name": "Sprint Timeline", "type": "gantt" }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_folder_views

{
  "folder_id": "78901234"
}
```

</details>

---

<details>
<summary><code>get_list_views</code> → List views in a List</summary>

Returns all views defined within the specified List.

**Inputs:**

- `list_id` (string, required) → The ID of the List.

**Output:**

```json
{
  "views": [
    { "id": "view005", "name": "Task List", "type": "list" }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_list_views

{
  "list_id": "56789012"
}
```

</details>

---

<details>
<summary><code>get_view</code> → Get a specific view</summary>

Returns full configuration details for a single view.

**Inputs:**

- `view_id` (string, required) → The ID of the view.

**Output:**

```json
{
  "view": {
    "id": "view001",
    "name": "All Tasks",
    "type": "list",
    "grouping": { "field": "status" },
    "filters": {}
  }
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_view

{
  "view_id": "view001"
}
```

</details>

---

<details>
<summary><code>get_view_tasks</code> → List tasks in a view</summary>

Returns the tasks visible in the specified view, with pagination support.

**Inputs:**

- `view_id` (string, required) → The ID of the view.
- `page` (integer, optional) → Page number (0-indexed). Default: `0`.

**Output:**

```json
{
  "tasks": [
    { "id": "abc123", "name": "Fix login bug", "status": { "status": "in progress" } }
  ],
  "last_page": false
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_view_tasks

{
  "view_id": "view001",
  "page": 0
}
```

</details>

---

### Webhooks

<details>
<summary><code>get_webhooks</code> → List all webhooks in a Workspace</summary>

Returns all registered webhooks for the specified Workspace.

**Inputs:**

- `team_id` (string, required) → The ID of the Workspace (team).

**Output:**

```json
{
  "webhooks": [
    {
      "id": "wh001",
      "endpoint": "https://example.com/webhook",
      "events": ["taskCreated", "taskUpdated"],
      "health": { "status": "active" }
    }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_webhooks

{
  "team_id": "9876543"
}
```

</details>

---

<details>
<summary><code>create_webhook</code> → Register a new webhook</summary>

Creates a webhook that fires on specified ClickUp events.

**Inputs:**

- `team_id` (string, required) → The ID of the Workspace (team).
- `body` (string, required) → JSON string of the webhook definition.

**Body fields:**

- `endpoint` (string, required) → URL to send webhook payloads to.
- `events` (array of strings, required) → Events to subscribe to (e.g. `taskCreated`, `taskUpdated`, `taskDeleted`, `listCreated`, `spaceCreated`).
- `space_id` (integer, optional) → Limit events to a specific Space.
- `folder_id` (integer, optional) → Limit events to a specific Folder.
- `list_id` (integer, optional) → Limit events to a specific List.
- `task_id` (string, optional) → Limit events to a specific task.

**Output:**

```json
{
  "id": "wh002",
  "webhook": {
    "id": "wh002",
    "endpoint": "https://example.com/webhook",
    "events": ["taskCreated"]
  }
}
```

**Usage Example:**

```bash
POST /mcp/clickup/create_webhook

{
  "team_id": "9876543",
  "body": "{\"endpoint\": \"https://example.com/webhook\", \"events\": [\"taskCreated\", \"taskUpdated\"]}"
}
```

</details>

---

<details>
<summary><code>update_webhook</code> → Update a webhook</summary>

Updates the endpoint URL, event subscriptions, or status of a webhook.

**Inputs:**

- `webhook_id` (string, required) → The ID of the webhook.
- `body` (string, required) → JSON string of fields to update.

**Body fields:**

- `endpoint` (string, optional) → New endpoint URL.
- `events` (array of strings, optional) → Updated event list.
- `status` (string, optional) → `active` or `inactive`.

**Output:**

```json
{
  "webhook": {
    "id": "wh001",
    "endpoint": "https://example.com/new-webhook",
    "status": "active"
  }
}
```

**Usage Example:**

```bash
POST /mcp/clickup/update_webhook

{
  "webhook_id": "wh001",
  "body": "{\"endpoint\": \"https://example.com/new-webhook\"}"
}
```

</details>

---

<details>
<summary><code>delete_webhook</code> → Delete a webhook</summary>

Permanently removes a webhook registration.

**Inputs:**

- `webhook_id` (string, required) → The ID of the webhook to delete.

**Output:**

```json
{
  "success": true
}
```

**Usage Example:**

```bash
POST /mcp/clickup/delete_webhook

{
  "webhook_id": "wh001"
}
```

</details>

---

### Docs

<details>
<summary><code>search_docs</code> → Search for Docs in a Workspace</summary>

Searches ClickUp Docs within the specified Workspace by query string.

**Inputs:**

- `team_id` (string, required) → The ID of the Workspace (team).
- `query` (string, optional) → Search query string.

**Output:**

```json
{
  "docs": [
    {
      "id": "doc001",
      "name": "Engineering Handbook",
      "date_created": "1717100000000"
    }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/search_docs

{
  "team_id": "9876543",
  "query": "onboarding"
}
```

</details>

---

<details>
<summary><code>get_doc_pages</code> → List all pages in a Doc</summary>

Returns all pages within the specified Doc.

**Inputs:**

- `doc_id` (string, required) → The ID of the Doc.

**Output:**

```json
{
  "pages": [
    { "id": "page001", "name": "Introduction", "date_created": "1717100000000" },
    { "id": "page002", "name": "Setup Guide", "date_created": "1717110000000" }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_doc_pages

{
  "doc_id": "doc001"
}
```

</details>

---

<details>
<summary><code>create_doc_page</code> → Create a new page in a Doc</summary>

Adds a new page with a title and markdown content to the specified Doc.

**Inputs:**

- `doc_id` (string, required) → The ID of the Doc.
- `body` (string, required) → JSON string of the page definition.

**Body fields:**

- `name` (string, required) → Page title.
- `content` (string, optional) → Page content in markdown.
- `parent_page_id` (string, optional) → Parent page ID for nested pages.

**Output:**

```json
{
  "id": "page003",
  "name": "API Reference",
  "date_created": "1717200000000"
}
```

**Usage Example:**

```bash
POST /mcp/clickup/create_doc_page

{
  "doc_id": "doc001",
  "body": "{\"name\": \"API Reference\", \"content\": \"## Endpoints\\n...\"}"
}
```

</details>

---

### Chat

<details>
<summary><code>get_chat_channels</code> → List chat channels in a Workspace</summary>

Returns all chat channels available in the specified Workspace.

**Inputs:**

- `team_id` (string, required) → The ID of the Workspace (team).

**Output:**

```json
{
  "channels": [
    { "id": "ch001", "name": "general" },
    { "id": "ch002", "name": "engineering" }
  ]
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_chat_channels

{
  "team_id": "9876543"
}
```

</details>

---

<details>
<summary><code>send_chat_message</code> → Post a message to a chat channel</summary>

Sends a message to the specified chat channel.

**Inputs:**

- `channel_id` (string, required) → The ID of the chat channel.
- `body` (string, required) → JSON string of the message.

**Body fields:**

- `content` (string, required) → Message text.

**Output:**

```json
{
  "id": "msg001",
  "content": "Hello team!",
  "date": "1717200000000"
}
```

**Usage Example:**

```bash
POST /mcp/clickup/send_chat_message

{
  "channel_id": "ch001",
  "body": "{\"content\": \"Hello team!\"}"
}
```

</details>

---

### Shared Hierarchy

<details>
<summary><code>get_shared_hierarchy</code> → List resources shared with the authenticated user</summary>

Returns all Spaces, Folders, Lists, and tasks that have been explicitly shared with the authenticated user.

**Inputs:**

- `team_id` (string, required) → The ID of the Workspace (team).

**Output:**

```json
{
  "shared": {
    "tasks": [{ "id": "abc123", "name": "Fix login bug" }],
    "lists": [{ "id": "56789012", "name": "Backlog" }],
    "folders": []
  }
}
```

**Usage Example:**

```bash
POST /mcp/clickup/get_shared_hierarchy

{
  "team_id": "9876543"
}
```

</details>

---

<details>
<summary><strong>API Parameters Reference</strong></summary>

### Common Parameters

- `team_id` → ClickUp Workspace (team) identifier. Find yours via `get_authorized_teams`.
- `page` → Zero-indexed page number for paginated responses. Increment to fetch subsequent pages.
- `archived` → Pass `true` to include archived resources alongside active ones.
- `include_closed` → Pass `true` in task queries to include tasks in closed/completed statuses.
- `order_by` → Sort tasks by field: `id`, `created`, `updated`, or `due_date`.
- `reverse` → Pass `true` to reverse the sort direction of `order_by`.

### Priority Levels

| Value | Priority |
|-------|----------|
| `1` | Urgent |
| `2` | High |
| `3` | Normal |
| `4` | Low |

### Timestamps

All date/time values use **Unix milliseconds** (epoch × 1000).

```
Example: 1717200000000 → 2024-06-01 00:00:00 UTC
```

### ID Formats

**Workspace (team):**
```
Format: numeric string
Example: "9876543"
```

**Space / Folder / List:**
```
Format: numeric string
Example: "90110011"
```

**Task:**
```
Format: alphanumeric string
Example: "abc123"
```

**Comment / Time Entry:**
```
Format: numeric string
Example: "1234567890"
```

### Webhook Events

| Event | Description |
|-------|-------------|
| `taskCreated` | A task was created |
| `taskUpdated` | A task field was changed |
| `taskDeleted` | A task was deleted |
| `taskCommentPosted` | A comment was added to a task |
| `taskStatusUpdated` | A task's status changed |
| `listCreated` | A list was created |
| `listUpdated` | A list was updated |
| `listDeleted` | A list was deleted |
| `folderCreated` | A folder was created |
| `folderUpdated` | A folder was updated |
| `folderDeleted` | A folder was deleted |
| `spaceCreated` | A space was created |
| `spaceUpdated` | A space was updated |
| `spaceDeleted` | A space was deleted |

</details>

---

<details>
<summary><strong>OAuth Setup Guide</strong></summary>

Credentials are injected server-side via `fastmcp-credentials`. No tool accepts auth parameters directly — you configure credentials once on the platform and every tool call uses them automatically.

### Step 1: Create a ClickUp OAuth App

1. Log in to [ClickUp](https://app.clickup.com)
2. Go to **Settings** → **Integrations** → **ClickUp API**
3. Click **Create an App**
4. Enter a name and your redirect URI
5. Copy the **Client ID** and **Client Secret**

### Step 2: Authorize and Obtain an Access Token

1. Direct users to the authorization URL:
   ```
   https://app.clickup.com/api?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}
   ```
2. After the user approves, exchange the returned `code` for an access token:
   ```bash
   POST https://api.clickup.com/api/v2/oauth/token
   Content-Type: application/json

   {
     "client_id": "YOUR_CLIENT_ID",
     "client_secret": "YOUR_CLIENT_SECRET",
     "code": "AUTHORIZATION_CODE"
   }
   ```
3. The response contains the `access_token` to use for all API calls.

### Step 3: Configure on the Platform

Provide the access token to the Curious Layer platform. It will be injected into every tool call via the `X-MCP-Cred-Access-Token` header — no token is ever passed as a tool parameter.

### Required Scopes

ClickUp's OAuth does not use granular scopes. An authorized token grants access to all Workspaces and resources the user has permission to see within their account.

Refer to the [ClickUp Authentication Guide](https://developer.clickup.com/docs/authentication) for detailed steps.

</details>

---

<details>
<summary><strong>Troubleshooting</strong></summary>

### Missing or Invalid Credential

- **Cause:** OAuth access token not injected by the platform or the token is malformed.
- **Solution:**
  1. Verify the credential is configured in your Curious Layer account for ClickUp.
  2. Re-authorize the ClickUp integration to obtain a fresh access token.
  3. Check that the platform is passing `X-MCP-Cred-Access-Token` to the server.

### Insufficient Credits

- **Cause:** API calls have exceeded your request limits.
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard.
  2. Upgrade to a paid plan or add credits for higher limits.
  3. Contact support for credit adjustments.

### Malformed Request Payload

- **Cause:** The `body` parameter contains invalid JSON or is missing required fields.
- **Solution:**
  1. Validate your JSON string before passing it as `body`.
  2. Ensure all required fields for the specific operation are included.
  3. Check that numeric values (IDs, timestamps) are not wrapped in quotes where integers are expected.

### Resource Not Found (404)

- **Cause:** An ID refers to a resource that does not exist, has been deleted, or belongs to a different Workspace.
- **Solution:**
  1. Verify the ID using the corresponding `get_*` or `get_authorized_teams` tool.
  2. Confirm the resource belongs to the Workspace associated with the authenticated token.
  3. Check whether the resource was archived (use `archived: true` to surface it).

### Authentication Token Invalid or Expired

- **Cause:** ClickUp rejected the access token.
- **Solution:**
  1. Re-authorize the ClickUp integration on the Curious Layer platform.
  2. Verify the token has not been revoked in ClickUp Settings → Integrations.
  3. Obtain a fresh token via the OAuth flow and update the platform credential.

### Rate Limit Exceeded (429)

- **Cause:** Too many requests in a short period.
- **Solution:**
  1. Reduce the frequency of API calls.
  2. Add delays between bulk operations.
  3. Refer to [ClickUp Rate Limits](https://developer.clickup.com/docs/rate-limits) for current limits.

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[ClickUp API Documentation](https://developer.clickup.com/reference)** → Official API reference
- **[ClickUp Authentication Guide](https://developer.clickup.com/docs/authentication)** → OAuth setup and token management
- **[ClickUp Rate Limits](https://developer.clickup.com/docs/rate-limits)** → Request limits and throttling policy
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** → FastMCP specification
- **[fastmcp-credentials package](https://pypi.org/project/fastmcp-credentials/)** → Server-side credential injection for FastMCP

</details>
