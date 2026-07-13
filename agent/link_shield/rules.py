"""
rules.py — Link Shield: Local Rule-Based Fast Check
RakshaSootra AI

Pure Python, fully deterministic. NO AI calls, NO network requests.
This module performs the initial fast "rule check" gate for the Link Shield agent.
"""

import re
from difflib import SequenceMatcher
from urllib.parse import urlparse

# Target Indian financial / utility domains commonly typosquatted
TARGET_DOMAINS = (
    "sbi.co.in",
    "hdfcbank.com",
    "icicibank.com",
    "uidai.gov.in",
    "paytm.com",
    "amazon.in",
    "flipkart.com",
)

TYPOSQUAT_MIN_RATIO = 0.70
TYPOSQUAT_MAX_RATIO = 0.99

SUSPICIOUS_TLDS = (".xyz", ".top", ".club", ".win", ".bid", ".loan", ".click", ".site", ".online")

SUSPICIOUS_KEYWORDS = (
    "win-prize", "lucky-draw", "free-gift", "account-blocked", 
    "kyc-update", "otp-verify", "part-time-job", "claim-amount"
)

def _extract_domain(url: str) -> str:
    """Safely extracts clean root domain from a raw URL."""
    try:
        url_lower = url.lower().strip()
        if not (url_lower.startswith("http://") or url_lower.startswith("https://")):
            url_lower = "http://" + url_lower
        parsed = urlparse(url_lower)
        netloc = parsed.netloc.split(":")[0]
        if netloc.startswith("www."):
            netloc = netloc[4:]
        return netloc
    except Exception:
        return ""

def _is_raw_ip(domain: str) -> bool:
    """Checks if the extracted target is a raw IPv4 address string."""
    return bool(re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", domain))

def check_link_rules(url: str) -> dict:
    """
    Executes fast-fail pattern validations against structural fraud vectors.
    """
    domain = _extract_domain(url)
    entities = {"domain": domain}

    # 1. Raw IP Red Flag (High Risk)
    if _is_raw_ip(domain):
        return {
            "risk_level": "high risk",
            "explanation": "Flagged raw IP address structure instead of a registered domain registry record.",
            "extracted_entities": entities
        }

    # 2. Hard Typosquat Detection (High Risk)
    for target in TARGET_DOMAINS:
        if domain == target:
            continue
        ratio = SequenceMatcher(None, domain, target).ratio()
        if TYPOSQUAT_MIN_RATIO <= ratio <= TYPOSQUAT_MAX_RATIO:
            return {
                "risk_level": "high risk",
                "explanation": f"Identified severe structural similarity typosquat impersonating trusted domain '{target}'.",
                "extracted_entities": entities
            }

    # 3. Suspicious Domain TLD or Scambait Keyword (Risky)
    has_bad_tld = any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS)
    has_bad_keyword = any(kw in url.lower() for kw in SUSPICIOUS_KEYWORDS)

    if has_bad_tld or has_bad_keyword:
        return {
            "risk_level": "risky",
            "explanation": "URL contains anomalous generic top-level domains or high-pressure phishing phrases.",
            "extracted_entities": entities
        }

    # 4. Safe Default Pass-through (Escalates to Day 2 LLM Layer)
    return {
        "risk_level": "safe",
        "explanation": "No immediate localized structural rule signatures matched. Escalating to deep dynamic assessment.",
        "extracted_entities": entities
    }