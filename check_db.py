import sqlite3

conn = sqlite3.connect("raksha_sootra.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM sebi_registered")
count = cursor.fetchone()[0]

print("Total Records:", count)

conn.close()