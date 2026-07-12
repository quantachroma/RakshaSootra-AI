def run_scam_script(state: dict) -> dict:
    """Person 2 will build the real logic here later."""
    state["risk_level"] = "high_risk"
    state["explanation"] = "[Scam Script Agent] Detected 'Digital Arrest' keywords (CBI, Aadhaar)."
    state["extracted_entities"] = {"phone": ["+91-9876543210"]}
    return state
