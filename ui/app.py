#owner - Shraddha Tyagi
import os
import random
import sys
import uuid

import networkx as nx
import pandas as pd
import pydeck as pdk
import streamlit as st
from streamlit_agraph import Config, Edge, Node, agraph

# Ensure the root directory is in the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.router import rakshasootra_router

st.set_page_config(page_title="RakshaSootra AI", page_icon="🛡️", layout="centered")

# Custom CSS for a cleaner look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTextArea textarea { background-color: #161b22; color: white; border: 1px solid #30363d; }

    /* LEA tab distinct styling */
    div[data-baseweb="tab-panel"]:nth-of-type(2) {
        background-color: #0a0f1f;
        border-left: 3px solid #D9480F;
        padding: 1.2rem;
        border-radius: 6px;
    }
    </style>
    """, unsafe_allow_html=True)


def seed_fake_reports():
    fake_reports = [
        {"id": "report_101", "entities": {"phone": ["+91-9876543210"], "upi": ["scammer@ybl"]}},
        {"id": "report_102", "entities": {"domain": ["hdfcbank-secure.com"], "upi": ["scammer@ybl"]}},
        {"id": "report_103", "entities": {"phone": ["+91-9123456789"], "upi": ["fraud-payout@okicici"]}},
        {"id": "report_104", "entities": {"domain": ["sbi-kyc-verify.xyz"]}},
        {"id": "report_105", "entities": {"phone": ["+91-9876543210"], "domain": ["paytm-cashback-claim.top"]}},
        {"id": "report_106", "entities": {"upi": ["fraud-payout@okicici"], "platform": ["CryptoMax Profit"]}},
        {"id": "report_107", "entities": {"domain": ["power-bill-update.xyz"]}},
        {"id": "report_108", "entities": {"phone": ["+91-9000011122"]}},
        {"id": "report_109", "entities": {"upi": ["urgent-hospital-bill@okaxis"]}},
        {"id": "report_110", "entities": {"domain": ["hdfcbank-secure.com"]}},
    ]
    g = st.session_state.fraud_graph
    for report in fake_reports:
        g.add_node(report["id"], type="report")
        for entity_type, values in report["entities"].items():
            for val in values:
                g.add_node(val, type=entity_type)
                g.add_edge(report["id"], val)


def init_session_state():
    if "fraud_graph" not in st.session_state:
        st.session_state.fraud_graph = nx.Graph()
        seed_fake_reports()


def update_fraud_graph(result: dict):
    g = st.session_state.fraud_graph
    entities = result.get("extracted_entities", {})
    if not entities:
        return

    report_id = f"live_report_{uuid.uuid4().hex[:6]}"
    g.add_node(report_id, type="report")

    for entity_type, values in entities.items():
        values = values if isinstance(values, list) else [values]
        for val in values:
            g.add_node(val, type=entity_type)
            g.add_edge(report_id, val)


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
    config = Config(width=900, height=550, directed=False, physics=True, backgroundColor="#161b22")

    with st.container(border=True):
        agraph(nodes=nodes, edges=edges, config=config)


def render_hotspot_map():
    hotspots = pd.DataFrame([
        {"city": "Delhi", "lat": 28.6139, "lon": 77.2090, "reports": 34},
        {"city": "Mumbai", "lat": 19.0760, "lon": 72.8777, "reports": 27},
        {"city": "Bengaluru", "lat": 12.9716, "lon": 77.5946, "reports": 19},
        {"city": "Hyderabad", "lat": 17.3850, "lon": 78.4867, "reports": 15},
        {"city": "Pune", "lat": 18.5204, "lon": 73.8567, "reports": 11},
        {"city": "Ahmedabad", "lat": 23.0225, "lon": 72.5714, "reports": 9},
    ])

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=hotspots,
        get_position=["lon", "lat"],
        get_radius="reports * 1500",
        get_fill_color=[217, 72, 15, 160],  # saffron, semi-transparent
        pickable=True,
    )

    view_state = pdk.ViewState(latitude=22.0, longitude=79.0, zoom=4, pitch=0)

    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/dark-v10",
        tooltip={"text": "{city}: {reports} reports"},
    ))


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
            
                st.write(f"Routing to {result['input_type'].upper()} specialist...")
                status.update(label="Scan Complete!", state="complete", expanded=False)

            # 3. Professional Verdict Display
            st.subheader("Security Verdict")

            risk = result.get("risk_level", "unknown").lower()

            if "high" in risk:
                st.error("### 🔴 HIGH RISK DETECTED")
                icon = "🚨"
            elif "risky" in risk:
                st.warning("### 🟠 SUSPICIOUS ACTIVITY")
                icon = "⚠️"
            elif "safe" in risk:
                st.success("### 🟢 SAFE")
                icon = "✅"
            else:
                st.info("### ⚪ UNKNOWN")
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

        st.subheader("📍 Reported Fraud Hotspots")
        render_hotspot_map()


if __name__ == "__main__":
    main()