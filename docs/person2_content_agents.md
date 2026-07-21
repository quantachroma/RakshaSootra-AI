

#  Member Documentation: Defense Subsystem & Agents

**Owner:** Priyanshi Saini (Person 2)

**Modules:** Link Shield Agent, Scam Script Checker Agent, RAG Subsystem, & Vector Store Engine

**Project:** RakshaSootra AI

---

##  1. Overview & Key Contributions

As **Person 2**, my primary responsibility in the RakshaSootra AI project was to design, implement, and validate a dual-layer threat detection engine consisting of two core AI agents—the **Link Shield Agent** and the **Scam Script Checker Agent**—backed by a persistent **Retrieval-Augmented Generation (RAG)** pipeline.

### Key Deliverables Achieved

* **Link Shield Agent (`agent/link_shield/`):** Engineered a multi-stage URL verification agent that detects phishing domains, typosquatting/homograph attacks, suspicious TLDs, IP-based URLs, and obfuscated redirect links.
* **Scam Script Checker Agent (`agent/scam_script/`):** Built an agent that evaluates suspicious text messages, WhatsApp forwards, and phone call scripts using a hybrid approach (deterministic rules + RAG advisory context + LLM reasoning).
* **Advisory Knowledge Base (`data/raw/`):** Standardized and indexed **23 raw `.txt` government and regulatory advisory files** published by the Ministry of Home Affairs (MHA I4C), RBI, CERT-In, and SEBI to serve as the ground-truth knowledge base.
* **Persistent Vector DB & RAG Subsystem (`tool/chroma_client.py` & `rag.py`):** Implemented a singleton ChromaDB client powered by local `sentence-transformers` (`all-MiniLM-L6-v2`) embeddings with cosine distance thresholding ($d \le 0.75$) to retrieve relevant advisory context without external latency.
* **Full Test Coverage & Quality Validation:** Built a unit and integration test harness (`test_rules.py`, `test_rag_retrieval.py`, `test_rag_quality.py`) achieving a **100% pass rate (9/9 tests)** and meeting all live LLM advisory citation targets.

---

##  2. System Architecture & File Structure

```text
RakshaSootra-AI/
├── data/
│   ├── raw/                           # Ground-Truth Advisory Corpus (23 .txt files)
│   │   ├── digital_arrest_scam_advisory.txt
│   │   ├── fake_job_offer_sms_scam.txt
│   │   ├── electricity_bill_kyc_phishing.txt
│   │   └── ... (20 additional official advisory files)
│   └── chroma_store/                  # Persistent ChromaDB vector storage index
├── tool/
│   └── chroma_client.py               # Singleton persistent ChromaDB client initialization
└── agent/
    ├── link_shield/                   # LINK SHIELD AGENT
    │   ├── agent.py                   # Main Link Shield orchestrator
    │   ├── heuristics.py              # URL parsing, entropy check, and pattern matching
    │   └── models.py                  # Pydantic schemas for URL inspection requests/responses
    └── scam_script/                   # SCAM SCRIPT CHECKER AGENT
        ├── models.py                  # Request/Response schemas for script evaluation
        ├── rules.py                   # Deterministic regex & keyword pattern matcher
        ├── rag.py                     # Vector search & distance-threshold filtering engine
        ├── scam_script_agent.py       # Main agent orchestrator (Rules -> RAG -> LLM Reasoning)
        ├── build_rag_index.py         # CLI utility to chunk and index raw .txt advisories
        ├── test_rules.py              # Unit tests for deterministic rule engine
        ├── test_rag_retrieval.py      # Unit tests for RAG vector retrieval & file indexing
        └── test_rag_quality.py        # Quality QA test verifying live LLM citations (>=3/5 target)

```

---

##  3. Component Breakdown

### A. Link Shield Agent

The **Link Shield Agent** acts as the front-line shield against web-based phishing and malicious links:

1. **Heuristic Pre-Screening:** Inspects target URLs for suspicious patterns (e.g., raw IP addresses, excessive subdomains, brand typosquatting like `hdfc-bank-verify.com`, dangerous TLDs like `.zip` or `.top`).
2. **Entropy & Obfuscation Detection:** Measures domain entropy and checks for double URL encoding or shortened redirect chains.
3. **Structured Threat Reporting:** Returns a structured verdict (`safe`, `suspicious`, `malicious`) with explicit warning tags for the frontend interface.

### B. Scam Script Checker Agent

The **Scam Script Checker Agent** uses a defense-in-depth pipeline to analyze social engineering transcripts:

1. **Rule Engine (`rules.py`):** Pre-screens text using deterministic regex matchers for immediate red flags (digital arrest threats, fake CBI/Police authority, urgent bank block warnings, guaranteed investment returns).
2. **RAG Context Injection (`rag.py`):** Queries ChromaDB to find matching government advisories from the `data/raw/` corpus.
3. **LLM Synthesis & Citation:** Combines the user script, deterministic flags, and retrieved advisory chunks into a unified prompt to generate user-friendly explanations with official citations.

