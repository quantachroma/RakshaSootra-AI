
#  RakshaSootra AI (रक्षा सूत्र)
### AI-Powered Digital Public Safety Intelligence Platform

> **RakshaSootra AI** is an Agentic AI platform that proactively protects citizens from digital fraud by detecting phishing links, digital arrest scams, suspicious financial transactions, and fraudulent investment schemes before financial loss occurs.

---

##  Problem Statement

Built for the **Economic Times AI Hackathon 2026** — **Problem Statement #6**
> **AI for Digital Public Safety: Defeating Counterfeiting, Fraud & Digital Arrest Scams**

With cyber fraud increasing every year, victims often realise they are being scammed only after money has already been transferred. Existing systems focus on post-incident investigation rather than prevention.

RakshaSootra AI shifts cybersecurity from **reactive investigation** to **proactive prevention** operating on the **"Citizen as Sensor"** paradigm.

---

## 💡 Our Solution

RakshaSootra AI is a **multi-agent AI system** that intelligently analyses different types of suspicious inputs. Instead of using one large AI model for everything, the platform routes each input to a specialized AI agent designed specifically for that threat vector.

Our platform protects citizens across four major fraud entry points:

| Threat Vector | AI Agent | Core Capability |
| :--- | :--- | :--- |
| **Phishing Links** | `Link Shield` | Analyzes URLs for typosquatting, domain age, WHOIS flags, and fake login pages. |
| **Digital Arrest Calls & Messages** | `Scam Script Checker` | Detects coercion language, digital arrest threats, fake ED/CBI calls, and authority impersonation using ChromaDB RAG. |
| **Suspicious Transactions** | `Transaction Guard` | Checks UPI handle patterns, flags unverified payees, velocity limits, and enforces cooling-off timers. |
| **Fake Investment Schemes** | `Investment Verifier` | Cross-checks investment schemes against registered SEBI databases to detect high-yield Ponzi algorithms. |

---

## ✨ Key Features

- **Multi-Agent AI Architecture:** Specialized agents for link, script, payment, and investment vectors.
- **LangGraph-based Intelligent Routing:** Intent classification engine directing queries to the right specialist.
- **Two-Stage Detection Engine:** Fast deterministic rule checks followed by LLM fallback verification.
- **Regulatory RAG Grounding:** Cross-references scam scripts with official MHA/RBI advisories using ChromaDB.
- **Fraud Entity Extraction:** Regex & NLP engine capturing UPI IDs, phone numbers, and domain URLs.
- **Fraud Intelligence Graph:** Interactive NetworkX graph linking shared scam infrastructure across reports.
- **Dual Dashboard:** Citizen Self-Defense Portal + Law Enforcement Agency (LEA) Intelligence Dashboard.

---

## 📐 System Architecture

RakshaSootra follows a **Two-Stage Hybrid Intelligence Pipeline** to reduce API costs, eliminate hallucinations, and deliver instant responses:

```text
                        Citizen Input
                              │
                              ▼
                     Streamlit Interface
                              │
                              ▼
                    LangGraph Router Agent
                              │
         ┌────────────┬───────┴────────┬────────────┐
         ▼            ▼                ▼            ▼
    Link Shield  Scam Script  Transaction Guard  Investment Verifier
         │            │                │            │
         └────────────┴───────┬────────┴────────────┘
                              │
                              ▼
                     Stage 1: Rule Engine
                (Python / WHOIS / Regex / SEBI DB)
                              │
                 ┌────────────┴────────────┐
                 │                         │
         (High Risk / Clear)       (Ambiguous / Complex)
                 │                         │
                 ▼                         ▼
         Immediate Verdict    Stage 2: Gemini 2.5 Flash
                                     (via OpenRouter)
                                           │
                                           ▼
                                 Unified Risk Verdict
                                           │
                                           ▼
                                   Entity Extraction
                                (UPIs / Phones / Domains)
                                           │
                                           ▼
                                Fraud Intelligence Graph
                                           │
                                           ▼
                                 Citizen + LEA Dashboard

```

---

## 🛠️ Tech Stack Overview

