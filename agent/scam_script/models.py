"""
models.py — Scam Script Data Models
RakshaSootra AI

Defines the strict schema contract for the Scam Script agent's outputs.
"""

from typing import Optional, List, Literal

from pydantic import BaseModel, Field


class ScamScriptEntities(BaseModel):
    """
    Structured entities extracted from scam scripts.

    These entities explain why a message/call was classified
    as suspicious and feed into the fraud intelligence layer.
    """

    impersonated_agency: Optional[str] = Field(
        default=None,
        description="Government agency or authority being impersonated."
    )

class ScamScriptVerdict(BaseModel):
    """
    Unified output schema for the Scam Script Agent.

    All rule-based and AI-based detections must conform
    to this structure.
    """

    risk_level: Literal[
        "safe",
        "risky",
        "high risk"
    ] = Field(
        ...,
        description="Risk classification of the scam script."
    )

    explanation: str = Field(
        ...,
        description="Human-readable explanation for the verdict."
    )

    extracted_entities: ScamScriptEntities = Field(
        ...,
        description="Detected scam-related entities."
    )