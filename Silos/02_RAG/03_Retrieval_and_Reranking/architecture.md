# Architecture: Retrieval and Reranking

```
[ Query ] ──► [ Fast Dense Top-K Retrieval ] ──► [ Cross-Encoder Reranker ] ──► [ Refined Top-1 Document ]
```

```mermaid
graph LR
    A[Query] --> B[Top-5 Vector Search]
    B --> C[Re-Ranker Scoring Pass]
    C --> D[Top-1 High Precision Context]
```
