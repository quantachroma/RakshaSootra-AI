from agent.transaction_guard.models import Transaction
from agent.transaction_guard.rules import analyze_transaction

#Fake transaction
transaction1 = transaction2 = Transaction(
    amount=800,
    payee_name="Priya",
    upi_id="priya@ybl",
    transaction_time="15:00"

)

verdict = analyze_transaction(transaction1)
print("\nRisk Level")
print(verdict.risk_level)

print("\nExplanation")
print(verdict.explanation)

print("\nExtracted Entities")
print(verdict.extracted_entities)