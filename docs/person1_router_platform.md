# RakshaSootra AI — Person 1 Contribution Document
**Owner:** Shraddha Tyagi
**Ownership Areas:** Router Agent · Platform Architecture · LEA Fraud Entity Graph

---

## 1. Role Summary

As Person 1, I owned the backbone of RakshaSootra AI — the piece that ties all four specialist
agents together and the intelligence layer that turns individual citizen reports into a connected
fraud network for law enforcement. Concretely, this covered three areas:

1. **Router Agent** — the LangGraph orchestrator that classifies incoming citizen input and
   dispatches it to the correct specialist agent.
2. **Platform Architecture** — the Streamlit application shell, state management, and
   integration layer that holds all four agents together as one working product.
3. **LEA Fraud Entity Graph** — the "secret weapon" feature: a live, growing network graph
   that connects entities (UPI IDs, phone numbers, domains) across different citizen reports,
   surfacing potential fraud syndicates instead of treating each report in isolation.

---

## 2. Router Agent

**File:** `agent/router.py`

- Built using `LangGraph`'s `StateGraph`, with a shared `AgentState` (TypedDict) carrying
  `user_input`, `input_type`, `risk_level`, `explanation`, and `extracted_entities` across
  every node.
- `classify_input()` performs keyword/pattern-based routing:
  - Link-like input (`http`, `.com`, `.xyz`, `.in`) → Link Shield
  - Transaction language (`upi`, `paid`, `debited`, `transfer`) → Transaction Guard
  - Investment language (`invest`, `returns`, `crypto`, `sebi`) → Investment Verifier
  - Everything else → Scam Script Checker
- Conditional edges route to exactly one of the four specialist agents, each terminating at `END`.
- Verified working end-to-end for all four categories after integration testing (see §5).

---

## 3. Platform Architecture

**File:** `ui/app.py`

- Streamlit shell with two tabs: **Check Suspicious Activity** (citizen-facing scanner) and
  **LEA Intelligence** (law-enforcement-facing graph + hotspot view).
- State management via `st.session_state`, since Streamlit reruns the full script on every
  interaction — the fraud graph (`networkx.Graph`) is initialized once per session and persists
  across scans without needing a database.
- Wired the router's output (`risk_level`, `explanation`, `extracted_entities`) directly into the
  UI's verdict display (color-coded HIGH RISK / SUSPICIOUS / SAFE / UNKNOWN states).
- Added visual polish: distinct LEA tab styling (dark background + saffron accent border),
  button hover states, rounded verdict-box corners.

---

## 4. LEA Fraud Entity Graph

**Stack:** `networkx` + `streamlit-agraph` + `pydeck`

### 4.1 Design
Each citizen report becomes its own graph node, connected to every entity extracted from it
(UPI ID, phone number, domain, platform name). Two reports that happen to share an entity —
even if submitted by different citizens, about seemingly unrelated scams — become visually
linked through that shared node. This is what allows the graph to reveal a fraud syndicate
network instead of a list of disconnected incidents.

### 4.2 Implementation
- `seed_fake_reports()` — 10 pre-loaded demo reports with deliberate entity overlaps, used to
  demonstrate syndicate-linking behavior without waiting on live data.
- `update_fraud_graph()` — hooks into every live scan result; creates a new report node and
  links it to whatever entities the router returned, regardless of which agent produced them.
- `render_fraud_graph()` — renders the graph with `streamlit-agraph`, color-coded by entity
  type (green = UPI, blue = phone, saffron = domain, amber = platform, gray = report), with
  truncated labels and a legend.
- `render_hotspot_map()` — a `pydeck` scatter + text layer showing static demo fraud hotspots
  across major Indian cities, bordered and cached for performance.

### 4.3 Verified Behavior
- Confirmed via live testing: a real transaction scan sharing a UPI ID with a seeded report
  correctly produced a visible graph connection (**Entities Tracked: 22, Connections Found: 16**
  at last test).
- Confirmed rendering performance holds after 8-10 back-to-back live scans with no visible lag.

---

## 5. Integration Testing & Bugs Found

As part of end-to-end integration testing across all four agents, the following issues were
identified and resolved:

| # | Bug | Root Cause | Fix | Owner |
|---|---|---|---|---|
| 1 | Link Shield never short-circuited on confirmed high-risk links (typosquat/raw IP), silently falling through to slower LLM path | `risk_level` string mismatch — `"high risk"` (space) in `rules.py` vs. `"high_risk"` (underscore) expected in `link_shield_agent.py` | Corrected both `rules.py` return statements to use `"high_risk"` | Person 1 (flagged), Person 2 (file owner) |
| 2 | App crashed on startup: `ImportError: cannot import name 'run_transaction_guard'` | Stray triple-quote characters (`''''` / `"""`) accidentally wrapped the entire function definition as a string literal, twice, on two separate occasions | Removed stray quote characters, restored valid function syntax | Person 1 (diagnosed + fixed) |
| 3 | Investment Verifier crashed: `sqlite3.OperationalError: no such table: sebi_registered` | DB schema (`create_tables()` in `tool/db_client.py`) existed but was never executed on a fresh clone | Ran `create_tables()` once to initialize `raksha_sootra.db` with all required tables | Person 1 (diagnosed + fixed) |
| 4 | Transaction Guard crashed: `sqlite3.OperationalError: no such table: user_rules` | Same root cause as #3 — same fix resolved both simultaneously | Same as #3 | Person 1 |
| 5 | LEA graph nodes rendering overlapped/unreadable at scale | Fixed random coordinate spread was too tight for growing node count; long entity labels had no truncation | Switched to physics-based layout for connected graphs, added label truncation + legend | Person 1 |

---

## 6. Known Limitations (Honest Status)

- **Scam Script Checker** is still a hardcoded stub — always returns the same fixed phone
  number and explanation regardless of actual input text. Functional for demo purposes but
  not yet running real detection logic.
- **Hotspot map uses static demo data**, not live geolocation from actual reports.
- **Cross-report linking only works when entities exactly match** (e.g., identical UPI string).
  Fuzzy-matching similar-but-not-identical entities (e.g., minor UPI typos) is not yet built.
- **Tab-switch fade animation** was attempted via CSS but not completed — Streamlit 1.59's
  internal DOM structure differs from the selectors initially used; parked as low-priority
  cosmetic polish.

---

## 7. Summary

The Router Agent, application shell, and LEA Fraud Entity Graph are fully functional and
integration-tested against all four specialist agents. Four integration-blocking bugs were
found and resolved during testing, unblocking Transaction Guard and Investment Verifier for
the whole team. The graph's core "citizen as sensor" behavior — connecting otherwise unrelated
reports through shared fraud entities — is confirmed working end-to-end.