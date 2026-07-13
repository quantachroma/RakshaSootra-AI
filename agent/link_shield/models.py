"""
models.py — Link Shield Data Models
RakshaSootra AI

Defines the strict schema contract for the Link Shield agent's outputs.
"""

from pydantic import BaseModel, Field

class LinkShieldEntities(BaseModel):
    """
    Structured entities extracted from the URL logic.
    Feeds directly into the central fraud network graph.
    """
    domain: str = Field(
        ..., 
        description="The clean root domain extracted from the URL (e.g., 'hdfccbank.com')."
    )

class LinkShieldVerdict(BaseModel):
    """
    The unified verdict shape required for the Link Shield agent.
    Both local rules and LLM checks must return this exact structure.
    """
    risk_level: str = Field(
        ..., 
        description="Must strictly be: 'safe', 'risky', or 'high risk'."
    )
    explanation: str = Field(
        ..., 
        description="A plain-language, human-readable sentence explaining the verdict."
    )
    extracted_entities: LinkShieldEntities = Field(
        ..., 
        description="The metadata dictionary containing parsed threat entities."
    )