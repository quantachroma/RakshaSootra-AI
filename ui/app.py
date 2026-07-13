import streamlit as st

# PAGE CONFIGURATION
st.set_page_config(
    page_title="RakshaSootra AI 🛡️", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    st.title("🛡️ RakshaSootra AI")
    st.markdown("""
    > **रक्षा सूत्र (RakshaSootra)** — A protective thread. 
    > Threading together citizen reports into one connected shield against fraud.
    """)
    st.divider()

    # --- TAB STRUCTURE ---
    tab_citizen, tab_lea = st.tabs([
        "👤 Citizen View (Check & Report)", 
        "🚨 LEA View (Intelligence Network)"
    ])

    # ==========================================
    # TAB 1: CITIZEN VIEW
    # ==========================================
    with tab_citizen:
        st.header("Verify a Suspicious Link, Message, or Payment")
        st.markdown("""
        Paste any of the following below, and our system will route it to the right security scanner:
        * **A link** (SMS/WhatsApp/Email)
        * **A suspicious message or call transcript** (e.g., "Digital Arrest" threats)
        * **A payment detail** (UPI transfer)
        * **An investment pitch** (Trading apps, celebrity endorsements)
        """)
        
        user_input = st.text_area(
            "What would you like to check?", 
            height=150, 
            placeholder="e.g., http://hdfc-update-kyc.xyz OR 'CBI Alert: Your Aadhaar is suspended...'"
        )
        
        if st.button("Analyze & Protect", type="primary", use_container_width=True):
            if user_input.strip():
                with st.spinner("RakshaSootra Router is analyzing the input..."):
                    # TODO: Wire LangGraph router here on Day 3
                    st.success("Analysis Complete! (Mock Output for Day 1)")
                    
                    with st.container(border=True):
                        st.subheader("Verdict: 🔴 High Risk")
                        st.write("**Agent Used:** Placeholder")
                        st.write("**Explanation:** This is a mock response. The LangGraph router will be connected here soon.")
            else:
                st.warning("⚠️ Please enter some text or a link to analyze.")

    # ==========================================
    # TAB 2: LEA VIEW (Law Enforcement Agency)
    # ==========================================
    with tab_lea:
        st.header("Fraud Syndicate Intelligence")
        st.markdown("Visualizing connected scam entities (UPI IDs, Phone Numbers, Domains) across all citizen reports.")
        
        with st.container(border=True):
            st.info("🚧 **Entity Graph Placeholder**")
            st.write("The `networkx` + `streamlit-agraph` visualization will render here, showing how different citizen reports connect to the same scam rings.")

if __name__ == "__main__":
    main()