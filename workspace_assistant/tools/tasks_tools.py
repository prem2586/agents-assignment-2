"""
Option B: Tasks Manager Tools

Implement at least 3 tools for Google Tasks operations.
"""

from typing import Optional
from google.adk.tools import FunctionTool
from workspace_assistant.tools.auth import get_tasks_service


# TODO: Implement your tasks tools
# Define each tool as a plain Python function with a clear docstring and type
# hints (ADK reads these to build the tool schema and auto-wraps the function),
# then add it to the list below. Each tool should return a dict with 'status'
# and relevant data. Wrapping with FunctionTool(func=my_function) is optional
# and only needed when you want explicit control over the tool.
def list_tasks(max_results: int = 10) -> dict:
    """List upcoming calendar events.


    Args:
        max_results: Maximum number of events to return.

    Returns:
        dict with 'status' and 'events' keys.
    """
    try:
        service = get_tasks_service()
        events_result = service.tasks().list(
            tasklist="@default",
            maxResults=max_results
        ).execute()
        return {"status": "success", "events": events_result.get("items", [])}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def create_task(title: str) -> dict:
    """Add a taks to my task list.


    Args:
        title: Title of the task.

    Returns:
        dict with 'status' and 'TaskList' keys.
    """
    try:
        service = get_tasks_service()
        events_result = service.tasks().insert(
            tasklist="@default",
            body={
                "title": title
            }
        ).execute()
        return {"status": "success", "tast": events_result}
    except Exception as e:
        return {"status": "error", "message": str(e)}    

def complete_task(task_id: str) -> dict:
    """Mark a task as completed.

    Args:
        task_id: Google Tasks ID of the task.
    """
    try:
        service = get_tasks_service()
        result = service.tasks().patch(
            tasklist="@default",
            task=task_id,
            body={"status": "completed"},
        ).execute()

        return {"status": "success", "task": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def update_task(
    task_id: str,
    title: str = "",
    notes: str = "",
) -> dict:
    """Update a task's title or notes.

    Args:
        task_id: Google Tasks ID of the task.
        title: New title; empty string means unchanged.
        notes: New notes; empty string means unchanged.
    """
    try:
        body = {}

        if title:
            body["title"] = title
        if notes:
            body["notes"] = notes

        if not body:
            return {
                "status": "error",
                "message": "Provide a title or notes to update."
            }

        service = get_tasks_service()
        result = service.tasks().patch(
            tasklist="@default",
            task=task_id,
            body=body,
        ).execute()

        return {"status": "success", "task": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def delete_task(task_id: str) -> dict:
    """Delete a task from the default task list.

    Args:
        task_id: Google Tasks ID of the task.
    """
    try:
        service = get_tasks_service()
        service.tasks().delete(
            tasklist="@default",
            task=task_id,
        ).execute()

        return {
            "status": "success",
            "message": "Task deleted successfully.",
            "task_id": task_id,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


tasks_tools = [
    list_tasks,
    create_task,
    complete_task,
    update_task,
    delete_task,
]
