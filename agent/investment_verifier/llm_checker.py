import json

from tool.llm_client import ask_llm
from agent.investment_verifier.prompts import (
    SCAM_DETECTION_SYSTEM_PROMPT,
)


def analyze_pitch(pitch: str):

    response = ask_llm(
        system_prompt=SCAM_DETECTION_SYSTEM_PROMPT,
        user_text=pitch
    )

    try:
        return json.loads(response)

    except Exception:

        return {
            "risk": "Unknown",
            "reason": response
        }