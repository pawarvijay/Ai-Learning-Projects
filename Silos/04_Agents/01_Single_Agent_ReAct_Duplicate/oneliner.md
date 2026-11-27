# Single-Agent ReAct API Reference

| Status & Link | Code | API Type | Safety / Status | Description |
| :---: | :--- | :--- | :--- | :------------------------------------------------------------------------------------------------------------------- |
| &check; [link](src/single_agent_react_duplicate/state.py#L5-L8) | `class AgentState(TypedDict): messages: Annotated[list, add_messages]` | LangGraph | Active | Defines shared agent state; `add_messages` appends new messages instead of overwriting history. |
| &check; [link](src/single_agent_react_duplicate/tools.py#L4-L8) | `@tool` | LangChain Core | Active | Converts a Python function and its docstring into a callable tool schema for the LLM. |
| &check; [link](src/single_agent_react_duplicate/model.py#L20-L26) | `ChatGoogleGenerativeAI(...).bind_tools(tools)` | LangChain Google | Active | Attaches tool schemas to the Gemini model so it can request tool calls. |
| &check; [link](src/single_agent_react_duplicate/model.py#L29) | `models[0].with_fallbacks(models[1:])` | LangChain Core | Active | Automatically retries with backup models if the primary model fails or hits rate limits. |
| &check; [link](src/single_agent_react_duplicate/graph.py#L24) | `workflow = StateGraph(AgentState)` | LangGraph | Active | Creates the state-machine graph that passes `AgentState` between nodes. |
| &check; [link](src/single_agent_react_duplicate/graph.py#L25-L26) | `workflow.add_node("agent", call_model)` / `ToolNode(tools)` | LangGraph | Active | Registers the LLM reasoning node and prebuilt `ToolNode` that executes requested tools. |
| &check; [link](src/single_agent_react_duplicate/graph.py#L28-L30) | `add_edge(START, "agent")` / `add_conditional_edges(...)` | LangGraph | Active | Wires the ReAct loop: `START -> agent`, then branches to `tools` or `END`, and loops `tools -> agent`. |
| &check; [link](src/single_agent_react_duplicate/graph.py#L31) | `workflow.compile()` | LangGraph | Active | Compiles the graph definition into a runnable agent. |
| &check; [link](src/single_agent_react_duplicate/main.py#L14) | `agent.invoke({"messages": [("user", query)]})` | LangGraph | Active | Runs the compiled agent synchronously from initial user message to final response. |
