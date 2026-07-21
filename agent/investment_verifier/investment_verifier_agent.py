# from agent.investment_verifier.llm_checker import (
#     analyze_investment
# )

# from agent.investment_verifier.rules import (
#     check_platform
# )

# from agent.investment_verifier.models import (
#     FinalVerdict
# )


# def investment_verifier_agent(user_input: str):

#     # -----------------------------------------------------
#     # STEP 1 : Analyze User Input using LLM
#     # -----------------------------------------------------

#     analysis = analyze_investment(user_input)

#     # -----------------------------------------------------
#     # STEP 2 : Verify Company with SEBI Database
#     # -----------------------------------------------------

#     verification = check_platform(

#         company_name=analysis.company_name,

#         registration_number=analysis.registration_number

#     )

#     # -----------------------------------------------------
#     # STEP 3 : Decision Engine
#     # -----------------------------------------------------

#     recommendation = ""

#     risk_score = ""

#     reason = ""

#     # =====================================================
#     # VERIFIED
#     # =====================================================

#     if verification.status == "VERIFIED":

#         if analysis.risk == "SAFE":

#             recommendation = "INVEST"

#             risk_score = "Low"

#             reason = (

#                 f"{verification.explanation}\n\n"

#                 f"LLM Analysis: {analysis.reason}"

#             )

#         else:

#             recommendation = "DO NOT INVEST"

#             risk_score = "High"

#             reason = (

#                 f"{verification.explanation}\n\n"

#                 "Although the company is SEBI registered, "

#                 "the investment pitch contains scam "

#                 "indicators.\n\n"

#                 f"LLM Analysis: {analysis.reason}"

#             )

#     # =====================================================
#     # LIKELY VERIFIED
#     # =====================================================

#     elif verification.status == "LIKELY VERIFIED":

#         if analysis.risk == "SAFE":

#             recommendation = "VERIFY DETAILS BEFORE INVESTING"

#             risk_score = "Medium"

#             reason = (

#                 f"{verification.explanation}\n\n"

#                 "The company closely matches a "

#                 "SEBI registered broker, "

#                 "but the match is not exact.\n\n"

#                 f"LLM Analysis: {analysis.reason}"

#             )

#         else:

#             recommendation = "DO NOT INVEST"

#             risk_score = "High"

#             reason = (

#                 f"{verification.explanation}\n\n"

#                 "The company is similar to a SEBI "

#                 "registered broker, but the investment "

#                 "pitch itself contains multiple scam "

#                 "indicators.\n\n"

#                 f"LLM Analysis: {analysis.reason}"

#             )

#     # =====================================================
#     # SUSPICIOUS
#     # =====================================================

#     elif verification.status == "SUSPICIOUS":

#         recommendation = "DO NOT INVEST"

#         risk_score = "High"

#         reason = (

#             f"{verification.explanation}\n\n"

#             "The company name resembles a "

#             "SEBI registered broker but "

#             "is not an exact match.\n\n"

#             f"LLM Analysis: {analysis.reason}"

#         )

#     # =====================================================
#     # UNREGISTERED
#     # =====================================================

#     else:

#         recommendation = "DO NOT INVEST"

#         risk_score = "High"

#         reason = (

#             f"{verification.explanation}\n\n"

#             "The company could not be verified "

#             "in the SEBI registered brokers "

#             "database.\n\n"

#             f"LLM Analysis: {analysis.reason}"

#         )

#     # -----------------------------------------------------
#     # STEP 4 : Create Final Verdict Object
#     # -----------------------------------------------------

#     verdict = FinalVerdict(

#         recommendation=recommendation,

#         risk_score=risk_score,

#         reason=reason

#     )
#         # -----------------------------------------------------
#     # STEP 5 : Return Complete Result
#     # -----------------------------------------------------

#     return {

#         # ================================================
#         # LLM ANALYSIS
#         # ================================================

#         "investment_analysis": {

#             "company_name": analysis.company_name,

#             "registration_number": analysis.registration_number,

#             "pitch": analysis.pitch,

#             "risk": analysis.risk,

#             "reason": analysis.reason

#         },

#         # ================================================
#         # COMPANY VERIFICATION
#         # ================================================

#         "company_verification": {

#             "status": verification.status,

#             "confidence": verification.confidence,

#             "matched_company": verification.matched_company,

#             "registration_number": verification.registration_number,

