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
            /* Smooth fade-in transition when switching tabs */
    div[role="tabpanel"] {
        animation: fadeSlideIn 0.35s ease-out;
    }
    }

    @keyframes fadeSlideIn {
        from {
            opacity: 0;
            transform: translateY(8px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Smoother tab underline/hover feel */
    button[data-baseweb="tab"] {
        transition: color 0.2s ease, border-color 0.2s ease;
    }

    /* Metric numbers animate in slightly too, feels more "alive" */
    div[data-testid="stMetricValue"] {
        animation: fadeSlideIn 0.4s ease-out;
    }
            /* Rounded, consistent button styling */
    .stButton > button {
        border-radius: 8px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(217, 72, 15, 0.25);
    }

    /* Softer status/verdict box corners */
    div[data-testid="stAlert"] {
        border-radius: 10px;
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


ENTITY_COLORS = {
    "report": "#6B7280",    # gray - report nodes are just connectors
    "upi": "#1E7A3E",       # green
    "upi_ids": "#1E7A3E",   # same, in case a teammate used the other key name
    "phone": "#2563EB",     # blue
    "phone_numbers": "#2563EB",
    "domain": "#D9480F",    # saffron
    "platform": "#B36B00",  # amber
}


def _short_label(text: str, max_len: int = 18) -> str:
    return text if len(text) <= max_len else text[:max_len - 1] + "…"


def render_fraud_graph():
    g = st.session_state.fraud_graph
    if g.number_of_nodes() == 0:
        st.warning("No fraud entities reported yet.")
        return

    random.seed(42)  # keeps positions consistent across reruns
    nodes = []
    for n, attrs in g.nodes(data=True):
        node_type = attrs.get("type", "unknown")
        color = ENTITY_COLORS.get(node_type, "#9CA3AF")
        size = 15 if node_type == "report" else 25
        nodes.append(Node(
            id=n, label=_short_label(n), size=size, color=color,
            x=random.randint(-250, 250), y=random.randint(-150, 150),
        ))

    edges = [Edge(source=s, target=t, color="#3A3F4B") for s, t in g.edges()]
    config = Config(width=900, height=550, directed=False, physics=True, backgroundColor="#161b22")

    with st.container(border=True):
        agraph(nodes=nodes, edges=edges, config=config)

        st.markdown(
            """
            <div style="display:flex; gap:18px; flex-wrap:wrap; padding-top:8px; font-size:12px; color:#9CA3AF;">
                <span>🟢 UPI ID</span>
                <span>🔵 Phone</span>
                <span>🟠 Domain</span>
                <span>🟤 Platform</span>
                <span>⚪ Report</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


@st.cache_data
def get_hotspot_data():
    return pd.DataFrame([
        {"city": "Delhi", "lat": 28.6139, "lon": 77.2090, "reports": 34},
        {"city": "Mumbai", "lat": 19.0760, "lon": 72.8777, "reports": 27},
        {"city": "Bengaluru", "lat": 12.9716, "lon": 77.5946, "reports": 19},
        {"city": "Hyderabad", "lat": 17.3850, "lon": 78.4867, "reports": 15},
        {"city": "Pune", "lat": 18.5204, "lon": 73.8567, "reports": 11},
        {"city": "Ahmedabad", "lat": 23.0225, "lon": 72.5714, "reports": 9},
    ])

def render_hotspot_map():
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=get_hotspot_data(),
        get_position=["lon", "lat"],
        get_radius="reports * 1500",
        get_fill_color=[217, 72, 15, 160],
        pickable=True,
    )
    text_layer = pdk.Layer(
        "TextLayer",
        data=get_hotspot_data(),
        get_position=["lon", "lat"],
        get_text="city",
        get_size=14,
        get_color=[255, 255, 255, 200],
        get_pixel_offset=[0, -20],
    )

    view_state = pdk.ViewState(latitude=21.5, longitude=80.5, zoom=3.6, pitch=0)

    with st.container(border=True):
        st.pydeck_chart(pdk.Deck(
            layers=[layer, text_layer],
            initial_view_state=view_state,
            map_style="mapbox://styles/mapbox/dark-v10",
            tooltip={"text": "{city}: {reports} reports"},
        ))
        st.caption("Static demo data — live geolocation planned for future phase")


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