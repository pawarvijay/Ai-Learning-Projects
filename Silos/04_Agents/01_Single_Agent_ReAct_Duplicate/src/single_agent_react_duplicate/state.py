from typing import Annotated, TypedDict
from langgraph.graph import add_messages


class AgentState(TypedDict):
    """Shared graph state holding the conversation message history."""

    messages: Annotated[list, add_messages]
