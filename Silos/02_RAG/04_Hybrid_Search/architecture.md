# Architecture: Hybrid Search (Vector + BM25)

```
[ User Query ] ──┬──► [ Dense Vector Search ] ──┐
                 └──► [ Sparse BM25 Keyword ] ──┴──► [ Reciprocal Rank Fusion (RRF) ] ──► [ Winner ]
```

```mermaid
graph TD
    A[Query] --> B[Dense Embeddings]
    A --> C[Sparse BM25]
    B --> D[Fusion Ranker: RRF]
    C --> D
    D --> E[Final Consolidated Context]
```
