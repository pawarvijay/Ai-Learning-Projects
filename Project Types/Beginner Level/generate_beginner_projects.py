import os
from pathlib import Path

base_dir = Path("D:/Ai Learning Projects/Project Types/Beginner Level")

projects = [
    {
        "id": "01-pdf-document-qa-chatbot",
        "title": "PDF Document Q&A Chatbot",
        "description": "Consumes user-uploaded PDF files, chunks and embeds the document content into a local vector store, and answers user queries with accurate source page citations.",
        "industry_use_case": "HR policy manuals, legal contract review, and internal company wiki search.",
        "skills_tested": "Document loading, recursive chunking, vector embeddings, similarity search, prompt grounding.",
        "packages": [
            "`pypdf` / `pdfplumber` (Extract text and page metadata from PDF bytes)",
            "`langchain-text-splitters` (RecursiveCharacterTextSplitter for chunking)",
            "`langchain-google-genai` (Embeddings & Gemini Flash LLM generation)",
            "`chromadb` / `faiss-cpu` (Vector database for similarity search)",
            "`pydantic` (Data schemas for cited sources and answers)"
        ],
        "diagram_40k": """+-------------+       +-------------------+       +--------------------+
|  User PDF   | ----> | PDF Q&A Assistant | ----> | Accurate Answers   |
|  & Question |       |  (RAG Knowledge)  |       | with Source Pages  |
+-------------+       +-------------------+       +--------------------+""",
        "diagram_20k": """[ Uploaded PDF ] ──► [ PyPDF Parser ] ──► [ Text Chunks ] ──► [ ChromaDB Vector Store ]
                                                                             │
[ User Question ] ──────────────────────────────────────────► [ Similarity Search ]
                                                                             │ Context
                                                                             ▼
                                                                     [ Gemini LLM ]
                                                                             │
                                                                             ▼
                                                                     [ Answer + Citations ]""",
        "diagram_0k": """1. Client POSTs PDF bytes to /api/upload
2. pypdf.PdfReader iterates pages: extract_text() -> yields Document(page_content, metadata={"page": i})
3. RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents()
4. GoogleGenerativeAIEmbeddings(model="models/embedding-001").embed_documents(chunks)
5. Vector store upsert: Chroma.add_texts(ids, vectors, metadatas)
6. User query -> embeddings.embed_query(query) -> collection.query(top_k=3)
7. Format prompt: ChatPromptTemplate.from_template("Context: {context} \\n\\n Question: {question}")
8. gemini-3.5-flash-lite.invoke() -> returns JSON: {"answer": str, "citations": [page_numbers]}"""
    },
    {
        "id": "02-customer-support-ticket-routing-classifier",
        "title": "Customer Support Ticket Routing Classifier",
        "description": "Ingests customer support messages, classifies them into operational departments, and flags urgency priority with strict JSON output.",
        "industry_use_case": "Automated ticket triage for Zendesk, Jira Service Desk, and Freshdesk.",
        "skills_tested": "Few-shot intent classification, structured Pydantic output, latency optimization.",
        "packages": [
            "`langchain-google-genai` (ChatGoogleGenerativeAI with structured output)",
            "`pydantic` (TicketClassification schema validation: category, priority, confidence)",
            "`fastapi` (REST API webhook endpoint receiving ticket submissions)",
            "`python-dotenv` (Secure environment key loading)"
        ],
        "diagram_40k": """+----------------+       +----------------------+       +-----------------------+
| Support Ticket | ----> | AI Intent Classifier | ----> | Routed Department &   |
| (Raw Message)  |       |                      |       | Priority SLA (P1-P4)  |
+----------------+       +----------------------+       +-----------------------+""",
        "diagram_20k": """[ Customer Email/Ticket ] ──► [ API Gateway / Webhook ]
                                         │
                                         ▼
                             [ Classification Prompt ]
                             - Categories: Billing, Tech, Account, General
                             - Priority Rules: P1 (Outage) to P4 (Low)
                                         │
                                         ▼
                             [ Gemini 3.5 Flash Lite ]
                                         │
                                         ▼
                             [ Pydantic JsonParser ] ──► [ Zendesk / Jira Route ]""",
        "diagram_0k": """1. Incoming Webhook receives payload: {"ticket_id": "T-102", "body": "Cannot login, 500 error"}
2. Define Pydantic Schema:
   class TicketRoute(BaseModel):
       category: Literal['Billing', 'Technical', 'Account', 'General']
       priority: Literal['P1', 'P2', 'P3', 'P4']
       summary: str
       confidence: float
3. Model binding: llm.with_structured_output(TicketRoute)
4. Prompt invocation: ChatPromptTemplate with strict 0-shot classification guidelines
5. Response parsed directly into typed Python model without string regex
6. HTTP POST dispatched to downstream queue: router.forward(ticket.category, ticket.priority)"""
    },
    {
        "id": "03-meeting-transcript-summarizer-and-action-item-extractor",
        "title": "Meeting Transcript Summarizer & Action Item Extractor",
        "description": "Processes conversational transcripts to produce executive summaries, key decisions, and assigned action item checklists.",
        "industry_use_case": "Post-meeting workflow automation for Zoom, Google Meet, and Slack.",
        "skills_tested": "Token budget management, entity extraction, markdown report generation.",
        "packages": [
            "`langchain-core` (Prompts and LCEL chain pipeline)",
            "`langchain-google-genai` (Gemini Flash for large token context processing)",
            "`pydantic` (ActionItem schema with owner, task, and deadline)",
            "`python-docx` / `markdown` (Exporting meeting minutes to docx or markdown)"
        ],
        "diagram_40k": """+--------------------+       +--------------------+       +---------------------+
| Meeting Transcript | ----> | Transcript Parser  | ----> | Decisions, Summary  |
|   (Audio to Text)  |       |    & Synthesizer   |       | & Assigned Action Items|
+--------------------+       +--------------------+       +---------------------+""",
        "diagram_20k": """[ Raw VTT/SRT Transcript ] ──► [ Transcript Cleaner / Normalizer ]
                                                  │
                                                  ▼
                                      [ Multi-Task Prompt Chain ]
                                      ├── Executive Summary Node
                                      ├── Decisions Made Node
                                      └── Action Items Extractor (Owner, Task)
                                                  │
                                                  ▼
                                      [ Structured Meeting Report ]""",
        "diagram_0k": """1. File loader reads meeting .vtt or plain text transcript
2. Clean noise: strip timestamps, speaker repetition artifacts
3. Prompt assembly:
   System: "Extract: 1. Executive Summary (3 bullets), 2. Decisions, 3. Action Items (Owner, Task, Deadline)"
4. LLM call: gemini-3.5-flash-lite.invoke(messages) with max_output_tokens=500
5. JsonOutputParser extracts ActionItem list: [{"owner": "Alex", "task": "Update AWS config", "due": "Friday"}]
6. Output written to markdown file or dispatched to Slack channel webhook"""
    },
    {
        "id": "04-sql-query-generator-text-to-sql",
        "title": "Natural Language SQL Query Generator (Text-to-SQL)",
        "description": "Converts plain English business questions into syntactically valid, safe SELECT queries against an existing database schema.",
        "industry_use_case": "Self-service business intelligence (BI) for non-technical product and sales managers.",
        "skills_tested": "Database schema injection, SQL dialect constraints, safety guardrails (read-only validation).",
        "packages": [
            "`sqlalchemy` (Database schema inspection and safe query execution)",
            "`sqlparse` (SQL formatting, syntax validation, and statement verification)",
            "`langchain-google-genai` (Prompt-to-SQL translation)",
            "`sqlite3` / `psycopg2-binary` (Underlying database engines)"
        ],
        "diagram_40k": """+---------------------+       +----------------------+       +----------------------+
| Plain English Query | ----> | Text-to-SQL Engine   | ----> | Verified Database    |
| ("Top 5 customers") |       | (Grounded in Schema) |       | Report / Query Result|
+---------------------+       +----------------------+       +----------------------+""",
        "diagram_20k": """[ User Question ] ──┬──► [ Text-to-SQL Generator ] ──► [ Raw SQL Query ]
                     │                 │                                │
[ DB Table Schema ] ─┘                 ▼                                ▼
                               [ Gemini LLM ]                [ SQL Safety Guard ]
                                                             - Block DROP/UPDATE/DELETE
                                                             - Enforce LIMIT clauses
                                                                        │
                                                                        ▼
                                                             [ Database Engine (SQL) ]
                                                                        │
                                                                        ▼
                                                             [ Tabular Data Result ]""",
        "diagram_0k": """1. SQLAlchemy engine inspects target DB: inspector.get_table_names(), get_columns()
2. Assemble prompt containing DDL schema strings + business question
3. LLM instructed: "Generate ONLY a SQLite-compatible SELECT statement. Never use DROP/DELETE/INSERT."
4. Resulting string cleaned of markdown backticks
5. sqlparse.parse(query) verifies AST contains only DML SELECT statements
6. Connection executed with read-only cursor: db.execute(text(clean_sql)).fetchall()
7. Returned rows formatted into clean tabular markdown or JSON"""
    },
    {
        "id": "05-resumes-and-job-description-matcher",
        "title": "Resume & Job Description Matcher (ATS Screener)",
        "description": "Evaluates candidate resumes against job specifications to score compatibility, missing technical skills, and candidate strengths.",
        "industry_use_case": "Applicant Tracking Systems (ATS) and automated HR candidate screening.",
        "skills_tested": "Semantic vector similarity, structured evaluation rubrics, resume parsing.",
        "packages": [
            "`pypdf` / `docx2txt` (Parsing multi-format resume files)",
            "`scikit-learn` (Cosine similarity between dense embedding vectors)",
            "`langchain-google-genai` (Deep qualitative skill gap analysis)",
            "`pydantic` (CandidateEvaluation report schema)"
        ],
        "diagram_40k": """+-----------------+       +-------------------+       +--------------------+
| Resume (PDF) &  | ----> | ATS Matcher &     | ----> | Match Score (%),   |
| Job Description |       | Qualitative Grader|       | Skill Gaps & Verdict|
+-----------------+       +-------------------+       +--------------------+""",
        "diagram_20k": """[ Resume Text ] ────────► [ Dense Embedder ] ──┐
                                               ▼
[ Job Description Text ] ► [ Dense Embedder ] ─► [ Cosine Similarity Score (0-100%) ]
                                               │
                                               ▼
                                  [ Qualitative Gap Evaluator ]
                                  - Missing Must-Have Skills
                                  - Candidate Strengths & Weaknesses
                                               │
                                               ▼
                                  [ Candidate Scorecard ]""",
        "diagram_0k": """1. Parse resume (pypdf/docx2txt) and extract normalized text
2. Embed resume and JD text using GoogleGenerativeAIEmbeddings
3. Calculate baseline cosine similarity: dot(res_vec, jd_vec) / (norm(res) * norm(jd))
4. Pass both texts to Gemini LLM with rubric:
   "Identify: 1. Matched Required Skills, 2. Missing Skills, 3. Interview Questions"
5. Parse output into CandidateReview Pydantic schema
6. Combine mathematical semantic score (40%) + qualitative LLM grade (60%) into final ranking"""
    },
    {
        "id": "06-sentiment-and-aspect-analyzer-for-reviews",
        "title": "E-Commerce Review Sentiment & Aspect Analyzer",
        "description": "Analyzes batch customer feedback to extract fine-grained sentiment across product dimensions (Price, Delivery, Quality, Usability).",
        "industry_use_case": "Customer experience analytics for Amazon, Shopify, and Trustpilot reviews.",
        "skills_tested": "Aspect-based sentiment classification, batch processing, JSON array generation.",
        "packages": [
            "`langchain-google-genai` (Batch LLM invocation)",
            "`pydantic` (AspectSentiment schema validation)",
            "`pandas` (Tabular aggregation and CSV report generation)",
            "`matplotlib` / `seaborn` (Visual sentiment distribution charts)"
        ],
        "diagram_40k": """+--------------------+       +----------------------+       +---------------------+
| Customer Reviews   | ----> | Aspect Sentiment AI  | ----> | Dimension Breakdown |
| (Batch Text Data)  |       |                      |       | (Price, Quality, etc)|
+--------------------+       +----------------------+       +---------------------+""",
        "diagram_20k": """[ Customer Reviews (CSV) ] ──► [ Batch Processing Loop ]
                                            │
                                            ▼
                               [ Aspect Extraction Prompt ]
                               ├── Shipping & Delivery
                               ├── Product Build Quality
                               ├── Pricing & Value
                               └── Customer Service
                                            │
                                            ▼
                               [ Gemini Structured JSON ]
                                            │
                                            ▼
                               [ Aggregated Pandas Dashboard ]""",
        "diagram_0k": """1. pandas.read_csv('reviews.csv') loads customer comments
2. Schema defined: List[AspectRating(aspect=str, sentiment='POS'|'NEG'|'NEU', evidence=str)]
3. LLM executes batch processing with low temperature (0.0)
4. Model maps input sentences to explicit domain aspects
5. JSON parsed into pandas DataFrame
6. Summary computed: Net Sentiment Score per product dimension"""
    },
    {
        "id": "07-website-faq-rag-assistant",
        "title": "Website FAQ RAG Assistant",
        "description": "Grounded Q&A assistant built over company FAQ URLs or documentation that provides verified customer support answers.",
        "industry_use_case": "SaaS website conversion widget and 24/7 self-service customer support.",
        "skills_tested": "HTML scraping, chunking, retrieval grounding, hallucination prevention.",
        "packages": [
            "`beautifulsoup4` / `httpx` (Web scraping and HTML text extraction)",
            "`langchain-community` (WebBaseLoader / Document wrappers)",
            "`chromadb` (Embedded vector search store)",
            "`langchain-google-genai` (Gemini Flash Lite Q&A generator)"
        ],
        "diagram_40k": """+-----------------+       +---------------------+       +----------------------+
| Company Website | ----> | FAQ RAG Assistant   | ----> | Instant, Verified    |
| & User Question |       | (Grounded in Pages) |       | Customer Answers     |
+-----------------+       +---------------------+       +----------------------+""",
        "diagram_20k": """[ FAQ Webpages ] ──► [ BeautifulSoup Parser ] ──► [ Text Chunks ] ──► [ ChromaDB Store ]
                                                                                   │
[ User Inquiries ] ──────────────────────────────────────────────► [ Vector Retrieval ]
                                                                                   │
                                                                                   ▼
                                                                        [ Grounded Prompt ]
                                                                        (Strict: "Answer ONLY
                                                                         from context")
                                                                                   │
                                                                                   ▼
                                                                        [ Customer Response ]""",
        "diagram_0k": """1. httpx fetches HTML content from FAQ URL endpoints
2. BeautifulSoup strips <script>, <style>, <nav> tags, extracting clean article body
3. RecursiveCharacterTextSplitter generates overlapping chunks (chunk_size=400, overlap=50)
4. Chroma.from_documents() embeds chunks using GoogleGenerativeAIEmbeddings
5. Customer types inquiry: "How do I request a refund?"
6. retriever.invoke(query) fetches top 3 matching chunks
7. Prompt encloses retrieved text: "Answer using ONLY this text. If absent, say 'Please contact support.'\"
8. Model generates clean, safe response with zero hallucination"""
    },
    {
        "id": "08-invoice-data-extractor-json",
        "title": "Invoice & Receipt Key-Value Extractor",
        "description": "Extracts structured metadata (Invoice #, Date, Vendor Name, Line Items, Tax, Total Due) from unstructured receipt and invoice texts into validated JSON.",
        "industry_use_case": "Automated accounts payable and expense management (Expensify, QuickBooks).",
        "skills_tested": "Zero-shot extraction, Pydantic data schemas, nested JSON validation.",
        "packages": [
            "`pypdf` / `pytesseract` (PDF/OCR text extraction)",
            "`pydantic` (Strict InvoiceSchema with line-item array)",
            "`langchain-google-genai` (Structured output extraction with Gemini)",
            "`json` (Standard JSON serialization and file exports)"
        ],
        "diagram_40k": """+---------------------+       +---------------------+       +----------------------+
| Raw Invoice /       | ----> | Zero-Shot Structured| ----> | Clean, Validated     |
| Receipt Text        |       | Data Extractor      |       | JSON Database Record |
+---------------------+       +---------------------+       +----------------------+""",
        "diagram_20k": """[ Invoice Text / OCR ] ──► [ Schema-Enforced Prompt ]
                                        │
                                        ▼
                            [ Gemini Flash Lite ]
                                        │
                                        ▼
                            [ Pydantic Invoice Validator ]
                            ├── vendor_name (str)
                            ├── invoice_number (str)
                            ├── line_items: List[Item(desc, qty, price)]
                            └── total_amount (float)
                                        │
                                        ▼
                            [ ERP / Accounting Database ]""",
        "diagram_0k": """1. Ingest invoice text via file read or OCR
2. Define Pydantic schema:
   class LineItem(BaseModel):
       description: str; quantity: int; unit_price: float; total: float
   class Invoice(BaseModel):
       vendor: str; invoice_no: str; date: str; items: List[LineItem]; total: float
3. Invoke model: llm.with_structured_output(Invoice)
4. LLM analyzes raw receipt text, performing implicit entity resolution
5. Python validates currency numeric values and calculates line item math checks
6. Write validated JSON payload to output directory or database table"""
    },
    {
        "id": "09-code-bug-explainer-and-fixer",
        "title": "Code Bug Explainer & Auto-Fixer",
        "description": "Takes buggy code snippets alongside error tracebacks, diagnoses the root cause, and generates corrected code patches with explanations.",
        "industry_use_case": "Developer tooling, CI/CD automated triage, and coding education.",
        "skills_tested": "Code reasoning, traceback parsing, diff/patch generation.",
        "packages": [
            "`langchain-core` (Structured prompt templates)",
            "`langchain-google-genai` (Code reasoning with Gemini)",
            "`pydantic` (BugDiagnosis schema with root cause, fix, and explanation)",
            "`rich` (Syntax-highlighted terminal diff rendering)"
        ],
        "diagram_40k": """+---------------------+       +----------------------+       +----------------------+
| Buggy Code &        | ----> | AI Debugger & Code   | ----> | Root Cause Diagnosis |
| Error Traceback     |       | Repair Engine        |       | & Verified Fix Patch |
+---------------------+       +----------------------+       +----------------------+""",
        "diagram_20k": """[ Buggy Snippet + Stack Trace ] ──► [ Prompt with Language Context ]
                                                    │
                                                    ▼
                                        [ Gemini Reasoning Model ]
                                                    │
                                                    ▼
                                        [ Structured Diagnosis ]
                                        ├── Root Cause Explanation
                                        ├── Corrected Code Block
                                        └── Preventive Recommendations
                                                    │
                                                    ▼
                                        [ Developer Terminal / PR ]""",
        "diagram_0k": """1. Collect runtime error trace + faulty code function
2. Construct Prompt: "Analyze this stack trace. Explain the bug in 2 sentences and return the fixed code."
3. Send to Gemini Flash Lite with temperature=0.1 for high code determinism
4. Parse response into markdown blocks: `Explanation` and `Fixed Code`
5. Print diff to developer using rich.syntax.Syntax"""
    },
    {
        "id": "10-pii-data-scrubber-and-redactor",
        "title": "PII Data Scrubber & Anonymizer",
        "description": "Detects and redacts Personally Identifiable Information (Emails, Phone Numbers, Credit Cards, SSNs) from input text before downstream LLM processing.",
        "industry_use_case": "Compliance (GDPR, HIPAA) and enterprise AI safety gateways.",
        "skills_tested": "Regex + LLM hybrid detection, data masking, safety guardrails.",
        "packages": [
            "`re` (Fast regex pre-filtering for standard patterns like SSN, email, credit card)",
            "`langchain-google-genai` (Context-aware entity detection for names and addresses)",
            "`pydantic` (Masking configuration and audit log schemas)"
        ],
        "diagram_40k": """+---------------------+       +----------------------+       +----------------------+
| Raw Sensitive Text  | ----> | PII Redaction        | ----> | Safe Anonymized Text |
| (Contains PII/GDPR) |       | Firewall             |       | (Ready for LLM APIs) |
+---------------------+       +----------------------+       +----------------------+""",
        "diagram_20k": """[ Raw User Input ] ──► [ Fast Regex Filter ] (Emails, Phone, SSN)
                                      │
                                      ▼
                        [ LLM Contextual Scrubber ] (Names, Addresses, Identifiers)
                                      │
                                      ▼
                        [ Masked Output: <REDACTED_EMAIL>, <REDACTED_NAME> ]
                                      │
                                      ▼
                        [ Downstream Cloud LLM / Logs ]""",
        "diagram_0k": """1. Pass input string through compiled regex: re.sub(EMAIL_REGEX, '<EMAIL>', text)
2. Run contextual NLP/LLM pass for ambiguous entities (e.g. personal names, medical IDs)
3. Generate token replacement map: {'John Doe': '<USER_1>', 'San Jose': '<CITY_1>'}
4. Replace occurrences while retaining grammatical readability
5. Return anonymized payload alongside audit log of redacted entity types"""
    },
    {
        "id": "11-email-reply-generator-with-tone-control",
        "title": "Smart Email Drafter with Tone Modulation",
        "description": "Drafts contextual email responses based on incoming thread context, allowing the user to select tones (Professional, Friendly, Concise, Urgent).",
        "industry_use_case": "Executive inbox productivity and sales outreach automation.",
        "skills_tested": "Tone modulation, prompt templating, contextual chaining.",
        "packages": [
            "`langchain-core` (ChatPromptTemplate with tone parameter)",
            "`langchain-google-genai` (Gemini Flash Lite generator)",
            "`pydantic` (EmailDraft schema validation)"
        ],
        "diagram_40k": """+--------------------+       +----------------------+       +--------------------+
| Incoming Email &   | ----> | Contextual Email     | ----> | Ready-to-Send      |
| Selected Tone      |       | Drafter              |       | Tailored Email     |
+--------------------+       +----------------------+       +--------------------+""",
        "diagram_20k": """[ Email Thread Context ] ──┬──► [ Prompt Template ]
                           │          - Tone parameter (Formal / Casual / Urgent)
[ Desired Tone / Intent ] ─┘          - Key points to include
                                                │
                                                ▼
                                    [ Gemini 3.5 Flash Lite ]
                                                │
                                                ▼
                                    [ Formatted Subject + Body ]""",
        "diagram_0k": """1. Ingest thread context: sender, original message, user's key reply bullet points
2. User specifies tone: Enum['Formal', 'Friendly', 'Direct', 'Negotiation']
3. Prompt template applies stylistic few-shot instructions matching target tone
4. Gemini generates response enforcing concise business communication standards
5. Output returns structured draft: {"subject": str, "body": str, "sign_off": str}"""
    },
    {
        "id": "12-product-recommendation-advisor",
        "title": "E-Commerce Product Recommendation Advisor",
        "description": "Matches customer preferences, budget, and constraints against a catalog of products (JSON) to suggest the top 3 best matching items with purchase justifications.",
        "industry_use_case": "Online shopping assistants and retail personalized search.",
        "skills_tested": "Content-based filtering, semantic catalog search, persuasive generation.",
        "packages": [
            "`langchain-google-genai` (Gemini Flash Lite reasoning)",
            "`pydantic` (Product catalog and recommendation schemas)",
            "`json` (Catalog loading and query filtering)"
        ],
        "diagram_40k": """+---------------------+       +----------------------+       +--------------------+
| Shopper Needs &     | ----> | Product Advisor AI   | ----> | Top 3 Products     |
| Budget Constraints  |       | (Catalog Grounded)   |       | with Reasons       |
+---------------------+       +----------------------+       +--------------------+""",
        "diagram_20k": """[ User Request / Budget ] ──┬──► [ Catalog Pre-Filter ] (Price <= Budget)
                            │                 │
[ Product Catalog JSON ] ───┘                 ▼
                                    [ Grounded Recommendation Prompt ]
                                              │
                                              ▼
                                    [ Gemini Flash Lite ]
                                              │
                                              ▼
                                    [ Top 3 Picks + Value Justification ]""",
        "diagram_0k": """1. Load product catalog JSON: [{'id': 1, 'name': 'Laptop', 'price': 800, 'tags': ['lightweight']}]
2. Filter items strictly exceeding user budget ceiling
3. Pass filtered candidates + user preferences to LLM
4. LLM selects top 3 candidates and drafts a 1-sentence value pitch for each
5. Return structured recommendation card ready for frontend UI rendering"""
    },
    {
        "id": "13-csv-data-analyst-agent",
        "title": "CSV Data Analyst & Insights Generator",
        "description": "Loads a tabular CSV dataset, inspects schema and summary statistics, and generates executive business insights and trends.",
        "industry_use_case": "Automated weekly reporting and ad-hoc data analysis.",
        "skills_tested": "Data schema inspection, tabular grounding, trend synthesis.",
        "packages": [
            "`pandas` (Dataframe loading, cleaning, and describe() statistics)",
            "`langchain-google-genai` (Statistical synthesis and insights)",
            "`tabulate` (Clean ASCII table formatting for prompt grounding)"
        ],
        "diagram_40k": """+--------------------+       +----------------------+       +--------------------+
| Raw CSV Dataset    | ----> | Tabular Data Analyst | ----> | Executive Insights |
| (Sales/Metrics)    |       |                      |       | & Key Trends       |
+--------------------+       +----------------------+       +--------------------+""",
        "diagram_20k": """[ Raw CSV File ] ──► [ Pandas Dataframe ]
                              │
                              ▼
                   [ Statistical Profiler ]
                   - df.info(), df.describe()
                   - Top outliers and correlations
                              │
                              ▼
                   [ LLM Insight Synthesizer ]
                              │
                              ▼
                   [ 5 Actionable Executive Takeaways ]""",
        "diagram_0k": """1. pandas.read_csv('sales.csv') loads data into memory
2. Compute summary metrics: total revenue, top-selling category, month-over-month growth
3. Format summary metrics into concise markdown string
4. Send to Gemini with prompt: "Synthesize 3 key trends and 2 risks from these statistics."
5. Output formatted as an executive briefing note"""
    },
    {
        "id": "14-social-media-content-repurposer",
        "title": "Multi-Platform Social Media Content Repurposer",
        "description": "Converts a single blog post or article into tailored copy for LinkedIn, X/Twitter, and Instagram with platform-specific formatting.",
        "industry_use_case": "Marketing automation and content creation workflows.",
        "skills_tested": "Persona prompting, platform character constraints, multi-output pipelines.",
        "packages": [
            "`langchain-core` (Prompt formatting and branching)",
            "`langchain-google-genai` (Creative multi-format generation)",
            "`pydantic` (MultiPlatformPost schema with character limit validation)"
        ],
        "diagram_40k": """+--------------------+       +----------------------+       +---------------------+
| Blog Post / Article| ----> | Content Repurposer   | ----> | LinkedIn, X Thread, |
|                    |       |                      |       | & Instagram Copy    |
+--------------------+       +----------------------+       +---------------------+""",
        "diagram_20k": """[ Long-Form Blog Post ] ──► [ Core Message Extractor ]
                                         │
                                         ▼
                     ┌───────────────────┼───────────────────┐
                     ▼                   ▼                   ▼
             [ LinkedIn Node ]    [ X Thread Node ]  [ Instagram Node ]
             - Professional tone  - Hook + 5 tweets  - Visual caption
             - Formatting spacing - <280 chars each  - Hashtags
                     │                   │                   │
                     └───────────────────┼───────────────────┘
                                         ▼
                             [ Multi-Channel Bundle ]""",
        "diagram_0k": """1. Ingest article string and extract primary thesis
2. Run single LLM pass with structured schema returning 3 platform variants
3. Enforce validation: X tweets must not exceed 280 characters
4. LinkedIn post includes thought-leadership hook and call-to-action
5. Output structured JSON ready for social media scheduler APIs (Buffer/Hootsuite)"""
    },
    {
        "id": "15-multilingual-translator-and-localizer",
        "title": "Contextual Language Translator & Localizer",
        "description": "Translates UI copy or marketing messages across multiple languages while preserving regional idioms and technical terminology.",
        "industry_use_case": "SaaS internationalization (i18n) and cross-border customer service.",
        "skills_tested": "Domain-specific translation, glossary enforcement, few-shot formatting.",
        "packages": [
            "`langchain-google-genai` (Multilingual LLM translation)",
            "`pydantic` (Translation dictionary schema)",
            "`json` (Exporting standard i18n JSON translation files)"
        ],
        "diagram_40k": """+--------------------+       +----------------------+       +--------------------+
| English UI String  | ----> | Context-Aware        | ----> | Localized JSON     |
| & Target Language  |       | Localizer            |       | for Spanish/French |
+--------------------+       +----------------------+       +--------------------+""",
        "diagram_20k": """[ Source Strings ] ──┬──► [ Context & Glossary Injector ]
                     │          (Do not translate brand names: e.g. "CloudPay")
[ Target Locales ] ──┘                    │
                                          ▼
                              [ Gemini Multilingual LLM ]
                                          │
                                          ▼
                              [ Validated i18n JSON Bundle ]""",
        "diagram_0k": """1. Load source strings: {"login_cta": "Sign in to continue"}
2. Inject glossary constraints: "Keep company brand name in English; adapt idioms for locale."
3. Request translation for target locales (e.g., 'es-ES', 'fr-FR', 'de-DE')
4. Model generates localized strings matching native phrasing
5. Verify placeholders ({username}, %d) remain intact
6. Write out `es.json`, `fr.json` standard translation dictionaries"""
    },
    {
        "id": "16-news-article-fact-checker-evaluator",
        "title": "Article Fact-Checker & Hallucination Evaluator",
        "description": "Compares an AI-generated summary against source facts to detect fabricated claims, scoring factual consistency from 1 to 10.",
        "industry_use_case": "LLMOps quality evaluation and automated journalism compliance.",
        "skills_tested": "Evaluator-Optimizer pattern, LLM-as-a-judge, claim verification.",
        "packages": [
            "`langchain-google-genai` (LLM-as-a-judge evaluator)",
            "`pydantic` (FactCheckResult schema with consistency score and flagged hallucinations)"
        ],
        "diagram_40k": """+---------------------+       +----------------------+       +--------------------+
| Generated Summary & | ----> | LLM Fact-Checker     | ----> | Faithfulness Score |
| Ground-Truth Facts  |       | (Judge)              |       | (1-10) & Audit Log |
+---------------------+       +----------------------+       +--------------------+""",
        "diagram_20k": """[ Ground-Truth Article ] ──┬──► [ Claim Extraction Engine ]
                           │                │
[ AI-Generated Summary ] ──┘                ▼
                                 [ Cross-Verification Matrix ]
                                 - Check every claim in summary
                                 - Flag unsupported assertions
                                            │
                                            ▼
                                 [ Faithfulness Scorecard ]""",
        "diagram_0k": """1. Break summary into discrete atomic propositions: ["Company founded in 2020", "Raised $5M"]
2. For each proposition, verify whether ground truth source text explicitly entails it
3. LLM evaluates: ENTAILED | CONTRADICTED | NOT_MENTIONED (Hallucination)
4. Calculate faithfulness score: (entailed_claims / total_claims) * 10
5. Output report with flagged hallucinations highlighted for human review"""
    },
    {
        "id": "17-unit-test-case-generator",
        "title": "Automated Unit Test Case Generator",
        "description": "Analyzes Python/Node.js utility functions and outputs comprehensive test suites covering edge cases, null inputs, and happy paths.",
        "industry_use_case": "Developer productivity suites and automated code review.",
        "skills_tested": "Code AST reasoning, boundary-value analysis, test framework syntax.",
        "packages": [
            "`pytest` / `unittest` (Target Python test execution)",
            "`langchain-google-genai` (Code generation with Gemini)",
            "`pydantic` (Test suite structure validation)"
        ],
        "diagram_40k": """+--------------------+       +----------------------+       +--------------------+
| Source Code        | ----> | Automated Test       | ----> | Executable Pytest  |
| Function           |       | Generator            |       | Test Suite         |
+--------------------+       +----------------------+       +--------------------+""",
        "diagram_20k": """[ Source Function Snippet ] ──► [ Function Signature & Logic Analyzer ]
                                                  │
                                                  ▼
                                      [ Test Scenario Planner ]
                                      ├── Happy Path Cases
                                      ├── Boundary & Edge Cases
                                      └── Exception & Type Handling
                                                  │
                                                  ▼
                                      [ Gemini Code Generator ]
                                                  │
                                                  ▼
                                      [ test_*.py Test Suite ]""",
        "diagram_0k": """1. Read target function: e.g. `def calculate_discount(price, tier): ...`
2. Prompt instructs LLM: "Write 4 pytest functions covering: normal case, 0 price, negative price, invalid tier."
3. Model outputs pure executable Python test code
4. Save to `test_suite.py`
5. Optional execution validation: subprocess.run(['pytest', 'test_suite.py'])"""
    },
    {
        "id": "18-slack-discord-notification-bot",
        "title": "DevOps Incident Summary & Alert Bot",
        "description": "Consumes raw server/cloud error logs, filters out repetitive noise, and formats a high-priority incident summary for Slack/Discord webhooks.",
        "industry_use_case": "SRE/DevOps on-call alerts and Datadog/PagerDuty log synthesis.",
        "skills_tested": "Log anomaly parsing, webhook JSON formatting, alert prioritization.",
        "packages": [
            "`httpx` / `requests` (Posting payloads to Slack/Discord webhook URLs)",
            "`langchain-google-genai` (Log summarization and triage)",
            "`pydantic` (SlackBlockKit JSON payload schema)"
        ],
        "diagram_40k": """+--------------------+       +----------------------+       +--------------------+
| Raw Cloud Server   | ----> | Incident Triage AI   | ----> | Actionable Slack / |
| Error Logs         |       |                      |       | Discord Alert Card |
+--------------------+       +----------------------+       +--------------------+""",
        "diagram_20k": """[ Unstructured Server Logs ] ──► [ Error Deduplication & Grouping ]
                                                │
                                                ▼
                                    [ Gemini Incident Analyzer ]
                                    - Root Cause Hypothesis
                                    - Impact Assessment
                                    - Recommended First Step
                                                │
                                                ▼
                                    [ Slack BlockKit JSON Payload ]
                                                │
                                                ▼
                                    [ Webhook POST to #devops ]""",
        "diagram_0k": """1. Ingest stack trace batch from cloud logs
2. Filter duplicate exception signatures
3. Send top anomalies to Gemini: "Synthesize into a 2-line incident alert with recommended immediate action."
4. Format output into Slack BlockKit JSON: {"blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": ...}}]}
5. httpx.post(SLACK_WEBHOOK_URL, json=payload) delivers alert directly to on-call engineers"""
    },
    {
        "id": "19-api-documentation-generator",
        "title": "API Documentation Generator from Code",
        "description": "Inspects backend API endpoints and functions to generate developer-friendly OpenAPI/Swagger specs and clean Markdown documentation.",
        "industry_use_case": "Engineering documentation maintenance and developer portals.",
        "skills_tested": "OpenAPI spec generation, schema deduction, technical documentation.",
        "packages": [
            "`langchain-google-genai` (API schema analysis)",
            "`pydantic` (OpenAPI 3.0 schema modeling)",
            "`pyyaml` / `json` (Exporting swagger.yaml and OpenAPI specifications)"
        ],
        "diagram_40k": """+--------------------+       +----------------------+       +--------------------+
| Backend Code /     | ----> | API Spec Generator   | ----> | OpenAPI 3.0 Spec & |
| Express Endpoints  |       |                      |       | Markdown Docs      |
+--------------------+       +----------------------+       +--------------------+""",
        "diagram_20k": """[ Raw Controller / Route Code ] ──► [ AST / Route Endpoint Parser ]
                                                   │
                                                   ▼
                                       [ Gemini Spec Synthesizer ]
                                       - Extract HTTP Verb, Path, Query/Body
                                       - Document Status Codes (200, 400, 500)
                                                   │
                                                   ▼
                                       [ Validated OpenAPI 3.0 JSON / YAML ]""",
        "diagram_0k": """1. Read Express/FastAPI route file: `app.post('/api/users', (req, res) => ...)`
2. LLM identifies request parameters, auth headers, and expected return types
3. Generate standard OpenAPI 3.0 schema YAML
4. Validate schema syntax using pyyaml
5. Write `openapi.yaml` and human-readable `API_REFERENCE.md`"""
    },
    {
        "id": "20-personal-finance-expense-categorizer",
        "title": "Personal Finance Transaction Categorizer",
        "description": "Classifies raw bank transactions into standard budget buckets (Groceries, Travel, Utilities, Dining) with monthly spend aggregation.",
        "industry_use_case": "Fintech consumer apps (Mint, YNAB, Revolut) and expense tracking.",
        "skills_tested": "Unstructured text categorization, merchant normalization, summary aggregation.",
        "packages": [
            "`pandas` (Transaction data handling and monthly aggregation)",
            "`langchain-google-genai` (Zero-shot merchant normalization and categorization)",
            "`pydantic` (TransactionRecord schema validation)"
        ],
        "diagram_40k": """+---------------------+       +----------------------+       +--------------------+
| Raw Bank Statement  | ----> | Merchant Normalizer  | ----> | Categorized Spend  |
| ("UBR*TRIP 982")    |       | & Categorizer        |       | Dashboard & Budget |
+---------------------+       +----------------------+       +--------------------+""",
        "diagram_20k": """[ Raw Transaction Text ] ──► [ Merchant Normalization ] (UBR*TRIP -> "Uber")
                                          │
                                          ▼
                             [ Spending Category Classifier ]
                             - Categories: Travel, Food, Utilities, Subscriptions
                                          │
                                          ▼
                             [ Categorized Transaction Ledger ]
                                          │
                                          ▼
                             [ Pandas Monthly Budget Summary ]""",
        "diagram_0k": """1. Load bank statement CSV: ['DATE', 'RAW_DESC', 'AMOUNT']
2. Process raw descriptions through LLM: "Normalize merchant and categorize into: [Dining, Travel, Groceries, Utilities, Shopping]"
3. Parse response into structured columns: Normalized_Merchant, Category
4. pandas.groupby('Category')['AMOUNT'].sum() aggregates monthly spend
5. Print clean budget breakdown table to terminal or export as JSON"""
    }
]

