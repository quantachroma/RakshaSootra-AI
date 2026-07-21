"""
test_rules.py — Link Shield rule-check tests
RakshaSootra AI

Run with:
    python3 -m pytest test_rules.py -v
or, if pytest isn't installed:
    python3 test_rules.py
"""

from agent.link_shield.rules import check_link_rules
# ---------------------------------------------------------------------------
# 5 known-bad URLs (should NOT come back "safe")
# ---------------------------------------------------------------------------
KNOWN_BAD = [
    ("http://hdfcbank-verify.com/login", "typosquat"),
    ("http://192.168.1.1/win", "raw IP"),
    ("http://spin-and-win-prize.xyz/claim", "bait + suspicious TLD"),
    ("http://free-gift-amazon.xyz/win-amount", "bait on unverified domain"),
    ("https://myrandomsite.com/account-credited-notice", "fake account alert"),
]

# ---------------------------------------------------------------------------
# 5 known-good URLs (SHOULD come back "safe")
# ---------------------------------------------------------------------------
KNOWN_GOOD = [
    "https://sbi.co.in/personal-banking",
    "https://www.hdfcbank.com/personal",
    "https://www.icicibank.com/",
    "https://uidai.gov.in/",
    "https://www.amazon.in/orders",
]


def test_known_bad_urls_are_flagged():
    for url, reason in KNOWN_BAD:
        result = check_link_rules(url)
        assert result["risk_level"] in ("risky", "high risk"), (
            f"Expected '{url}' to be flagged ({reason}), got {result['risk_level']}"
        )
        assert "domain" in result["extracted_entities"]
        print(f"[BAD]  {url:55s} -> {result['risk_level']:9s} | {result['explanation']}")


def test_known_good_urls_are_safe():
    for url in KNOWN_GOOD:
        result = check_link_rules(url)
        assert result["risk_level"] == "safe", (
            f"Expected '{url}' to be safe, got {result['risk_level']}: {result['explanation']}"
        )
        print(f"[GOOD] {url:55s} -> {result['risk_level']:9s} | {result['explanation']}")


def test_output_schema():
    result = check_link_rules("https://example.com")
    assert set(result.keys()) == {"risk_level", "explanation", "extracted_entities"}
    assert result["risk_level"] in ("safe", "risky", "high risk")
    assert isinstance(result["explanation"], str) and result["explanation"]
    assert "domain" in result["extracted_entities"]


if __name__ == "__main__":
    # Allows running directly with `python3 test_rules.py` without pytest
    print("\n--- Known-bad URLs ---")
    for url, reason in KNOWN_BAD:
        r = check_link_rules(url)
        status = "PASS" if r["risk_level"] in ("risky", "high risk") else "FAIL"
        print(f"[{status}] {url}\n        -> {r}\n")

    print("--- Known-good URLs ---")
    for url in KNOWN_GOOD:
        r = check_link_rules(url)
        status = "PASS" if r["risk_level"] == "safe" else "FAIL"
        print(f"[{status}] {url}\n        -> {r}\n")

    print("--- Running Schema Checks ---")
    try:
        test_output_schema()
        print("[PASS] Schema validated successfully.\n")
    except AssertionError as e:
        print(f"[FAIL] Schema mismatch: {e}\n")

    print("All manual checks completed. Verify that there are no [FAIL] lines.")