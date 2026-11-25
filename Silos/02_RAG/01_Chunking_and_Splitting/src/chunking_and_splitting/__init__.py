def split_text(text: str, chunk_size: int = 60, overlap: int = 15):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def main():
    doc = "Retrieval-Augmented Generation (RAG) optimizes LLM output by referencing an authoritative knowledge base outside of its training data before generating a response."
    chunks = split_text(doc)
    print(f"Total Chunks: {len(chunks)}")
    for i, ch in enumerate(chunks):
        print(f" Chunk {i+1}: {ch}")

if __name__ == "__main__":
    main()
