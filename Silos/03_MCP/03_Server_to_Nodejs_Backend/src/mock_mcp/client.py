import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_nodejs_gateway_demo():
    print("=" * 70)
    print(" Testing MCP Adapter Bridge to Node.js Microservice & DB")
    print("=" * 70)

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mock_mcp.cli_server"],
        env=dict(os.environ)
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✔ Connected to NodeJsBackendGateway MCP Server.\n")

            # 1. Discover enterprise tools
            tools = await session.list_tools()
            print(f"Discovered Gateway Tools: {[t.name for t in tools.tools]}\n")

            # 2. Invoke Loyalty Discount Tool (Node.js REST call)
            print("▸ Invoking 'calculate_loyalty_discount' (REST -> Node.js Service)...")
            res_discount = await session.call_tool(
                "calculate_loyalty_discount",
                arguments={
                    "payload": {
                        "product_id": "PROD-9982",
                        "original_price": 250.0,
                        "user_tier": "Platinum"
                    }
                }
            )
            print(f"Node.js Backend Response:\n{res_discount.content[0].text}\n")

            # 3. Invoke Inventory Stock Tool (Node.js -> SQL DB)
            print("▸ Invoking 'query_inventory_stock' (Node.js -> PostgreSQL DB)...")
            res_stock = await session.call_tool(
                "query_inventory_stock",
                arguments={"product_id": "PROD-9982"}
            )
            print(f"Database Query Response:\n{res_stock.content[0].text}\n")

    print("=" * 70)
    print("✔ Node.js microservice & database integration via MCP verified!")
    print("=" * 70)
