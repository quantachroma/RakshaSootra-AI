import sqlite3
DB_NAME = "raksha_sootra.db"

def get_connection():
    connection = sqlite3.connect(DB_NAME)
    return connection

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_rules (
    id INTEGER PRIMARY KEY,
    threshold REAL,
    check_new_payee BOOLEAN
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payee_history (
    id INTEGER PRIMARY KEY,
    payee_name TEXT,
    upi_id TEXT
    )
    """)
    connection.commit()
    connection.close()
    

