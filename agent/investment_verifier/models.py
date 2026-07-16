from dataclasses import dataclass


# -------------------------------------------------------
# Information extracted by the LLM
# -------------------------------------------------------

@dataclass
class InvestmentAnalysis:

    company_name: str

    registration_number: str

    pitch: str

    risk: str

    reason: str


# -------------------------------------------------------
# Result of SEBI verification
# -------------------------------------------------------

@dataclass
class CompanyVerification:

    status: str

    confidence: float

    matched_company: str

    registration_number: str

    city: str

    state: str

    explanation: str


# -------------------------------------------------------
# Final Result
# -------------------------------------------------------

@dataclass
class FinalVerdict:

    recommendation: str

    risk_score: str

    reason: str