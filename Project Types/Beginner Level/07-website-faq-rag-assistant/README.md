# Website FAQ RAG Assistant

## 📌 Project Overview
**Title:** Website FAQ RAG Assistant  
**Industry Category:** SaaS website conversion widget and 24/7 self-service customer support.  

### 📝 Description
Grounded Q&A assistant built over company FAQ URLs or documentation that provides verified customer support answers.

---

## 💼 Enterprise & Industry Use Case
SaaS website conversion widget and 24/7 self-service customer support.

---

## 🎯 Interview Skills Tested
HTML scraping, chunking, retrieval grounding, hallucination prevention.

---

## 📦 Required Packages & Libraries
- `beautifulsoup4` / `httpx` (Web scraping and HTML text extraction)
- `langchain-community` (WebBaseLoader / Document wrappers)
- `chromadb` (Embedded vector search store)
- `langchain-google-genai` (Gemini Flash Lite Q&A generator)

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+-----------------+       +---------------------+       +----------------------+
| Company Website | ----> | FAQ RAG Assistant   | ----> | Instant, Verified    |
| & User Question |       | (Grounded in Pages) |       | Customer Answers     |
+-----------------+       +---------------------+       +----------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ FAQ Webpages ] ──► [ BeautifulSoup Parser ] ──► [ Text Chunks ] ──► [ ChromaDB Store ]
                                                                                   │
[ User Inquiries ] ──────────────────────────────────────────────► [ Vector Retrieval ]
                                                                                   │
                                                                                   ▼
                                                                        [ Grounded Prompt ]
                                                                        (Strict: "Answer ONLY
                                                                         from context")
                                                                                   │
                                                                                   ▼
                                                                        [ Customer Response ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. httpx fetches HTML content from FAQ URL endpoints
2. BeautifulSoup strips <script>, <style>, <nav> tags, extracting clean article body
3. RecursiveCharacterTextSplitter generates overlapping chunks (chunk_size=400, overlap=50)
4. Chroma.from_documents() embeds chunks using GoogleGenerativeAIEmbeddings
5. Customer types inquiry: "How do I request a refund?"
6. retriever.invoke(query) fetches top 3 matching chunks
7. Prompt encloses retrieved text: "Answer using ONLY this text. If absent, say 'Please contact support.'"
8. Model generates clean, safe response with zero hallucination
```
