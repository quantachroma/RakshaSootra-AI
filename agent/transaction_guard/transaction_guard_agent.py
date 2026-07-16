''''def run_transaction_guard(state: dict) -> dict:
    """Person 3 will build the real logic here later."""
    state["risk_level"] = "risky"
    state["explanation"] = "[Transaction Guard] Transfer amount exceeds safe threshold for new payee."
    state["extracted_entities"] = {"upi": ["scammer@ybl"]}
    return state'''