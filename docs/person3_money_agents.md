
# Person 3 – Money-Side Agents

Name: Ritisha Sharma

## Overview

As Person 3, I developed the money-side fraud detection modules of RakshaSootra AI. My work focused on identifying fraudulent financial transactions and suspicious investment opportunities by combining rule-based validation with LLM-powered analysis. I also implemented structured entity extraction to support fraud graph generation across the system.

---

## Module 1 – Transaction Guard

### Objective

To detect suspicious UPI transactions before money is transferred and classify their risk level.

### Work Done

* Implemented rule-based transaction analysis.
* Added validation for:

  * High transaction amounts
  * New payees
  * Unusual transaction timings
* Integrated LLM analysis for contextual explanations.
* Implemented structured extraction of:

  * UPI IDs
  * Phone Numbers
* Generated standardized risk levels:

  * SAFE
  * LOW_RISK
  * MEDIUM_RISK
  * HIGH_RISK
* Performed testing across multiple transaction scenarios to validate rule execution and entity extraction.

---

## Module 2 – Investment Verifier

### Objective

To verify the legitimacy of investment platforms and identify potentially fraudulent investment opportunities.

### Work Done

* Implemented SEBI database verification using SQLite.
* Added:

  * Registration number verification
  * Exact company matching
  * Fuzzy company matching using RapidFuzz
* Integrated LLM-based investment pitch analysis.
* Implemented structured extraction of:

  * Platform Names
  * Domains
* Generated final investment recommendations based on SEBI verification and pitch analysis.
* Tested the module using registered brokers, fake platforms, guaranteed-return schemes, and other scam scenarios.

---

## Entity Extraction

Implemented a standardized entity extraction format across money-side agents to ensure compatibility with the Fraud Graph.

Transaction Guard

* UPI IDs
* Phone Numbers

Investment Verifier

* Platform Names
* Domains

---

## Testing

Validated the modules using diverse test cases covering:
[21-07-2026 20:59] Nerdo: * Legitimate and suspicious UPI transactions
* High-value transactions
* New payees
* Transactions during unusual hours
* Registered and unregistered investment platforms
* Guaranteed-return investment scams
* Fake investment pitches
* Fuzzy company name matching

---

## Technologies Used

* Python
* LangGraph
* SQLite
* OpenRouter API
* RapidFuzz
* Regular Expressions

---

## Key Contributions

* Developed the Transaction Guard module with rule-based fraud detection and LLM-assisted analysis.
* Developed the Investment Verifier with SEBI verification, fuzzy matching, and investment pitch evaluation.
* Implemented standardized entity extraction for UPI IDs, phone numbers, platform names, and domains.
* Integrated outputs with the LangGraph workflow to support downstream fraud graph generation.
* Performed comprehensive testing and debugging to ensure reliable and consistent module behavior.

This version is concise, professional, and suitable for inclusion in both your project repository and your evaluator documentation.