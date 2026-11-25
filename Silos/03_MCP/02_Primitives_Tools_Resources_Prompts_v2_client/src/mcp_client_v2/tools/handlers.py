"""Tool client operations."""

from typing import Any
from mcp import ClientSession
from mcp.types import CallToolResult, ListToolsResult


async def fetch_tools(session: ClientSession) -> ListToolsResult:
    """Discovers all available tools exposed by the server."""
    return await session.list_tools()


async def execute_tool(session: ClientSession, name: str, arguments: dict[str, Any] | None = None) -> CallToolResult:
    """Invokes a specific tool on the server with arguments."""
    return await session.call_tool(name=name, arguments=arguments or {})
