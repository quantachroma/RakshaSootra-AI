# 

import json
import re

from tool.llm_client import ask_llm

from agent.investment_verifier.prompts import (
    SCAM_DETECTION_SYSTEM_PROMPT
)

from agent.investment_verifier.models import (
    InvestmentAnalysis,
    ExtractedEntities
)


# ============================================================
# Extract JSON from LLM Response
# ============================================================

def extract_json(response: str) -> dict:
    """
    Extracts JSON from an LLM response.

    Handles cases where the model accidentally returns
    extra text or markdown.
    """

    try:
        return json.loads(response)

    except Exception:

        match = re.search(
            r"\{.*\}",
            response,
            re.DOTALL
        )

        if match:

            try:
                return json.loads(match.group())

            except Exception:
                pass

    raise ValueError(
        "LLM did not return valid JSON."
    )


# ============================================================
# Analyse Investment Pitch
# ============================================================

def analyze_pitch(pitch: str) -> InvestmentAnalysis:

    response = ask_llm(

        system_prompt=SCAM_DETECTION_SYSTEM_PROMPT,

        user_text=pitch

    )

    data = extract_json(response)

    entities = data.get(
        "extracted_entities",
        {}
    )

    extracted_entities = ExtractedEntities(

        platform_names=entities.get(
            "platform_names",
            []
        ),

        domains=entities.get(
            "domains",
            []
        )

    )

    return InvestmentAnalysis(

        company_name=data.get(
            "company_name",
            ""
        ),

        registration_number=data.get(
            "registration_number",
            ""
        ),

        pitch=pitch,

        risk=data.get(
            "risk",
            "UNKNOWN"
        ),

        reason=data.get(
            "reason",
            ""
        ),

        extracted_entities=extracted_entities

    )