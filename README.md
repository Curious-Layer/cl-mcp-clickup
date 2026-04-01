# ClickUp MCP Server

This server provides a set of tools to interact with the ClickUp API, allowing you to manage workspaces, spaces, folders, lists, tasks, time tracking, and more through the Model Context Protocol (MCP).

## Documentation Reference

- [ClickUp API Reference](https://developer.clickup.com/reference)
- [ClickUp MCP Documentation](https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server)
- [ClickUp Authentication](https://developer.clickup.com/docs/authentication)

## Authentication

All tools require a `token_data` parameter. This is a JSON string containing your OAuth 2.0 access token or personal API token. The structure of the JSON should be as follows:

### For OAuth 2.0:

```json
{
  "access_token": "YOUR_ACCESS_TOKEN",
  "token_type": "Bearer"
}
```

### For Personal API Token:

```json
{
  "access_token": "pk_YOUR_PERSONAL_API_TOKEN"
}
```

### OAuth 2.0 Flow

ClickUp uses the authorization code grant type for OAuth 2.0:

1. **Authorization URL**: `https://app.clickup.com/api?client_id={client_id}&redirect_uri={redirect_uri}`
2. **Access Token URL**: `https://api.clickup.com/api/v2/oauth/token`

To set up OAuth:

1. Log in to ClickUp
2. Go to Settings → Apps
3. Click "Create new app"
4. You'll receive a `client_id` and `secret`
5. Implement the OAuth flow to exchange authorization codes for access tokens

---

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
# Using stdio transport (default)
python server.py

# Using SSE transport
python server.py -t sse --host 0.0.0.0 --port 8080

# Using streamable-http transport
python server.py -t streamable-http --host 0.0.0.0 --port 8080
```

## Project Structure

```text
cl-mcp-clickup/
|-- clickup_mcp/
|   |-- __init__.py
|   |-- cli.py
|   |-- config.py
|   `-- tools.py
|-- server.py
|-- requirements.txt
`-- README.md
```

- `server.py` is the main runtime entrypoint.
- `clickup_mcp/tools.py` contains ClickUp MCP tool registrations.
- `clickup_mcp/config.py` centralizes logging and API base config.
- `clickup_mcp/cli.py` contains transport/host/port argument parsing.

---

## Available Tools

### Authorization

#### `get_authorized_user`
Get the user that belongs to the access token.

* `token_data` (string, required): The JSON string of the user's access token.

#### `get_authorized_teams`
Get the authorized Workspaces (teams) for the access token.

* `token_data` (string, required): The JSON string of the user's access token.

---

### Spaces

#### `get_spaces`
Get all Spaces in a Workspace.

* `token_data` (string, required): The JSON string of the user's access token.
* `team_id` (string, required): The ID of the Workspace (team).
* `archived` (boolean, optional): Whether to include archived spaces. Default: false.

#### `get_space`
Get a specific Space.

* `token_data` (string, required): The JSON string of the user's access token.
* `space_id` (string, required): The ID of the Space.

#### `create_space`
Create a new Space in a Workspace.

* `token_data` (string, required): The JSON string of the user's access token.
* `team_id` (string, required): The ID of the Workspace (team).
* `body` (string, required): A JSON string representing the space to create.

#### `update_space`
Update an existing Space.

* `token_data` (string, required): The JSON string of the user's access token.
* `space_id` (string, required): The ID of the Space to update.
* `body` (string, required): A JSON string with the fields to update.

#### `delete_space`
Delete a Space.

* `token_data` (string, required): The JSON string of the user's access token.
* `space_id` (string, required): The ID of the Space to delete.

---

### Folders

#### `get_folders`
Get all Folders in a Space.

* `token_data` (string, required): The JSON string of the user's access token.
* `space_id` (string, required): The ID of the Space.
* `archived` (boolean, optional): Whether to include archived folders. Default: false.

#### `get_folder`
Get a specific Folder.

* `token_data` (string, required): The JSON string of the user's access token.
* `folder_id` (string, required): The ID of the Folder.

#### `create_folder`
Create a new Folder in a Space.

* `token_data` (string, required): The JSON string of the user's access token.
* `space_id` (string, required): The ID of the Space.
* `body` (string, required): A JSON string representing the folder to create.

#### `update_folder`
Update an existing Folder.

* `token_data` (string, required): The JSON string of the user's access token.
* `folder_id` (string, required): The ID of the Folder to update.
* `body` (string, required): A JSON string with the fields to update.

#### `delete_folder`
Delete a Folder.

* `token_data` (string, required): The JSON string of the user's access token.
* `folder_id` (string, required): The ID of the Folder to delete.

---

### Lists

#### `get_lists`
Get all Lists in a Folder.

* `token_data` (string, required): The JSON string of the user's access token.
* `folder_id` (string, required): The ID of the Folder.
* `archived` (boolean, optional): Whether to include archived lists. Default: false.

#### `get_folderless_lists`
Get all Lists in a Space that are not in a Folder.

* `token_data` (string, required): The JSON string of the user's access token.
* `space_id` (string, required): The ID of the Space.
* `archived` (boolean, optional): Whether to include archived lists. Default: false.

#### `get_list`
Get a specific List.

* `token_data` (string, required): The JSON string of the user's access token.
* `list_id` (string, required): The ID of the List.

#### `create_list`
Create a new List in a Folder.

* `token_data` (string, required): The JSON string of the user's access token.
* `folder_id` (string, required): The ID of the Folder.
* `body` (string, required): A JSON string representing the list to create.

#### `create_folderless_list`
Create a new List in a Space (not in a Folder).

* `token_data` (string, required): The JSON string of the user's access token.
* `space_id` (string, required): The ID of the Space.
* `body` (string, required): A JSON string representing the list to create.

#### `update_list`
Update an existing List.

* `token_data` (string, required): The JSON string of the user's access token.
* `list_id` (string, required): The ID of the List to update.
* `body` (string, required): A JSON string with the fields to update.

#### `delete_list`
Delete a List.

* `token_data` (string, required): The JSON string of the user's access token.
* `list_id` (string, required): The ID of the List to delete.

---

### Tasks

#### `get_tasks`
Get tasks in a List.

* `token_data` (string, required): The JSON string of the user's access token.
* `list_id` (string, required): The ID of the List.
* `archived` (boolean, optional): Whether to include archived tasks.
* `include_closed` (boolean, optional): Whether to include closed tasks.
* `page` (integer, optional): Page number for pagination (0-indexed).
* `order_by` (string, optional): Field to order by (id, created, updated, due_date).
* `reverse` (boolean, optional): Whether to reverse the order.
* `subtasks` (boolean, optional): Whether to include subtasks.
* `statuses` (string, optional): Comma-separated list of status names to filter by.
* `assignees` (string, optional): Comma-separated list of assignee user IDs to filter by.
* `due_date_gt` (integer, optional): Filter tasks with due date greater than (Unix timestamp in ms).
* `due_date_lt` (integer, optional): Filter tasks with due date less than (Unix timestamp in ms).
* `date_created_gt` (integer, optional): Filter tasks created after (Unix timestamp in ms).
* `date_created_lt` (integer, optional): Filter tasks created before (Unix timestamp in ms).
* `date_updated_gt` (integer, optional): Filter tasks updated after (Unix timestamp in ms).
* `date_updated_lt` (integer, optional): Filter tasks updated before (Unix timestamp in ms).

#### `get_task`
Get a specific task.

* `token_data` (string, required): The JSON string of the user's access token.
* `task_id` (string, required): The ID of the task.
* `include_subtasks` (boolean, optional): Whether to include subtasks.
* `include_markdown_description` (boolean, optional): Whether to include markdown description.

#### `create_task`
Create a new task in a List.

* `token_data` (string, required): The JSON string of the user's access token.
* `list_id` (string, required): The ID of the List.
* `body` (string, required): A JSON string representing the task to create.

Example body:
```json
{
  "name": "Task name",
  "description": "Task description",
  "assignees": [123],
  "priority": 3,
  "due_date": 1609459200000,
  "status": "Open"
}
```

#### `update_task`
Update an existing task.

* `token_data` (string, required): The JSON string of the user's access token.
* `task_id` (string, required): The ID of the task to update.
* `body` (string, required): A JSON string with the fields to update.

#### `delete_task`
Delete a task.

* `token_data` (string, required): The JSON string of the user's access token.
* `task_id` (string, required): The ID of the task to delete.

#### `get_filtered_team_tasks`
Get all tasks in a Workspace (team) with optional filters.

* `token_data` (string, required): The JSON string of the user's access token.
* `team_id` (string, required): The ID of the Workspace (team).
* Various filter parameters (see function documentation).

---

### Task Comments

#### `get_task_comments`
Get comments on a task.

* `token_data` (string, required): The JSON string of the user's access token.
* `task_id` (string, required): The ID of the task.
* `start` (integer, optional): Enter the start date for comments as a Unix timestamp in milliseconds.
* `start_id` (string, optional): Enter the Comment ID to start from.

#### `create_task_comment`
Create a comment on a task.

* `token_data` (string, required): The JSON string of the user's access token.
* `task_id` (string, required): The ID of the task.
* `body` (string, required): A JSON string representing the comment.

Example body:
```json
{
  "comment_text": "This is a comment",
  "notify_all": false
}
```

#### `update_comment`
Update a comment.

* `token_data` (string, required): The JSON string of the user's access token.
* `comment_id` (string, required): The ID of the comment to update.
* `body` (string, required): A JSON string with the updated comment.

#### `delete_comment`
Delete a comment.

* `token_data` (string, required): The JSON string of the user's access token.
* `comment_id` (string, required): The ID of the comment to delete.

---

### Time Tracking

#### `get_time_entries`
Get time entries within a date range.

* `token_data` (string, required): The JSON string of the user's access token.
* `team_id` (string, required): The ID of the Workspace (team).
* `start_date` (integer, optional): Start date as Unix timestamp in milliseconds.
* `end_date` (integer, optional): End date as Unix timestamp in milliseconds.
* `assignee` (string, optional): User ID to filter time entries by.

#### `create_time_entry`
Create a time entry.

* `token_data` (string, required): The JSON string of the user's access token.
* `team_id` (string, required): The ID of the Workspace (team).
* `body` (string, required): A JSON string representing the time entry.

Example body:
```json
{
  "tid": "task_id",
  "start": 1609459200000,
  "duration": 3600000,
  "description": "Work description"
}
```

#### `start_time_entry`
Start a timer for time tracking.

* `token_data` (string, required): The JSON string of the user's access token.
* `team_id` (string, required): The ID of the Workspace (team).
* `body` (string, required): A JSON string with timer details.

#### `stop_time_entry`
Stop the currently running timer.

* `token_data` (string, required): The JSON string of the user's access token.
* `team_id` (string, required): The ID of the Workspace (team).

#### `get_running_time_entry`
Get the currently running timer.

* `token_data` (string, required): The JSON string of the user's access token.
* `team_id` (string, required): The ID of the Workspace (team).

---

### Members

#### `get_workspace_members`
Get all members in a Workspace.

* `token_data` (string, required): The JSON string of the user's access token.
* `team_id` (string, required): The ID of the Workspace (team).

#### `get_task_members`
Get members assigned to a task.

* `token_data` (string, required): The JSON string of the user's access token.
* `task_id` (string, required): The ID of the task.

#### `get_list_members`
Get members with access to a list.

* `token_data` (string, required): The JSON string of the user's access token.
* `list_id` (string, required): The ID of the list.

---

### Tags

#### `get_space_tags`
Get all tags in a Space.

* `token_data` (string, required): The JSON string of the user's access token.
* `space_id` (string, required): The ID of the Space.

#### `create_space_tag`
Create a new tag in a Space.

* `token_data` (string, required): The JSON string of the user's access token.
* `space_id` (string, required): The ID of the Space.
* `body` (string, required): A JSON string representing the tag.

#### `add_tag_to_task`
Add a tag to a task.

* `token_data` (string, required): The JSON string of the user's access token.
* `task_id` (string, required): The ID of the task.
* `tag_name` (string, required): The name of the tag to add.

#### `remove_tag_from_task`
Remove a tag from a task.

* `token_data` (string, required): The JSON string of the user's access token.
* `task_id` (string, required): The ID of the task.
* `tag_name` (string, required): The name of the tag to remove.

---

### Goals

#### `get_goals`
Get all goals in a Workspace.

* `token_data` (string, required): The JSON string of the user's access token.
* `team_id` (string, required): The ID of the Workspace (team).
* `include_completed` (boolean, optional): Whether to include completed goals.

#### `get_goal`
Get a specific goal.

* `token_data` (string, required): The JSON string of the user's access token.
* `goal_id` (string, required): The ID of the goal.

#### `create_goal`
Create a new goal.

* `token_data` (string, required): The JSON string of the user's access token.
* `team_id` (string, required): The ID of the Workspace (team).
* `body` (string, required): A JSON string representing the goal.

#### `update_goal`
Update a goal.

* `token_data` (string, required): The JSON string of the user's access token.
* `goal_id` (string, required): The ID of the goal to update.
* `body` (string, required): A JSON string with the fields to update.

#### `delete_goal`
Delete a goal.

* `token_data` (string, required): The JSON string of the user's access token.
* `goal_id` (string, required): The ID of the goal to delete.

---

### Checklists

#### `create_checklist`
Create a new checklist in a task.

* `token_data` (string, required): The JSON string of the user's access token.
* `task_id` (string, required): The ID of the task.
* `body` (string, required): A JSON string representing the checklist.

#### `update_checklist`
Update a checklist.

* `token_data` (string, required): The JSON string of the user's access token.
* `checklist_id` (string, required): The ID of the checklist.
* `body` (string, required): A JSON string with the fields to update.

#### `delete_checklist`
Delete a checklist.

* `token_data` (string, required): The JSON string of the user's access token.
* `checklist_id` (string, required): The ID of the checklist to delete.

#### `create_checklist_item`
Create a new checklist item.

* `token_data` (string, required): The JSON string of the user's access token.
* `checklist_id` (string, required): The ID of the checklist.
* `body` (string, required): A JSON string representing the checklist item.

#### `update_checklist_item`
Update a checklist item.

* `token_data` (string, required): The JSON string of the user's access token.
* `checklist_id` (string, required): The ID of the checklist.
* `checklist_item_id` (string, required): The ID of the checklist item.
* `body` (string, required): A JSON string with the fields to update.

#### `delete_checklist_item`
Delete a checklist item.

* `token_data` (string, required): The JSON string of the user's access token.
* `checklist_id` (string, required): The ID of the checklist.
* `checklist_item_id` (string, required): The ID of the checklist item to delete.

---

### Custom Fields

#### `get_accessible_custom_fields`
Get all custom fields accessible in a list.

* `token_data` (string, required): The JSON string of the user's access token.
* `list_id` (string, required): The ID of the list.

#### `set_custom_field_value`
Set a custom field value on a task.

* `token_data` (string, required): The JSON string of the user's access token.
* `task_id` (string, required): The ID of the task.
* `field_id` (string, required): The ID of the custom field.
* `body` (string, required): A JSON string with the value.

#### `remove_custom_field_value`
Remove a custom field value from a task.

* `token_data` (string, required): The JSON string of the user's access token.
* `task_id` (string, required): The ID of the task.
* `field_id` (string, required): The ID of the custom field.

---

### Views

#### `get_team_views`
Get all views at the Workspace level.

* `token_data` (string, required): The JSON string of the user's access token.
* `team_id` (string, required): The ID of the Workspace (team).

#### `get_space_views`
Get all views in a Space.

* `token_data` (string, required): The JSON string of the user's access token.
* `space_id` (string, required): The ID of the Space.

#### `get_folder_views`
Get all views in a Folder.

* `token_data` (string, required): The JSON string of the user's access token.
* `folder_id` (string, required): The ID of the Folder.

#### `get_list_views`
Get all views in a List.

* `token_data` (string, required): The JSON string of the user's access token.
* `list_id` (string, required): The ID of the List.

#### `get_view`
Get a specific view.

* `token_data` (string, required): The JSON string of the user's access token.
* `view_id` (string, required): The ID of the view.

#### `get_view_tasks`
Get tasks in a view.

* `token_data` (string, required): The JSON string of the user's access token.
* `view_id` (string, required): The ID of the view.
* `page` (integer, optional): Page number for pagination (0-indexed).

---

### Webhooks

#### `get_webhooks`
Get all webhooks in a Workspace.

* `token_data` (string, required): The JSON string of the user's access token.
* `team_id` (string, required): The ID of the Workspace (team).

#### `create_webhook`
Create a new webhook.

* `token_data` (string, required): The JSON string of the user's access token.
* `team_id` (string, required): The ID of the Workspace (team).
* `body` (string, required): A JSON string representing the webhook.

Example body:
```json
{
  "endpoint": "https://example.com/webhook",
  "events": ["taskCreated", "taskUpdated"]
}
```

#### `update_webhook`
Update a webhook.

* `token_data` (string, required): The JSON string of the user's access token.
* `webhook_id` (string, required): The ID of the webhook.
* `body` (string, required): A JSON string with the fields to update.

#### `delete_webhook`
Delete a webhook.

* `token_data` (string, required): The JSON string of the user's access token.
* `webhook_id` (string, required): The ID of the webhook to delete.

---

### Docs

#### `search_docs`
Search for Docs in a Workspace.

* `token_data` (string, required): The JSON string of the user's access token.
* `team_id` (string, required): The ID of the Workspace (team).
* `query` (string, optional): Search query string.

#### `get_doc_pages`
Get all pages in a Doc.

* `token_data` (string, required): The JSON string of the user's access token.
* `doc_id` (string, required): The ID of the Doc.

#### `create_doc_page`
Create a new page in a Doc.

* `token_data` (string, required): The JSON string of the user's access token.
* `doc_id` (string, required): The ID of the Doc.
* `body` (string, required): A JSON string representing the page.

---

### Chat

#### `get_chat_channels`
Get all chat channels in a Workspace.

* `token_data` (string, required): The JSON string of the user's access token.
* `team_id` (string, required): The ID of the Workspace (team).

#### `send_chat_message`
Send a message to a chat channel.

* `token_data` (string, required): The JSON string of the user's access token.
* `channel_id` (string, required): The ID of the chat channel.
* `body` (string, required): A JSON string representing the message.

---

### Shared Hierarchy

#### `get_shared_hierarchy`
Get the shared hierarchy for a Workspace.

* `token_data` (string, required): The JSON string of the user's access token.
* `team_id` (string, required): The ID of the Workspace (team).

---

## Example Usage

### Getting Started

1. First, get your access token (either OAuth or personal API token)
2. Get your authorized teams/workspaces:

```python
token_data = '{"access_token": "pk_your_token_here"}'
result = get_authorized_teams(token_data)
```

3. Get spaces in your workspace:

```python
result = get_spaces(token_data, team_id="your_team_id")
```

4. Create a task:

```python
task_body = json.dumps({
    "name": "New Task",
    "description": "Task description",
    "priority": 3,
    "status": "Open"
})
result = create_task(token_data, list_id="your_list_id", body=task_body)
```

---

## Priority Levels

ClickUp uses the following priority levels:
- 1: Urgent
- 2: High
- 3: Normal
- 4: Low

---

## Timestamps

All timestamps in ClickUp API are in Unix milliseconds format.

Example: `1609459200000` represents January 1, 2021 00:00:00 UTC

---

## Rate Limits

ClickUp API has rate limits. For details, see the [ClickUp Rate Limits documentation](https://developer.clickup.com/docs/rate-limits).

---

## License

This MCP server is provided as-is for integration with ClickUp's API.
