import json

from tool.llm_client import ask_llm

from agent.investment_verifier.prompts import (
    INVESTMENT_ANALYSIS_SYSTEM_PROMPT,
)

from agent.investment_verifier.models import (
    InvestmentAnalysis,
)


def analyze_investment(user_input: str) -> InvestmentAnalysis:
    """
    Sends the user's investment message to the LLM,
    parses the JSON response, and returns an
    InvestmentAnalysis object.
    """

    response = ask_llm(
        system_prompt=INVESTMENT_ANALYSIS_SYSTEM_PROMPT,
        user_text=user_input
    )

    try:

        data = json.loads(response)

        return InvestmentAnalysis(

            company_name=data.get("company_name", "").strip(),

            registration_number=data.get(
                "registration_number",
                ""
            ).strip(),

            pitch=data.get("pitch", "").strip(),

            risk=data.get(
                "risk",
                "UNKNOWN"
            ).strip().upper(),

            reason=data.get(
                "reason",
                "No reason provided."
            ).strip()

        )

    except Exception:

        return InvestmentAnalysis(

            company_name="",

            registration_number="",

            pitch=user_input,

            risk="UNKNOWN",

            reason="Unable to parse LLM response."

        )