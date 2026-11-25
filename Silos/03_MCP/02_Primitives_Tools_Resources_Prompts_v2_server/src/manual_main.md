# MCP Python SDK v2 — Core Architecture Cheat Sheet

## The 3 Rules That Matter Most

1. **Default to `mcp.run()`** — It is the official v2 entry point and automatically runs `anyio.run(mcp.run_stdio_async)` under the hood.
2. **Never call `mcp.run()` or `anyio.run()` inside an `async def` function** — Use `await mcp.run_stdio_async()` instead to avoid crashing the active event loop.
3. **Use `@mcp.tool()` for the AI and `@mcp.custom_route()` for HTTP systems** — Tools consume LLM context tokens, while custom routes handle `/health`, webhooks, and OAuth over HTTP with zero token overhead.s

------

### When to Use vs Skip
#### mcp.run("sse") / mcp.run("streamable-http")

| Scenario | What to Use | Do you need `mcp.sse_app()` / `mcp.streamable_http_app()`? |
| :--- | :--- | :---: |
| **Standard Standalone Server** (Most common) | `mcp.run("sse")` or `mcp.run("streamable-http")` | **NO** (Skip it) |
| **CLI / Local Process** (Desktop AI apps) | `mcp.run("stdio")` | **NO** (Skip it) |
| **Existing Web App** (Mounting MCP inside an existing FastAPI / Starlette backend alongside your own REST APIs) | `app.mount("/mcp", mcp.sse_app())` | **YES** |

---

### Flat Recommendation
**Skip it for now.** 

Use `mcp.run()` directly unless you are embedding MCP into a pre-existing enterprise FastAPI application.