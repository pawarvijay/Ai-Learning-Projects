# Silos Deep-Dive Curriculum

This directory contains focused, isolated deep-dives into core AI engineering building blocks:

## 1. LangChain (`01_LangChain/`)
- `01_Prompts_and_Templates`: ChatPromptTemplate, FewShot, partial variables.
- `02_LCEL_Pipelines`: LangChain Expression Language pipe syntax (`prompt | model | parser`).
- `03_Structured_Output_Parsers`: Pydantic, JSON output validation, and auto-fixing parsers.
- `04_Memory_and_History`: Conversational buffers and runnable history.

## 2. RAG (`02_RAG/`)
- `01_Chunking_and_Splitting`: Character, recursive, semantic, and markdown chunking strategies.
- `02_Embeddings_and_VectorDB`: Generating dense vector representations and vector store indexing.
- `03_Retrieval_and_Reranking`: Top-K similarity, MMR (Maximal Marginal Relevance), and Cohere/cross-encoder rerankers.
- `04_Hybrid_Search`: Combining sparse keyword search (BM25) with dense vector search.

## 3. MCP (`03_MCP/`)
- `01_Transports_stdio_and_SSE`: Local child-process (stdio) vs. remote HTTP Server-Sent Events (SSE).
- `02_Primitives_Tools_Resources_Prompts`: Hands-on implementations of the 3 MCP primitives.
- `03_Server_to_Nodejs_Backend`: Wrapping Node.js REST services and SQL databases into standardized MCP tools.
