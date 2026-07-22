# Owner- Shraddha Tyagi 
from typing import TypedDict, Dict
from langgraph.graph import StateGraph, END
import re


from agent.link_shield.link_shield_agent import run_link_shield
from agent.scam_script.scam_script_agent import run_scam_script
from agent.transaction_guard.transaction_guard_agent import run_transaction_guard
from agent.investment_verifier.investment_verifier_agent import run_investment_verifier

class AgentState(TypedDict):
    user_input: str
    input_type: str          
    risk_level: str          
    explanation: str         
    extracted_entities: Dict 

def classify_input(state: AgentState) -> AgentState:
    text = state["user_input"].lower()
    # Logic to decide which agent to call
    if "http" in text or ".com" in text or ".xyz" in text or ".in" in text:
        state["input_type"] = "link"
    elif any(word in text for word in ["rs.", "inr", "upi", "paid", "transfer", "debited", "account"]):
        state["input_type"] = "transaction"
    elif any(word in text for word in ["invest", "returns", "profit", "trading", "crypto", "sebi", "stock"]):
        state["input_type"] = "investment"
    else:
        state["input_type"] = "message"
    return state

def route_to_agent(state: AgentState) -> str:
    return state["input_type"]

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
