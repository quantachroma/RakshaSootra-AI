from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END
import re

# ==========================================
# TASK 1: DEFINE THE SHARED STATE
# ==========================================
# This is the "luggage tag" passed between agents
class AgentState(TypedDict):
    user_input: str
    input_type: str          # 'link', 'message', 'transaction', 'investment'
    risk_level: str          # 'safe', 'risky', 'high_risk'
    explanation: str         # Plain language explanation of the verdict
    extracted_entities: Dict # e.g., {"upi": [], "phone": [], "domain": []}

# ==========================================
# TASK 2: CLASSIFICATION LOGIC
# ==========================================
def classify_input(state: AgentState) -> AgentState:
    """Analyzes the raw input and determines which scanner it goes to."""
    text = state["user_input"].lower()
    
    # Simple heuristic routing
    if "http://" in text or "https://" in text or re.search(r'\.[a-z]{2,3}(/|$)', text):
        state["input_type"] = "link"
    elif any(word in text for word in ["rs.", "inr", "upi", "paid", "transfer", "debited"]):
        state["input_type"] = "transaction"
    elif any(word in text for word in ["invest", "returns", "profit", "trading", "crypto", "sebi"]):
        state["input_type"] = "investment"
    else:
        # Default to message/script checker
        state["input_type"] = "message"
        
    return state

# ==========================================
# TASK 3: PLACEHOLDER NODES (The 4 Scanners)
# ==========================================
def link_shield_node(state: AgentState) -> AgentState:
    state["risk_level"] = "high_risk"
    state["explanation"] = "[Mock Link Shield] This domain is newly registered and uses typosquatting."
    state["extracted_entities"] = {"domain": ["hdfc-update-kyc.xyz"]}
    return state

def scam_script_node(state: AgentState) -> AgentState:
    state["risk_level"] = "high_risk"
    state["explanation"] = "[Mock Scam Script] Matches 'Digital Arrest' fear tactics. CBI does not call via WhatsApp."
    state["extracted_entities"] = {"phone": ["+91-9876543210"]}
    return state

def transaction_guard_node(state: AgentState) -> AgentState:
    state["risk_level"] = "risky"
    state["explanation"] = "[Mock Txn Guard] Amount exceeds your 10k threshold and payee is new."
    state["extracted_entities"] = {"upi": ["scammer@ybl"]}
    return state

def investment_verifier_node(state: AgentState) -> AgentState:
    state["risk_level"] = "risky"
    state["explanation"] = "[Mock Invest Verifier] Platform promises 'guaranteed returns' but is not on SEBI list."
    state["extracted_entities"] = {"platform": ["CryptoMax Profit"]}
    return state

# ==========================================
# BUILD THE LANGGRAPH WORKFLOW
# ==========================================
def route_to_agent(state: AgentState) -> str:
    """Reads the input_type and tells LangGraph which node to go to next."""
    return state["input_type"]

workflow = StateGraph(AgentState)

# Add all nodes
workflow.add_node("classifier", classify_input)
workflow.add_node("link", link_shield_node)
workflow.add_node("message", scam_script_node)
workflow.add_node("transaction", transaction_guard_node)
workflow.add_node("investment", investment_verifier_node)

# Set the entry point
workflow.set_entry_point("classifier")

# Add conditional edges from the classifier to the specific agents
workflow.add_conditional_edges(
    "classifier",
    route_to_agent,
    {
        "link": "link",
        "message": "message",
        "transaction": "transaction",
        "investment": "investment"
    }
)

# All agents end the workflow after they do their job
workflow.add_edge("link", END)
workflow.add_edge("message", END)
workflow.add_edge("transaction", END)
workflow.add_edge("investment", END)

# Compile the router
rakshasootra_router = workflow.compile()

# ==========================================
# TASK 4: TEST ROUTING WITH 4 HARDCODED INPUTS
# ==========================================
if __name__ == "__main__":
    print("🛡️ Testing RakshaSootra Router...\n")
    
    test_inputs = [
        "Please update your KYC here: http://hdfc-update-kyc.xyz",
        "CBI Alert: Your Aadhaar is suspended. Pay fine immediately.",
        "Paid Rs. 15000 to unknown@ybl",
        "Invest 5000 today and get guaranteed 200% returns in crypto!"
    ]
    
    for text in test_inputs:
        print(f"📥 Input: {text}")
        
        # Initialize empty state
        initial_state = {
            "user_input": text,
            "input_type": "",
            "risk_level": "",
            "explanation": "",
            "extracted_entities": {}
        }
        
        # Run the graph
        result = rakshasootra_router.invoke(initial_state)
        
        print(f"🔀 Routed to: {result['input_type'].upper()} Agent")
        print(f"⚠️ Verdict: {result['risk_level']}")
        print(f"📝 Explanation: {result['explanation']}\n")
        print("-" * 50 + "\n")
        