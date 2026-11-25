# MCP v2 Server API Reference

| Status & Link | Code | API Type | Safety / Status | Description |
| :---: | :--- | :--- | :--- | :------------------------------------------------------------------------------------------------------------------- |
| &check; [link](src/mcp_server_v2/instance.py#L1) | `from mcp.server import MCPServer` | Python SDK | Active | Imports official v2 high-level server class. |
| &check; [link](src/mcp_server_v2/instance.py#L4-L8) | `mcp = MCPServer("Name"` | Python SDK | Active | Instantiates server with metadata adhering to MCP protocol. |
| &check; [link](src/mcp_server_v2/tools/handlers.py#L10) | `@mcp.tool()` | Official MCP Spec | Active | Registers executable tool *(triggered from client)*. |
| &check; [link](src/mcp_server_v2/resources/handlers.py#L3) | `@mcp.resource("config://app/s")` | Official MCP Spec | Active | Registers static read-only URI data source *(triggered from client)*. |
| &check; [link](src/mcp_server_v2/resources/handlers.py#L8) | `@mcp.resource("schema://da")` | Official MCP Spec | Active | Registers dynamic parameterized resource *(triggered from client)*. |
| &check; [link](src/mcp_server_v2/prompts/handlers.py#L3) | `@mcp.prompt()` | Official MCP Spec | Active | Registers reusable prompt template *(triggered from client)*. |
| [link](src/mcp_server_v2/completions/handlers.py#L4) | `@mcp.completion()` | Official MCP Spec | Active | Registers autocomplete handler for arguments *(triggered from client)*. |
| &check; [link](src/mcp_server_v2/routes/handlers.py#L5) | `@mcp.custom_route("/health",` | Python SDK | Active | Registers standard HTTP route (Starlette) for health checks or webhooks. |
| &check; [link](src/mcp_server_v2/tools/handlers.py#L31) | `mcp.add_tool(fn)` / `mcp.remove_tool(name)` | Python SDK | Active | Programmatically adds or removes a tool at runtime. |
| &check; - | `mcp.add_resource(res)` / `mcp.add_prompt(p)` / `mcp.remove_prompt(name)` | Python SDK | Active | Programmatically manages resources and prompts at runtime. |
| - | `mcp.sse_app()` / `mcp.streamable_http_app()` | Python SDK | Active (`sse_app` legacy) | Returns Starlette ASGI app for mounting into custom web servers (`streamable_http_app` preferred for HTTP). |
| &check; [link](src/manual_main.md) | `mcp.run()` | Python SDK *(Recommended)* | Active | Synchronous entry point; calls `anyio.run(...)` under the hood. |
| &check; [link](src/manual_main.md) | `anyio.run(mcp.run_stdio_async)` | AnyIO / Lower-level | Active | Manual async runner for custom event loop or lifespan configuration. |
