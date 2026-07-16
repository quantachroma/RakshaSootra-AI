from agent.investment_verifier.investment_verifier_agent import (
    investment_verifier_agent
)

test_cases = [

    {
        "platform": "Zerodha",
        "pitch": "Invest in mutual funds through Zerodha for long-term wealth creation."
    },

    {
        "platform": "Zerodha",
        "pitch": "Guaranteed returns! Double your money in 30 days. Limited time offer!"
    },

    {
        "platform": "Fake Investments Pvt Ltd",
        "pitch": "Build wealth by investing regularly in diversified equity funds."
    },

    {
        "platform": "Unknown Broker",
        "pitch": "100% profit. No risk. Invest immediately before the offer ends."
    },

    {
        "platform": "Angel One",
        "pitch": "Start a SIP and invest consistently to achieve your long-term financial goals."
    }

]

for i, test in enumerate(test_cases, start=1):

    print("\n" + "=" * 60)
    print(f"TEST CASE {i}")
    print("=" * 60)

    result = investment_verifier_agent(
        platform_name=test["platform"],
        pitch=test["pitch"]
    )

    print("\nBroker Verification")
    print("-------------------")
    print(result["broker_verification"])

    print("\nPitch Analysis")
    print("--------------")
    print(result["pitch_analysis"])

    print("\nFinal Verdict")
    print("-------------")
    print(result["final_verdict"])