| Layer | Technology / Tool | Application in RakshaSootra |
| --- | --- | --- |
| **User Interface** | **Streamlit** | Core web framework for Citizen Reporting Portal and LEA Dashboard. |
| **Graph Visualization** | **streamlit-agraph** | Interactive UI rendering of the Fraud Entity Graph for Law Enforcement. |
| **Agent Orchestration** | **LangGraph & LangChain** | State-driven workflow routing, intent classification, and multi-agent dispatching. |
| **LLM Engine** | **Gemini 2.5 Flash** *(via OpenRouter)* | Stage-2 hybrid reasoning engine for complex, ambiguous scam scripts & pitches. |
| **Vector DB & RAG** | **ChromaDB** | Local persistent vector database storing chunked MHA & RBI advisory embeddings. |
| **Embeddings** | **Sentence-Transformers** `all-MiniLM-L6-v2` | Dense vector embeddings for advisory chunk matching. |
| **Graph Analytics** | **NetworkX** | Entity-relation triples (UPIs, phones, domains) mapping crime syndicates. |
| **Rule & Regex Engine** | **Pure Python / Levenshtein** | Stage-1 deterministic checks (typosquatting distance, WHOIS, regex pattern matching). |
| **Database & Schema** | **SQLite3** | Relational storage for user reports, entity mappings, and historical logs. |
| **Data Validation** | **Pydantic (v2)** | Defining strict schema contracts and typed verdict output structures across agents. |
| **Runtime & Testing** | **Python 3.10+ / Pytest** | Execution runtime, unit testing, and RAG quality evaluation. |

---

## 📂 Repository Structure

```text
RakshaSootra-AI/
├── agent/
│   ├── __init__.py
│   ├── router_agent.py          # Person 1: LangGraph Intent Classifier
│   ├── link_shield/             # Person 2: Phishing URL & Domain analysis
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── rules.py
│   │   ├── link_shield_agent.py
│   │   └── test_rules.py
│   ├── scam_script/             # Person 2: Digital Arrest & Coercion detection
│   │   ├── __init__.py
│   │   ├── build_rag_index.py   # RAG index initialization script
│   │   ├── models.py            # Pydantic schemas for verdicts
│   │   ├── rules.py             # Rule matching for CBI/ED/Police calls
│   │   ├── rag.py               # ChromaDB retrieval pipeline
│   │   ├── scam_script_agent.py # RAG + OpenRouter Gemini agent
│   │   ├── test_rules.py        # Rule heuristic unit tests
│   │   ├── test_rag_retrieval.py# Basic retrieval query tests
│   │   └── test_rag_quality.py  # RAG citation benchmark test
│   ├── transaction_guard/       # Person 3: UPI Payment safety checks
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── rules.py
│   │   ├── transaction_guard.py
│   │   └── test_rules.py
│   └── investment_verifier/     # Person 3: SEBI checks & Ponzi detection
│       ├── __init__.py
│       ├── models.py
│       ├── rules.py
│       ├── investment_verifier_agent.py
│       └── test_rules.py
├── data/
│   ├── rawFolder/               # Official MHA and RBI advisory .txt files
│   ├── processed/               # ChromaDB persistent vector index
│   └── sebi_registry.sqlite     # Offline SEBI registered entity database
├── docs/
│   ├── person1_router_platform.md
│   ├── person2_content_agents.md
│   └── person3_money_agents.md
├── tool/
│   ├── __init__.py
│   ├── chroma_client.py         # ChromaDB advisory collection helper
│   ├── db_client.py             # SQLite DB client for reports & graph data
│   ├── entity_extractor.py      # Regex parser for UPIs, phones, domains
│   ├── llm_client.py            # Centralized OpenRouter API client
│   └── whois_client.py          # WHOIS & domain lookup helper
├── ui/
│   ├── app.py                   # Main Streamlit Dashboard entry point
│   └── components/
│       ├── citizen_view.py      # Citizen input & safety report tab
│       └── lea_graph.py         # LEA Fraud Entity Graph visualizer
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

```

---

## Specialized AI Agents

### 1️⃣ Link Shield

* **Detects:** Phishing URLs, fake banking/government portals, typosquatting domains, newly created domain names (<30 days).
* **Techniques:** Levenshtein string distance, Python-WHOIS lookups, URL pattern regex, Gemini LLM fallback.

### 2️⃣ Scam Script Checker

* **Detects:** Digital arrest threats, fake CBI/ED/Police calls, authority impersonation, coercion, urgent money demands.
* **Techniques:** Deterministic keyword rules, ChromaDB vector RAG over official MHA/RBI circulars, OpenRouter LLM context analysis.

### 3️⃣ Transaction Guard

