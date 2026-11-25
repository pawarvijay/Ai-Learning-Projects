from mcp.server import MCPServer

# Centralized MCPServer instance with metadata
mcp = MCPServer(
    "EnterprisePrimitivesV2Server",
    instructions="Enterprise MCP v2 server exposing tools, resources, prompts, completions, and custom HTTP routes.",
    website_url="https://modelcontextprotocol.io",
)
