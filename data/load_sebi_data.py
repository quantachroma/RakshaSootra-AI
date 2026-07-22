import sqlite3
import pandas as pd

from tool.db_client import create_tables


create_tables()

# Read Excel
df = pd.read_excel(
    "data/Registered Stock Brokers in equity segment as on Jul 10 2026.xls",
    engine="xlrd",
    header=1
)

# Remove second header row
df = df.iloc[1:].reset_index(drop=True)

# Connect Database
conn = sqlite3.connect("raksha_sootra.db")
cursor = conn.cursor()

# Insert Data
for _, row in df.iterrows():

    cursor.execute("""
    INSERT INTO sebi_registered
    (broker_name, registration_no, city, state, validity)
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        row["Unnamed: 0"],
        row["Unnamed: 1"],
        row["Unnamed: 7"],
        row["Unnamed: 8"],
        row["Validity"]
    ))

conn.commit()
conn.close()

print("SEBI Data Imported Successfully!")