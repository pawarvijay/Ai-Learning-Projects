from .graph import build_react_agent


def main():
    """Runs the single-agent ReAct tool-calling loop on a sample query."""
    print("=" * 65)
    print(" PATTERN: 2. REACT TOOL LOOP (SINGLE-AGENT)")
    print(" Flow: START -> Agent <-> ToolNode -> END")
    print("=" * 65)

    agent = build_react_agent()
    query = "Calculate a 20% discount on a $250 item."
    print(f"User Query: {query}\n")

    res = agent.invoke({"messages": [("user", query)]})
    for msg in res["messages"]:
        if getattr(msg, "tool_calls", None):
            print(f"[Tool Call]: {msg.tool_calls[0]['name']} -> {msg.tool_calls[0]['args']}")
        elif msg.type == "tool":
            print(f"[Tool Result]: {msg.content}")
        elif msg.type == "ai" and msg.content:
            text = getattr(msg, "text", msg.content)
            print(f"[Agent Response]: {text}")

    print("=" * 65)


if __name__ == "__main__":
    main()
