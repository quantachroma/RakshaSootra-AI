"""
Owner- Person 2 - Priyanshi Saini
test_rules.py — Link Shield Rule Engine Tests
RakshaSootra AI

Run:

pytest test_rules.py -v

or

python test_rules.py
"""

from agent.link_shield.rules import check_link_rules


# ==========================================================
# Known malicious URLs
# ==========================================================

KNOWN_BAD = [

    (
        "https://sbii.co.in/login",
        "Typosquatting"
    ),

    (
        "https://secure-sbi-login.xyz",
        "Trusted brand + suspicious TLD"
    ),

    (
        "https://192.168.1.1/login",
        "Raw IP"
    ),

    (
        "https://bit.ly/abcd123",
        "URL Shortener"
    ),

    (
        "https://tinyurl.com/demo",
        "URL Shortener"
    ),

    (
        "https://paytm-reward.xyz",
        "Reward Scam"
    ),

    (
        "https://verify-kyc-update.com",
        "Keyword Detection"
    ),

    (
        "https://amazon-login.xyz",
        "Fake Amazon"
    ),

    (
        "https://freegift.club",
        "Suspicious TLD"
    ),

    (
        "abcd",
        "Invalid URL"
    ),
]


# ==========================================================
# Known legitimate URLs
# ==========================================================

KNOWN_GOOD = [

    "https://google.com", "https://sbi.co.in",    "https://paytm.com",    "https://amazon.in",
    "https://flipkart.com", "https://uidai.gov.in",    "https://hdfcbank.com",
    "https://icicibank.com", "https://github.com",  "https://stackoverflow.com",   
    "https://linkedin.com",  

]


# ==========================================================
# Bad URL Tests
# ==========================================================

def test_known_bad_urls_are_flagged():

    for url, reason in KNOWN_BAD:

        result = check_link_rules(url)

        assert result["risk_level"] in (
            "risky",
            "high risk",
        ), (
            f"{url} ({reason}) was incorrectly classified as SAFE."
        )

        assert "domain" in result["extracted_entities"]

        assert isinstance(
            result["extracted_entities"]["domain"],
            str,
        )


# ==========================================================
# Good URL Tests
# ==========================================================

def test_known_good_urls_are_safe():

    for url in KNOWN_GOOD:

        result = check_link_rules(url)

        assert result["risk_level"] == "safe", (
            f"{url} incorrectly flagged as "
            f"{result['risk_level']}"
        )


# ==========================================================
# Schema Validation
# ==========================================================

def test_output_schema():

    result = check_link_rules("https://example.com")

    assert set(result.keys()) == {

        "risk_level",

        "explanation",

        "extracted_entities",

    }

    assert result["risk_level"] in (

        "safe",

        "risky",

        "high risk",

    )

    assert isinstance(result["explanation"], str)

    assert isinstance(

        result["extracted_entities"],

        dict,

    )

    assert "domain" in result["extracted_entities"]

    assert isinstance(

        result["extracted_entities"]["domain"],

        str,

    )


# ==========================================================
# Domain Extraction
# ==========================================================

def test_domain_extraction():

    result = check_link_rules(
        "https://www.paytm.com/pay"
    )

    assert (
        result["extracted_entities"]["domain"]
        == "paytm.com"
    )


# ==========================================================
# Empty URL
# ==========================================================

def test_empty_url():

    result = check_link_rules("")

    assert result["risk_level"] == "risky"


# ==========================================================
# Manual Execution
# ==========================================================

if __name__ == "__main__":

    print("\n========== BAD URL TESTS ==========\n")

    for url, reason in KNOWN_BAD:

        result = check_link_rules(url)

        passed = result["risk_level"] in (

            "risky",

            "high risk",

        )

        print(
            f"[{'PASS' if passed else 'FAIL'}] "
            f"{url}"
        )

        print(
            f"Reason      : {reason}"
        )

        print(
            f"Risk Level  : {result['risk_level']}"
        )

        print(
            f"Explanation : {result['explanation']}"
        )

        print()

    print("\n========== GOOD URL TESTS ==========\n")

    for url in KNOWN_GOOD:

        result = check_link_rules(url)

        passed = result["risk_level"] == "safe"

        print(
            f"[{'PASS' if passed else 'FAIL'}] "
            f"{url}"
        )

        print(
            f"Risk Level  : {result['risk_level']}"
        )

        print(
            f"Explanation : {result['explanation']}"
        )

        print()

    print("\n========== SCHEMA TEST ==========\n")

    try:

        test_output_schema()

        print("PASS - Output schema validated.")

    except AssertionError as e:

        print("FAIL -", e)

    print("\n========== DONE ==========\n")