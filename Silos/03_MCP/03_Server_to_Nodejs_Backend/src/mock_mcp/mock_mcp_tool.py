def mock_mcp_tool_execute(tool_name: str, args: dict):
    # Simulates MCP server delegating to Node.js microservice
    print(f"[MCP] Calling Node.js backend: /api/{tool_name} with {args}")
    # Simulated Node.js response
    return {"status": 200, "data": {"discounted_price": args["price"] * 0.8}}