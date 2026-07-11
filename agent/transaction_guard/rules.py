from datetime import datetime
from agent.transaction_guard.models import (
    Transaction,
    TransactionVerdict
)

from tool.db_client import get_connection

def get_threshold():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT threshold FROM user_rules WHERE id = 1"
    )

    result = cursor.fetchone()   # Fetch the row
    connection.close()           # Close the connection

    if result:
        return result[0]         # Return the threshold value

    return None

def check_amount(transaction: Transaction):
    threshold = get_threshold()

    if transaction.amount > threshold:
        return True, "Transaction amount exceeds threshold."

    return False, ""

def check_new_payee(transaction: Transaction):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM payee_history WHERE upi_id = ?",
        (transaction.upi_id,)
    )

    result = cursor.fetchone()

    connection.close()

    if result is None:
        return True, "Recipient is a new payee."

    return False, ""

def check_transaction_time(transaction: Transaction):
    transaction_time = datetime.strptime(
    transaction.transaction_time,
    "%H:%M"
    )
    hour = transaction_time.hour
    if 0 <= hour < 5:
       return True, "Transaction made during unusual hours."

    return False, ""

def analyze_transaction(transaction: Transaction):
    reasons = []
    
    amount_flag, amount_reason = check_amount(transaction)
    
    if amount_flag:
        reasons.append(amount_reason)
    
    
    new_payee_flag, new_payee_reason = check_new_payee(transaction)

    if new_payee_flag:
        reasons.append(new_payee_reason)

    
    time_flag, time_reason = check_transaction_time(transaction)

    if time_flag:
       reasons.append(time_reason)
    

    if reasons:
        return TransactionVerdict(
            risk_level="High Risk",
            explanation="\n".join(reasons),
        )

    return TransactionVerdict(
        risk_level="Safe",
        explanation="No suspicious activity detected.",
    )