from dataclasses import dataclass


@dataclass
class InvestmentPlatform:
    platform_name: str


@dataclass
class InvestmentVerdict:
    risk_level: str
    explanation: str