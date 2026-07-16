from agent.investment_verifier.rules import check_platform
from agent.investment_verifier.llm_checker import analyze_pitch
from agent.investment_verifier.models import InvestmentPlatform


def investment_verifier_agent(platform_name: str, pitch: str):
    """
    Combines:
    1. SEBI Registration Check
    2. LLM Scam Language Detection
    3. Generates a Final Investment Recommendation
    """

    # -----------------------------
    # Step 1: Create Platform Object
    # -----------------------------
    platform = InvestmentPlatform(platform_name)

    # -----------------------------
    # Step 2: Rule-based SEBI Check
    # -----------------------------
    broker_result = check_platform(platform)

    # -----------------------------
    # Step 3: LLM Scam Detection
    # -----------------------------
    pitch_result = analyze_pitch(pitch)

    # -----------------------------
    # Step 4: Determine Safety
    # -----------------------------
    broker_safe = broker_result.risk_level.lower() == "safe"

    pitch_safe = (
        pitch_result["risk"].lower() == "safe"
    )

    # -----------------------------
    # Step 5: Final Decision
    # -----------------------------
    if broker_safe and pitch_safe:

        recommendation = "INVEST"

        risk_score = "Low"

        final_reason = (
            "The broker is SEBI registered and the investment pitch "
            "does not contain obvious scam indicators."
        )

    elif broker_safe and not pitch_safe:

        recommendation = "DO NOT INVEST"

        risk_score = "Medium"

        final_reason = (
            "The broker is SEBI registered, but the investment pitch "
            "contains suspicious or misleading claims."
        )

    elif not broker_safe and pitch_safe:

        recommendation = "DO NOT INVEST"

        risk_score = "High"

        final_reason = (
            "The investment pitch appears genuine, but the broker "
            "is not registered with SEBI."
        )

    else:

        recommendation = "HIGH RISK - DO NOT INVEST"

        risk_score = "Critical"

        final_reason = (
            "The broker is not registered with SEBI and the "
            "investment pitch contains scam indicators."
        )

    # -----------------------------
    # Step 6: Return Final Result
    # -----------------------------
    return {
        "broker_verification": {
            "risk": broker_result.risk_level,
            "reason": broker_result.explanation
        },

        "pitch_analysis": {
            "risk": pitch_result["risk"],
            "reason": pitch_result["reason"]
        },

        "final_verdict": {
            "recommendation": recommendation,
            "risk_score": risk_score,
            "reason": final_reason
        }
    }