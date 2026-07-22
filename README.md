# 🛡️ RakshaSootra AI
### The Digital Protective Thread

RakshaSootra (रक्षा सूत्र) — "a protective thread." Just as a physical raksha sootra is tied
around a wrist to safeguard a person, this system threads together individual citizen fraud
reports into one connected shield against digital scam syndicates.

AI for Digital Public Safety: Defeating Counterfeiting, Fraud & Digital Arrest Scams

Instead of treating every scam as an isolated incident, RakshaSootra acts as a unified security checkpoint that catches fraudsters at the four main doors they use to steal money: malicious
links, coercive calls/messages, manipulated payments, and fake investment pitches — and then
connects the dots across citizens to reveal the syndicate behind them.

---

## 🚨 The Problem — 4 Doors of Fraud

| Door | Description |
|---|---|
| 🔗 **The Link** | Phishing SMS/WhatsApp messages that steal UPI PINs |
| 📞 **The Call** | "Digital Arrest" scams impersonating CBI/Police, threatening jail time |
| 💰 **The Payment** | Panic-driven UPI transfers made under manipulation |
| 📈 **The Pitch** | Deepfake celebrity endorsements, fake trading apps promising unrealistic returns |

## ✈️ The Solution

| Threat Vector | AI Agent | Core Capability |
|---|---|---|
| Phishing Links | **Link Shield** | Analyzes URLs for typosquatting, domain age, WHOIS flags, and fake login pages |
| Digital Arrest Calls & Messages | **Scam Script Checker** | Detects coercion language, digital arrest threats, fake ED/CBI calls, and authority impersonation using ChromaDB RAG |
| Suspicious Transactions | **Transaction Guard** | Checks UPI handle patterns, flags unverified payees, velocity limits, and enforces cooling-off timers |
| Fake Investment Schemes | **Investment Verifier** | Cross-checks investment schemes against registered SEBI databases to detect high-yield Ponzi schemes |

---

## 🏗️ Architecture

```
                    ┌─────────────────────────────────┐
                    │     STREAMLIT FRONTEND (ui/app.py)│
                    │  Tab 1: Citizen Scan │ Tab 2: LEA │
                    └────────────┬─────────────────────┘
                                 │
                                 ▼
                       ┌───────────────────┐
                       │   ROUTER AGENT     │
                       │   (LangGraph)      │
                       └─────────┬──────────┘
           ┌───────────┬─────────┴────────┬────────────┐
           ▼           ▼                  ▼            ▼
     ┌──────────┐ ┌───────────┐   ┌───────────────┐ ┌────────────┐
     │   LINK   │ │ SCAM SCRIPT│  │  TRANSACTION   │ │ INVESTMENT │
     │  SHIELD  │ │  CHECKER   │  │     GUARD      │ │  VERIFIER  │
     └────┬─────┘ └─────┬──────┘   └───────┬────────┘ └─────┬──────┘
          │             │                  │                 │
          │      Stage 1: Rule / DB Check (fast, deterministic)
          │             │                  │                 │
          │      Stage 2: LLM Fallback (OpenRouter, ambiguous cases)
          │             │                  │                 │
          └─────────────┴──────┬───────────┴─────────────────┘
                                ▼
                     ┌─────────────────────┐
                     │  Unified Verdict     │
                     │  risk_level +        │
                     │  explanation +       │
                     │  extracted_entities  │
                     └──────────┬───────────┘
                                ▼
                     ┌─────────────────────┐
                     │  Fraud Entity Graph  │
                     │  (NetworkX, session)  │
                     └──────────┬───────────┘
                                ▼
                     ┌─────────────────────┐
                     │  LEA Intelligence Tab│
                     │  streamlit-agraph +   │
                     │  pydeck hotspot map   │
                     └─────────────────────┘
```

---

## 💻 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Orchestration | LangGraph |
| AI Reasoning | OpenRouter-hosted LLM (see `.env` for the configured model) |
| Rule Engine / Structured Data | SQLite (`raksha_sootra.db`) |
| Knowledge Retrieval | ChromaDB (RAG over MHA/RBI advisories, Scam Script agent) |
| Intelligence Mapping | NetworkX + streamlit-agraph |
| Geospatial View | pydeck |

---

## 👥 Team & Ownership

### 🧩 Person 1 — Shraddha Tyagi
**Platform, Router & Intelligence Layer**
Owns: Streamlit shell · Router Agent (LangGraph) · shared SQLite schema · Fraud Entity Graph ·LEA-style second tab.


