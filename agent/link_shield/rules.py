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
# Trusted brand domains (used for typosquat comparison)
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
# NEW: Globally trusted / high-reputation domains
# These bypass typosquat/keyword/LLM scrutiny entirely once matched,
# fixing false positives like github.com being flagged as suspicious.
# -------------------------------------------------------------------

GLOBALLY_TRUSTED_DOMAINS = (
    "google.com",
    "github.com",
    "microsoft.com",
    "apple.com",
    "wikipedia.org",
    "linkedin.com",
    "stackoverflow.com",
    "youtube.com",
    "openai.com",
    "anthropic.com",
    "mozilla.org",
    "cloudflare.com",
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


def _has_embedded_credentials(raw_url: str) -> bool:
    """
    Detects the 'https://paypal.com@evil-site.com' / 'user:pass@host'
    pattern — the '@' before the real host is classic brand-spoofing.
    Everything before the LAST '@' in the netloc is userinfo, not the host.
    """
    try:
        url = raw_url.strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        parsed = urlparse(url)
        return "@" in parsed.netloc
    except Exception:
        return False


def _is_punycode(domain: str) -> bool:
    """Detects xn-- punycode-encoded domains, commonly used for homograph attacks."""
    return any(label.startswith("xn--") for label in domain.split("."))


def _has_non_ascii(domain: str) -> bool:
    """Detects Unicode homograph attacks (e.g. Cyrillic 'а' instead of Latin 'a')."""
    try:
        domain.encode("ascii")
        return False
    except UnicodeEncodeError:
        return True


def _extract_domain(url: str) -> str:
    """
    Extract clean domain from URL.

    FIXED: uses parsed.hostname (which correctly strips userinfo AND port)
    instead of splitting netloc on ':', which previously mis-parsed
    'user:password@evil.com' as domain 'user'.
    """

    try:
        url = url.strip().lower()

        if not url:
            return ""

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        parsed = urlparse(url)

        domain = parsed.hostname or ""

        if domain.startswith("www."):
            domain = domain[4:]

        if "." not in domain:
            return ""

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


def _is_globally_trusted(domain: str) -> bool:
    return domain in GLOBALLY_TRUSTED_DOMAINS


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
# NEW: Port / length thresholds
# -------------------------------------------------------------------

STANDARD_PORTS = (80, 443)          # normal HTTP/HTTPS — everything else is "unusual"
MAX_REASONABLE_URL_LENGTH = 300     # legitimate URLs are almost never this long


def _has_unusual_port(raw_url: str) -> bool:
    """
    Flags non-standard ports (e.g. :9999, :8080) — phishing/malware
    infrastructure frequently runs on non-standard ports to evade
    basic domain-based blocklists.
    """
    try:
        url = raw_url.strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        parsed = urlparse(url)
        if parsed.port is not None and parsed.port not in STANDARD_PORTS:
            return True
        return False
    except Exception:
        return False


def _is_excessively_long(raw_url: str) -> bool:
    """
    Flags abnormally long URLs — a common technique to bury a malicious
    payload/redirect deep in the path/query string where a human won't
    read it, or to break naive parsers.
    """
    return len(raw_url) > MAX_REASONABLE_URL_LENGTH

# -------------------------------------------------------------------
# Fake subdomain / brand-in-path spoofing
# -------------------------------------------------------------------

ALL_TRUSTED_BRANDS = TARGET_DOMAINS + GLOBALLY_TRUSTED_DOMAINS


def _is_fake_subdomain(domain: str) -> tuple:
    for brand in ALL_TRUSTED_BRANDS:
        if domain == brand:
            continue
        if domain.endswith("." + brand):
            continue
        if brand in domain:
            return True, brand
    return False, None

# -------------------------------------------------------------------
# Main Rule Engine
# -------------------------------------------------------------------


def check_link_rules(url: str) -> dict:

    domain = _extract_domain(url)
    entities = {"domain": domain}

    if not domain:
        return {
            "risk_level": "risky",
            "explanation": "Unable to extract a valid domain from the provided URL.",
            "extracted_entities": entities,
        }

    if _is_globally_trusted(domain):
        return {
            "risk_level": "safe",
            "explanation": "Domain is on the verified global trust list.",
            "extracted_entities": entities,
        }

    if _has_embedded_credentials(url):
        return {
            "risk_level": "high risk",
            "explanation": "The URL embeds credentials or a fake brand name before the '@' symbol, a classic phishing technique to disguise the true destination domain.",
            "extracted_entities": entities,
        }

    if _is_punycode(domain):
        return {
            "risk_level": "high risk",
            "explanation": "The domain uses punycode (xn--) encoding, frequently used to disguise homograph phishing domains that visually mimic trusted brands.",
            "extracted_entities": entities,
        }

    if _has_non_ascii(domain):
        return {
            "risk_level": "high risk",
            "explanation": "The domain contains non-standard Unicode characters designed to visually mimic a trusted domain (homograph attack).",
            "extracted_entities": entities,
        }

    fake_sub, spoofed_brand = _is_fake_subdomain(domain)
    if fake_sub:
        return {
            "risk_level": "high risk",
            "explanation": f"The domain embeds the trusted brand '{spoofed_brand}' as a decoy label, but the actual registered domain is different — a common subdomain-spoofing phishing technique.",
            "extracted_entities": entities,
        }

    if _is_valid_ip(domain):
        return {
            "risk_level": "high risk",
            "explanation": "The URL uses a raw IP address instead of a registered domain, a common phishing indicator.",
            "extracted_entities": entities,
        }

    if _is_shortener(domain):
        return {
            "risk_level": "risky",
            "explanation": "The URL uses a shortening service that hides the final destination.",
            "extracted_entities": entities,
        }

    typo, target = _is_typosquat(domain)
    if typo:
        return {
            "risk_level": "high risk",
            "explanation": f"The domain appears to imitate the trusted website '{target}'.",
            "extracted_entities": entities,
        }

    if _contains_suspicious_tld(domain):
        return {
            "risk_level": "risky",
            "explanation": "The domain uses a top-level domain frequently abused in phishing campaigns.",
            "extracted_entities": entities,
        }

    if _contains_keywords(url):
        return {
            "risk_level": "risky",
            "explanation": "The URL contains words commonly associated with phishing or social engineering attacks.",
            "extracted_entities": entities,
        }

    if _has_unusual_port(url):
        return {
            "risk_level": "risky",
            "explanation": "The URL specifies a non-standard port, which is unusual for legitimate consumer-facing websites and is sometimes used to host malicious infrastructure.",
            "extracted_entities": entities,
        }

    if _is_excessively_long(url):
        return {
            "risk_level": "risky",
            "explanation": f"The URL is unusually long ({len(url)} characters), which can be used to obscure malicious redirects or overwhelm basic URL parsers.",
            "extracted_entities": entities,
        }

    return {
        "risk_level": "safe",
        "explanation": "No suspicious URL patterns were detected during the rule-based analysis.",
        "extracted_entities": entities,
    }


def _is_fake_subdomain(domain: str) -> tuple:
    """
    Detects domains like 'google.com.evil-domain.com' where a trusted
    brand name appears as a LABEL PREFIX rather than as the actual
    registered domain.

    A legitimate subdomain of a trusted brand ENDS with '.brand.com'
    (e.g. 'accounts.google.com'). A spoof instead has the brand name
    embedded earlier, followed by a completely different real domain
    (e.g. 'google.com.evil-domain.com' — the real domain is
    'evil-domain.com', and 'google.com' is just a decoy label).
    """

    for brand in ALL_TRUSTED_BRANDS:

        if domain == brand:
            continue

        # Legitimate case: real subdomain of the brand, e.g. accounts.google.com
        if domain.endswith("." + brand):
            continue

        # Spoof case: brand name appears somewhere in the domain,
        # but NOT as a legitimate trailing subdomain relationship
        if brand in domain:
            return True, brand

    return False, None

    return {
        "risk_level": "safe",
        "explanation": "No suspicious URL patterns were detected during the rule-based analysis.",
        "extracted_entities": entities,
    }