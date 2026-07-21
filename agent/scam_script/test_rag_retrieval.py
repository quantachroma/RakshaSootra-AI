"""
Owner - Person 2 - Priyanshi Saini
test_rag_retrieval.py — Day 7: basic retrieval query tests
RakshaSootra AI

Confirms chunks are actually retrievable from ChromaDB and roughly
topic-relevant. Run build_rag_index.py first if the store is empty.

Run:
    python3 -m agent.scam_script.build_rag_index
    python3 -m pytest agent/scam_script/test_rag_retrieval.py -v
"""

import pytest
from agent.scam_script.rag import build_index, retrieve_advisories


@pytest.fixture(scope="module", autouse=True)
def setup_rag_index():
    """
    Builds/resets the ChromaDB index ONCE before running any tests in this file.
    This avoids slow re-indexing overhead inside individual test functions.
    """
    build_index(reset=True)


# Function 1: Digital Arrest Scam Check
def test_digital_arrest_query_matches_advisory():
    query = "Officer from Police says I am under digital arrest on video call."
    matches = retrieve_advisories(query, top_k=3)
    assert matches, "Expected at least one advisory match."
    sources = [m["source"] for m in matches]
    assert any("digital_arrest" in s for s in sources), f"Expected a digital arrest advisory, but got {sources}" 


# Function 2: Fake Job Offer Scam Check (Replaces OTP check)
def test_fake_job_query_matches_advisory():
    query = "Your CV has been selected for high paying part time work from home job."
    matches = retrieve_advisories(query, top_k=3)
    assert matches, "Expected at least one advisory match."
    sources = [m["source"] for m in matches]
    assert "fake_job_offer_sms_scam.txt" in sources  


# Function 3: Crypto / Trust Wallet Check (Replaces generic investment check)
def test_crypto_trust_wallet_query_matches_advisory():
    query = "Connect your Trust Wallet to verify crypto assets on testwallet site."
    matches = retrieve_advisories(query, top_k=3)
    assert matches, "Expected at least one advisory match."
    sources = [m["source"] for m in matches]
    assert "trust_wallet_crypto_scam.txt" in sources  


# Function 4: NHAI FASTag Check
def test_fastag_query_matches_advisory():
    query = "Buy NHAI FASTag annual pass recharge on discounted website link."
    matches = retrieve_advisories(query, top_k=3)
    assert matches, "Expected at least one advisory match."
    sources = [m["source"] for m in matches]
    assert "nhai_fastag_scam.txt" in sources


def test_empty_query_returns_no_matches():
    matches = retrieve_advisories("", top_k=3)
    assert matches == []


def test_unrelated_text_may_return_no_high_confidence_match():
    query = "Hey, are we still on for lunch at the office cafeteria today?"
    matches = retrieve_advisories(query, top_k=3)

    # Not a strict assertion of zero matches (embeddings are fuzzy) —
    # this just documents expected behaviour for a genuinely safe text.
    for match in matches:
        assert match["distance"] <= 0.75


if __name__ == "__main__":
    print("Building index...")
    build_index(reset=True)

    print("\nQuery: digital arrest script")
    for m in retrieve_advisories(
        "CBI officer says I am under digital arrest, pay to avoid arrest", 3
    ):
        print(f"  [{m['distance']}] {m['source']} — {m['topic']}")

    print("\nQuery: OTP script")
    for m in retrieve_advisories(
        "Bank asked me to share OTP to verify my account", 3
    ):
        print(f"  [{m['distance']}] {m['source']} — {m['topic']}")

    print("\nAll manual checks complete.")