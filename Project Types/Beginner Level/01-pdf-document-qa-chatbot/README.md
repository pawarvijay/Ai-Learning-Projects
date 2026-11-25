# PDF Document Q&A Chatbot

## 📌 Project Overview
**Title:** PDF Document Q&A Chatbot  
**Industry Category:** HR policy manuals, legal contract review, and internal company wiki search.  

### 📝 Description
Consumes user-uploaded PDF files, chunks and embeds the document content into a local vector store, and answers user queries with accurate source page citations.

---

## 💼 Enterprise & Industry Use Case
HR policy manuals, legal contract review, and internal company wiki search.

---

## 🎯 Interview Skills Tested
Document loading, recursive chunking, vector embeddings, similarity search, prompt grounding.

---

## 📦 Required Packages & Libraries
- `pypdf` / `pdfplumber` (Extract text and page metadata from PDF bytes)
- `langchain-text-splitters` (RecursiveCharacterTextSplitter for chunking)
- `langchain-google-genai` (Embeddings & Gemini Flash LLM generation)
- `chromadb` / `faiss-cpu` (Vector database for similarity search)
- `pydantic` (Data schemas for cited sources and answers)

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+-------------+       +-------------------+       +--------------------+
|  User PDF   | ----> | PDF Q&A Assistant | ----> | Accurate Answers   |
|  & Question |       |  (RAG Knowledge)  |       | with Source Pages  |
+-------------+       +-------------------+       +--------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ Uploaded PDF ] ──► [ PyPDF Parser ] ──► [ Text Chunks ] ──► [ ChromaDB Vector Store ]
                                                                             │
[ User Question ] ──────────────────────────────────────────► [ Similarity Search ]
                                                                             │ Context
                                                                             ▼
                                                                     [ Gemini LLM ]
                                                                             │
                                                                             ▼
                                                                     [ Answer + Citations ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. Client POSTs PDF bytes to /api/upload
2. pypdf.PdfReader iterates pages: extract_text() -> yields Document(page_content, metadata={"page": i})
3. RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents()
4. GoogleGenerativeAIEmbeddings(model="models/embedding-001").embed_documents(chunks)
5. Vector store upsert: Chroma.add_texts(ids, vectors, metadatas)
6. User query -> embeddings.embed_query(query) -> collection.query(top_k=3)
7. Format prompt: ChatPromptTemplate.from_template("Context: {context} \n\n Question: {question}")
8. gemini-3.5-flash-lite.invoke() -> returns JSON: {"answer": str, "citations": [page_numbers]}
```
