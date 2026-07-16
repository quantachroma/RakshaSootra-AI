# Owner- Shraddha Tyagi 
from typing import TypedDict, Dict
from langgraph.graph import StateGraph, END
import re

# --- 1. SHARED STATE ---
class AgentState(TypedDict):
    user_input: str
    input_type: str          
    risk_level: str          
    explanation: str         
    extracted_entities: Dict 

# --- 2. AGENT NODES (Mock Logic for Day 4 Demo) ---
# These will be replaced by real imports on Day 5
def run_link_shield(state: AgentState) -> AgentState:
    state["risk_level"] = "high_risk"
    state["explanation"] = "CRITICAL: This URL uses a 'typosquatted' domain (fake bank name) and matches known phishing patterns."
    state["extracted_entities"] = {"domain": ["hdfc-update-kyc.xyz"]}
    return state

def run_scam_script(state: AgentState) -> AgentState:
    state["risk_level"] = "high_risk"
    state["explanation"] = "Matches 'Digital Arrest' patterns. Real authorities (CBI/Police) never conduct legal proceedings via WhatsApp."
    state["extracted_entities"] = {"phone": ["+91-9876543210"]}
    return state

def run_transaction_guard(state: AgentState) -> AgentState:
    state["risk_level"] = "risky"
    state["explanation"] = "This transaction exceeds your ₹10,000 safety limit for a recipient you have never paid before."
    state["extracted_entities"] = {"upi": ["scammer@ybl"]}
    return state

def run_investment_verifier(state: AgentState) -> AgentState:
    state["risk_level"] = "high_risk"
    state["explanation"] = "SCAM ALERT: 'Guaranteed 200% returns' is a hallmark of Ponzi schemes. This platform is NOT SEBI-registered."
    state["extracted_entities"] = {"platform": ["CryptoMax Profit"]}
    return state

# --- 3. CLASSIFICATION LOGIC ---
def classify_input(state: AgentState) -> AgentState:
    text = state["user_input"].lower()
    if "http" in text or ".com" in text or ".xyz" in text:
        state["input_type"] = "link"
    elif any(word in text for word in ["rs.", "inr", "upi", "paid", "transfer"]):
        state["input_type"] = "transaction"
    elif any(word in text for word in ["invest", "returns", "profit", "crypto"]):
        state["input_type"] = "investment"
    else:
        state["input_type"] = "message"
    return state

def route_to_agent(state: AgentState) -> str:
    return state["input_type"]

# --- 4. GRAPH ASSEMBLY ---
workflow = StateGraph(AgentState)
workflow.add_node("classifier", classify_input)
workflow.add_node("link", run_link_shield)
workflow.add_node("message", run_scam_script)
workflow.add_node("transaction", run_transaction_guard)
workflow.add_node("investment", run_investment_verifier)

workflow.set_entry_point("classifier")
workflow.add_conditional_edges("classifier", route_to_agent, {
    "link": "link", "message": "message", "transaction": "transaction", "investment": "investment"
})
workflow.add_edge("link", END)
workflow.add_edge("message", END)
workflow.add_edge("transaction", END)
workflow.add_edge("investment", END)

rakshasootra_router = workflow.compile()
