"""
rules.py — Scam Script Checker: Local Rule-Based Fast Check
RakshaSootra AI

Pure Python, fully deterministic. NO AI calls, NO network requests.
Scans incoming messages, transcripts, or chat copy for severe extortion markers 
and administrative impersonation signatures.
"""

import re

# High-profile agencies frequently utilized by domestic extortion syndicates
IMPERSONATED_AGENCIES = {
    "CBI": r"\b(cbi|central bureau of investigation)\b",
    "ED": r"\b(ed|enforcement directorate)\b",
    "TRAI": r"\b(trai|telecom regulatory authority)\b",
    "MUMBAI_POLICE": r"\b(mumbai police|crime branch)\b",
    "CUSTOMS": r"\b(customs department|customs officer|ncb)\b",
}

# Clear indicators of administrative coercion or fake legal confinement
DIGITAL_ARREST_TACTICS = (
    "digital arrest",
    "cannot leave the camera",
    "stay on the video call",
    "skype verification",
    "confidentiality agreement",
    "national security case",
)

# Threats targeting asset liquidations or public services
ASSET_SEIZURES = (
    "parcel seized",
    "illegal contraband",
    "passport suspended",
    "sim block",
    "identity theft tracking",
    "money laundering link",
)

# Direct financial ultimatums to bypass immediate arrest loops
FINANCIAL_EXTORTION = (
    "pay to clear your name",
    "refundable verification deposit",
    "transfer to secret vault",
    "settle out of court",
    "avoid immediate arrest",
)

def check_script_rules(text: str) -> dict:
    """
    Executes fast token scanning to intercept digital arrest setups.
    Returns a unified dict mapping to the team schema contract.
    """
    text_lower = text.lower()
    entities = {"impersonated_agency": None}

    # Identify if a specific regulatory/law enforcement agency profile matches
    matched_agency = None
    for agency_key, pattern in IMPERSONATED_AGENCIES.items():
        if re.search(pattern, text_lower):
            matched_agency = agency_key
            entities["impersonated_agency"] = agency_key
            break

    # Structural cross-examinations
    has_digital_arrest_tactics = any(phrase in text_lower for phrase in DIGITAL_ARREST_TACTICS)
    has_asset_seizure = any(phrase in text_lower for phrase in ASSET_SEIZURES)
    has_financial_extortion = any(phrase in text_lower for phrase in FINANCIAL_EXTORTION)

    # 1. PRIORITY 1: HIGH RISK (Direct Extortion or Multi-layered Digital Arrest Signature)
    if has_financial_extortion or (has_digital_arrest_tactics and matched_agency):
        return {
            "risk_level": "high risk",
            "explanation": "Flagged extreme extortion pattern matching known high-pressure 'Digital Arrest' mechanics or direct financial demands to circumvent arrest.",
            "extracted_entities": entities
        }

    # 2. PRIORITY 2: RISKY (Isolated administrative threat vectors or authority claims)
    if has_asset_seizure or has_digital_arrest_tactics or matched_agency:
        return {
            "risk_level": "risky",
            "explanation": "Text flags isolated suspicious elements, such as unauthorized government agency claims, cargo seizure alerts, or telecom suspension threats.",
            "extracted_entities": entities
        }

    # 3. PRIORITY 3: SAFE DEFAULT (No hard rule signatures found -> passes downstream)
    return {
        "risk_level": "safe",
        "explanation": "No localized structural script rules triggered. Passing to dynamic behavioral layer.",
        "extracted_entities": entities
    }