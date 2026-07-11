from agent.transaction_guard.models import Transaction
from agent.transaction_guard.rules import analyze_transaction

#Fake transaction
transaction1 = Transaction(
    amount=500,
    payee_name="Rahul",
    upi_id="rahul@ybl",
    transaction_time="14:30"
)
verdict = analyze_transaction(transaction1)
print(verdict)