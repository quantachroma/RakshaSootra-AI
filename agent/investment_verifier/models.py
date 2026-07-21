# from dataclasses import dataclass


# # -------------------------------------------------------
# # Information extracted by the LLM
# # -------------------------------------------------------

# @dataclass
# class InvestmentAnalysis:

#     company_name: str

#     registration_number: str

#     pitch: str

#     risk: str

#     reason: str


# # -------------------------------------------------------
# # Result of SEBI verification
# # -------------------------------------------------------

# @dataclass
# class CompanyVerification:

#     status: str

#     confidence: float

#     matched_company: str

#     registration_number: str

#     city: str

#     state: str

#     explanation: str


# # -------------------------------------------------------
# # Final Result
# # -------------------------------------------------------

# @dataclass
# class FinalVerdict:

#     recommendation: str

#     risk_score: str

#     reason: str

from dataclasses import dataclass, field
from typing import List


# ============================================================
# Extracted Entities
# ============================================================

@dataclass
class ExtractedEntities:
    """
    Entities extracted from the investment pitch.

    This structure is shared across all agents so that the
    Fraud Graph can consume a common schema.
    """

    platform_names: List[str] = field(default_factory=list)
    domains: List[str] = field(default_factory=list)


# ============================================================
# LLM Analysis
# ============================================================

@dataclass
class InvestmentAnalysis:
    """
    Output returned by the LLM after analysing
    an investment pitch.
    """

    company_name: str

    registration_number: str

    pitch: str

    risk: str

    reason: str

    extracted_entities: ExtractedEntities


# ============================================================
# Company Verification
# ============================================================

@dataclass
class CompanyVerification:
    """
    Result after checking against
    the SEBI database.
    """

    status: str

    confidence: float

    matched_company: str

    registration_number: str

    city: str

    state: str

    explanation: str


# ============================================================
# Final Verdict
# ============================================================

@dataclass
class FinalVerdict:
    """
    Final recommendation shown to the user.
    """

    recommendation: str

    risk_score: str

    reason: str