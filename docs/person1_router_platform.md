🛡️ Member Documentation: Platform Architecture & Intelligence Orchestration
Owner: Shraddha Tyagi (Person 1)
Modules: LangGraph Router, Streamlit Platform, Shared SQLite Schema, & Fraud Entity Graph (LEA Intelligence)
Project: RakshaSootra AI
1. Overview & Key Contributions
As Person 1, my primary responsibility was to design the overarching system architecture and build the "connective tissue" of RakshaSootra AI. I engineered the central orchestration layer that transforms four independent security agents into a unified, stateful defense platform.
Key Deliverables Achieved
LangGraph Router Agent (agent/router.py): Developed the "Airport Security" orchestrator using LangGraph. It implements a hybrid heuristic-classifier that identifies threat vectors (Link, Message, Payment, or Investment) and routes them to specialized agents while maintaining a shared AgentState.
Streamlit Command Center (ui/app.py): Built a dual-view dashboard. The Citizen View provides a simplified "one-box" interface for threat analysis, while the LEA View provides a high-level intelligence dashboard for law enforcement.
Shared State & Data Contract: Defined the AgentState TypedDict, which acts as a "digital luggage tag," ensuring seamless data flow and consistent JSON schemas across all team members' modules.
Fraud Entity Graph (LEA Intelligence): Engineered a relational intelligence engine using NetworkX and streamlit-agraph. This system extracts entities (UPI IDs, Phone Numbers, Domains) and visually "threads" (Sootra) disparate reports together to map criminal syndicates.
Shared Infrastructure: Established the project’s foundation, including the tool/llm_client.py (OpenRouter integration), .env security protocols, and the shared SQLite database schema to unblock money-side rule checks.
2. System Architecture & File Structure
code
Text
RakshaSootra-AI/
├── ui/
│   └── app.py                  # Main Streamlit Shell & UI Logic
├── agent/
│   ├── router.py               # LangGraph Orchestrator & State Machine
│   ├── __init__.py             # Package initialization for absolute imports
│   └── ... (Agent Subfolders)
├── tool/
│   ├── llm_client.py           # Shared OpenRouter/Llama-3 Client
│   ├── database.py             # Shared SQLite Schema & Connection Logic
│   └── check_db.py             # DB Verification Utilities
├── data/
│   └── processed/
│       └── raksha_sootra.db    # Shared SQLite Database File
└── utils/
    └── graph_utils.py          # NetworkX Logic & Entity Mapping
3. Component Breakdown
A. LangGraph Router (The "Traffic Cop")
The router is the brain of the platform. It prevents "Agent Overload" by ensuring only the relevant specialist looks at the user's input.
Heuristic Classification: Uses regex and keyword matching to instantly categorize input, saving LLM tokens and reducing latency.
Stateful Orchestration: Manages the AgentState object, ensuring that risk_level and extracted_entities are preserved as the data moves from the classifier to the specialist agents.
Error Handling: Implemented "Fallback Nodes" to ensure the UI remains stable even if an individual agent module fails.
B. LEA Intelligence Graph (The "Sootra")
This module implements the project's core "Citizen as Sensor" pivot:
Entity Extraction: Automatically pulls UPI IDs, Phone Numbers, and Domains from agent verdicts.
Relational Mapping: Uses NetworkX to create edges between different citizen reports that share the same fraud entity.
Syndicate Visualization: Renders a dynamic, color-coded graph where clusters represent potential fraud rings rather than isolated incidents.
C. Shared SQLite Schema
Designed a lightweight, persistent storage layer to support deterministic security checks:
user_rules: Stores personalized safety thresholds (e.g., ₹10,000 limit).
payee_history: Tracks successful past transactions to identify "New Payee" risks.
sebi_list: A searchable index of registered investment intermediaries.
4. Orchestration Iterations & Engineering
Ensuring a seamless "one-click" experience required multiple iterations of the orchestration logic.
Iteration 1: Independent Tools
Approach: Each agent had its own UI and logic.
Drawbacks: Users had to know which tool to use. No data was shared between reports, making it impossible to see the "big picture."
Iteration 2: Simple LLM Routing
Approach: Used an LLM to decide which agent should run.
Drawbacks: Added 2-3 seconds of latency and increased API costs for every single query, even for obvious links.
Iteration 3 (Production Standard): LangGraph Hybrid Router
Approach:
Implemented a Heuristic Layer for 0-latency classification.
Used LangGraph to create a formal state machine.
Standardized the Agent Return Schema so the UI could dynamically render results regardless of which agent was triggered.
5. Quality Assurance & Integration Testing
I managed the "Integration Day" (Day 5) to ensure all subsystems communicated without errors.
Integration Execution Summary
Test Area	Focus	Status	Result
State Flow	Data passing between Router and Agents	PASSED	AgentState remains intact across all 4 routing paths.
Import Integrity	Absolute vs Relative pathing	PASSED	Fixed sys.path issues allowing UI to run from root.
Graph Persistence	Data retention across tab switches	PASSED	Used st.session_state to prevent graph resets.
End-to-End	Zero-to-Verdict latency	PASSED	Average response time < 4 seconds using Llama-3-8B.
6. Known Limitations & Future Roadmap
Real-Time Database Triggers:
Current Limitation: The LEA Graph updates only when the tab is refreshed or a new scan is run.
Roadmap: Implement a real-time listener (e.g., via Supabase or WebSockets) to update the graph instantly as reports come in nationwide.
Advanced Graph Analytics:
Current Limitation: The graph shows connections but doesn't "score" the risk of a cluster.
Roadmap: Implement PageRank or Community Detection algorithms to automatically flag "High-Density Fraud Hubs" for LEA priority.
Cross-Platform Input:
Current Limitation: System relies on manual text/link pasting.
Roadmap: Develop a browser extension and WhatsApp bot that pipes data directly into the RakshaSootra Router via API.