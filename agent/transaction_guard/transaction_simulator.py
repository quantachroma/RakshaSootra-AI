from agent.transaction_guard.models import Transaction
from agent.transaction_guard.countdown import process_transaction


def simulate_transactions():

    transactions = [

        Transaction(
            amount=500,
            payee_name="Rahul",
            upi_id="rahul@ybl",
            transaction_time="14:30"
        ),

        Transaction(
            amount=25000,
            payee_name="Unknown",
            upi_id="unknown@ybl",
            transaction_time="02:15"
        ),

        Transaction(
            amount=20000,
            payee_name="Rahul",
            upi_id="rahul@ybl",
            transaction_time="18:30"
        ),

        Transaction(
            amount=700,
            payee_name="Amit",
            upi_id="amit@ybl",
            transaction_time="01:00"
        ),
        Transaction(
            amount=50000,
            payee_name="Investment Company",
            upi_id="investment@oksbi",
            transaction_time="03:10"
        )

    ]

    for transaction in transactions:

        process_transaction(transaction)


if __name__ == "__main__":
    simulate_transactions()