#             "city": verification.city,

#             "state": verification.state,

#             "explanation": verification.explanation

#         },

#         # ================================================
#         # FINAL VERDICT
#         # ================================================

#         "final_verdict": {

#             "recommendation": verdict.recommendation,

#             "risk_score": verdict.risk_score,

#             "company_status": verification.status,

#             "confidence": verification.confidence,

#             "reason": verdict.reason

#         }

#     }

# def run_investment_verifier(state):
#     """
#     LangGraph node wrapper function.
#     Receives AgentState and calls investment_verifier_agent.
#     """

#     print("Investment Verifier Agent Running...")

#     user_input = state.get("user_input", "")

#     result = investment_verifier_agent(user_input)

#     return {
#         "investment_result": result
#     }
# # def run_investment_verifier(state: dict) -> dict:
# #     """Person 3 will build the real logic here later."""
# #     state["risk_level"] = "risky"
# #     state["explanation"] = "[Investment Verifier] Platform not found in SEBI registry. Promises unrealistic returns."
# #     state["extracted_entities"] = {"platform": ["CryptoMax Profit"]}
# #     return state

from dataclasses import asdict

from agent.investment_verifier.llm_checker import analyze_pitch
from agent.investment_verifier.rules import check_platform
from agent.investment_verifier.models import FinalVerdict


# ============================================================
# Investment Verifier Agent
# ============================================================

def investment_verifier_agent(user_input: str):

    # --------------------------------------------------------
    # Step 1
    # Analyse Investment Pitch using LLM
    # --------------------------------------------------------

    analysis = analyze_pitch(user_input)

    # --------------------------------------------------------
    # Step 2
    # Verify Company with SEBI
    # --------------------------------------------------------

    company_verification = check_platform(

        company_name=analysis.company_name,

        registration_number=analysis.registration_number

    )

    # --------------------------------------------------------
    # Step 3
    # Decide Final Recommendation
    # --------------------------------------------------------

    recommendation = "SAFE"

    risk_score = "LOW"

    final_reason = []

    # -----------------------------
    # Company Not Registered
    # -----------------------------

    if company_verification.status == "UNREGISTERED":

        recommendation = "DO NOT INVEST"

        risk_score = "HIGH"

        final_reason.append(

            "Company not found in SEBI database."

        )

    # -----------------------------
    # Suspicious Company
    # -----------------------------

    elif company_verification.status == "SUSPICIOUS":

        recommendation = "VERIFY BEFORE INVESTING"

        risk_score = "MEDIUM"

        final_reason.append(

            "Company resembles a registered broker but is not an exact match."

        )

    # -----------------------------
    # LLM Risk
    # -----------------------------

    if analysis.risk.upper() == "HIGH_RISK":

        recommendation = "DO NOT INVEST"

        risk_score = "HIGH"

        final_reason.append(

            analysis.reason

        )

    elif analysis.risk.upper() == "MEDIUM_RISK":

        if risk_score != "HIGH":

            recommendation = "VERIFY BEFORE INVESTING"

            risk_score = "MEDIUM"

        final_reason.append(

            analysis.reason

        )

    elif analysis.risk.upper() == "LOW_RISK":

        if risk_score == "LOW":

            recommendation = "SAFE"

        final_reason.append(

            analysis.reason

        )

    elif analysis.risk.upper() == "SAFE":

        final_reason.append(

            analysis.reason

        )

    # --------------------------------------------------------
    # Remove Duplicate Reasons
    # --------------------------------------------------------

    final_reason = list(

        dict.fromkeys(final_reason)

    )

    verdict = FinalVerdict(

        recommendation=recommendation,

        risk_score=risk_score,

        reason=" ".join(final_reason)

    )

    # --------------------------------------------------------
    # Final JSON
    # --------------------------------------------------------

    return {

        "investment_analysis": asdict(

            analysis

        ),

        "company_verification": asdict(

            company_verification

        ),

        "final_verdict": asdict(

            verdict

        )

    }


# ============================================================
# LangGraph Wrapper
# ============================================================

def run_investment_verifier(state: dict):

    result = investment_verifier_agent(

        state["user_input"]

    )

    state["risk_level"] = result["final_verdict"]["risk_score"]

    state["explanation"] = result["final_verdict"]["reason"]

    state["extracted_entities"] = result["investment_analysis"]["extracted_entities"]

    return state