def run_link_shield(state: dict) -> dict:
    """Person 2 will build the real logic here later."""
    state["risk_level"] = "high_risk"
    state["explanation"] = "[Link Shield Agent] Detected suspicious typosquatting in the domain."
    state["extracted_entities"] = {"domain": ["hdfc-update-kyc.xyz"]}
    return state