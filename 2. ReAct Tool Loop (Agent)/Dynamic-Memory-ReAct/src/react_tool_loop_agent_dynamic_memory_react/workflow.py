import os
from typing import TypedDict, Annotated
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


@tool
def lookup_weather(city: str) -> str:
    """Gets the current weather for a city."""
    return f"Weather in {city}: 22°C and Sunny"


tools = [lookup_weather]


def get_model():
    candidates = [
        os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite"),
        "gemini-3.1-flash-lite",
        "gemini-3.6-flash",
        "gemini-3.7-flash",
        "gemini-3.5-flash"
    ]
    models = [
        ChatGoogleGenerativeAI(
            model=m,
            temperature=0,
            timeout=20,
            max_retries=0,
            max_output_tokens=35
        ).bind_tools(tools)
        for m in candidates
    ]
    return models[0].with_fallbacks(models[1:])


model_with_tools = get_model()


def call_model(state: AgentState):
    return {"messages": [model_with_tools.invoke(state["messages"])]}


def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tools"
    return END


def build_memory_agent():
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools))

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    workflow.add_edge("tools", "agent")

    # In-memory persistence engine
    return workflow.compile(checkpointer=MemorySaver())


def main():
    print("=" * 65)
    print(" PATTERN: 2. REACT TOOL LOOP (DYNAMIC-MEMORY-REACT)")
    print(" Flow: Multi-Turn Conversation across Thread IDs with Checkpoint")
    print("=" * 65)

    agent = build_memory_agent()
    # Unique conversation session ID
    thread_1 = {"configurable": {"thread_id": "user-session-42"}}

    # Turn 1: User introduces facts
    print("\n--- Turn 1 (Thread user-session-42) ---")
    q1 = "Hi, my favorite city is Tokyo. What is the weather there?"
    print(f"User: {q1}")
    res1 = agent.invoke({"messages": [("user", q1)]}, config=thread_1)
    text1 = getattr(res1["messages"][-1], "text", res1["messages"][-1].content)
    print(f"Agent: {text1}\n")

    # Turn 2: User asks follow-up referencing past memory
    print("--- Turn 2 (Thread user-session-42: Context Recall) ---")
    q2 = "What city did I just ask about?"
    print(f"User: {q2}")
    res2 = agent.invoke({"messages": [("user", q2)]}, config=thread_1)
    text2 = getattr(res2["messages"][-1], "text", res2["messages"][-1].content)
    print(f"Agent: {text2}\n")

    # Turn 3: Separate Thread (Isolated Memory)
    thread_2 = {"configurable": {"thread_id": "user-session-99"}}
    print("--- Turn 3 (New Thread user-session-99: Isolated Session) ---")
    q3 = "Do you know my favorite city?"
    print(f"User: {q3}")
    res3 = agent.invoke({"messages": [("user", q3)]}, config=thread_2)
    text3 = getattr(res3["messages"][-1], "text", res3["messages"][-1].content)
    print(f"Agent: {text3}")

    print("=" * 65)


if __name__ == "__main__":
    main()
