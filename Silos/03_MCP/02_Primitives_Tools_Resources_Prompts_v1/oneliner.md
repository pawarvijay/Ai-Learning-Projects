# MCP Primitives API Reference — One-Liners

Complete one-liner reference and progress tracker for all APIs and protocol methods used in this project (`02_Primitives_Tools_Resources_Prompts`).

> **Legend:**
> - Replace ❌ with ✅ when you have mastered an item!
> - ❌ = Not yet practiced / understood
> - ✅ = Mastered & verified

---

## 🛠️ 1. FastMCP Server Decorators & Methods (`server.py`)

- ✅ `FastMCP("ServerName")` — Instantiates an official MCP server with automatic JSON-RPC protocol handling.
- ✅ `@mcp.tool()` — Decorates a Python function as an executable action callable by LLMs with automatic Pydantic schema validation.
- ✅ `@mcp.resource("config://app/settings")` — Registers a static read-only data source accessible by the client/LLM via URI scheme.
- ✅ `@mcp.resource("schema://database/{table_name}")` — Registers a dynamic parameterized resource template using URI path parameters.
- ✅ `@mcp.prompt()` — Registers a standardized, reusable prompt template that accepts arguments and compiles messages for LLMs.
- ❌ `mcp.run_stdio_async()` — Runs the FastMCP server event loop over standard I/O (stdin/stdout) child process transport.

---

## 📡 2. Wire Protocol JSON-RPC Methods (Over-The-Wire Contract)

- ❌ `initialize` — Handshake request negotiating protocol version, server identity, and capability flags.
- ❌ `notifications/initialized` — Client notification signaling that handshake is complete and server is ready for calls.
- ❌ `tools/list` — Wire method returning all registered server tools along with their input argument schemas.
- ❌ `tools/call` — Wire method executing a specific tool by name with arguments dict and returning result content.
- ❌ `resources/list` — Wire method discovering all static read-only resource URIs hosted by the server.
- ❌ `resources/read` — Wire method fetching text or binary contents of a specific resource matching a URI string.
- ❌ `prompts/list` — Wire method listing all server-hosted prompt templates and their parameter requirements.
- ❌ `prompts/get` — Wire method compiling a prompt template with provided argument values into LLM-ready messages.

---

## 💻 3. Client SDK APIs (`client.py`)

- ❌ `StdioServerParameters(command, args, env)` — Configures executable path and arguments to spawn the local MCP server daemon.
- ❌ `stdio_client(server_params)` — Asynchronous context manager establishing stdin/stdout pipe connection to server process.
- ❌ `ClientSession(read, write)` — High-level protocol session managing message serialization and request-response IDs.
- ❌ `session.initialize()` — Sends the handshake request to the server and verifies capability responses.
- ❌ `session.list_tools()` — Client call returning `ListToolsResult` containing all discoverable server tools.
- ❌ `session.call_tool(name, arguments)` — Client call executing a tool on the server and returning `CallToolResult`.
- ❌ `session.list_resources()` — Client call returning `ListResourcesResult` with available resource URIs.
- ❌ `session.read_resource(uri)` — Client call retrieving text/metadata contents for a target URI.
- ❌ `session.list_prompts()` — Client call returning `ListPromptsResult` with all available prompt templates.
- ❌ `session.get_prompt(name, arguments)` — Client call evaluating and compiling prompt template with given arguments.
