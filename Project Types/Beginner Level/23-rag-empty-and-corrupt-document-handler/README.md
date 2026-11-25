# RAG Empty, Scanned & Corrupt Document Resilience

## 📌 Project Overview
**Title:** RAG Empty, Scanned & Corrupt Document Resilience  
**Industry Category:** Enterprise document processing systems dealing with messy real-world files.  

### 📝 Description
Robust document ingestion pipeline that handles scanned PDFs (no text layer), corrupted files, empty documents, password locks, and non-English encodings.

---

## 💼 Enterprise & Industry Use Case
Enterprise document processing systems dealing with messy real-world files.

---

## 🎯 Interview Skills Tested
File validation, OCR fallback (pytesseract/pdf2image), corrupt file quarantining, exception isolation.

---

## 📦 Required Packages & Libraries
- `pypdf` (Standard text extraction)
- `pdf2image` / `pytesseract` (Fallback OCR for scanned image PDFs)
- `filetype` (MIME-type binary validation and extension verification)
- `langchain-core` (Document metadata normalization)

---

## ⚠️ Real-World Edge Cases & Failure Modes
- **Critical Failure Mode:** Production outages, runaway token bills, and prompt injection exploits.
- **Defensive Mechanism:** Built specifically to catch, isolate, and mitigate failure modes before they reach core business logic.

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
+--------------------+       +----------------------+       +--------------------+
| Messy / Scanned /  | ----> | Defensive Document   | ----> | Validated Text     |
| Corrupt Files      |       | Ingestion Pipeline   |       | or Quarantined Log |
+--------------------+       +----------------------+       +--------------------+
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
[ Uploaded File ] ──► [ Magic-Byte & MIME Validator ]
                                    │
                                    ├── (Corrupted / Password-Locked) ──► [ Quarantine Folder + Error Log ]
                                    │
                                    ▼ (Valid PDF)
                         [ Standard PyPDF Text Extract ]
                                    │
                        ┌───────────┴───────────┐
                        ▼ (Extracted Text > 50 chars)  ▼ (Empty / Scanned Image)
                [ Clean Text Chunks ]           [ Fallback OCR Engine (Tesseract) ]
                        │                               │
                        └───────────────┬───────────────┘
                                        ▼
                            [ ChromaDB Vector Index ]
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
1. filetype.guess(file_bytes) validates actual file signature matches claimed .pdf extension
2. Attempt PyPDF read; catch PdfReadError, FileNotDecryptedError -> isolate to quarantine/ with status code
3. If extracted character count < 50: flag as scanned image
4. Trigger pdf2image.convert_from_bytes() -> run pytesseract.image_to_string()
5. Strip unprintable/corrupt unicode surrogate characters
6. Pass cleanly extracted, verified text into standard RAG text splitters
```
