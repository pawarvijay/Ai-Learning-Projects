import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_client_diagnostics():
    """Spawns this server over stdio and queries tools via official ClientSession."""
    print("=" * 60)
    print(" Official MCP stdio Client - Diagnostic Test")
    print("=" * 60)

    # Path to server execution via python module
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "transports_stdio_and_sse.cli_server"],
        env=dict(os.environ)
    )

    print("[Client] Connecting to MCP server over stdio transport...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. Initialize protocol handshake
            await session.initialize()
            print("[Client] Handshake established successfully.")

            # 2. List tools
            tools_result = await session.list_tools()
            tool_names = [t.name for t in tools_result.tools]
            print(f"[Client] Discovered Tools: {tool_names}")

            # 3. Call echo tool
            print("[Client] Invoking 'echo' tool...")
            echo_res = await session.call_tool("echo", arguments={"message": "Hello Model Context Protocol!"})
            print(f"[Client] Tool Response: {echo_res.content[0].text}")

            # 4. Call system_ping tool
            print("[Client] Invoking 'system_ping' tool...")
            ping_res = await session.call_tool("system_ping", arguments={})
            print(f"[Client] Ping Response: {ping_res.content[0].text}")

    print("=" * 60)
    print("✔ MCP stdio Transport roundtrip verified successfully!")
    print("=" * 60)
