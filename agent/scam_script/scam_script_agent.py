"""
scam_script_agent.py — Scam Script Checker Agent (Day 4 Integrated)
RakshaSootra AI
"""
import json
import re
from functools import lru_cache
from tool.llm_client import ask_llm
from agent.scam_script.rules import check_script_rules


@lru_cache(maxsize=128)
def llm_check_script(text: str) -> dict:
    system_prompt = """
    You are an expert fraud detection analyst for the Raksha Sootra system. 
    Analyze the provided text message or transcript. 
    Does the overall narrative match a known scam script, even with different keywords?
    Look for psychological manipulation, false urgency, isolation tactics, or fake authority.
    
    You must return a raw JSON object with strictly these two keys:
    1. "risk_level": strictly one of ["safe", "risky", "high risk"]
    2. "explanation": a plain-language explanation of your verdict
    """
    
    try:
        response_text = ask_llm(system_prompt, text)
        
        # 1. Clean out markdown code blocks if Gemini includes them
        cleaned_response = response_text.replace("```json", "").replace("```", "").strip()
        
        # 2. Extract the JSON object safely
        json_match = re.search(r'\{.*\}', cleaned_response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group(0))
        else:
            raise ValueError(f"No valid JSON object found in response: {response_text}")
        
        if result.get("risk_level") not in ["safe", "risky", "high risk"]:
            result["risk_level"] = "risky"
            
        return {
            "risk_level": result["risk_level"], 
            "explanation": result["explanation"]
        }
    except Exception as e:
        return {
            "risk_level": "risky", 
            "explanation": f"LLM failed: {str(e)}"
        }
        

def check_script(text: str) -> dict:
    """
    Main Consolidated Entry Point:
    Golden Rule Flow: Rule Check (rules.py) -> Gemini Check -> Unified Verdict.
    """
    # 1. Fast Rule Check (calls your untouched rules.py logic)
    rule_verdict = check_script_rules(text)
    
    # Fast fail if rules caught a definitive High Risk signature (saves API latency)
    if rule_verdict["risk_level"] == "high risk":
        return rule_verdict
        
    # 2. Gemini LLM Check (catches keyword dodges and psychological manipulation)
    llm_verdict = llm_check_script(text)
    
    # If the rule check caught isolated risky elements (e.g. agency mention), preserve that baseline
    if rule_verdict["risk_level"] == "risky" and llm_verdict["risk_level"] == "safe":
        return rule_verdict
        
    return llm_verdict

def run_scam_script(state: dict) -> dict:
    """
    LangGraph Router Node Entry Point (Required by Person 1).
    Reads input from shared state and returns updated verdict state.
    """
    user_input = state.get("input") or state.get("user_input") or state.get("text") or ""
    verdict = check_script(user_input)
    
    state["risk_level"] = verdict["risk_level"]
    state["explanation"] = verdict["explanation"]
    state["extracted_entities"] = verdict.get("extracted_entities", {})
    
    return state

if __name__ == "__main__":
    # Day 4 Requirement: Test on 5 scripts that dodge basic keyword matching
    test_scripts = [
        # 1. Crypto / Arbitrage Investment Scam Dodge
        # Dodges: 'part-time job', 'lottery', 'UPI transfer'
        "Hey VIP member! Our exclusive algorithmic cryptocurrency arbitrage bot has locked in a 400% return for this week's crypto bull run. Transfer USDT to our liquidity pool wallet within 30 minutes to claim your payout before the smart contract locks.",

        # 2. Fake Billing / Auto-Renewal Scam Dodge
        # Dodges: 'electricity bill', 'KYC', 'bank account'
        "Alert from Billing Support: Your annual cloud storage and streaming subscription auto-renewal of $399.00 has been processed. If you did not authorize this charge, click the secure verification portal link below immediately to cancel and receive an instant refund.",

        # 3. IT Support / Remote Access Scam Dodge
        # Dodges: 'police', 'customs', 'parcel'
        "Microsoft Security Center Warning: Your system registry has detected suspicious outbound data packets originating from an unauthorized IP. Call our toll-free support helpline immediately to allow a certified technician to cleanse your device.",

        # 4. Disaster Relief / Fake Charity Scam Dodge
        # Dodges: 'loan', 'job', 'lottery'
        "Urgent Relief Appeal: Severe flash floods have stranded hundreds of families in your zone. Direct emergency medical supplies and food kits are dispatching now. Scan this QR code to sponsor an instant rescue kit.",

        # 5. Safe Baseline (Urgent Professional / Calendar Change)
        # Tests that professional urgency does not trigger false positives
        "Hi team, the client presentation has been moved up to 10:00 AM sharp due to an international timezone shift. Please review the updated slide deck before joining the conference bridge."
    ]
    print("--- Running Integrated Day 4 Scam Script Agent (Rule Check + Gemini) ---")
    for i, script in enumerate(test_scripts, 1):
        print(f"\n[Test {i}] Input: '{script}'")
        verdict = check_script(script)
        print(f"         Verdict: {verdict}")