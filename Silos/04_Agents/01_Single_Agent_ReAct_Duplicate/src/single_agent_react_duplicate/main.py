import asyncio
from .tools import load_mcp_tools
from .graph import build_react_agent


async def run_agent():
    print("=" * 65)
    print(" PATTERN: 2. REACT TOOL LOOP (SINGLE-AGENT + MCP)")
    print(" Flow: START -> Agent <-> ToolNode(MCP) -> END")
    print("=" * 65)

    tools = await load_mcp_tools()
    agent = build_react_agent(tools)
    query = "Calculate order total for 2 items of SKU 'ABC' at $125 each with discount code SAVE15."
    print(f"User Query: {query}\n")

    res = await agent.ainvoke({"messages": [("user", query)]})
    for msg in res["messages"]:
        if getattr(msg, "tool_calls", None):
            print(f"[Tool Call]: {msg.tool_calls[0]['name']} -> {msg.tool_calls[0]['args']}")
        elif msg.type == "tool":
            print(f"[Tool Result]: {msg.content}")
        elif msg.type == "ai" and msg.content:
            text = getattr(msg, "text", msg.content)
            print(f"[Agent Response]: {text}")

    print("=" * 65)


def main():
    asyncio.run(run_agent())


if __name__ == "__main__":
    main()
