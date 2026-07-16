#owner - Shraddha Tyagi
import streamlit as st
import sys
import os

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

def main():
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
        st.header("Fraud Network Graph")
        st.info("Visualizing connections between reported scams. (Coming Phase 2)")

if __name__ == "__main__":
    main()