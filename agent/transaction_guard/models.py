from dataclasses import dataclass, field
from typing import List


# ============================================================
# Transaction Information
# ============================================================

@dataclass
class Transaction:

    amount: float

    payee_name: str

    upi_id: str

    transaction_time: str

    status: str = "Pending"


# ============================================================
# Extracted Entities
# ============================================================

@dataclass
class ExtractedEntities:

    upi_ids: List[str] = field(default_factory=list)

    phone_numbers: List[str] = field(default_factory=list)


# ============================================================
# Rule Engine Result
# ============================================================

@dataclass
class RuleResult:

    risk_level: str

    explanation: str


# ============================================================
# LLM Analysis
# ============================================================

@dataclass
class TransactionAnalysis:

    risk: str

    reason: str

    extracted_entities: ExtractedEntities


# ============================================================
# Final Verdict
# ============================================================

@dataclass
class TransactionVerdict:

    risk_level: str

    explanation: str

    extracted_entities: ExtractedEntities