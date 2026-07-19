import json
import re

from tool.llm_client import ask_llm

from agent.transaction_guard.prompts import (
    TRANSACTION_GUARD_SYSTEM_PROMPT
)

from agent.transaction_guard.models import (
    TransactionAnalysis,
    ExtractedEntities,
    Transaction
)


# ============================================================
# Extract JSON safely from LLM response
# ============================================================

def extract_json(response: str) -> dict:
    """
    Extract JSON from OpenRouter response.
    Handles cases where the model accidentally
    returns markdown or extra text.
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

    raise ValueError("LLM returned invalid JSON.")


# ============================================================
# Analyze Transaction
# ============================================================

def analyze_transaction_llm(
    transaction: Transaction
) -> TransactionAnalysis:

    user_prompt = f"""
Amount : ₹{transaction.amount}

Payee Name : {transaction.payee_name}

UPI ID : {transaction.upi_id}

Transaction Time : {transaction.transaction_time}
"""

    response = ask_llm(

        system_prompt=TRANSACTION_GUARD_SYSTEM_PROMPT,

        user_text=user_prompt

    )

    data = extract_json(response)

    entities = data.get(
        "extracted_entities",
        {}
    )

    extracted_entities = ExtractedEntities(

        upi_ids=entities.get(
            "upi_ids",
            []
        ),

        phone_numbers=entities.get(
            "phone_numbers",
            []
        )

    )

    return TransactionAnalysis(

        risk=data.get(
            "risk",
            "SAFE"
        ),

        reason=data.get(
            "reason",
            ""
        ),

        extracted_entities=extracted_entities

    )