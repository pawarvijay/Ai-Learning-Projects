from starlette.requests import Request
from starlette.responses import JSONResponse
from mcp_server_v2.instance import mcp

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    """Health check endpoint for HTTP-based MCP transports."""
    return JSONResponse({"status": "ok", "server": mcp.name})
