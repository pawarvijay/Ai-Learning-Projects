# MCP SDK: `@mcp.tool()` vs `@mcp.custom_route("/path")`

`@mcp.custom_route()` exposes standard HTTP endpoints (such as REST APIs, webhooks, or health checks) for external systems and browsers, whereas `@mcp.tool()` exposes JSON-RPC functions strictly for the AI model (LLM) to call.

## Feature Comparison

| Feature | `@mcp.tool()` | `@mcp.custom_route("/path")` |
| :--- | :--- | :--- |
| **Who calls it?** | The **LLM / AI Agent** during reasoning. | **External software** (browsers, AWS/Kubernetes, Stripe, frontend apps). |
| **Protocol** | MCP (JSON-RPC over `stdio` or SSE/Streamable HTTP). | Standard HTTP (`GET`, `POST`, etc. via Starlette). |
| **Transport Compatibility** | Works on **all transports** (`stdio`, SSE, Streamable HTTP). | **HTTP only.** Won't work or be accessible if your server runs purely over `stdio`. |
| **Visible to the AI?** | **Yes**—sent in the model's system prompt/tool list. | **No**—completely hidden from the LLM (uses 0 context tokens). |
| **Data Format & Streaming** | Strictly structured MCP JSON-RPC (`CallToolResult`, JSON, Text/Image content blocks). | Any standard HTTP payload: binary streams, HTML, raw file downloads, webhook bytes, redirects (`302`). |
| **Authentication & Middleware** | Governed by MCP client session & connection handshake. | Standard Starlette/FastAPI HTTP middleware (CORS, Bearer tokens, IP whitelisting, cookies). |
| **Execution Lifecycle** | MCP Client / LLM controls when, how, and in what order it is invoked. | Independent of the AI session—can trigger even before or after an AI session exists. |
| **Main Use Cases** | Database queries, running code, sending emails, agent actions. | `/health` checks, OAuth callbacks, webhooks, file uploads, admin UIs. |

## Why Use `@mcp.custom_route()` in Real Applications

* **Infrastructure Health Checks:** Cloud platforms (Docker, Kubernetes, Render, AWS) ping `GET /health` to verify your server is alive without initializing an MCP session.
* **Webhooks & OAuth Callbacks:** Third-party services (like Stripe, GitHub, or Slack) require standard HTTP URLs to push events or redirect users back to your server.
* **Saving LLM Context Tokens:** Every `@mcp.tool()` is injected into the LLM's context window, whereas custom HTTP routes consume zero context tokens.
* **Single-Port Deployment:** Lets you serve both MCP endpoints and standard HTTP routes from the same server process and port without running a separate web server.
