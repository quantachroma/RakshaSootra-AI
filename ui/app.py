import streamlit as st

# --- PAGE CONFIGURATION ---
# Must be the first Streamlit command
st.set_page_config(
    page_title="RakshaSootra AI 🛡️", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)
def main():
    # --- HEADER SECTION ---
    st.title("🛡️ RakshaSootra AI")
    st.markdown("""
    > **रक्षा सूत्र (RakshaSootra)** — A protective thread. 
    > Threading together citizen reports into one connected shield against fraud.
    """)
    st.divider()

    # --- TAB STRUCTURE (Day 1 Requirement) ---
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
        
        # User Input
        user_input = st.text_area(
            "What would you like to check?", 
            height=150, 
            placeholder="e.g., http://hdfc-update-kyc.xyz OR 'CBI Alert: Your Aadhaar is suspended. Pay 50,000 immediately...'"
        )
        
        # Submit Button
        if st.button("Analyze & Protect", type="primary", use_container_width=True):
            if user_input.strip():
                # Day 1: Placeholder for the Router Agent
                with st.spinner("RakshaSootra Router is analyzing the input..."):
                    
                    # TODO (Day 3): Call the LangGraph Router here
                    # state = router_agent.invoke({"input": user_input})
                    
                    # Mocking the output for Day 1 UI testing
                    st.success("Analysis Complete!")
                    
                    # Displaying a mock verdict card
                    with st.container(border=True):
                        st.subheader("Verdict: 🔴 High Risk")
                        st.write("**Agent Used:** Scam Script Checker (Mock)")
                        st.write("**Explanation:** This matches the exact pattern of a 'Digital Arrest' scam. Law enforcement agencies like the CBI will never ask you to transfer money to avoid arrest.")
                        
            else:
                st.warning("⚠️ Please enter some text or a link to analyze.")

    # ==========================================
    # TAB 2: LEA VIEW (Law Enforcement Agency)
    # ==========================================
    with tab_lea:
        st.header("Fraud Syndicate Intelligence")
        st.markdown("Visualizing connected scam entities (UPI IDs, Phone Numbers, Domains) across all citizen reports.")
        
        # Day 1: Placeholder for the Graph
        with st.container(border=True):
            st.info("🚧 **Entity Graph Placeholder**")
            st.write("On Day 6, this space will render the `networkx` + `streamlit-agraph` visualization, showing how different citizen reports connect to the same scam rings.")
            
            # Optional: A small placeholder image or empty space just to hold the layout
            st.markdown("<div style='height: 300px; display: flex; align-items: center; justify-content: center; background-color: #1E1E1E; border-radius: 10px;'>Graph will render here</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    