
## Architecture Core Principle
> "Every box in this diagram is just a standard function call or network request. You can call any of them directly whenever you don't need the middleman."


Agent is not a required "middleman" layer. An Agent is only introduced when you want an LLM to autonomously decide which tool to call or when to stop looping.
LangChain / LangGraph are not walled gardens—they are just orchestrators and helper libraries.
Any node, script, or function can call Node.js APIs, RAG databases, MCP servers, and LLM endpoints directly.

