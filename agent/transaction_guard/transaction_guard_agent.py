import re

from agent.transaction_guard.models import Transaction
from agent.transaction_guard.rules import analyze_transaction


# ============================================================
# Extract Transaction Details from User Input
# ============================================================

def extract_transaction(user_input: str) -> Transaction:

    text = user_input.lower()

    # ----------------------------
    # Amount
    # ----------------------------

    amount = 0

    amount_match = re.search(

        r"(?:₹|rs\.?|inr)?\s*(\d+(?:,\d+)*)",

        text,

        re.IGNORECASE

    )

    if amount_match:

        amount = float(

            amount_match.group(1).replace(",", "")

        )

    # ----------------------------
    # UPI ID
    # ----------------------------

    upi = ""

    upi_match = re.search(

        r"[\w.\-]+@[a-zA-Z]+",

        user_input

    )

    if upi_match:

        upi = upi_match.group()

    # ----------------------------
    # Time
    # ----------------------------

    time = "12:00"

    time_match = re.search(

        r"(\d{1,2}:\d{2})",

        user_input

    )

    if time_match:

        time = time_match.group(1)

    # ----------------------------
    # Payee Name
    # ----------------------------

    payee = "Unknown"

    payee_match = re.search(

        r"(?:to|paid to|recipient)\s+([A-Za-z ]+)",

        user_input,

        re.IGNORECASE

    )

    if payee_match:

        payee = payee_match.group(1).strip()

    return Transaction(

        amount=amount,

        payee_name=payee,

        upi_id=upi,

        transaction_time=time

    )


# ============================================================
# LangGraph Node
# ============================================================

def run_transaction_guard(state: dict):

    transaction = extract_transaction(

        state["user_input"]

    )

    verdict = analyze_transaction(

        transaction

    )

    state["risk_level"] = verdict.risk_level

    state["explanation"] = verdict.explanation

    state["extracted_entities"] = {

        "upi_ids": verdict.extracted_entities.upi_ids,

        "phone_numbers": verdict.extracted_entities.phone_numbers

    }

    return state