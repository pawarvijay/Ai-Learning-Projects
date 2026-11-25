# Beginner Level AI Projects (Interview & Industry Popular)

Curated list of 20 practical, industry-standard AI projects frequently encountered in technical interviews and enterprise workflows.

Each project contains:
- **Core Python Packages Used**
- **40k Feet Architecture Diagram** (Executive / Business View)
- **20k Feet Architecture Diagram** (Component & Data Flow)
- **0 Feet Ground Level Diagram** (Exact Wire / Protocol / Step Execution)

| # | Project Title | Industry Use Case | Key Skills Tested |
|---|---------------|-------------------|-------------------|
| 01 | [PDF Document Q&A Chatbot](./01-pdf-document-qa-chatbot/README.md) | HR policy manuals, legal contract review, and internal company wiki search. | Document loading, recursive chunking, vector embeddings, similarity search, prompt grounding. |
| 02 | [Customer Support Ticket Routing Classifier](./02-customer-support-ticket-routing-classifier/README.md) | Automated ticket triage for Zendesk, Jira Service Desk, and Freshdesk. | Few-shot intent classification, structured Pydantic output, latency optimization. |
| 03 | [Meeting Transcript Summarizer & Action Item Extractor](./03-meeting-transcript-summarizer-and-action-item-extractor/README.md) | Post-meeting workflow automation for Zoom, Google Meet, and Slack. | Token budget management, entity extraction, markdown report generation. |
| 04 | [Natural Language SQL Query Generator (Text-to-SQL)](./04-sql-query-generator-text-to-sql/README.md) | Self-service business intelligence (BI) for non-technical product and sales managers. | Database schema injection, SQL dialect constraints, safety guardrails (read-only validation). |
| 05 | [Resume & Job Description Matcher (ATS Screener)](./05-resumes-and-job-description-matcher/README.md) | Applicant Tracking Systems (ATS) and automated HR candidate screening. | Semantic vector similarity, structured evaluation rubrics, resume parsing. |
| 06 | [E-Commerce Review Sentiment & Aspect Analyzer](./06-sentiment-and-aspect-analyzer-for-reviews/README.md) | Customer experience analytics for Amazon, Shopify, and Trustpilot reviews. | Aspect-based sentiment classification, batch processing, JSON array generation. |
| 07 | [Website FAQ RAG Assistant](./07-website-faq-rag-assistant/README.md) | SaaS website conversion widget and 24/7 self-service customer support. | HTML scraping, chunking, retrieval grounding, hallucination prevention. |
| 08 | [Invoice & Receipt Key-Value Extractor](./08-invoice-data-extractor-json/README.md) | Automated accounts payable and expense management (Expensify, QuickBooks). | Zero-shot extraction, Pydantic data schemas, nested JSON validation. |
| 09 | [Code Bug Explainer & Auto-Fixer](./09-code-bug-explainer-and-fixer/README.md) | Developer tooling, CI/CD automated triage, and coding education. | Code reasoning, traceback parsing, diff/patch generation. |
| 10 | [PII Data Scrubber & Anonymizer](./10-pii-data-scrubber-and-redactor/README.md) | Compliance (GDPR, HIPAA) and enterprise AI safety gateways. | Regex + LLM hybrid detection, data masking, safety guardrails. |
| 11 | [Smart Email Drafter with Tone Modulation](./11-email-reply-generator-with-tone-control/README.md) | Executive inbox productivity and sales outreach automation. | Tone modulation, prompt templating, contextual chaining. |
| 12 | [E-Commerce Product Recommendation Advisor](./12-product-recommendation-advisor/README.md) | Online shopping assistants and retail personalized search. | Content-based filtering, semantic catalog search, persuasive generation. |
| 13 | [CSV Data Analyst & Insights Generator](./13-csv-data-analyst-agent/README.md) | Automated weekly reporting and ad-hoc data analysis. | Data schema inspection, tabular grounding, trend synthesis. |
| 14 | [Multi-Platform Social Media Content Repurposer](./14-social-media-content-repurposer/README.md) | Marketing automation and content creation workflows. | Persona prompting, platform character constraints, multi-output pipelines. |
| 15 | [Contextual Language Translator & Localizer](./15-multilingual-translator-and-localizer/README.md) | SaaS internationalization (i18n) and cross-border customer service. | Domain-specific translation, glossary enforcement, few-shot formatting. |
| 16 | [Article Fact-Checker & Hallucination Evaluator](./16-news-article-fact-checker-evaluator/README.md) | LLMOps quality evaluation and automated journalism compliance. | Evaluator-Optimizer pattern, LLM-as-a-judge, claim verification. |
| 17 | [Automated Unit Test Case Generator](./17-unit-test-case-generator/README.md) | Developer productivity suites and automated code review. | Code AST reasoning, boundary-value analysis, test framework syntax. |
| 18 | [DevOps Incident Summary & Alert Bot](./18-slack-discord-notification-bot/README.md) | SRE/DevOps on-call alerts and Datadog/PagerDuty log synthesis. | Log anomaly parsing, webhook JSON formatting, alert prioritization. |
| 19 | [API Documentation Generator from Code](./19-api-documentation-generator/README.md) | Engineering documentation maintenance and developer portals. | OpenAPI spec generation, schema deduction, technical documentation. |
| 20 | [Personal Finance Transaction Categorizer](./20-personal-finance-expense-categorizer/README.md) | Fintech consumer apps (Mint, YNAB, Revolut) and expense tracking. | Unstructured text categorization, merchant normalization, summary aggregation. |
| 21 | [Prompt Injection & Jailbreak Defense Firewall](./21-prompt-injection-firewall-guardrail/README.md) | AI safety gateway, OWASP Top 10 for LLMs compliance, public chatbot hardening. | Adversarial input detection, multi-stage guardrails, input sanitization, threat classification. |
| 22 | [LLM Rate Limit & Quota Circuit Breaker (Resilience)](./22-llm-rate-limit-and-quota-fallback-circuit-breaker/README.md) | High-availability enterprise LLM infrastructure, resilient production APIs. | Circuit breaker pattern, exponential backoff, multi-model fallback chains (`with_fallbacks`). |
| 23 | [RAG Empty, Scanned & Corrupt Document Resilience](./23-rag-empty-and-corrupt-document-handler/README.md) | Enterprise document processing systems dealing with messy real-world files. | File validation, OCR fallback (pytesseract/pdf2image), corrupt file quarantining, exception isolation. |
| 24 | [Self-Healing JSON Schema Parser (Output Repair)](./24-json-schema-healing-and-retry-parser/README.md) | High-reliability backend services consuming structured LLM outputs. | Output parsing defense, JSON recovery algorithms, OutputFixingParser. |
| 25 | [Autonomous Agent Loop Watchdog & Budget Guard](./25-infinite-loop-and-token-budget-watchdog/README.md) | Agentic production reliability, cloud cost containment, DoS prevention. | Loop guardrails, state-based step counters, token budget tracking, timeout decorators. |
