def main():
    candidates = [
        {"id": 1, "text": "LangGraph manages state machines and cyclic graphs."},
        {"id": 2, "text": "RAG retrieves relevant chunks before generation."},
        {"id": 3, "text": "Python 3.14 features faster runtime execution."}
    ]
    query = "state machine workflows"
    # Stage 2: Rerank based on exact term overlap
    scored = []
    for c in candidates:
        match_count = sum(1 for w in query.split() if w.lower() in c['text'].lower())
        scored.append((match_count, c['text']))
    scored.sort(key=lambda x: x[0], reverse=True)
    print(f"Top Reranked Context: {scored[0][1]}")

if __name__ == "__main__":
    main()
