import re

from rapidfuzz import process, fuzz

from tool.db_client import get_connection

from agent.investment_verifier.models import (
    CompanyVerification
)


# --------------------------------------------------------
# Normalize Company Name
# --------------------------------------------------------

def normalize_company_name(name: str) -> str:
    """
    Removes common company suffixes and punctuation so
    company names can be compared more accurately.
    """

    if not name:
        return ""

    name = name.lower()

    # Remove punctuation
    name = re.sub(r"[^\w\s]", " ", name)

    # Remove multiple spaces
    name = re.sub(r"\s+", " ", name).strip()

    # Remove common company suffixes
    suffixes = {
        "private",
        "pvt",
        "limited",
        "ltd",
        "llp",
        "inc",
        "corp",
        "corporation",
        "company",
        "co"
    }

    words = [
        word
        for word in name.split()
        if word not in suffixes
    ]

    return " ".join(words)


# --------------------------------------------------------
# Main Verification Function
# --------------------------------------------------------

def check_platform(
    company_name: str,
    registration_number: str = ""
) -> CompanyVerification:

    conn = get_connection()
    cursor = conn.cursor()

    # =====================================================
    # STEP 1
    # Registration Number Verification
    # =====================================================

    if registration_number:

        cursor.execute(
            """
            SELECT broker_name,
                   registration_no,
                   city,
                   state
            FROM sebi_registered
            WHERE LOWER(registration_no)=LOWER(?)
            """,
            (registration_number,)
        )

        row = cursor.fetchone()

        if row:

            conn.close()

            return CompanyVerification(

                status="VERIFIED",

                confidence=100,

                matched_company=row[0],

                registration_number=row[1],

                city=row[2],

                state=row[3],

                explanation=(
                    "Registration number successfully "
                    "verified in SEBI database."
                )
            )

    # =====================================================
    # STEP 2
    # Load Entire SEBI Database
    # =====================================================

    cursor.execute(
        """
        SELECT
            broker_name,
            registration_no,
            city,
            state
        FROM sebi_registered
        """
    )

    brokers = cursor.fetchall()

    conn.close()

    if not brokers:

        return CompanyVerification(

            status="UNKNOWN",

            confidence=0,

            matched_company="",

            registration_number="",

            city="",

            state="",

            explanation="SEBI database is empty."

        )

    # =====================================================
    # STEP 3
    # Normalize Input
    # =====================================================

    normalized_input = normalize_company_name(company_name)

    # =====================================================
    # STEP 4
    # Exact Match
    # =====================================================

    for broker in brokers:

        normalized_db = normalize_company_name(broker[0])

        if normalized_input == normalized_db:

            return CompanyVerification(

                status="VERIFIED",

                confidence=100,

                matched_company=broker[0],

                registration_number=broker[1],

                city=broker[2],

                state=broker[3],

                explanation=(
                    "Exact company match found in "
                    "SEBI database."
                )

            )

    # =====================================================
    # STEP 5
    # Fuzzy Matching
    # =====================================================

    normalized_names = [
        normalize_company_name(
            broker[0]
        )
        for broker in brokers
    ]

    match = process.extractOne(

        normalized_input,

        normalized_names,

        scorer=fuzz.token_sort_ratio

    )

    if match is None:

        return CompanyVerification(

            status="UNREGISTERED",

            confidence=0,

            matched_company="",

            registration_number="",

            city="",

            state="",

            explanation=(
                "No matching company found in "
                "SEBI database."
            )

        )

    matched_name = match[0]

    confidence = round(match[1], 2)

    matched_broker = None

    for broker in brokers:

        if normalize_company_name(
            broker[0]
        ) == matched_name:

            matched_broker = broker

            break

    # =====================================================
    # VERIFIED
    # =====================================================

    if confidence >= 98:

        return CompanyVerification(

            status="LIKELY VERIFIED",

            confidence=confidence,

            matched_company=matched_broker[0],

            registration_number=matched_broker[1],

            city=matched_broker[2],

            state=matched_broker[3],

            explanation=(
                "Company name is almost identical "
                "to a SEBI registered broker."
            )

        )

    # =====================================================
    # SUSPICIOUS
    # =====================================================

    if confidence >= 80:

        return CompanyVerification(

            status="SUSPICIOUS",

            confidence=confidence,

            matched_company=matched_broker[0],

            registration_number=matched_broker[1],

            city=matched_broker[2],

            state=matched_broker[3],

            explanation=(
                "The company name closely resembles "
                "a SEBI registered broker but is "
                "not an exact match."
            )

        )

    # =====================================================
    # UNREGISTERED
    # =====================================================

    return CompanyVerification(

        status="UNREGISTERED",

        confidence=confidence,

        matched_company="",

        registration_number="",

        city="",

        state="",

        explanation=(
            "No reliable SEBI registered broker "
            "matches this company."
        )

    )