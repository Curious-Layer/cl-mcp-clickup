import json
import logging
from typing import Dict, Optional

import httpx
from fastmcp import FastMCP

from .config import CLICKUP_API_BASE

logger = logging.getLogger("clickup-mcp-server")


def _get_token_data(token_data: str) -> Dict:
    """Decode access token JSON string to dictionary."""
    try:
        data = json.loads(token_data)
        return {
            "access_token": data.get("access_token") or data.get("token"),
            "token_type": data.get("token_type", "Bearer"),
        }
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode access token: {e}")
        return {}


def _get_headers(token_data: str) -> Dict[str, str]:
    """Create authorization headers for ClickUp API requests."""
    auth_data = _get_token_data(token_data)
    access_token = auth_data.get("access_token", "")
    return {
        "Authorization": f"{access_token}",
        "Content-Type": "application/json",
    }


def _make_request(
    method: str,
    endpoint: str,
    token_data: str,
    params: Optional[Dict] = None,
    body: Optional[Dict] = None,
) -> str:
    """Make HTTP request to ClickUp API."""
    url = f"{CLICKUP_API_BASE}{endpoint}"
    headers = _get_headers(token_data)

    try:
        with httpx.Client(timeout=30.0) as client:
            if method == "GET":
                response = client.get(url, headers=headers, params=params)
            elif method == "POST":
                response = client.post(url, headers=headers, json=body, params=params)
            elif method == "PUT":
                response = client.put(url, headers=headers, json=body)
            elif method == "DELETE":
                response = client.delete(url, headers=headers)
            else:
                return json.dumps({"error": f"Unsupported HTTP method: {method}"})

            response.raise_for_status()

            if response.status_code == 204:
                return json.dumps({"success": True})

            return json.dumps(response.json())
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
        try:
            error_detail = e.response.json()
        except Exception:
            error_detail = e.response.text
        return json.dumps({"error": str(e), "detail": error_detail})
    except Exception as e:
        logger.error(f"Request failed: {e}")
        return json.dumps({"error": str(e)})


