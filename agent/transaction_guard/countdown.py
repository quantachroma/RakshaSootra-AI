import time

from agent.transaction_guard.models import Transaction
from agent.transaction_guard.rules import analyze_transaction


import streamlit as st
import time


def start_countdown(seconds):

    placeholder = st.empty()

    for remaining in range(seconds, 0, -1):
        placeholder.warning(
            f"⏳ Transaction will be processed in {remaining} seconds..."
        )
        time.sleep(1)

    placeholder.success("Countdown Complete")


def process_transaction(transaction: Transaction):
    """
    Complete transaction flow.
    """

    print("\n==============================")
    print("📩 Transaction Received")
    print("==============================")

    verdict = analyze_transaction(transaction)

    if verdict.risk_level == "High Risk":

        transaction.status = "Pending"

        print("\n⚠ High Risk Transaction Detected")
        print(verdict.explanation)

        print("\nStatus :", transaction.status)

        start_countdown(10)

        transaction.status = "Cancelled"

        print("\n❌ Transaction Cancelled")

    else:

        transaction.status = "Approved"

        print("\n✅ Transaction Approved")

    print("\nFinal Status :", transaction.status)