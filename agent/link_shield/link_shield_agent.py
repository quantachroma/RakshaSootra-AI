"""
link_shield_agent.py — Link Shield Agent Core (Day 2 Integration)
RakshaSootra AI

Coordinates deterministic local rule checks, raw webpage textual scraping,
WHOIS domain context generation, and deep dynamic Gemini completions.
"""

import json
import whois
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Absolute package path imports targeting shared utility layers
from tool.llm_client import ask_llm
from agent.link_shield.rules import check_link_rules

def _fetch_domain_age_days(domain: str) -> int:
    """Performs live network query checking domain registration life window."""
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if isinstance(creation_date, datetime):
            delta = datetime.now() - creation_date
            return max(0, delta.days)
    except Exception:
        return -1
    return -1

def _scrape_page_content(url: str) -> str:
    """Crawls visible layout interface text data safely, stripping structural boilerplate."""
    scraped_url = url.strip()
    if not (scraped_url.startswith("http://") or scraped_url.startswith("https://")):
        scraped_url = "http://" + scraped_url

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        response = requests.get(scraped_url, headers=headers, timeout=5, allow_redirects=True)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            text = soup.get_text(separator=" ")
            return " ".join([line.strip() for line in text.splitlines() if line.strip()])[:4000]
    except Exception as e:
        return f"[Network extraction window closed due to execution block: {str(e)}]"
    return "[Non-200 transaction receipt status response code]"

def llm_check_link(url: str, domain: str, domain_age_days: int, page_text: str) -> dict:
    """Queries the centralized Gemini OpenRouter deployment model."""
    age_str = f"{domain_age_days} days old" if domain_age_days >= 0 else "Unknown / Recently Registered"

    system_prompt = "You are an elite cyber-forensics intelligence model inspecting Indian digital payment system fraud."
    
    user_prompt = f"""
    Evaluate the target URL structural parameters and scraped page text content for malicious patterns.

    [FORENSIC PARAMETERS]
    URL: {url}
    Domain: {domain}
    Registration Profile: {age_str}

    [SCRAPED WEB PAGE CONTENT LAYOUT]
    {page_text}

    [BEHAVIORAL RISK THREAT VECTORS]
    Inspect aggressively for these high-volume Indian financial scams:
    1. "Pay vs Receive" Inversion: Site offers a refund, claim credit, or lottery reward but guides users to type a UPI PIN.
    2. Hidden Autopay / e-Mandate Traps: Tricking citizens into setting continuous transaction authorizations.
    3. Remote Access Utility Injection: Instructing the target to download third-party software (AnyDesk, APKs).
    4. E-Commerce Uniform Pricing Fraud: Storefront displays completely distinct goods sharing flat discount prices.
    5. Fake Reputed Certifications: Cohorts using unauthorized IIT, AICTE, NPTEL badges.
    6. Viral Shared Forwarding Gates: Forcing visitors to distribute the URL link to WhatsApp chat groups.

    [OUTPUT COMPLIANCE DESIGN]
    Return ONLY a raw, unformatted JSON dictionary matching this architecture. Avoid markdown fences or text wrappers:
    {{
        "risk_level": "safe" or "risky" or "high_risk",
        "explanation": "A concise one-sentence description outlining the precise dynamic risk finding."
    }}
    """
    
    # FIX: Pass both system_prompt and user_prompt to our shared LLM client
    raw_response = ask_llm(system_prompt=system_prompt, user_text=user_prompt)
    
    try:
        clean_json = raw_response.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
    except Exception:
        return {
            "risk_level": "risky",
            "explanation": "Dynamic deep packet inspection triggered, but response payload failed structure extraction parsing."
        }

def check_link(url: str) -> dict:
    """Main consolidated link defense door entry point."""
    # 1. First Pass: Deterministic Local Rules
    rule_verdict = check_link_rules(url)
    domain = rule_verdict["extracted_entities"]["domain"]

    # Short circuit logic if local rules confidently confirm high risk
    if rule_verdict["risk_level"] == "high_risk":
        return rule_verdict

    # 2. Second Pass: Dynamic Context Extraction
    domain_age = _fetch_domain_age_days(domain)
    scraped_data = _scrape_page_content(url)

    # 3. Third Pass: Dynamic LLM Behavioral Assessment
    llm_verdict = llm_check_link(url, domain, domain_age, scraped_data)

    final_risk = llm_verdict.get("risk_level", rule_verdict["risk_level"])
    final_explanation = llm_verdict.get("explanation", rule_verdict["explanation"])

    # 4. Volatile Lifespan Override Filter
    if 0 <= domain_age < 30 and final_risk == "safe":
        final_risk = "risky"
        final_explanation = f"Page data patterns appear generic, but the registration record for domain ({domain}) is under 30 days old ({domain_age} days old), representing an elevated tracking window."

    return {
        "risk_level": final_risk,
        "explanation": final_explanation,
        "extracted_entities": {"domain": [domain]}
    }

# ==========================================
# LANGGRAPH INTEGRATION NODE
# ==========================================
def run_link_shield(state: dict) -> dict:
    """
    This is the LangGraph node. It takes the state, extracts the user's input,
    runs Person 2's real logic, and updates the state with the real verdict!
    """
    url = state.get("user_input", "").strip()
    
    # Run the REAL logic!
    real_verdict = check_link(url)
    
    # Update the LangGraph state
    state["risk_level"] = real_verdict["risk_level"]
    state["explanation"] = real_verdict["explanation"]
    state["extracted_entities"] = real_verdict["extracted_entities"]
    
    return state
