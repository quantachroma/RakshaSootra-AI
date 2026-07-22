import sqlite3

conn = sqlite3.connect("raksha_sootra.db")
cursor = conn.cursor()

print("Tables in database:")

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

conn.close()