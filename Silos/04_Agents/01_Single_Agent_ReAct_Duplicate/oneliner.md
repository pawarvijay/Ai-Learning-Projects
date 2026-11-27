# Single-Agent ReAct + MCP API Reference

| Status & Link | Code | API Type | Safety / Status | Description |
| :---: | :--- | :--- | :--- | :------------------------------------------------------------------------------------------------------------------- |
| &check; [link](src/single_agent_react_duplicate/state.py#L5-L8) | `class AgentState(TypedDict): messages: Annotated[list, add_messages]` | LangGraph | Active | Defines shared agent state; `add_messages` appends new messages instead of overwriting history. |
| &check; [link](src/single_agent_react_duplicate/tools.py#L11-L14) | `MultiServerMCPClient(MCP_SERVERS).get_tools()` | LangChain MCP Adapters | Active | Connects to the running MCP server (`streamable_http`) and converts its tools into LangChain tools. |
| &check; [link](src/single_agent_react_duplicate/model.py#L17-L23) | `ChatGoogleGenerativeAI(...).bind_tools(tools)` | LangChain Google | Active | Attaches MCP tool schemas to the Gemini model so it can request tool calls. |
| &check; [link](src/single_agent_react_duplicate/model.py#L26) | `models[0].with_fallbacks(models[1:])` | LangChain Core | Active | Automatically retries with backup models if the primary model fails or hits rate limits. |
| &check; [link](src/single_agent_react_duplicate/graph.py#L24) | `workflow = StateGraph(AgentState)` | LangGraph | Active | Creates the state-machine graph that passes `AgentState` between nodes. |
| &check; [link](src/single_agent_react_duplicate/graph.py#L25-L26) | `workflow.add_node("agent", call_model)` / `ToolNode(tools)` | LangGraph | Active | Registers the LLM reasoning node and prebuilt `ToolNode` that executes requested MCP tools. |
| &check; [link](src/single_agent_react_duplicate/graph.py#L28-L30) | `add_edge(START, "agent")` / `add_conditional_edges(...)` | LangGraph | Active | Wires the ReAct loop: `START -> agent`, then branches to `tools` or `END`, and loops `tools -> agent`. |
| &check; [link](src/single_agent_react_duplicate/graph.py#L31) | `workflow.compile()` | LangGraph | Active | Compiles the graph definition into a runnable agent. |
| &check; [link](src/single_agent_react_duplicate/main.py#L18) | `await agent.ainvoke({"messages": [("user", query)]})` | LangGraph | Active | Runs the compiled agent asynchronously from initial user message to final response. |
