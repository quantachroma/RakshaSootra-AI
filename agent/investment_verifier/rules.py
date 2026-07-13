from tool.db_client import get_connection
from agent.investment_verifier.models import (
    InvestmentPlatform,
    InvestmentVerdict
)


def check_platform(platform: InvestmentPlatform):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT broker_name, registration_no
        FROM sebi_registered
        WHERE LOWER(broker_name) LIKE LOWER(?)
        """,
        (f"%{platform.platform_name}%",)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return InvestmentVerdict(
            risk_level="Safe",
            explanation=f"{result[0]} is registered with SEBI.\nRegistration No: {result[1]}"
        )

    return InvestmentVerdict(
        risk_level="High Risk",
        explanation="Platform not found in the SEBI registered brokers database."
    )