### 🔗 Person 2 — Priyanshi Saini
**Content Checks (What a Scammer Sends You?)**
Owns: Link Shield Agent · Scam Script Checker Agent · (stretch) RAG upgrade via ChromaDB over
MHA/RBI advisories.

Defends the first two doors — the link someone clicks, and the call or message someone falls for. 
Both agents follow the same rule-check then LLM-check pattern,allowing shared pipelines for heuristic
pre-screening and grounded regulatory analysis..

### 💰 Person 3 — Ritisha Sharma
**Money Checks (What Happens to Your Money?)**
Owns: Transaction Guard Agent · Investment Verifier Agent · Entity Extraction (feeding Person
1's graph).

Full individual write-ups: [`docs/person1_router_platform.md`](docs/person1_router_platform.md) ·
[`docs/person2_content_agents.md`](docs/person2_content_agents.md) ·
[`docs/person3_money_agents.md`](docs/person3_money_agents.md)

---

## 📁 Project Structure

```
RakshaSootra-AI/
├── agent/
│   ├── router.py                    # LangGraph orchestrator (Person 1)
│   ├── link_shield/                 # Person 2
│   │   ├── link_shield_agent.py
│   │   ├── models.py
│   │   ├── rules.py
│   │   └── test_rules.py, test_edge_cases.py
│   ├── scam_script/                 # Person 2
│   │   ├── scam_script_agent.py
│   │   ├── rules.py
│   │   ├── rag.py, build_rag_index.py
│   │   └── test_rag_quality.py, test_rag_retrieval.py, test_rules.py
│   ├── transaction_guard/           # Person 3
│   │   ├── transaction_guard_agent.py
│   │   ├── models.py, rules.py, llm_checker.py, prompts.py
│   │   ├── transaction_simulator.py, insert_test_payees.py
│   │   └── test_rules.py
│   └── investment_verifier/         # Person 3
│       ├── investment_verifier_agent.py
│       ├── models.py, rules.py, llm_checker.py, prompts.py
│       └── test_agent.py, test_llm.py, test_rules.py, test_sebi_search.py
├── data/
│   ├── chroma_store/                # ChromaDB vector store (Scam Script RAG)
│   ├── rawFolder/                   # Source advisory documents
│   └── load_sebi_data.py            # Seeds SEBI-registered broker data
├── docs/
│   ├── person1_router_platform.md
│   ├── person2_content_agents.md
│   └── person3_money_agents.md
├── tool/
│   ├── db_client.py                 # SQLite connection + create_tables()
│   ├── chroma_client.py             # ChromaDB connection
│   ├── check_db.py
│   └── llm_client.py                # Shared OpenRouter LLM wrapper
├── ui/
│   └── app.py                       # Streamlit app (Person 1)
├── .env.example
├── .gitignore
├── raksha_sootra.db                 # SQLite database (generated, gitignored ideally)
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

**1. Clone and enter the project**
```bash
git clone <repo-url>
cd RakshaSootra-AI
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**
```bash
cp .env.example .env
```
Fill in your OpenRouter API key and any other required values in `.env`.

**5. Initialize the SQLite database**
This creates `raksha_sootra.db` with the `user_rules`, `payee_history`, and `sebi_registered`
tables required by Transaction Guard and Investment Verifier:
```bash
python -c "from tool.db_client import create_tables; create_tables()"
```

**6. Seed SEBI broker data (required for Investment Verifier)**
```bash
python data/load_sebi_data.py
```

**7. Build the RAG index (required for Scam Script Checker)**
```bash
python agent/scam_script/build_rag_index.py
```

**8. Run the app**
```bash
streamlit run ui/app.py
```

---

## 🧪 Testing

Each agent module includes its own test suite. Run all tests from the project root:
```bash
pytest
```
Or target a specific agent, e.g.:
```bash
pytest agent/investment_verifier/
```

For manual end-to-end testing through the actual UI (recommended before any demo), see the
test input examples in [`docs/person1_router_platform.md`](docs/person1_router_platform.md).

---

## 🕸️ Known Limitations

- Scam Script Checker's rule layer is deterministic; RAG-based advisory matching is a stretch
  goal and may not cover all scam variants.
- The LEA hotspot map currently uses static demo data, not live geolocation.
- Cross-report entity linking in the Fraud Entity Graph requires an exact match (e.g., identical
  UPI string) — fuzzy matching for near-duplicate entities is not yet implemented.
- The fraud graph resets when the Streamlit session restarts (in-memory via `st.session_state`,
  not yet persisted to a database).

---
## 📄 License

This repository is created exclusively for the **ET AI Hackathon 2026**. All rights reserved.
