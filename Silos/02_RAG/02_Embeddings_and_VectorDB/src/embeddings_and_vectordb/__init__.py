import math

def mock_embed(text: str):
    # Deterministic 4-dim mock vector for demo
    words = text.lower().split()
    return [len(words), len(text) % 10, 1.0 if 'rag' in text.lower() else 0.0, 1.0]

def cosine(v1, v2):
    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))
    return dot / (mag1 * mag2) if mag1 and mag2 else 0

def main():
    docs = [
        "RAG models fetch external data.",
        "Node.js runs on V8 javascript engine."
    ]
    vectors = [mock_embed(d) for d in docs]
    query = "How does RAG work?"
    q_vec = mock_embed(query)
    
    scores = [cosine(q_vec, v) for v in vectors]
    best_idx = scores.index(max(scores))
    print(f"Best match (score {scores[best_idx]:.2f}): {docs[best_idx]}")

if __name__ == "__main__":
    main()
