import sqlite3
import base64

DB_FILE = "users.db"

def initialize_db():
    """Create the database for storing users."""
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

def add_user(username, password):
    """Add a new user to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print(f"[INFO] User '{username}' added successfully.")
    except sqlite3.IntegrityError:
        print(f"[INFO] User '{username}' already exists.")
    conn.close()

def authenticate(auth_header):
    """Authenticate a user from the Authorization header."""
    if not auth_header or not auth_header.startswith("Basic "):
        return False  # No authentication provided

    # Decode the Base64-encoded credentials
    encoded_creds = auth_header.split(" ")[1]
    decoded_creds = base64.b64decode(encoded_creds).decode("utf-8")
    
    # Extract username and password
    username, password = decoded_creds.split(":", 1)

    # Validate credentials in the database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    return user is not None  # Return True if user exists

# Run only when executed directly
if __name__ == "__main__":
    initialize_db()
    add_user("admin", "password123")  # Add a default admin user
