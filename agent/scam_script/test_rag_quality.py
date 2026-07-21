"""
Owner - Person 2 - Priyanshi Saini
test_rag_quality.py — Day 9: RAG output quality check
RakshaSootra AI

Goal (per project plan): run 5 sample scam scripts through the full
RAG-enhanced Scam Script Checker and confirm at least 3 of 5 produce a
real advisory citation in the final explanation.

This calls the LIVE agent (rule check + RAG + OpenRouter LLM check), so
it needs OPENROUTER_API_KEY set and network access. Run manually:

    python3 agent/scam_script/test_rag_quality.py
"""

from agent.scam_script.rag import build_index
from agent.scam_script.scam_script_agent import check_script


SAMPLE_SCRIPTS = [
    # 1. Digital arrest — matches digital_arrest_scam.txt
    "This is Inspector Verma from CBI cyber cell. Your account is linked "
    "to a money laundering case. Do not disconnect this video call or "
    "you will be arrested within the hour. Stay on Skype for verification.",

    # 2. OTP / Bank fraud — matches fake_job_offer_sms_scam.txt / banking advisories
    "Sir this is HDFC Bank customer care, your account will be blocked "
    "today. Please share the OTP sent to your phone so we can verify and "
    "reactivate your account immediately.",

    # 3. Crypto / Investment scam — matches trust_wallet_crypto_scam.txt
    "Join our VIP crypto trading group on Telegram, our SEBI registered "
    "advisor guarantees 20% profit daily with zero risk. Deposit now to "
    "lock in today's rate before the offer closes.",

    # 4. Customs / Parcel scam — matches digital_arrest_scam.txt / customs advisories
    "This is Customs Department. A parcel under your name containing "
    "banned substances was intercepted at Mumbai airport. To avoid "
    "arrest you must pay a customs clearance deposit immediately.",

    # 5. Safe baseline — should NOT get a scam-advisory citation
    "Hi, just confirming our team meeting is still at 4 PM today in "
    "conference room B. Let me know if that time doesn't work for you.",
]


def run_quality_check():

    print("Rebuilding index to ensure it's current...")
    build_index(reset=True)

    citation_count = 0

    for i, script in enumerate(SAMPLE_SCRIPTS, start=1):

        print("\n" + "=" * 70)
        print(f"SAMPLE {i}")
        print("=" * 70)
        print(f"Script   : {script[:90]}...")

        verdict = check_script(script)

        has_citation = "advisory" in verdict["explanation"].lower()

        if has_citation:
            citation_count += 1

        print(f"Risk     : {verdict['risk_level']}")
        print(f"Explain  : {verdict['explanation']}")
        print(f"Cited?   : {has_citation}")

    print("\n" + "=" * 70)
    print(f"RESULT: {citation_count}/5 samples produced an advisory citation.")
    print(
        "PASS — target of >=3/5 met."
        if citation_count >= 3
        else "FAIL — target of >=3/5 NOT met, review retrieval threshold / prompt."
    )
    print("=" * 70)

    return citation_count

def test_rag_quality_target_met():
    """Pytest wrapper asserting that at least 3/5 scripts trigger citations."""
    citation_count = run_quality_check()
    assert citation_count >= 3, f"Quality check failed: only {citation_count}/5 citations produced."


if __name__ == "__main__":
    run_quality_check()