from tool.db_client import get_connection

payees = [
    ("Rahul", "rahul@ybl"),
    ("Amit", "amit@ybl"),
    ("Priya", "priya@okaxis"),
    ("Neha", "neha@ibl"),
    ("Mom", "mom@oksbi")
]

conn = get_connection()
cursor = conn.cursor()

# Optional: clear old test data
cursor.execute("DELETE FROM payee_history")

for payee_name, upi_id in payees:
    cursor.execute(
        """
        INSERT INTO payee_history (payee_name, upi_id)
        VALUES (?, ?)
        """,
        (payee_name, upi_id)
    )

conn.commit()
conn.close()

print("Test payees inserted successfully!")