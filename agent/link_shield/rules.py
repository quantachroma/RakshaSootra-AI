"""
Owner- Person 2 - Priyanshi Saini
rules.py — Link Shield: Local Rule-Based Fast Check
RakshaSootra AI

Fast deterministic checks that run before any LLM call.
"""

import re
import ipaddress
from urllib.parse import urlparse
from difflib import SequenceMatcher

# -------------------------------------------------------------------
# Trusted domains
# -------------------------------------------------------------------

TARGET_DOMAINS = (
    "sbi.co.in",
    "hdfcbank.com",
    "icicibank.com",
    "axisbank.com",
    "kotak.com",
    "paytm.com",
    "amazon.in",
    "flipkart.com",
    "uidai.gov.in",
)

# -------------------------------------------------------------------
# Common phishing URL shorteners
# -------------------------------------------------------------------

URL_SHORTENERS = (
    "bit.ly",
    "tinyurl.com",
    "goo.gl",
    "t.co",
    "cutt.ly",
    "rb.gy",
    "rebrand.ly",
    "shorturl.at",
)

# -------------------------------------------------------------------
# Suspicious TLDs
# -------------------------------------------------------------------

SUSPICIOUS_TLDS = (
    ".xyz",
    ".top",
    ".club",
    ".click",
    ".loan",
    ".win",
    ".bid",
    ".online",
    ".site",
)

# -------------------------------------------------------------------
# Common phishing keywords
# -------------------------------------------------------------------

SUSPICIOUS_KEYWORDS = (
    "otp",
    "verify",
    "verification",
    "kyc",
    "update",
    "bank-update",
    "aadhaar",
    "aadhaar-update",
    "pan-update",
    "upi",
    "refund",
    "reward",
    "cashback",
    "gift",
    "winner",
    "lottery",
    "claim",
    "claim-prize",
    "claim-amount",
    "free",
    "credit",
    "account-blocked",
    "login",
    "secure",
    "payment",
    "activate",
)

# -------------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------------


def _extract_domain(url: str) -> str:
    """Extract clean domain from URL."""

    try:
        url = url.strip().lower()

        if not url:
            return ""

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        parsed = urlparse(url)

        domain = parsed.netloc.split(":")[0]

        if domain.startswith("www."):
            domain = domain[4:]

        # Validate domain
        if "." not in domain:
            return ""

        # Domain should not start/end with dot
        if domain.startswith(".") or domain.endswith("."):
            return ""

        return domain

    except Exception:
        return ""

def _is_valid_ip(domain: str) -> bool:
    """Return True only if domain is a valid IPv4/IPv6 address."""

    try:
        ipaddress.ip_address(domain)
        return True
    except ValueError:
        return False


def _is_shortener(domain: str) -> bool:
    return domain in URL_SHORTENERS


def _contains_suspicious_tld(domain: str) -> bool:
    return any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS)


def _contains_keywords(url: str) -> bool:
    url = url.lower()
    return any(keyword in url for keyword in SUSPICIOUS_KEYWORDS)


def _is_typosquat(domain: str):
    """
    Detect typo domains such as:
    sbii.co.in
    paytm-secure.com
    secure-sbi-login.com
    amazon-login.xyz
    """

    for target in TARGET_DOMAINS:

        if domain == target:
            continue

        similarity = SequenceMatcher(None, domain, target).ratio()

        if similarity >= 0.82:
            return True, target

        root = target.split(".")[0]

        if root in domain and domain != target:
            return True, target

    return False, None


# -------------------------------------------------------------------
# Main Rule Engine
# -------------------------------------------------------------------


def check_link_rules(url: str) -> dict:

    domain = _extract_domain(url)

    entities = {
        "domain": domain
    }

    # Invalid URL
    if not domain:
        return {
            "risk_level": "risky",
            "explanation": "Unable to extract a valid domain from the provided URL.",
            "extracted_entities": entities,
        }

    # Raw IP Address
    if _is_valid_ip(domain):
        return {
            "risk_level": "high risk",
            "explanation": "The URL uses a raw IP address instead of a registered domain, a common phishing indicator.",
            "extracted_entities": entities,
        }

    # URL Shortener
    if _is_shortener(domain):
        return {
            "risk_level": "risky",
            "explanation": "The URL uses a shortening service that hides the final destination.",
            "extracted_entities": entities,
        }

    # Typosquatting
    typo, target = _is_typosquat(domain)

    if typo:
        return {
            "risk_level": "high risk",
            "explanation": f"The domain appears to imitate the trusted website '{target}'.",
            "extracted_entities": entities,
        }

    # Suspicious TLD
    if _contains_suspicious_tld(domain):
        return {
            "risk_level": "risky",
            "explanation": "The domain uses a top-level domain frequently abused in phishing campaigns.",
            "extracted_entities": entities,
        }

    # Suspicious Keywords
    if _contains_keywords(url):
        return {
            "risk_level": "risky",
            "explanation": "The URL contains words commonly associated with phishing or social engineering attacks.",
            "extracted_entities": entities,
        }

    return {
        "risk_level": "safe",
        "explanation": "No suspicious URL patterns were detected during the rule-based analysis.",
        "extracted_entities": entities,
    }