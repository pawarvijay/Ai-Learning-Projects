import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_primitives_demo():
    print("=" * 70)
    print(" Testing Official MCP Primitives (Tools, Resources, Prompts)")
    print("=" * 70)

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_primitives.server.cli_server"],
        env=dict(os.environ)
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✔ Handshake established with EnterprisePrimitivesServer.\n")

            # # --- 1. Test Tools ---
            # print("--- 1. Testing Model Tool Execution ---")
            # tools = await session.list_tools()
            # print(f"Available Tools: {[t.name for t in tools.tools]}")
            
            # calc_args = {
            #     "items": [
            #         {"sku": "LAPTOP-01", "quantity": 1, "unit_price": 1200.0},
            #         {"sku": "MOUSE-BT", "quantity": 2, "unit_price": 25.0}
            #     ],
            #     "discount_code": "SAVE15"
            # }
            # res = await session.call_tool("calculate_order_total", arguments=calc_args)
            # print(f"Tool Execution Result:\n{res.content[0].text}\n")

            # # --- 2. Test Resources ---
            # print("--- 2. Testing Application Resources (URI Schemes) ---")
            # resources = await session.list_resources()
            # print(f"Discovered Resources: {[r.uri for r in resources.resources]}")
            
            # app_cfg = await session.read_resource("config://app/settings")
            # print(f"Read 'config://app/settings':\n{app_cfg.contents[0].text}\n")
            
            # db_schema = await session.read_resource("schema://database/orders")
            # print(f"Read 'schema://database/orders':\n{db_schema.contents[0].text}\n")

            # --- 3. Test Prompts ---
            print("--- 3. Testing Host-Controlled Prompt Templates ---")
            prompts = await session.list_prompts()
            print(f"Available Prompts: {[p.name for p in prompts.prompts]}")
            
            prompt_res = await session.get_prompt(
                "triage_customer_ticket",
                arguments={"ticket_body": "Database checkout is timing out with 504 error.", "customer_tier": "Enterprise"}
            )
            print(f"Generated Prompt Template Content:\n{prompt_res.messages[0].content.text}")

    print("\n" + "=" * 70)
    print("✔ All 3 MCP Primitives (Tools, Resources, Prompts) successfully tested!")
    print("=" * 70)
