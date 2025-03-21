import sqlite3

DB_FILE = "users.db"

def setup_database():
    """Create the user database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("[SETUP] User database initialized successfully.")

if __name__ == "__main__":
    setup_database()
