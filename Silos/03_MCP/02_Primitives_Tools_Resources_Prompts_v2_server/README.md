# MCP v2 Server — Enterprise Primitives

Standalone MCP Server project running over stdio (with support for SSE and Streamable HTTP).

## Structure
```
server/
├── .python-version
├── pyproject.toml
├── README.md
├── oneliner.md
└── src/
    ├── main.py                     # Server daemon entrypoint (stdio)
    └── mcp_server_v2/
        ├── instance.py             # Central MCPServer instance & metadata
        ├── __init__.py             # Aggregate exports
        ├── tools/
        │   └── __init__.py         # @mcp.tool() and mcp.add_tool()
        ├── resources/
        │   └── __init__.py         # @mcp.resource()
        ├── prompts/
        │   └── __init__.py         # @mcp.prompt()
        ├── completions/
        │   └── __init__.py         # @mcp.completion()
        └── routes/
            └── __init__.py         # @mcp.custom_route()
```

## Running the Server
```powershell
uv sync
uv run start
```

## Server-Side APIs by Folder

### 1. `instance.py` (Server Initialization & Metadata)
- `MCPServer(name, instructions=..., website_url=...)` — Initializes server instance and configuration.

### 2. `tools/`
- `@mcp.tool()` — `calculate_order_total` *(triggered from client)*
- `mcp.add_tool(fn)` / `mcp.remove_tool(name)` — `ping_server` programmatic registration.

### 3. `resources/`
- `@mcp.resource("config://app/settings")` — `get_app_settings` *(triggered from client)*
- `@mcp.resource("schema://database/{table_name}")` — `get_table_schema` *(triggered from client)*
- `mcp.add_resource(res)` — Programmatic resource registration.

### 4. `prompts/`
- `@mcp.prompt()` — `triage_customer_ticket` *(triggered from client)*
- `mcp.add_prompt(p)` / `mcp.remove_prompt(name)` — Programmatic prompt management.

### 5. `completions/`
- `@mcp.completion()` — `handle_completion` *(triggered from client)*

### 6. `routes/`
- `@mcp.custom_route("/health", methods=["GET"])` — `health_check` endpoint for HTTP/SSE transports.

### 7. Transports & Execution
- `mcp.run(transport=...)` — Synchronous runner.
- `mcp.run_stdio_async()` — Async stdio runner (used with `anyio.run`).
- `mcp.sse_app()` / `mcp.streamable_http_app()` — Starlette ASGI applications.
