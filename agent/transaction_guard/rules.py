# from datetime import datetime
# from agent.transaction_guard.models import (
#     Transaction,
#     TransactionVerdict
# )

# from tool.db_client import get_connection

# def get_threshold():
#     connection = get_connection()
#     cursor = connection.cursor()

#     cursor.execute(
#         "SELECT threshold FROM user_rules WHERE id = 1"
#     )

#     result = cursor.fetchone()   # Fetch the row
#     connection.close()           # Close the connection

#     if result:
#         return result[0]         # Return the threshold value

#     return None

# def check_amount(transaction: Transaction):
#     threshold = get_threshold()

#     if transaction.amount > threshold:
#         return True, "Transaction amount exceeds threshold."

#     return False, ""

# def check_new_payee(transaction: Transaction):
#     connection = get_connection()
#     cursor = connection.cursor()

#     cursor.execute(
#         "SELECT * FROM payee_history WHERE upi_id = ?",
#         (transaction.upi_id,)
#     )

#     result = cursor.fetchone()

#     connection.close()

#     if result is None:
#         return True, "Recipient is a new payee."

#     return False, ""

# def check_transaction_time(transaction: Transaction):
#     transaction_time = datetime.strptime(
#     transaction.transaction_time,
#     "%H:%M"
#     )
#     hour = transaction_time.hour
#     if 0 <= hour < 5:
#        return True, "Transaction made during unusual hours."

#     return False, ""

# def analyze_transaction(transaction: Transaction):
#     reasons = []
    
#     amount_flag, amount_reason = check_amount(transaction)
    
#     if amount_flag:
#         reasons.append(amount_reason)
    
    
#     new_payee_flag, new_payee_reason = check_new_payee(transaction)

#     if new_payee_flag:
#         reasons.append(new_payee_reason)

    
#     time_flag, time_reason = check_transaction_time(transaction)

#     if time_flag:
#        reasons.append(time_reason)
    

#     if reasons:
#         return TransactionVerdict(
#             risk_level="High Risk",
#             explanation="\n".join(reasons),
#         )

#     return TransactionVerdict(
#         risk_level="Safe",
#         explanation="No suspicious activity detected.",
#     )


from datetime import datetime

from tool.db_client import get_connection

from agent.transaction_guard.models import (
    Transaction,
    TransactionVerdict,
    RuleResult,
    ExtractedEntities
)

from agent.transaction_guard.llm_checker import (
    analyze_transaction_llm
)


# ============================================================
# Get User Threshold
# ============================================================

def get_threshold():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT threshold FROM user_rules WHERE id=1"
    )

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return 10000


# ============================================================
# Amount Rule
# ============================================================

def check_amount(transaction: Transaction):

    threshold = get_threshold()

    if transaction.amount > threshold:

        return RuleResult(
            risk_level="HIGH_RISK",
            explanation=(
                f"Transaction amount ₹{transaction.amount} "
                f"exceeds threshold ₹{threshold}."
            )
        )

    return None


# ============================================================
# New Payee Rule
# ============================================================

def check_new_payee(transaction: Transaction):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM payee_history
        WHERE upi_id = ?
        """,
        (transaction.upi_id,)
    )

    result = cursor.fetchone()

    connection.close()

    if result is None:

        return RuleResult(
            risk_level="LOW_RISK",
            explanation="Recipient is a new payee."
        )

    return None


# ============================================================
# Transaction Time Rule
# ============================================================

def check_transaction_time(transaction: Transaction):

    transaction_time = datetime.strptime(
        transaction.transaction_time,
        "%H:%M"
    )

    hour = transaction_time.hour

    if 0 <= hour < 5:

        return RuleResult(
            risk_level="MEDIUM_RISK",
            explanation="Transaction initiated during unusual hours."
        )

    return None


# ============================================================
# Main Rule Engine
# ============================================================

def analyze_transaction(transaction: Transaction):

    explanations = []

    highest_risk = "SAFE"

    extracted_entities = ExtractedEntities(
        upi_ids=[],
        phone_numbers=[]
    )

    # -----------------------------
    # Amount Rule
    # -----------------------------

    amount_result = check_amount(transaction)

    if amount_result:

        explanations.append(amount_result.explanation)

        highest_risk = "HIGH_RISK"

    # -----------------------------
    # New Payee Rule
    # -----------------------------

    payee_result = check_new_payee(transaction)

    if payee_result:

        explanations.append(payee_result.explanation)

        if highest_risk == "SAFE":
            highest_risk = "LOW_RISK"

    # -----------------------------
    # Time Rule
    # -----------------------------

    time_result = check_transaction_time(transaction)

    if time_result:

        explanations.append(time_result.explanation)

        if highest_risk == "SAFE":
            highest_risk = "MEDIUM_RISK"

    # -----------------------------
    # LLM Analysis
    # -----------------------------

    try:

        llm_analysis = analyze_transaction_llm(transaction)

        extracted_entities.upi_ids.extend(
            llm_analysis.extracted_entities.upi_ids
        )

        extracted_entities.phone_numbers.extend(
            llm_analysis.extracted_entities.phone_numbers
        )

        # Only use LLM explanation when no rule has flagged the transaction
        if highest_risk == "SAFE" and llm_analysis.reason:
            explanations.append(llm_analysis.reason)

    except Exception:
        pass

    # -----------------------------
    # Remove Duplicate Entities
    # -----------------------------

    extracted_entities.upi_ids = list(
        set(extracted_entities.upi_ids)
    )

    extracted_entities.phone_numbers = list(
        set(extracted_entities.phone_numbers)
    )

    # -----------------------------
    # Remove Duplicate Explanations
    # -----------------------------

    explanations = list(
        dict.fromkeys(
            [x for x in explanations if x]
        )
    )

    # -----------------------------
    # Final Verdict
    # -----------------------------

    if highest_risk == "SAFE":

        return TransactionVerdict(
            risk_level="SAFE",
            explanation="No suspicious activity detected.",
            extracted_entities=extracted_entities
        )

    return TransactionVerdict(
        risk_level=highest_risk,
        explanation="\n".join(explanations),
        extracted_entities=extracted_entities
    )