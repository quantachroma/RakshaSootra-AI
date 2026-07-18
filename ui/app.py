#owner - Shraddha Tyagi
import networkx as nx
from streamlit_agraph import agraph, Node, Edge, Config
import streamlit as st
import sys
import os
import random

# Ensure the root directory is in the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.router import rakshasootra_router

st.set_page_config(page_title="RakshaSootra AI", page_icon="🛡️", layout="centered")

# Custom CSS for a cleaner look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTextArea textarea { background-color: #161b22; color: white; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

def init_session_state():
    if "fraud_graph" not in st.session_state:
        st.session_state.fraud_graph = nx.Graph()

def update_fraud_graph(result: dict):
    g = st.session_state.fraud_graph
    entities = result.get("extracted_entities", {})
    for entity_type, values in entities.items():
        values = values if isinstance(values, list) else [values]
        for val in values:
            g.add_node(val, type=entity_type)

import random

def render_fraud_graph():
    g = st.session_state.fraud_graph
    if g.number_of_nodes() == 0:
        st.warning("No fraud entities reported yet.")
        return

    random.seed(42)  # keeps positions consistent across reruns
    nodes = [
        Node(id=n, label=n, size=25, color="#D9480F",
             x=random.randint(-250, 250), y=random.randint(-150, 150))
        for n in g.nodes()
    ]
    edges = [Edge(source=s, target=t, color="#6B7280") for s, t in g.edges()]
    config = Config(width=750, height=400, directed=False, physics=False, backgroundColor="#161b22")

    with st.container(border=True):
        agraph(nodes=nodes, edges=edges, config=config)

def main():
    init_session_state()
    st.title("🛡️ RakshaSootra AI")
    st.caption("Citizen-led Fraud Intelligence Network")
    
    tab1, tab2 = st.tabs(["👤 Check Suspicious Activity", "🚨 LEA Intelligence"])

    with tab1:
        user_input = st.text_area(
            "Paste Link, Message, or Transaction Details:",
            height=150,
            placeholder="e.g., http://fake-bank.com or 'CBI Alert...'"
        )

        if st.button("Run Security Scan", type="primary", use_container_width=True):
            if not user_input.strip():
                st.warning("Please provide input to scan.")
                return

            # 1. Initialize State
            state = {
                "user_input": user_input,
                "input_type": "unknown",
                "risk_level": "unknown",
                "explanation": "Awaiting agent analysis...",
                "extracted_entities": {}
            }

            # 2. Run the Router with a professional status bar
            with st.status("Initializing RakshaSootra Scanners...", expanded=True) as status:
                st.write("Classifying threat vector...")
                # Run LangGraph
                result = rakshasootra_router.invoke(state)
                update_fraud_graph(result)
                st.write("🔍 DEBUG:", result)
                st.write("🔍 DEBUG — raw result:", result)   # <-- add this temporarily
                st.write(f"Routing to {result['input_type'].upper()} specialist...")
                status.update(label="Scan Complete!", state="complete", expanded=False)

            # 3. Professional Verdict Display
            st.subheader("Security Verdict")
            
            risk = result.get("risk_level", "unknown").lower()
            
            if "high" in risk:
                st.error(f"### 🔴 HIGH RISK DETECTED")
                icon = "🚨"
            elif "risky" in risk:
                st.warning(f"### 🟠 SUSPICIOUS ACTIVITY")
                icon = "⚠️"
            elif "safe" in risk:
                st.success(f"### 🟢 SAFE")
                icon = "✅"
            else:
                st.info(f"### ⚪ UNKNOWN")
                icon = "❓"

            with st.chat_message("assistant", avatar=icon):
                st.write(f"**Analysis:** {result.get('explanation')}")
                if result.get("extracted_entities"):
                    st.write("**Threat Entities Identified:**")
                    st.json(result["extracted_entities"])

    with tab2:
        st.header("🕸️ LEA Intelligence Graph")
        g = st.session_state.fraud_graph
        col1, col2 = st.columns(2)
        col1.metric("Entities Tracked", g.number_of_nodes())
        col2.metric("Connections Found", g.number_of_edges())
        render_fraud_graph()
if __name__ == "__main__":
    main()