### C. ChromaDB Engine & Raw Advisory Corpus (`data/raw/`)

* **Data Corpus:** Contains **23 curated `.txt` files** covering official advisories (Digital Arrest, Electricity Bill Phishing, FASTag Fraud, Fake Job Offers, Stock Market Advisory Scams, etc.).
* **Indexing Utility (`build_rag_index.py`):** Iterates through all `.txt` files in `data/raw/`, cleans content, generates semantic embeddings via `all-MiniLM-L6-v2`, and upserts them into ChromaDB idempotently.
* **Threshold Filtering:** Enforces a strict cosine distance cutoff ($d \le 0.75$) so that irrelevant context is never passed to the LLM.

---

##  4. Prompt Iterations & Engineering

Optimizing the LLM synthesis required multiple design iterations to ensure strict grounding and prevent hallucinations across both agents.

###  Iteration 1: Naive Free-Form Generation

* **Approach:** Sent user scripts or URLs directly to the LLM with a generic prompt: *"Analyze this content and tell me if it is a scam and cite any government advisories."*
* **Drawbacks:** The LLM hallucinated non-existent advisory numbers/titles and produced inconsistent JSON output structures that broke downstream UI rendering.

###  Iteration 2: Unfiltered RAG Context Injection

* **Approach:** Injected all top-$k$ retrieved vector chunks into the system prompt regardless of similarity distance.
* **Drawbacks:** When given a completely safe message (e.g., *"Meeting confirmed at 4 PM"*), the LLM still tried to force a citation from low-confidence vector results.

###  Iteration 3 (Production Standard): Guardrailed Synthesis with Strict Grounding

* **Approach:**
1. Enforced threshold filtering ($d \le 0.75$) at the Python level before prompt construction.
2. Defined explicit citation guardrails: **"Only cite an advisory if its exact filename is provided in the [RETRIEVED ADVISORIES] block. If empty, do not cite external documents."**
3. Structured response parameters through Pydantic data models (`models.py`) to guarantee consistent output formatting.



```text
[SYSTEM PROMPT TEMPLATE]
You are RakshaSootra AI's Fraud Analysis Specialist.
Evaluate the user submission using the deterministic flags and official advisory context provided below.

CRITICAL GROUNDING RULES:
- If [RETRIEVED ADVISORIES] contains context, explicitly cite the advisory document in your explanation.
- If [RETRIEVED ADVISORIES] is empty, rely on general safety analysis and DO NOT invent advisory names.

[USER SUBMISSION]
{submission_text}

[DETERMINISTIC RULE MATCHES]
{rule_flags}

[RETRIEVED ADVISORIES]
{rag_context}

```

---

##  5. Quality Assurance & Evaluation Results

All modules were validated using `pytest` across unit, integration, and quality evaluation suites.

```powershell
python -m pytest agent/scam_script/ -v

```

### Test Execution Summary

| Test Module | Focus Area | Status | Key Metric |
| --- | --- | --- | --- |
| `test_rules.py` | Deterministic Rule Matching | **PASSED** | Correctly catches known scam patterns and allows safe messages. |
| `test_rag_retrieval.py` | Vector Search & Corpus Coverage | **PASSED** | Confirms all 23 `.txt` files in `data/raw/` are indexed and retrievable. |
| `test_rag_quality.py` | End-to-End LLM Citation Quality | **PASSED** | **4/5 samples cited official advisories** (Exceeds target of $\ge 3/5$). |
| **Total Test Suite** | **All Modules** | **9 / 9 PASSED** | **100% Pass Rate** |

---

##  6. Known Limitations & Future Roadmap

1. **Multilingual Script Parsing:**
* *Current Limitation:* Rule matching and RAG embeddings are currently tuned for English and Romanized text (Hinglish).
* *Roadmap:* Integrate multilingual sentence transformers (e.g., `paraphrase-multilingual-MiniLM-L12-v2`) to better analyze native Hindi and regional language scripts.


2. **Real-Time Live URL Sandbox:**
* *Current Limitation:* Link Shield performs heuristic, structural, and domain-pattern checks locally.
* *Roadmap:* Integrate headless browser sandboxing (e.g., Playwright) to capture dynamic page screenshots and analyze live DOM trees for phishing forms.


3. **Automated Advisory Synchronization:**
* *Current Limitation:* Knowledge base relies on static `.txt` advisory files in `data/raw/`.
* *Roadmap:* Build an automated scraper pipeline to fetch new cybercrime advisories directly from MHA I4C and RBI RSS feeds to keep the ChromaDB index continuously updated.