"""
Part 2: GitHub MCP Integration

Configure McpToolset to connect to the GitHub MCP server.

Required: Direct configuration in Python code
Optional: File-based configuration from config/mcp_servers.json
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from mcp import ClientSession
from mcp.client.stdio import stdio_client
from google.adk.tools import FunctionTool
import traceback


load_dotenv()

# Path to MCP server configuration (for Option B)
MCP_CONFIG_PATH = Path(__file__).parent.parent / "config" / "mcp_servers.json"


# =============================================================================
# REQUIRED: Direct Configuration
# =============================================================================
# TODO: Implement get_github_mcp_toolset()
# Configure the GitHub MCP server directly in Python code.
#
# Example structure:
#
def get_github_mcp_toolset() -> McpToolset:
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not token:
        raise ValueError("GITHUB_PERSONAL_ACCESS_TOKEN not set in .env")

    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-github"],
        env={"GITHUB_PERSONAL_ACCESS_TOKEN": token}
    )

    return McpToolset(
        connection_params=StdioConnectionParams(server_params=server_params)
    )

def get_github_mcp_toolset_frequent() -> McpToolset:
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not token:
        raise ValueError("GITHUB_PERSONAL_ACCESS_TOKEN not set in .env")

    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-github"],
        env={"GITHUB_PERSONAL_ACCESS_TOKEN": token}
    )

    return McpToolset(
        connection_params=StdioConnectionParams(server_params=server_params),
        tool_filter=[
                    "search_repositories",
                    "get_file_contents",
        ]
    )

# =============================================================================
# OPTIONAL: File-based Configuration
# =============================================================================
def load_mcp_config() -> dict:
    """Load MCP server configuration from JSON file."""
    if not MCP_CONFIG_PATH.exists():
        raise FileNotFoundError(f"MCP config not found: {MCP_CONFIG_PATH}")

    with open(MCP_CONFIG_PATH) as f:
        config = json.load(f)

    # Replace environment variable placeholders
    github_config = config.get("mcpServers", {}).get("github", {})
    env = github_config.get("env", {})
    for key, value in env.items():
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            env_var = value[2:-1]
            env[key] = os.getenv(env_var, "")

    return config


# TODO: Implement get_github_mcp_toolset_from_config()
# Load configuration from config/mcp_servers.json
#
# Example structure:
#
# def get_github_mcp_toolset_from_config() -> McpToolset:
#     config = load_mcp_config()
#     github = config["mcpServers"]["github"]
#
#     token = github["env"].get("GITHUB_PERSONAL_ACCESS_TOKEN")
#     if not token:
#         raise ValueError("GITHUB_PERSONAL_ACCESS_TOKEN not set in .env")
#
#     server_params = StdioServerParameters(
#         command=github["command"],
#         args=github["args"],
#         env=github["env"]
#     )
#
#     return McpToolset(
#         connection_params=StdioConnectionParams(server_params=server_params)
#     )


# =============================================================================
# BONUS (+25 points) - Tool Search Pattern
# =============================================================================
# Implement defer_loading to reduce token usage by ~80%
#
# Why: GitHub MCP has 15+ tools (~8K tokens). Loading all upfront is wasteful.
# With defer_loading, tools are discovered on-demand (~1.5K tokens).
#
# Points breakdown:
# - search_github_tools function (10 pts)
# - defer_loading=True configured (10 pts)
# - create_agent_with_tool_search works (5 pts)
#
# Steps:
# 1. Create a search_github_tools tool that searches available MCP tools
# 2. Configure McpToolset with defer_loading=True
# 3. Keep only 1-2 frequently-used tools always loaded
#
# REQUIRED: In your reflection, compare context/token usage:
# - Run WITHOUT defer_loading, note context size (~8K tokens for 15+ tools)
# - Run WITH defer_loading, note context size (~1.5K tokens)
# - Calculate and report the % reduction
#
# Example structure:
#


async def search_github_tools(query: str) -> dict:
    """Search available GitHub MCP tools by keyword.

    Args:
        query: Search term such as repository, issues,
            or pull request.

    Returns:
        Matching GitHub tool names and descriptions.
    """
    toolset = get_github_mcp_toolset()

    try:
        tools = await toolset.get_tools()

        query_words = query.lower().strip().split()
        matches = []

        for tool in tools:
            name = tool.name
            description = getattr(tool, "description", "") or ""

            searchable = f"{name} {description}".lower()

            if any(word in searchable for word in query_words):
                matches.append({
                    "name": name,
                    "description": description,
                })

        return {
            "status": "success",
            "total_tools": len(tools),
            "matching_tools": matches[:10],
            "count": len(matches),
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"{type(e).__name__}: {e}",
            "matching_tools": [],
        }

    finally:
        await toolset.close()

# def get_github_mcp_toolset_deferred() -> McpToolset:
#     """Create McpToolset with defer_loading for on-demand tool discovery."""
#     token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
#     if not token:
#         raise ValueError("GITHUB_PERSONAL_ACCESS_TOKEN not set")

#     server_params = StdioServerParameters(
#         command="npx",
#         args=["-y", "@modelcontextprotocol/server-github"],
#         env={"GITHUB_PERSONAL_ACCESS_TOKEN": token}
#     )

#     return McpToolset(
#         connection_params=StdioConnectionParams(server_params=server_params),
#         defer_loading=True  # Key: tools loaded on-demand
#     )

def get_github_mcp_toolset_deferred() -> McpToolset:
    """Expose frequently used GitHub tools.

    Other GitHub operations are discovered through
    search_github_tools and executed through call_github_tool.

    This approximates deferred tool loading using tool filtering.
    """
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"],
            env={"GITHUB_PERSONAL_ACCESS_TOKEN": token}
    )
    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=server_params
        ),
        tool_filter=[
            "search_repositories",
            "get_file_contents",
        ],
        #Not using this since its not supported or have to go for custom implementation
        #defer_loading=True  # Key: tools loaded on-demand
    )



async def call_github_tool(
    tool_name: str,
    arguments: dict,
) -> dict:
    """Execute a GitHub MCP tool by name.

    Args:
        tool_name: Exact GitHub MCP tool name returned by search_github_tools.
        arguments: Arguments required by the selected MCP tool.

    Returns:
        Dictionary containing the execution result or error.
    """
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")

    if not token:
        return {
            "status": "error",
            "error": "GITHUB_PERSONAL_ACCESS_TOKEN is missing",
        }

    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-github"],
        env={
            **os.environ,
            "GITHUB_PERSONAL_ACCESS_TOKEN": token,
        },
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                available = await session.list_tools()
                tool_names = {
                    tool.name for tool in available.tools
                }

                if tool_name not in tool_names:
                    return {
                        "status": "error",
                        "error": f"Unknown GitHub tool: {tool_name}",
                        "available_tools": sorted(tool_names),
                    }

                result = await session.call_tool(
                    name=tool_name,
                    arguments=arguments,
                )

                return {
                    "status": "error" if getattr(result, "isError", False) else "success",
                    "tool_name": tool_name,
                    "result": result.model_dump(
                        mode="json",
                        exclude_none=True,
                    ),
                }

    except Exception as e:
        print("GitHub MCP error:")
        traceback.print_exception(type(e), e, e.__traceback__)

        return {
            "status": "error",
            "error_type": type(e).__name__,
            "error": str(e),
        }



mcp_tools = [
   get_github_mcp_toolset()
    # Example: get_github_mcp_toolset_from_config()
]

deferred_mcp_tools = [
   search_github_tools,
   call_github_tool,
   get_github_mcp_toolset_deferred()
]