index_md = "# Beginner Level AI Projects (Interview & Industry Popular)\n\n"
index_md += "Curated list of 20 practical, industry-standard AI projects frequently encountered in technical interviews and enterprise workflows.\n\n"
index_md += "Each project contains:\n"
index_md += "- **Core Python Packages Used**\n"
index_md += "- **40k Feet Architecture Diagram** (Executive / Business View)\n"
index_md += "- **20k Feet Architecture Diagram** (Component & Data Flow)\n"
index_md += "- **0 Feet Ground Level Diagram** (Exact Wire / Protocol / Step Execution)\n\n"
index_md += "| # | Project Title | Industry Use Case | Key Skills Tested |\n"
index_md += "|---|---------------|-------------------|-------------------|\n"

for i, p in enumerate(projects, 1):
    proj_folder = base_dir / p["id"]
    proj_folder.mkdir(parents=True, exist_ok=True)
    
    packages_md = "\n".join([f"- {pkg}" for pkg in p["packages"]])
    
    readme_path = proj_folder / "README.md"
    readme_content = f"""# {p['title']}

## 📌 Project Overview
**Title:** {p['title']}  
**Industry Category:** {p['industry_use_case']}  

### 📝 Description
{p['description']}

---

## 💼 Enterprise & Industry Use Case
{p['industry_use_case']}

---

## 🎯 Interview Skills Tested
{p['skills_tested']}

---

## 📦 Required Packages & Libraries
{packages_md}

---

## ⚠️ Real-World Edge Cases & Failure Modes
- **Input Edge Cases:** Empty/corrupt payloads, oversized inputs exceeding LLM context windows, and non-UTF-8 character encodings.
- **Model Edge Cases:** Hallucination under incomplete input, JSON formatting failures, and non-deterministic variations across runs.
- **System Failure Modes:** API rate limits (HTTP 429), token quota exhaustion, network timeouts, and partial API failures.
- **Production Defenses:** Strict Pydantic schema validation, exponential backoff retries with model fallbacks, hard token caps, and input length gating.

---

## 🏗️ Architecture Diagrams

### 🛫 40,000 Feet: Executive & Business View
```
{p['diagram_40k']}
```

### 🛩️ 20,000 Feet: Component & Data Flow View
```
{p['diagram_20k']}
```

### 🚜 0 Feet: Ground Level (Step-by-Step Wire Execution)
```
{p['diagram_0k']}
```
"""
    readme_path.write_text(readme_content, encoding="utf-8")
    index_md += f"| {i:02d} | [{p['title']}](./{p['id']}/README.md) | {p['industry_use_case']} | {p['skills_tested']} |\n"

(base_dir / "README.md").write_text(index_md, encoding="utf-8")
print("Successfully updated all 20 README files with packages and 3-altitude architecture diagrams.")
