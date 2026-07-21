import sqlite3

conn = sqlite3.connect("raksha_sootra.db")
cursor = conn.cursor()

broker = "Zerodha"

cursor.execute("""
SELECT broker_name, registration_no
FROM sebi_registered
WHERE LOWER(broker_name) LIKE LOWER(?)
""", (f"%{broker}%",))

result = cursor.fetchone()

if result:
    print("✅ Broker Found")
    print("Broker Name:", result[0])
    print("Registration No:", result[1])
else:
    print("❌ Broker Not Found")

conn.close()