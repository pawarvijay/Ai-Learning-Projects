import asyncio
import sys
from mcp.server.fastmcp import FastMCP

# Create a FastMCP server instance supporting both stdio and SSE
mcp_server = FastMCP(
    "TransportDemoServer",
    dependencies=["pydantic"]
)

@mcp_server.tool()
def echo(message: str) -> str:
    """Echoes back a string payload to test JSON-RPC roundtrip."""
    return f"Echo from FastMCP: {message}"

@mcp_server.tool()
def system_ping() -> dict:
    """Returns low-level server diagnostic information."""
    return {
        "status": "healthy",
        "transport_ready": True,
        "python_version": sys.version.split()[0]
    }

# async def run_stdio():
#     """Runs the server over stdio (standard input/output child process)."""
#     print("[MCP] Starting FastMCP Server on stdio transport...", file=sys.stderr)
#     await mcp_server.run_stdio_async()

async def run_sse(port: int = 8000):
    """Runs the server over HTTP with Server-Sent Events (SSE)."""
    print(f"[MCP] Starting FastMCP Server on HTTP-SSE at port {port}...", file=sys.stderr)
    await mcp_server.run_sse_async(port=port)
