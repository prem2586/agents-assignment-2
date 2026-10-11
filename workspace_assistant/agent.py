"""
Google Workspace Assistant - Main Agent Definition

Part 1: Implement tools and system instruction for Calendar OR Tasks
Part 2: Add McpToolset for GitHub integration
"""

import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters



from workspace_assistant.tools.mcp_tools import mcp_tools


from workspace_assistant.config.settings import Settings
from workspace_assistant.tools.tasks_tools import tasks_tools  # or tasks_tools

# Agent for Tasks
# def create_agent() -> LlmAgent:
#     settings = Settings()

#     instruction = """
#     You are a Google Workspace and GitHub assistant.

#     Google Tasks:
#     - List tasks.
#     - Create tasks.
#     - Complete tasks.
#     - Update task details.
#     - Delete tasks.
#     - Use Google Tasks tools for task operations.
#     - Confirm before deleting tasks.

#     Always use the appropriate tools.
#     Never invent task IDs or repository information.
#     """

#     return LlmAgent(
#         name="workspace_assistant",
#         model=settings.model_name,
#         instruction=instruction,
#         tools=tasks_tools,
#     )

#Agent for search github tools and defer loading all tools
# def create_agent() -> LlmAgent:
#     settings = Settings()


#     instruction = """
#     You are a GitHub assistant.

#     GITHUB WORKFLOW:
#         1. For a GitHub request, call search_github_tools ONCE.
#         2. Select the most relevant tool from the results.
#         3. Call call_github_tool using its exact name and input schema.
#         4. If execution succeeds:
#         - Read the returned data.
#         - Answer the user's original question.
#         - STOP calling tools.
#         5. If execution fails:
#         - Explain the error.
#         - Do not repeatedly retry with different search terms.
#         6. Never call search_github_tools more than once
#         for the same user request.
#         7. Never use Google Tasks tools for GitHub requests.

#     Never invent results.
#     """

#     return LlmAgent(
#         name="workspace_assistant",
#         model=settings.model_name,
#         instruction=instruction,
#         tools=mcp_tools,
#     )


#agent combining both task and github usecase
def create_agent() -> LlmAgent:
    settings = Settings()

    instruction = """
    You are a Google Workspace and GitHub assistant.

    GOOGLE TASKS:
    - List tasks using list_tasks.
    - Create tasks using create_task.
    - Complete tasks using complete_task.
    - Update task details using update_task.
    - Delete tasks using delete_task.
    - Find the correct task ID before modifying a task.
    - Confirm with the user before deleting tasks.

    GITHUB WORKFLOW:
        1. Understand the user's GitHub request and identify
        the operation needed.

        2. Check the tools already available to you.
        - If a directly available GitHub tool can fulfill
            the request, use it.
        - Otherwise, use search_github_tools to discover
            the appropriate GitHub MCP operation.

        3. When using tool discovery:
        - Search only once per user request.
        - Select the most relevant matching tool.
        - Read its input schema to determine the
            required arguments.
        - Execute it using call_github_tool.

        4. After tool execution:
        - If successful and the result satisfies the
            request, provide the final answer.
        - If additional operations are genuinely needed,
            use the appropriate tools.
        - If an error occurs, explain it clearly.
        - Do not repeatedly retry identical or
            equivalent failed operations.

        5. Never invent repository information.
        6. Never use Google Tasks tools for GitHub requests.
        7. Ask for explicit confirmation before modifying
        or deleting GitHub resources.

    GENERAL:
    - Select the appropriate tool based on the user's request.
    - Use Google Tasks tools for task operations.
    - Use GitHub MCP tools for GitHub operations.
    - Report tool errors clearly.
    - Never invent task IDs or repository information.
    """

    return LlmAgent(
        name="workspace_assistant",
        model=settings.model_name,
        instruction=instruction,
        tools=tasks_tools + mcp_tools,
    )


root_agent = create_agent()

def create_agent_with_tool_search() -> LlmAgent:
    """BONUS: Create agent with defer_loading for tool search."""
    raise NotImplementedError("Bonus: Implement tool search pattern")
