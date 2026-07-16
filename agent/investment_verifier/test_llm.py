from agent.investment_verifier.llm_checker import analyze_pitch

sample_pitch = """
Invest ₹10,000 today.

Guaranteed returns.

Double your money in 30 days.

Limited time offer.
"""

result = analyze_pitch(sample_pitch)

print(result)