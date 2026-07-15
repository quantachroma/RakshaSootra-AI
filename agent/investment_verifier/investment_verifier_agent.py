def run_investment_verifier(state: dict) -> dict:
    """Person 3 will build the real logic here later."""
    state["risk_level"] = "risky"
    state["explanation"] = "[Investment Verifier] Platform not found in SEBI registry. Promises unrealistic returns."
    state["extracted_entities"] = {"platform": ["CryptoMax Profit"]}
    return state