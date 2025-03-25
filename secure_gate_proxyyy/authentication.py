import sqlite3

DB_FILE = "auth_database.db"

def initialize_auth_database():
    """Create and initialize the authentication database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    default_users = [
        ("admin", "password123"),
        ("user", "userpass"),
    ]
    
    for username, password in default_users:
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            print(f"[DATABASE] Added User: {username}")
        except sqlite3.IntegrityError:
            pass  # Ignore duplicates
    
    conn.commit()
    conn.close()

def authenticate(username, password):
    """Validate username and password."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

if __name__ == "__main__":
    initialize_auth_database()
