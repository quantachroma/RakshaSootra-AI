"""
test_rules.py — Scam Script Checker rule-check tests
RakshaSootra AI

Run with:
    python3 -m pytest agent/scam_script/test_rules.py -v
or:
    python3 test_rules.py
"""

from agent.scam_script.rules import check_script_rules

# ---------------------------------------------------------------------------
# 5 Real-style attack vectors (Must flag as 'risky' or 'high risk')
# ---------------------------------------------------------------------------
KNOWN_SCAMS = [
    (
        "This is officer Sharma from Mumbai Police Crime Branch. A illegal parcel containing contraband has been seized under your name. You are under digital arrest and cannot turn off your webcam.",
        "high risk",
        "MUMBAI_POLICE"
    ),
    (
        "TRAI warning. Your mobile number will be disconnected within 2 hours due to illegal advertisements. Press 9 to connect to the executive for verification.",
        "risky",
        "TRAI"
    ),
    (
        "Your passport and bank accounts are being linked to a major money laundering case investigated by the CBI. To clear your name, you must transfer a refundable verification deposit of ₹50,000 immediately to avoid immediate arrest.",
        "high risk",
        "CBI"
    ),
    (
        "Customs Department Alert: A package sent from Taiwan containing fake identity cards and passports linked to you has been intercepted. Connect via Skype immediately for verification.",
        "risky",
        "CUSTOMS"
    ),
    (
        "Urgent court order notice from the Enforcement Directorate. Your assets are scheduled for administrative seizure. Pay to clear your name instantly out of court.",
        "high risk",
        "ED"
    )
]

# 5 Normal, safe communication structures
KNOWN_SAFE = [
    "Dear customer, your library book return date is tomorrow. Please return it on time to avoid fine.",
    "Hey, are we still meeting for lunch at the office cafeteria at 1 PM today? Let me know.",
    "Your package from Amazon has been delivered to the security gate. Please collect it.",
    "SBI Alert: Your account statement for June is generated. Download via official banking app.",
    "Reminder: Your project code sprint submission is due by Friday evening. Team leads please review."
]


def test_known_scams_are_caught():
    for text, expected_risk, expected_agency in KNOWN_SCAMS:
        result = check_script_rules(text)
        assert result["risk_level"] in ("risky", "high risk"), f"Failed to catch scam text: {text[:30]}..."
        if expected_risk == "high risk":
            assert result["risk_level"] == "high risk", f"Expected high risk for: {text[:30]}"
        assert result["extracted_entities"]["impersonated_agency"] == expected_agency
        print(f"[CATCH] Risk: {result['risk_level']:9s} | Agency: {result['extracted_entities']['impersonated_agency']:13s} | Match Verified.")


def test_safe_texts_pass_cleanly():
    for text in KNOWN_SAFE:
        result = check_script_rules(text)
        assert result["risk_level"] == "safe", f"False positive triggered on safe text: {text}"
        print(f"[SAFE] Clean clearance verified for general copy entry.")


if __name__ == "__main__":
    print("\n--- Executing Scam Script System Rules Check Execution ---")
    test_known_scams_are_caught()
    test_safe_texts_pass_cleanly()
    print("\nAll internal script rules checks passed successfully [PASS].")