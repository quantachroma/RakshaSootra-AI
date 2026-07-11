from dataclasses import dataclass


@dataclass
class Transaction:
    amount: float
    payee_name: str
    upi_id: str
    transaction_time: str
    status: str = "Pending"


@dataclass
class TransactionVerdict:
    risk_level: str
    explanation: str