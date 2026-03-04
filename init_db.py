import sqlite3

def init_db():
    conn = sqlite3.connect("assistant.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT
    )
    """)
    conn.commit()
    conn.close()
    print("✅ Database initialized and table 'logs' is ready.")

if __name__ == "__main__":
    init_db()