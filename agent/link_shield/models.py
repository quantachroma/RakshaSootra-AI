"""
Owner- Person 2 - Priyanshi Saini
models.py — Link Shield Data Models
RakshaSootra AI

Defines the strict schema contract for all Link Shield outputs.
This schema is shared across rule checks, LLM checks, and LangGraph routing.
"""

from typing import Literal
from pydantic import BaseModel, Field


class LinkShieldEntities(BaseModel):
    """
    Structured entities extracted from the URL.
    These entities are later used by the fraud graph.
    """

    domain: str = Field(
        ...,
        description="Root domain extracted from the URL.",
        examples=["sbi.co.in"]
    )


class LinkShieldVerdict(BaseModel):
    """
    Standard verdict returned by the Link Shield agent.
    Every execution path (rules or LLM) must return this schema.
    """

    risk_level: Literal["safe", "risky", "high risk"] = Field(
        ...,
        description="Overall risk classification."
    )

    explanation: str = Field(
        ...,
        description="Human-readable explanation of why the URL received this verdict."
    )

    extracted_entities: LinkShieldEntities = Field(
        ...,
        description="Structured entities extracted from the URL."
    )