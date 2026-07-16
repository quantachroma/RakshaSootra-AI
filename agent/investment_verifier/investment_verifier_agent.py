from agent.investment_verifier.llm_checker import (
    analyze_investment
)

from agent.investment_verifier.rules import (
    check_platform
)

from agent.investment_verifier.models import (
    FinalVerdict
)


def investment_verifier_agent(user_input: str):

    # -----------------------------------------------------
    # STEP 1 : Analyze User Input using LLM
    # -----------------------------------------------------

    analysis = analyze_investment(user_input)

    # -----------------------------------------------------
    # STEP 2 : Verify Company with SEBI Database
    # -----------------------------------------------------

    verification = check_platform(

        company_name=analysis.company_name,

        registration_number=analysis.registration_number

    )

    # -----------------------------------------------------
    # STEP 3 : Decision Engine
    # -----------------------------------------------------

    recommendation = ""

    risk_score = ""

    reason = ""

    # =====================================================
    # VERIFIED
    # =====================================================

    if verification.status == "VERIFIED":

        if analysis.risk == "SAFE":

            recommendation = "INVEST"

            risk_score = "Low"

            reason = (

                f"{verification.explanation}\n\n"

                f"LLM Analysis: {analysis.reason}"

            )

        else:

            recommendation = "DO NOT INVEST"

            risk_score = "High"

            reason = (

                f"{verification.explanation}\n\n"

                "Although the company is SEBI registered, "

                "the investment pitch contains scam "

                "indicators.\n\n"

                f"LLM Analysis: {analysis.reason}"

            )

    # =====================================================
    # LIKELY VERIFIED
    # =====================================================

    elif verification.status == "LIKELY VERIFIED":

        if analysis.risk == "SAFE":

            recommendation = "VERIFY DETAILS BEFORE INVESTING"

            risk_score = "Medium"

            reason = (

                f"{verification.explanation}\n\n"

                "The company closely matches a "

                "SEBI registered broker, "

                "but the match is not exact.\n\n"

                f"LLM Analysis: {analysis.reason}"

            )

        else:

            recommendation = "DO NOT INVEST"

            risk_score = "High"

            reason = (

                f"{verification.explanation}\n\n"

                "The company is similar to a SEBI "

                "registered broker, but the investment "

                "pitch itself contains multiple scam "

                "indicators.\n\n"

                f"LLM Analysis: {analysis.reason}"

            )

    # =====================================================
    # SUSPICIOUS
    # =====================================================

    elif verification.status == "SUSPICIOUS":

        recommendation = "DO NOT INVEST"

        risk_score = "High"

        reason = (

            f"{verification.explanation}\n\n"

            "The company name resembles a "

            "SEBI registered broker but "

            "is not an exact match.\n\n"

            f"LLM Analysis: {analysis.reason}"

        )

    # =====================================================
    # UNREGISTERED
    # =====================================================

    else:

        recommendation = "DO NOT INVEST"

        risk_score = "High"

        reason = (

            f"{verification.explanation}\n\n"

            "The company could not be verified "

            "in the SEBI registered brokers "

            "database.\n\n"

            f"LLM Analysis: {analysis.reason}"

        )

    # -----------------------------------------------------
    # STEP 4 : Create Final Verdict Object
    # -----------------------------------------------------

    verdict = FinalVerdict(

        recommendation=recommendation,

        risk_score=risk_score,

        reason=reason

    )
        # -----------------------------------------------------
    # STEP 5 : Return Complete Result
    # -----------------------------------------------------

    return {

        # ================================================
        # LLM ANALYSIS
        # ================================================

        "investment_analysis": {

            "company_name": analysis.company_name,

            "registration_number": analysis.registration_number,

            "pitch": analysis.pitch,

            "risk": analysis.risk,

            "reason": analysis.reason

        },

        # ================================================
        # COMPANY VERIFICATION
        # ================================================

        "company_verification": {

            "status": verification.status,

            "confidence": verification.confidence,

            "matched_company": verification.matched_company,

            "registration_number": verification.registration_number,

            "city": verification.city,

            "state": verification.state,

            "explanation": verification.explanation

        },

        # ================================================
        # FINAL VERDICT
        # ================================================

        "final_verdict": {

            "recommendation": verdict.recommendation,

            "risk_score": verdict.risk_score,

            "company_status": verification.status,

            "confidence": verification.confidence,

            "reason": verdict.reason

        }

    }

def run_investment_verifier(state):
    """
    LangGraph node wrapper function.
    Receives AgentState and calls investment_verifier_agent.
    """

    print("Investment Verifier Agent Running...")

    user_input = state.get("user_input", "")

    result = investment_verifier_agent(user_input)

    return {
        "investment_result": result
    }