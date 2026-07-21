from agent.investment_verifier.models import InvestmentPlatform
from agent.investment_verifier.rules import check_platform

platforms = [
    InvestmentPlatform("Zerodha"),
    InvestmentPlatform("Groww"),
    InvestmentPlatform("Angel One"),
    InvestmentPlatform("Upstox"),
    InvestmentPlatform("Fake Broker")
]

for platform in platforms:
    verdict = check_platform(platform)

    print("=" * 50)
    print("Platform:", platform.platform_name)
    print("Risk Level:", verdict.risk_level)
    print("Explanation:", verdict.explanation)