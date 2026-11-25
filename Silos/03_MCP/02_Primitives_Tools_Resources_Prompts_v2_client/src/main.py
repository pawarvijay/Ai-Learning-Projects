import asyncio
from mcp_client_v2 import (
    connect_streamable_http,
    ping_server,
    set_server_logging,
    fetch_tools,
    execute_tool,
    fetch_resources,
    fetch_resource_templates,
    read_resource_content,
    subscribe_to_resource,
    unsubscribe_from_resource,
    fetch_prompts,
    render_prompt,
)

SERVER_URL = "http://127.0.0.1:6162/mcp"


async def run_client():
    print("=" * 70)
    print(" [CLIENT] Standalone MCP v2 Client Connecting via Streamable HTTP")
    print(f" [CLIENT] Target Server: {SERVER_URL}")
    print("=" * 70)

    async with connect_streamable_http(SERVER_URL) as session:
        print("✔ Handshake successful with remote MCP v2 Server!\n")

        # 0. System APIs
        print("--- 0. System Operations ---")
        await ping_server(session)
        print("✔ send_ping: Server is healthy and responding.")
        logging_supported = await set_server_logging(session, "info")
        if logging_supported:
            print("✔ set_logging_level: Logging set to 'info'.\n")
        else:
            print("ℹ set_logging_level: Server does not expose logging capability (skipped).\n")

        # 1. Tools
        print("--- 1. Calling Server Tools ---")
        tools_result = await fetch_tools(session)
        print(f"Server Tools: {[t.name for t in tools_result.tools]}")

        res = await execute_tool(
            session,
            name="calculate_order_total",
            arguments={
                "items": [{"sku": "DEV-KIT-01", "quantity": 2, "unit_price": 150.0}],
                "discount_code": "SAVE15",
            },
        )
        print(f"Result from Server:\n{res.content[0].text}\n")

        # 2. Resources & Resource Templates
        print("--- 2. Reading Server Resources & Templates ---")
        resources = await fetch_resources(session)
        print(f"Static Resources: {[str(r.uri) for r in resources.resources]}")

        templates = await fetch_resource_templates(session)
        print(f"Resource Templates: {[t.uri_template for t in templates.resource_templates]}")

        cfg = await read_resource_content(session, "config://app/settings")
        print(f"Read 'config://app/settings':\n{cfg.contents[0].text}\n")

        # Dynamic template resource read
        dyn = await read_resource_content(session, "schema://database/customers")
        print(f"Read 'schema://database/customers':\n{dyn.contents[0].text}\n")

        # 3. Prompts
        print("--- 3. Fetching Server Prompts ---")
        prompts = await fetch_prompts(session)
        print(f"Available Prompts: {[p.name for p in prompts.prompts]}")

        prompt = await render_prompt(
            session,
            name="triage_customer_ticket",
            arguments={
                "ticket_body": "Payment gateway timeout on checkout",
                "customer_tier": "Enterprise",
            },
        )
        print(f"Compiled Prompt:\n{prompt.messages[0].content.text}")

    print("\n" + "=" * 70)
    print("✔ Standalone Client run completed successfully over Streamable HTTP!")
    print("=" * 70)


def main():
    asyncio.run(run_client())


if __name__ == "__main__":
    main()
