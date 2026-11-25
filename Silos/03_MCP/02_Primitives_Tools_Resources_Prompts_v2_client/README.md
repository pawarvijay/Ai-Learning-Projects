# MCP v2 Client — Enterprise Orchestrator

Standalone MCP Client project that connects to an MCP Server using `stdio_client` and `ClientSession`.

## Structure
```
client/
├── .python-version
├── pyproject.toml
└── src/
    ├── main.py             # Client runner (discovers server, initializes, runs workflows)
    └── mcp_client_v2/
        └── __init__.py     # run_client export
```

## Running the Client
```powershell
uv sync
uv run start
```

## Capabilities Demonstrated
1. **Initialize**: Protocol version handshake and server capabilities negotiation.
2. **Tools**: Discovering tools (`session.list_tools()`) and invoking them (`session.call_tool()`).
3. **Resources**: Reading configuration data (`session.read_resource()`).
4. **Prompts**: Fetching structured prompt templates (`session.get_prompt()`).