def register_tools(mcp: FastMCP) -> None:
    # =======================================================================================
    #                       UTILITY TOOLS
    # =======================================================================================
    
    
    @mcp.tool()
    def ping() -> str:
        """
        Health check tool to verify the MCP server is running.
        No authentication required.
    
        :return: A JSON string with server status and available tool count.
        """
        return json.dumps({
            "status": "ok",
            "server": "CL ClickUp MCP Server",
            "message": "Server is running successfully!",
            "api_base": CLICKUP_API_BASE,
        })
    
    
    # =======================================================================================
    #                       AUTHORIZATION TOOLS
    # =======================================================================================
    
    
    @mcp.tool()
    def get_authorized_user(token_data: str) -> str:
        """
        Get the user that belongs to the access token.
    
        :param token_data: The JSON string of the user's access token containing 'access_token' or 'token'.
        :return: A JSON string of the authorized user information.
        """
        return _make_request("GET", "/user", token_data)
    
    
    @mcp.tool()
    def get_authorized_teams(token_data: str) -> str:
        """
        Get the authorized Workspaces (teams) for the access token.
    
        :param token_data: The JSON string of the user's access token.
        :return: A JSON string of the list of authorized teams/workspaces.
        """
        return _make_request("GET", "/team", token_data)
    
    
    # =======================================================================================
    #                       WORKSPACE HIERARCHY TOOLS
    # =======================================================================================
    
    
    @mcp.tool()
    def get_spaces(token_data: str, team_id: str, archived: bool = False) -> str:
        """
        Get all Spaces in a Workspace.
    
        :param token_data: The JSON string of the user's access token.
        :param team_id: The ID of the Workspace (team).
        :param archived: Whether to include archived spaces.
        :return: A JSON string of the list of spaces.
        """
        params = {"archived": str(archived).lower()}
        return _make_request("GET", f"/team/{team_id}/space", token_data, params=params)
    
    
    @mcp.tool()
    def get_space(token_data: str, space_id: str) -> str:
        """
        Get a specific Space.
    
        :param token_data: The JSON string of the user's access token.
        :param space_id: The ID of the Space.
        :return: A JSON string of the space information.
        """
        return _make_request("GET", f"/space/{space_id}", token_data)
    
    
    @mcp.tool()
    def create_space(token_data: str, team_id: str, body: str) -> str:
        """
        Create a new Space in a Workspace.
    
        :param token_data: The JSON string of the user's access token.
        :param team_id: The ID of the Workspace (team).
        :param body: A JSON string representing the space to create. Example: {"name": "New Space", "multiple_assignees": true, "features": {"due_dates": {"enabled": true}}}
        :return: A JSON string of the created space.
        """
        try:
            space_data = json.loads(body)
            return _make_request("POST", f"/team/{team_id}/space", token_data, body=space_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def update_space(token_data: str, space_id: str, body: str) -> str:
        """
        Update an existing Space.
    
        :param token_data: The JSON string of the user's access token.
        :param space_id: The ID of the Space to update.
        :param body: A JSON string with the fields to update. Example: {"name": "Updated Space Name"}
        :return: A JSON string of the updated space.
        """
        try:
            space_data = json.loads(body)
            return _make_request("PUT", f"/space/{space_id}", token_data, body=space_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def delete_space(token_data: str, space_id: str) -> str:
        """
        Delete a Space.
    
        :param token_data: The JSON string of the user's access token.
        :param space_id: The ID of the Space to delete.
        :return: A JSON string indicating success or failure.
        """
        return _make_request("DELETE", f"/space/{space_id}", token_data)
    
    
    # =======================================================================================
    #                       FOLDER TOOLS
    # =======================================================================================
    
    
    @mcp.tool()
    def get_folders(token_data: str, space_id: str, archived: bool = False) -> str:
        """
        Get all Folders in a Space.
    
        :param token_data: The JSON string of the user's access token.
        :param space_id: The ID of the Space.
        :param archived: Whether to include archived folders.
        :return: A JSON string of the list of folders.
        """
        params = {"archived": str(archived).lower()}
        return _make_request("GET", f"/space/{space_id}/folder", token_data, params=params)
    
    
    @mcp.tool()
    def get_folder(token_data: str, folder_id: str) -> str:
        """
        Get a specific Folder.
    
        :param token_data: The JSON string of the user's access token.
        :param folder_id: The ID of the Folder.
        :return: A JSON string of the folder information.
        """
        return _make_request("GET", f"/folder/{folder_id}", token_data)
    
    
    @mcp.tool()
    def create_folder(token_data: str, space_id: str, body: str) -> str:
        """
        Create a new Folder in a Space.
    
        :param token_data: The JSON string of the user's access token.
        :param space_id: The ID of the Space.
        :param body: A JSON string representing the folder to create. Example: {"name": "New Folder"}
        :return: A JSON string of the created folder.
        """
        try:
            folder_data = json.loads(body)
            return _make_request("POST", f"/space/{space_id}/folder", token_data, body=folder_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def update_folder(token_data: str, folder_id: str, body: str) -> str:
        """
        Update an existing Folder.
    
        :param token_data: The JSON string of the user's access token.
        :param folder_id: The ID of the Folder to update.
        :param body: A JSON string with the fields to update. Example: {"name": "Updated Folder Name"}
        :return: A JSON string of the updated folder.
        """
        try:
            folder_data = json.loads(body)
            return _make_request("PUT", f"/folder/{folder_id}", token_data, body=folder_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def delete_folder(token_data: str, folder_id: str) -> str:
        """
        Delete a Folder.
    
        :param token_data: The JSON string of the user's access token.
        :param folder_id: The ID of the Folder to delete.
        :return: A JSON string indicating success or failure.
        """
        return _make_request("DELETE", f"/folder/{folder_id}", token_data)
    
    
    # =======================================================================================
    #                       LIST TOOLS
    # =======================================================================================
    
    
    @mcp.tool()
    def get_lists(token_data: str, folder_id: str, archived: bool = False) -> str:
        """
        Get all Lists in a Folder.
    
        :param token_data: The JSON string of the user's access token.
        :param folder_id: The ID of the Folder.
        :param archived: Whether to include archived lists.
        :return: A JSON string of the list of lists.
        """
        params = {"archived": str(archived).lower()}
        return _make_request("GET", f"/folder/{folder_id}/list", token_data, params=params)
    
    
    @mcp.tool()
    def get_folderless_lists(token_data: str, space_id: str, archived: bool = False) -> str:
        """
        Get all Lists in a Space that are not in a Folder.
    
        :param token_data: The JSON string of the user's access token.
        :param space_id: The ID of the Space.
        :param archived: Whether to include archived lists.
        :return: A JSON string of the list of folderless lists.
        """
        params = {"archived": str(archived).lower()}
        return _make_request("GET", f"/space/{space_id}/list", token_data, params=params)
    
    
    @mcp.tool()
    def get_list(token_data: str, list_id: str) -> str:
        """
        Get a specific List.
    
        :param token_data: The JSON string of the user's access token.
        :param list_id: The ID of the List.
        :return: A JSON string of the list information.
        """
        return _make_request("GET", f"/list/{list_id}", token_data)
    
    
    @mcp.tool()
    def create_list(token_data: str, folder_id: str, body: str) -> str:
        """
        Create a new List in a Folder.
    
        :param token_data: The JSON string of the user's access token.
        :param folder_id: The ID of the Folder.
        :param body: A JSON string representing the list to create. Example: {"name": "New List", "content": "List description"}
        :return: A JSON string of the created list.
        """
        try:
            list_data = json.loads(body)
            return _make_request("POST", f"/folder/{folder_id}/list", token_data, body=list_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def create_folderless_list(token_data: str, space_id: str, body: str) -> str:
        """
        Create a new List in a Space (not in a Folder).
    
        :param token_data: The JSON string of the user's access token.
        :param space_id: The ID of the Space.
        :param body: A JSON string representing the list to create. Example: {"name": "New List", "content": "List description"}
        :return: A JSON string of the created list.
        """
        try:
            list_data = json.loads(body)
            return _make_request("POST", f"/space/{space_id}/list", token_data, body=list_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def update_list(token_data: str, list_id: str, body: str) -> str:
        """
        Update an existing List.
    
        :param token_data: The JSON string of the user's access token.
        :param list_id: The ID of the List to update.
        :param body: A JSON string with the fields to update. Example: {"name": "Updated List Name"}
        :return: A JSON string of the updated list.
        """
        try:
            list_data = json.loads(body)
            return _make_request("PUT", f"/list/{list_id}", token_data, body=list_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def delete_list(token_data: str, list_id: str) -> str:
        """
        Delete a List.
    
        :param token_data: The JSON string of the user's access token.
        :param list_id: The ID of the List to delete.
        :return: A JSON string indicating success or failure.
        """
        return _make_request("DELETE", f"/list/{list_id}", token_data)
    
    
    # =======================================================================================
    #                       TASK TOOLS
    # =======================================================================================
    
    
    @mcp.tool()
    def get_tasks(
        token_data: str,
        list_id: str,
        archived: bool = False,
        include_closed: bool = False,
        page: int = 0,
        order_by: str = None,
        reverse: bool = None,
        subtasks: bool = None,
        statuses: str = None,
        assignees: str = None,
        due_date_gt: int = None,
        due_date_lt: int = None,
        date_created_gt: int = None,
        date_created_lt: int = None,
        date_updated_gt: int = None,
        date_updated_lt: int = None,
    ) -> str:
        """
        Get tasks in a List.
    
        :param token_data: The JSON string of the user's access token.
        :param list_id: The ID of the List.
        :param archived: Whether to include archived tasks.
        :param include_closed: Whether to include closed tasks.
        :param page: Page number for pagination (0-indexed).
        :param order_by: Field to order by (id, created, updated, due_date).
        :param reverse: Whether to reverse the order.
        :param subtasks: Whether to include subtasks.
        :param statuses: Comma-separated list of status names to filter by.
        :param assignees: Comma-separated list of assignee user IDs to filter by.
        :param due_date_gt: Filter tasks with due date greater than (Unix timestamp in ms).
        :param due_date_lt: Filter tasks with due date less than (Unix timestamp in ms).
        :param date_created_gt: Filter tasks created after (Unix timestamp in ms).
        :param date_created_lt: Filter tasks created before (Unix timestamp in ms).
        :param date_updated_gt: Filter tasks updated after (Unix timestamp in ms).
        :param date_updated_lt: Filter tasks updated before (Unix timestamp in ms).
        :return: A JSON string of the list of tasks.
        """
        params = {
            "archived": str(archived).lower(),
            "include_closed": str(include_closed).lower(),
            "page": page,
        }
        
        if order_by:
            params["order_by"] = order_by
        if reverse is not None:
            params["reverse"] = str(reverse).lower()
        if subtasks is not None:
            params["subtasks"] = str(subtasks).lower()
        if statuses:
            params["statuses[]"] = statuses
        if assignees:
            params["assignees[]"] = assignees
        if due_date_gt:
            params["due_date_gt"] = due_date_gt
        if due_date_lt:
            params["due_date_lt"] = due_date_lt
        if date_created_gt:
            params["date_created_gt"] = date_created_gt
        if date_created_lt:
            params["date_created_lt"] = date_created_lt
        if date_updated_gt:
            params["date_updated_gt"] = date_updated_gt
        if date_updated_lt:
            params["date_updated_lt"] = date_updated_lt
        
        return _make_request("GET", f"/list/{list_id}/task", token_data, params=params)
    
    
    @mcp.tool()
    def get_task(token_data: str, task_id: str, include_subtasks: bool = False, include_markdown_description: bool = False) -> str:
        """
        Get a specific task.
    
        :param token_data: The JSON string of the user's access token.
        :param task_id: The ID of the task.
        :param include_subtasks: Whether to include subtasks.
        :param include_markdown_description: Whether to include markdown description.
        :return: A JSON string of the task information.
        """
        params = {
            "include_subtasks": str(include_subtasks).lower(),
            "include_markdown_description": str(include_markdown_description).lower(),
        }
        return _make_request("GET", f"/task/{task_id}", token_data, params=params)
    
    
    @mcp.tool()
    def create_task(token_data: str, list_id: str, body: str) -> str:
        """
        Create a new task in a List.
    
        :param token_data: The JSON string of the user's access token.
        :param list_id: The ID of the List.
        :param body: A JSON string representing the task to create. Example: {"name": "Task name", "description": "Task description", "assignees": [123], "priority": 3, "due_date": 1609459200000, "status": "Open"}
        :return: A JSON string of the created task.
        """
        try:
            task_data = json.loads(body)
            return _make_request("POST", f"/list/{list_id}/task", token_data, body=task_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def update_task(token_data: str, task_id: str, body: str) -> str:
        """
        Update an existing task.
    
        :param token_data: The JSON string of the user's access token.
        :param task_id: The ID of the task to update.
        :param body: A JSON string with the fields to update. Example: {"name": "Updated Task", "status": "In Progress", "priority": 2}
        :return: A JSON string of the updated task.
        """
        try:
            task_data = json.loads(body)
            return _make_request("PUT", f"/task/{task_id}", token_data, body=task_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def delete_task(token_data: str, task_id: str) -> str:
        """
        Delete a task.
    
        :param token_data: The JSON string of the user's access token.
        :param task_id: The ID of the task to delete.
        :return: A JSON string indicating success or failure.
        """
        return _make_request("DELETE", f"/task/{task_id}", token_data)
    
    
    @mcp.tool()
    def get_filtered_team_tasks(
        token_data: str,
        team_id: str,
        page: int = 0,
        order_by: str = None,
        reverse: bool = None,
        subtasks: bool = None,
        space_ids: str = None,
        project_ids: str = None,
        list_ids: str = None,
        statuses: str = None,
        include_closed: bool = False,
        assignees: str = None,
        due_date_gt: int = None,
        due_date_lt: int = None,
        date_created_gt: int = None,
        date_created_lt: int = None,
        date_updated_gt: int = None,
        date_updated_lt: int = None,
    ) -> str:
        """
        Get all tasks in a Workspace (team) with optional filters.
    
        :param token_data: The JSON string of the user's access token.
        :param team_id: The ID of the Workspace (team).
        :param page: Page number for pagination (0-indexed).
        :param order_by: Field to order by (id, created, updated, due_date).
        :param reverse: Whether to reverse the order.
        :param subtasks: Whether to include subtasks.
        :param space_ids: Comma-separated list of Space IDs to filter by.
        :param project_ids: Comma-separated list of Folder IDs to filter by.
        :param list_ids: Comma-separated list of List IDs to filter by.
        :param statuses: Comma-separated list of status names to filter by.
        :param include_closed: Whether to include closed tasks.
        :param assignees: Comma-separated list of assignee user IDs to filter by.
        :param due_date_gt: Filter tasks with due date greater than (Unix timestamp in ms).
        :param due_date_lt: Filter tasks with due date less than (Unix timestamp in ms).
        :param date_created_gt: Filter tasks created after (Unix timestamp in ms).
        :param date_created_lt: Filter tasks created before (Unix timestamp in ms).
        :param date_updated_gt: Filter tasks updated after (Unix timestamp in ms).
        :param date_updated_lt: Filter tasks updated before (Unix timestamp in ms).
        :return: A JSON string of the filtered tasks.
        """
        params = {
            "page": page,
            "include_closed": str(include_closed).lower(),
        }
        
        if order_by:
            params["order_by"] = order_by
        if reverse is not None:
            params["reverse"] = str(reverse).lower()
        if subtasks is not None:
            params["subtasks"] = str(subtasks).lower()
        if space_ids:
            params["space_ids[]"] = space_ids
        if project_ids:
            params["project_ids[]"] = project_ids
        if list_ids:
            params["list_ids[]"] = list_ids
        if statuses:
            params["statuses[]"] = statuses
        if assignees:
            params["assignees[]"] = assignees
        if due_date_gt:
            params["due_date_gt"] = due_date_gt
        if due_date_lt:
            params["due_date_lt"] = due_date_lt
        if date_created_gt:
            params["date_created_gt"] = date_created_gt
        if date_created_lt:
            params["date_created_lt"] = date_created_lt
        if date_updated_gt:
            params["date_updated_gt"] = date_updated_gt
        if date_updated_lt:
            params["date_updated_lt"] = date_updated_lt
        
        return _make_request("GET", f"/team/{team_id}/task", token_data, params=params)
    
    
    # =======================================================================================
    #                       TASK COMMENTS TOOLS
    # =======================================================================================
    
    
    @mcp.tool()
    def get_task_comments(token_data: str, task_id: str, start: int = None, start_id: str = None) -> str:
        """
        Get comments on a task.
    
        :param token_data: The JSON string of the user's access token.
        :param task_id: The ID of the task.
        :param start: Enter the start date for comments as a Unix timestamp in milliseconds.
        :param start_id: Enter the Comment ID to start from.
        :return: A JSON string of the list of comments.
        """
        params = {}
        if start:
            params["start"] = start
        if start_id:
            params["start_id"] = start_id
        
        return _make_request("GET", f"/task/{task_id}/comment", token_data, params=params)
    
    
    @mcp.tool()
    def create_task_comment(token_data: str, task_id: str, body: str) -> str:
        """
        Create a comment on a task.
    
        :param token_data: The JSON string of the user's access token.
        :param task_id: The ID of the task.
        :param body: A JSON string representing the comment. Example: {"comment_text": "This is a comment", "notify_all": false}
        :return: A JSON string of the created comment.
        """
        try:
            comment_data = json.loads(body)
            return _make_request("POST", f"/task/{task_id}/comment", token_data, body=comment_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def get_list_comments(token_data: str, list_id: str, start: int = None, start_id: str = None) -> str:
        """
        Get comments on a list.
    
        :param token_data: The JSON string of the user's access token.
        :param list_id: The ID of the list.
        :param start: Enter the start date for comments as a Unix timestamp in milliseconds.
        :param start_id: Enter the Comment ID to start from.
        :return: A JSON string of the list of comments.
        """
        params = {}
        if start:
            params["start"] = start
        if start_id:
            params["start_id"] = start_id
        
        return _make_request("GET", f"/list/{list_id}/comment", token_data, params=params)
    
    
    @mcp.tool()
    def create_list_comment(token_data: str, list_id: str, body: str) -> str:
        """
        Create a comment on a list.
    
        :param token_data: The JSON string of the user's access token.
        :param list_id: The ID of the list.
        :param body: A JSON string representing the comment. Example: {"comment_text": "This is a comment", "notify_all": false}
        :return: A JSON string of the created comment.
        """
        try:
            comment_data = json.loads(body)
            return _make_request("POST", f"/list/{list_id}/comment", token_data, body=comment_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def update_comment(token_data: str, comment_id: str, body: str) -> str:
        """
        Update a comment.
    
        :param token_data: The JSON string of the user's access token.
        :param comment_id: The ID of the comment to update.
        :param body: A JSON string with the updated comment. Example: {"comment_text": "Updated comment text", "resolved": true}
        :return: A JSON string indicating success or failure.
        """
        try:
            comment_data = json.loads(body)
            return _make_request("PUT", f"/comment/{comment_id}", token_data, body=comment_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def delete_comment(token_data: str, comment_id: str) -> str:
        """
        Delete a comment.
    
        :param token_data: The JSON string of the user's access token.
        :param comment_id: The ID of the comment to delete.
        :return: A JSON string indicating success or failure.
        """
        return _make_request("DELETE", f"/comment/{comment_id}", token_data)
    
    
    # =======================================================================================
    #                       TIME TRACKING TOOLS
    # =======================================================================================
    
    
    @mcp.tool()
    def get_time_entries(
        token_data: str,
        team_id: str,
        start_date: int = None,
        end_date: int = None,
        assignee: str = None,
        include_task_tags: bool = False,
        include_location_names: bool = False,
    ) -> str:
        """
        Get time entries within a date range.
    
        :param token_data: The JSON string of the user's access token.
        :param team_id: The ID of the Workspace (team).
        :param start_date: Start date as Unix timestamp in milliseconds.
        :param end_date: End date as Unix timestamp in milliseconds.
        :param assignee: User ID to filter time entries by.
        :param include_task_tags: Whether to include task tags.
        :param include_location_names: Whether to include location names.
        :return: A JSON string of the list of time entries.
        """
        params = {
            "include_task_tags": str(include_task_tags).lower(),
            "include_location_names": str(include_location_names).lower(),
        }
        
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if assignee:
            params["assignee"] = assignee
        
        return _make_request("GET", f"/team/{team_id}/time_entries", token_data, params=params)
    
    
    @mcp.tool()
    def get_single_time_entry(token_data: str, team_id: str, timer_id: str) -> str:
        """
        Get a single time entry.
    
        :param token_data: The JSON string of the user's access token.
        :param team_id: The ID of the Workspace (team).
        :param timer_id: The ID of the time entry.
        :return: A JSON string of the time entry.
        """
        return _make_request("GET", f"/team/{team_id}/time_entries/{timer_id}", token_data)
    
    
    @mcp.tool()
    def create_time_entry(token_data: str, team_id: str, body: str) -> str:
        """
        Create a time entry.
    
        :param token_data: The JSON string of the user's access token.
        :param team_id: The ID of the Workspace (team).
        :param body: A JSON string representing the time entry. Example: {"tid": "task_id", "start": 1609459200000, "duration": 3600000, "description": "Work description"}
        :return: A JSON string of the created time entry.
        """
        try:
            time_data = json.loads(body)
            return _make_request("POST", f"/team/{team_id}/time_entries", token_data, body=time_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def update_time_entry(token_data: str, team_id: str, timer_id: str, body: str) -> str:
        """
        Update a time entry.
    
        :param token_data: The JSON string of the user's access token.
        :param team_id: The ID of the Workspace (team).
        :param timer_id: The ID of the time entry.
        :param body: A JSON string with the updated time entry fields.
        :return: A JSON string of the updated time entry.
        """
        try:
            time_data = json.loads(body)
            return _make_request("PUT", f"/team/{team_id}/time_entries/{timer_id}", token_data, body=time_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def delete_time_entry(token_data: str, team_id: str, timer_id: str) -> str:
        """
        Delete a time entry.
    
        :param token_data: The JSON string of the user's access token.
        :param team_id: The ID of the Workspace (team).
        :param timer_id: The ID of the time entry to delete.
        :return: A JSON string indicating success or failure.
        """
        return _make_request("DELETE", f"/team/{team_id}/time_entries/{timer_id}", token_data)
    
    
    @mcp.tool()
    def start_time_entry(token_data: str, team_id: str, body: str) -> str:
        """
        Start a timer for time tracking.
    
        :param token_data: The JSON string of the user's access token.
        :param team_id: The ID of the Workspace (team).
        :param body: A JSON string with timer details. Example: {"tid": "task_id", "description": "Working on task"}
        :return: A JSON string of the started timer.
        """
        try:
            timer_data = json.loads(body)
            return _make_request("POST", f"/team/{team_id}/time_entries/start", token_data, body=timer_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def stop_time_entry(token_data: str, team_id: str) -> str:
        """
        Stop the currently running timer.
    
        :param token_data: The JSON string of the user's access token.
        :param team_id: The ID of the Workspace (team).
        :return: A JSON string of the stopped timer.
        """
        return _make_request("POST", f"/team/{team_id}/time_entries/stop", token_data, body={})
    
    
    @mcp.tool()
    def get_running_time_entry(token_data: str, team_id: str) -> str:
        """
        Get the currently running timer.
    
        :param token_data: The JSON string of the user's access token.
        :param team_id: The ID of the Workspace (team).
        :return: A JSON string of the running timer, or empty if no timer is running.
        """
        return _make_request("GET", f"/team/{team_id}/time_entries/current", token_data)
    
    
    # =======================================================================================
    #                       MEMBERS TOOLS
    # =======================================================================================
    
    
    @mcp.tool()
    def get_workspace_members(token_data: str, team_id: str) -> str:
        """
        Get all members in a Workspace.
    
        :param token_data: The JSON string of the user's access token.
        :param team_id: The ID of the Workspace (team).
        :return: A JSON string of the workspace with member information.
        """
        return _make_request("GET", f"/team/{team_id}", token_data)
    
    
    @mcp.tool()
    def get_task_members(token_data: str, task_id: str) -> str:
        """
        Get members assigned to a task.
    
        :param token_data: The JSON string of the user's access token.
        :param task_id: The ID of the task.
        :return: A JSON string of the list of task members.
        """
        return _make_request("GET", f"/task/{task_id}/member", token_data)
    
    
    @mcp.tool()
    def get_list_members(token_data: str, list_id: str) -> str:
        """
        Get members with access to a list.
    
        :param token_data: The JSON string of the user's access token.
        :param list_id: The ID of the list.
        :return: A JSON string of the list of members.
        """
        return _make_request("GET", f"/list/{list_id}/member", token_data)
    
    
    # =======================================================================================
    #                       TAGS TOOLS
    # =======================================================================================
    
    
    @mcp.tool()
    def get_space_tags(token_data: str, space_id: str) -> str:
        """
        Get all tags in a Space.
    
        :param token_data: The JSON string of the user's access token.
        :param space_id: The ID of the Space.
        :return: A JSON string of the list of tags.
        """
        return _make_request("GET", f"/space/{space_id}/tag", token_data)
    
    
    @mcp.tool()
    def create_space_tag(token_data: str, space_id: str, body: str) -> str:
        """
        Create a new tag in a Space.
    
        :param token_data: The JSON string of the user's access token.
        :param space_id: The ID of the Space.
        :param body: A JSON string representing the tag. Example: {"tag": {"name": "Tag Name", "tag_fg": "#FFFFFF", "tag_bg": "#000000"}}
        :return: A JSON string of the created tag.
        """
        try:
            tag_data = json.loads(body)
            return _make_request("POST", f"/space/{space_id}/tag", token_data, body=tag_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def update_space_tag(token_data: str, space_id: str, tag_name: str, body: str) -> str:
        """
        Update a tag in a Space.
    
        :param token_data: The JSON string of the user's access token.
        :param space_id: The ID of the Space.
        :param tag_name: The name of the tag to update.
        :param body: A JSON string with the updated tag. Example: {"tag": {"name": "New Name", "tag_fg": "#FFFFFF", "tag_bg": "#FF0000"}}
        :return: A JSON string of the updated tag.
        """
        try:
            tag_data = json.loads(body)
            return _make_request("PUT", f"/space/{space_id}/tag/{tag_name}", token_data, body=tag_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def delete_space_tag(token_data: str, space_id: str, tag_name: str) -> str:
        """
        Delete a tag from a Space.
    
        :param token_data: The JSON string of the user's access token.
        :param space_id: The ID of the Space.
        :param tag_name: The name of the tag to delete.
        :return: A JSON string indicating success or failure.
        """
        return _make_request("DELETE", f"/space/{space_id}/tag/{tag_name}", token_data)
    
    
    @mcp.tool()
    def add_tag_to_task(token_data: str, task_id: str, tag_name: str) -> str:
        """
        Add a tag to a task.
    
        :param token_data: The JSON string of the user's access token.
        :param task_id: The ID of the task.
        :param tag_name: The name of the tag to add.
        :return: A JSON string indicating success or failure.
        """
        return _make_request("POST", f"/task/{task_id}/tag/{tag_name}", token_data, body={})
    
    
    @mcp.tool()
    def remove_tag_from_task(token_data: str, task_id: str, tag_name: str) -> str:
        """
        Remove a tag from a task.
    
        :param token_data: The JSON string of the user's access token.
        :param task_id: The ID of the task.
        :param tag_name: The name of the tag to remove.
        :return: A JSON string indicating success or failure.
        """
        return _make_request("DELETE", f"/task/{task_id}/tag/{tag_name}", token_data)
    
    
    # =======================================================================================
    #                       GOALS TOOLS
    # =======================================================================================
    
    
    @mcp.tool()
    def get_goals(token_data: str, team_id: str, include_completed: bool = False) -> str:
        """
        Get all goals in a Workspace.
    
        :param token_data: The JSON string of the user's access token.
        :param team_id: The ID of the Workspace (team).
        :param include_completed: Whether to include completed goals.
        :return: A JSON string of the list of goals.
        """
        params = {"include_completed": str(include_completed).lower()}
        return _make_request("GET", f"/team/{team_id}/goal", token_data, params=params)
    
    
    @mcp.tool()
    def get_goal(token_data: str, goal_id: str) -> str:
        """
        Get a specific goal.
    
        :param token_data: The JSON string of the user's access token.
        :param goal_id: The ID of the goal.
        :return: A JSON string of the goal information.
        """
        return _make_request("GET", f"/goal/{goal_id}", token_data)
    
    
    @mcp.tool()
    def create_goal(token_data: str, team_id: str, body: str) -> str:
        """
        Create a new goal.
    
        :param token_data: The JSON string of the user's access token.
        :param team_id: The ID of the Workspace (team).
        :param body: A JSON string representing the goal. Example: {"name": "Goal Name", "due_date": 1609459200000, "description": "Goal description", "multiple_owners": true, "owners": [123]}
        :return: A JSON string of the created goal.
        """
        try:
            goal_data = json.loads(body)
            return _make_request("POST", f"/team/{team_id}/goal", token_data, body=goal_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def update_goal(token_data: str, goal_id: str, body: str) -> str:
        """
        Update a goal.
    
        :param token_data: The JSON string of the user's access token.
        :param goal_id: The ID of the goal to update.
        :param body: A JSON string with the fields to update.
        :return: A JSON string of the updated goal.
        """
        try:
            goal_data = json.loads(body)
            return _make_request("PUT", f"/goal/{goal_id}", token_data, body=goal_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def delete_goal(token_data: str, goal_id: str) -> str:
        """
        Delete a goal.
    
        :param token_data: The JSON string of the user's access token.
        :param goal_id: The ID of the goal to delete.
        :return: A JSON string indicating success or failure.
        """
        return _make_request("DELETE", f"/goal/{goal_id}", token_data)
    
    
    # =======================================================================================
    #                       CHECKLISTS TOOLS
    # =======================================================================================
    
    
    @mcp.tool()
    def create_checklist(token_data: str, task_id: str, body: str) -> str:
        """
        Create a new checklist in a task.
    
        :param token_data: The JSON string of the user's access token.
        :param task_id: The ID of the task.
        :param body: A JSON string representing the checklist. Example: {"name": "Checklist Name"}
        :return: A JSON string of the created checklist.
        """
        try:
            checklist_data = json.loads(body)
            return _make_request("POST", f"/task/{task_id}/checklist", token_data, body=checklist_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def update_checklist(token_data: str, checklist_id: str, body: str) -> str:
        """
        Update a checklist.
    
        :param token_data: The JSON string of the user's access token.
        :param checklist_id: The ID of the checklist.
        :param body: A JSON string with the fields to update. Example: {"name": "Updated Checklist Name", "position": 0}
        :return: A JSON string of the updated checklist.
        """
        try:
            checklist_data = json.loads(body)
            return _make_request("PUT", f"/checklist/{checklist_id}", token_data, body=checklist_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def delete_checklist(token_data: str, checklist_id: str) -> str:
        """
        Delete a checklist.
    
        :param token_data: The JSON string of the user's access token.
        :param checklist_id: The ID of the checklist to delete.
        :return: A JSON string indicating success or failure.
        """
        return _make_request("DELETE", f"/checklist/{checklist_id}", token_data)
    
    
    @mcp.tool()
    def create_checklist_item(token_data: str, checklist_id: str, body: str) -> str:
        """
        Create a new checklist item.
    
        :param token_data: The JSON string of the user's access token.
        :param checklist_id: The ID of the checklist.
        :param body: A JSON string representing the checklist item. Example: {"name": "Item name", "assignee": 123}
        :return: A JSON string of the updated checklist with the new item.
        """
        try:
            item_data = json.loads(body)
            return _make_request("POST", f"/checklist/{checklist_id}/checklist_item", token_data, body=item_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def update_checklist_item(token_data: str, checklist_id: str, checklist_item_id: str, body: str) -> str:
        """
        Update a checklist item.
    
        :param token_data: The JSON string of the user's access token.
        :param checklist_id: The ID of the checklist.
        :param checklist_item_id: The ID of the checklist item.
        :param body: A JSON string with the fields to update. Example: {"name": "Updated Item", "resolved": true}
        :return: A JSON string of the updated checklist.
        """
        try:
            item_data = json.loads(body)
            return _make_request("PUT", f"/checklist/{checklist_id}/checklist_item/{checklist_item_id}", token_data, body=item_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def delete_checklist_item(token_data: str, checklist_id: str, checklist_item_id: str) -> str:
        """
        Delete a checklist item.
    
        :param token_data: The JSON string of the user's access token.
        :param checklist_id: The ID of the checklist.
        :param checklist_item_id: The ID of the checklist item to delete.
        :return: A JSON string indicating success or failure.
        """
        return _make_request("DELETE", f"/checklist/{checklist_id}/checklist_item/{checklist_item_id}", token_data)
    
    
    # =======================================================================================
    #                       CUSTOM FIELDS TOOLS
    # =======================================================================================
    
    
    @mcp.tool()
    def get_accessible_custom_fields(token_data: str, list_id: str) -> str:
        """
        Get all custom fields accessible in a list.
    
        :param token_data: The JSON string of the user's access token.
        :param list_id: The ID of the list.
        :return: A JSON string of the list of custom fields.
        """
        return _make_request("GET", f"/list/{list_id}/field", token_data)
    
    
    @mcp.tool()
    def set_custom_field_value(token_data: str, task_id: str, field_id: str, body: str) -> str:
        """
        Set a custom field value on a task.
    
        :param token_data: The JSON string of the user's access token.
        :param task_id: The ID of the task.
        :param field_id: The ID of the custom field.
        :param body: A JSON string with the value. Example: {"value": "field value"} or {"value": 123} depending on field type.
        :return: A JSON string indicating success or failure.
        """
        try:
            field_data = json.loads(body)
            return _make_request("POST", f"/task/{task_id}/field/{field_id}", token_data, body=field_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def remove_custom_field_value(token_data: str, task_id: str, field_id: str) -> str:
        """
        Remove a custom field value from a task.
    
        :param token_data: The JSON string of the user's access token.
        :param task_id: The ID of the task.
        :param field_id: The ID of the custom field.
        :return: A JSON string indicating success or failure.
        """
        return _make_request("DELETE", f"/task/{task_id}/field/{field_id}", token_data)
    
    
    # =======================================================================================
    #                       VIEWS TOOLS
    # =======================================================================================
    
    
    @mcp.tool()
    def get_team_views(token_data: str, team_id: str) -> str:
        """
        Get all views at the Workspace level.
    
        :param token_data: The JSON string of the user's access token.
        :param team_id: The ID of the Workspace (team).
        :return: A JSON string of the list of views.
        """
        return _make_request("GET", f"/team/{team_id}/view", token_data)
    
    
    @mcp.tool()
    def get_space_views(token_data: str, space_id: str) -> str:
        """
        Get all views in a Space.
    
        :param token_data: The JSON string of the user's access token.
        :param space_id: The ID of the Space.
        :return: A JSON string of the list of views.
        """
        return _make_request("GET", f"/space/{space_id}/view", token_data)
    
    
    @mcp.tool()
    def get_folder_views(token_data: str, folder_id: str) -> str:
        """
        Get all views in a Folder.
    
        :param token_data: The JSON string of the user's access token.
        :param folder_id: The ID of the Folder.
        :return: A JSON string of the list of views.
        """
        return _make_request("GET", f"/folder/{folder_id}/view", token_data)
    
    
    @mcp.tool()
    def get_list_views(token_data: str, list_id: str) -> str:
        """
        Get all views in a List.
    
        :param token_data: The JSON string of the user's access token.
        :param list_id: The ID of the List.
        :return: A JSON string of the list of views.
        """
        return _make_request("GET", f"/list/{list_id}/view", token_data)
    
    
    @mcp.tool()
    def get_view(token_data: str, view_id: str) -> str:
        """
        Get a specific view.
    
        :param token_data: The JSON string of the user's access token.
        :param view_id: The ID of the view.
        :return: A JSON string of the view information.
        """
        return _make_request("GET", f"/view/{view_id}", token_data)
    
    
    @mcp.tool()
    def get_view_tasks(token_data: str, view_id: str, page: int = 0) -> str:
        """
        Get tasks in a view.
    
        :param token_data: The JSON string of the user's access token.
        :param view_id: The ID of the view.
        :param page: Page number for pagination (0-indexed).
        :return: A JSON string of the list of tasks in the view.
        """
        params = {"page": page}
        return _make_request("GET", f"/view/{view_id}/task", token_data, params=params)
    
    
    # =======================================================================================
    #                       WEBHOOKS TOOLS
    # =======================================================================================
    
    
    @mcp.tool()
    def get_webhooks(token_data: str, team_id: str) -> str:
        """
        Get all webhooks in a Workspace.
    
        :param token_data: The JSON string of the user's access token.
        :param team_id: The ID of the Workspace (team).
        :return: A JSON string of the list of webhooks.
        """
        return _make_request("GET", f"/team/{team_id}/webhook", token_data)
    
    
    @mcp.tool()
    def create_webhook(token_data: str, team_id: str, body: str) -> str:
        """
        Create a new webhook.
    
        :param token_data: The JSON string of the user's access token.
        :param team_id: The ID of the Workspace (team).
        :param body: A JSON string representing the webhook. Example: {"endpoint": "https://example.com/webhook", "events": ["taskCreated", "taskUpdated"]}
        :return: A JSON string of the created webhook.
        """
        try:
            webhook_data = json.loads(body)
            return _make_request("POST", f"/team/{team_id}/webhook", token_data, body=webhook_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def update_webhook(token_data: str, webhook_id: str, body: str) -> str:
        """
        Update a webhook.
    
        :param token_data: The JSON string of the user's access token.
        :param webhook_id: The ID of the webhook.
        :param body: A JSON string with the fields to update. Example: {"endpoint": "https://example.com/new-webhook", "status": "active"}
        :return: A JSON string of the updated webhook.
        """
        try:
            webhook_data = json.loads(body)
            return _make_request("PUT", f"/webhook/{webhook_id}", token_data, body=webhook_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    @mcp.tool()
    def delete_webhook(token_data: str, webhook_id: str) -> str:
        """
        Delete a webhook.
    
        :param token_data: The JSON string of the user's access token.
        :param webhook_id: The ID of the webhook to delete.
        :return: A JSON string indicating success or failure.
        """
        return _make_request("DELETE", f"/webhook/{webhook_id}", token_data)
    
    
    # =======================================================================================
    #                       DOCS TOOLS
    # =======================================================================================
    
    
    @mcp.tool()
    def search_docs(token_data: str, team_id: str, query: str = None) -> str:
        """
        Search for Docs in a Workspace.
    
        :param token_data: The JSON string of the user's access token.
        :param team_id: The ID of the Workspace (team).
        :param query: Search query string.
        :return: A JSON string of the search results.
        """
        params = {}
        if query:
            params["query"] = query
        return _make_request("GET", f"/team/{team_id}/doc", token_data, params=params)
    
    
    @mcp.tool()
    def get_doc_pages(token_data: str, doc_id: str) -> str:
        """
        Get all pages in a Doc.
    
        :param token_data: The JSON string of the user's access token.
        :param doc_id: The ID of the Doc.
        :return: A JSON string of the list of pages.
        """
        return _make_request("GET", f"/doc/{doc_id}/page", token_data)
    
    
    @mcp.tool()
    def create_doc_page(token_data: str, doc_id: str, body: str) -> str:
        """
        Create a new page in a Doc.
    
        :param token_data: The JSON string of the user's access token.
        :param doc_id: The ID of the Doc.
        :param body: A JSON string representing the page. Example: {"name": "Page Title", "content": "Page content in markdown"}
        :return: A JSON string of the created page.
        """
        try:
            page_data = json.loads(body)
            return _make_request("POST", f"/doc/{doc_id}/page", token_data, body=page_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    # =======================================================================================
    #                       CHAT TOOLS
    # =======================================================================================
    
    
    @mcp.tool()
    def get_chat_channels(token_data: str, team_id: str) -> str:
        """
        Get all chat channels in a Workspace.
    
        :param token_data: The JSON string of the user's access token.
        :param team_id: The ID of the Workspace (team).
        :return: A JSON string of the list of chat channels.
        """
        return _make_request("GET", f"/team/{team_id}/chat/channel", token_data)
    
    
    @mcp.tool()
    def send_chat_message(token_data: str, channel_id: str, body: str) -> str:
        """
        Send a message to a chat channel.
    
        :param token_data: The JSON string of the user's access token.
        :param channel_id: The ID of the chat channel.
        :param body: A JSON string representing the message. Example: {"content": "Hello team!"}
        :return: A JSON string of the sent message.
        """
        try:
            message_data = json.loads(body)
            return _make_request("POST", f"/chat/channel/{channel_id}/message", token_data, body=message_data)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in body: {e}"})
    
    
    # =======================================================================================
    #                       SHARED HIERARCHY TOOLS
    # =======================================================================================
    
    
    @mcp.tool()
    def get_shared_hierarchy(token_data: str, team_id: str) -> str:
        """
        Get the shared hierarchy for a Workspace. Returns all resources shared with the authenticated user.
    
        :param token_data: The JSON string of the user's access token.
        :param team_id: The ID of the Workspace (team).
        :return: A JSON string of the shared hierarchy.
        """
        return _make_request("GET", f"/team/{team_id}/shared", token_data)
    
    
    # =======================================================================================
    #                       MCP TOOLS END
    # =======================================================================================
    
    
    

