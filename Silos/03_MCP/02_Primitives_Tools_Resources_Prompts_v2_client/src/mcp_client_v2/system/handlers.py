"""System & transport client operations."""

from contextlib import asynccontextmanager
from pathlib import Path
import os
from typing import AsyncGenerator
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.shared.exceptions import MCPError
from mcp.types import LoggingLevel


def create_stdio_parameters(server_dir: Path) -> StdioServerParameters:
    """Configures process parameters to spawn the standalone MCP v2 server."""
    # Strip parent virtual environment so child uv launches cleanly
    env = dict(os.environ)
    env.pop("VIRTUAL_ENV", None)
    return StdioServerParameters(
        command="uv",
        args=["run", "--directory", str(server_dir), "start"],
        env=env,
    )


@asynccontextmanager
async def connect_stdio(server_params: StdioServerParameters) -> AsyncGenerator[ClientSession, None]:
    """Asynchronous context manager establishing connection and managing ClientSession lifecycle."""
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session


async def ping_server(session: ClientSession) -> bool:
    """Sends ping request to verify server process is alive."""
    await session.send_ping()
    return True


async def set_server_logging(session: ClientSession, level: LoggingLevel = "info") -> bool:
    """Instructs the server which log levels to forward to client if server supports logging."""
    try:
        await session.set_logging_level(level)
        return True
    except MCPError:
        # Gracefully handle when server does not declare/support logging capability
        return False
