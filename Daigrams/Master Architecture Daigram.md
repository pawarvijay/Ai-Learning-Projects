```text
                [ User Request ]
                       |
                       v
    +-------------------------------------+
    |              LangGraph              |  <-- Orchestrator (Loops, State Machine)
    |   (Runs 1 Agent or a "Swarm")       |
    +-------------------------------------+
                       |
                       v
    +-------------------------------------+
    |                Agent                |  <-- Brain / Worker (Decides what to do)
    +-------------------------------------+
                       |
      +----------------+----------------+
      |                |                |
      v                v                v
+------------+   +------------+   +------------+
| LangChain  |   |    RAG     |   | MCP / Tool | <-- Tool Plug
| (Prompts & |   |(Reads PDFs |   |            |
| Glue Code) |   |& VectorDB) |   +------------+
+------------+   +------------+         |
      |                                 | (Calls API)
      v                                 v
+------------+                    +------------+
|    LLM     |                    |  Node.js   | <-- Your Service
|(GPT/Claude)|                    |  Service   |
+------------+                    +------------+
                                        |
                                        | (SQL Query)
                                        v
                                  +------------+
                                  | SQL Server | <-- Database
                                  +------------+
```
