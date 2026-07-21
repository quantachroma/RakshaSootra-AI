"""
Owner- Person 2 - Priyanshi Saini
test_edge_cases.py — Link Shield security edge case tests
Tests unusual URLs commonly used in phishing attacks.
"""

from agent.link_shield.rules import check_link_rules


# -------------------------------------------------------------------
# URLs that should NOT be considered safe
# -------------------------------------------------------------------

EDGE_CASES = [

    (
        "https://аррӏе.com",
        "Unicode homograph attack"
    ),

    (
        "https://xn--80ak6aa92e.com",
        "Punycode encoded domain"
    ),

    (
        "https://paypal.com@evil-site.com",
        "URL with @ symbol"
    ),

    (
        "https://user:password@evil.com",
        "Embedded credentials"
    ),

    (
        "http://192.168.1.10/login",
        "Private IP address"
    ),

    (
        "http://185.220.101.45:8080/login",
        "IP with port"
    ),

    (
        "ftp://malicious-site.com/file.exe",
        "FTP protocol"
    ),

    (
        "https://secure-login-account-verification.com",
        "Suspicious keyword chain"
    ),

    (
        "https://example.com:9999",
        "Unusual port"
    ),

    (
        "https://google.com.evil-domain.com",
        "Fake subdomain"
    ),

]


def test_edge_cases_are_not_safe():

    for url, reason in EDGE_CASES:

        result = check_link_rules(url)

        assert result["risk_level"] in (
            "risky",
            "high risk",
        ), (
            f"{url} ({reason}) was incorrectly classified as SAFE."
        )


# -------------------------------------------------------------------
# Very long URL test
# -------------------------------------------------------------------

def test_extremely_long_url():

    long_path = "a" * 5000

    url = (
        "https://example.com/"
        + long_path
    )

    result = check_link_rules(url)

    assert result["risk_level"] != "safe"



# -------------------------------------------------------------------
# Mixed-case domain test
# -------------------------------------------------------------------

def test_mixed_case_domain():

    url = "https://GoOgLe.CoM"

    result = check_link_rules(url)

    assert result["extracted_entities"]["domain"] == "google.com"