* **Detects:** Unverified UPI handles, suspicious payee patterns, rapid transfer velocity, high-risk payment requests.
* **Techniques:** VPA pattern validation, SQLite historical velocity tracking, automated cooling-off delay timers.

### 4️⃣ Investment Verifier

* **Detects:** Unregistered trading platforms, high-yield crypto Ponzi schemes, guaranteed return claims, fake SEBI advisors.
* **Techniques:** SQLite SEBI registration cross-checking, algorithmic return pattern detection, LLM pitch validation.

---

## 🕸️ Fraud Intelligence Graph

Whenever a scam is detected, the system extracts structured entities:

* **Phone Numbers**
* **UPI VPA IDs**
* **URLs & Domains**
* **Impersonated Agencies**

These entities are stored as triples in a central SQLite database. When multiple citizens report scams sharing identical or adjacent entities, the system links them automatically. Instead of isolated complaints, Law Enforcement receives a **connected syndicate intelligence graph**.

---

##  Team & Role Allocation

### Member 1 — Shraddha Tyagi (Platform Architecture & LEA Intelligence)

* **Core Responsibilities:**
* LangGraph Router Agent (`router_agent.py`) for intent routing.
* Streamlit Dashboard UI (`app.py`, `ui/components/`).
* NetworkX Fraud Intelligence Graph (`lea_graph.py`).
* SQLite database client and schema (`db_client.py`).



### Member 2 — Priyanshi Saini (Content Safeguards & RAG Engine)

* **Core Responsibilities:**
* `Link Shield` agent for phishing URL and WHOIS analysis.
* `Scam Script Checker` for digital arrest and coercion call detection.
* ChromaDB RAG retrieval pipeline (`rag.py`, `build_rag_index.py`).
* Prompt engineering & OpenRouter client integration.



### Member 3 — Ritisha Sharma (Financial Safeguards & Entity Extraction)

* **Core Responsibilities:**
* `Transaction Guard` agent for UPI payment security.
* `Investment Verifier` agent for SEBI registration checks.
* Regex & NLP entity extraction parser (`entity_extractor.py`).
* Integration of extracted entities into the Fraud Entity Graph.



---

##  Installation & Setup

### Prerequisites

* Python 3.10 or higher
* Git

### Step-by-Step Instructions

1. **Clone the repository:**
```bash
git clone [https://github.com/](https://github.com/)<username>/RakshaSootra-AI.git
cd RakshaSootra-AI

```


2. **Create and activate a virtual environment:**
```bash
python3 -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

```


3. **Install dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt

```


4. **Configure Environment Variables:**
Copy `.env.example` to `.env` and add your OpenRouter API Key:
```bash
cp .env.example .env

```


*Edit `.env`:*
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
DATABASE_PATH=data/raksha_sootra.db
CHROMA_DB_PATH=data/processed/chroma

```


5. **Initialize ChromaDB RAG Index (Mandatory First Run):**
```bash
python3 -m agent.scam_script.build_rag_index

```


6. **Run the Application:**
```bash
streamlit run ui/app.py

```



---

##  Testing

### Run All Unit Tests

```bash
pytest

```

### Run Module-Specific Rule Tests

```bash
python3 -m pytest agent/link_shield/test_rules.py -v
python3 -m pytest agent/scam_script/test_rules.py -v
python3 -m pytest agent/transaction_guard/test_rules.py -v
python3 -m pytest agent/investment_verifier/test_rules.py -v

```

### Run RAG Retrieval & Quality Verification

```bash
# Verify vector store retrieval
python3 -m pytest agent/scam_script/test_rag_retrieval.py -v

# Run RAG citation quality benchmark (Requires OPENROUTER_API_KEY)
python3 agent/scam_script/test_rag_quality.py

```

---

##  Future Enhancements

* **Voice Scam Detection:** Direct audio transcription via Whisper before script evaluation.
* **Deepfake Video Interception:** Real-time facial artifact detection for fake video calls.
* **WhatsApp & Telecom Integration:** Instant verification via WhatsApp bot and IVR helpline.
* **NCRP Automated Reporting:** Direct API integration with the National Cyber Crime Reporting Portal (1930).

---

##  Acknowledgements

* **Economic Times AI Hackathon 2026**
* **Ministry of Home Affairs (MHA) & NCRB**
* **Reserve Bank of India (RBI)**
* **CERT-In**
* **OpenRouter & Google Gemini**

---

## 📄 License

This repository is created exclusively for the **ET AI Hackathon 2026**. All rights reserved.

```

```
