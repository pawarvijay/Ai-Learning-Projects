from langchain_mcp_adapters.client import MultiServerMCPClient

MCP_SERVERS = {
    "mcp_v2": {
        "transport": "streamable_http",
        "url": "http://127.0.0.1:6162/mcp",
    }
}


async def load_mcp_tools():
    client = MultiServerMCPClient(MCP_SERVERS)
    return await client.get_tools()
