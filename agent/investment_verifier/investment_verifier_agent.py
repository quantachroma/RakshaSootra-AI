from agent.investment_verifier.models import InvestmentPlatform
from agent.investment_verifier.rules import check_platform


def investment_verifier_agent(platform_name: str):
    """
    Entry point for the Investment Verifier agent.
    """

    platform = InvestmentPlatform(
        platform_name=platform_name
    )

    return check_platform(platform)