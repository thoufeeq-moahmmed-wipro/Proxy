import sqlite3

DB_FILE = "url_database.db"

def initialize_database():
    """Create and initialize the URL categorization database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create the table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS url_categorization (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL CHECK(category IN ('ALLOW', 'BLOCK'))
        )
    """)
    
    # Insert default values (if not already present)
    default_urls = [
        ("http://www.example.com/", "ALLOW"),
        ("http://www.google.com/", "ALLOW"),
        ("http://www.blockedwebsite.com/", "BLOCK"),
    ]
    
    for url, category in default_urls:
        try:
            cursor.execute("INSERT INTO url_categorization (url, category) VALUES (?, ?)", (url, category))
            print(f"[DATABASE] Added URL: {url} as {category}")
        except sqlite3.IntegrityError:
            pass  # Ignore duplicates
    
    conn.commit()
    conn.close()

def is_url_allowed(url):
    """Check if a URL is explicitly allowed."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT category FROM url_categorization WHERE url = ?", (url,))
    result = cursor.fetchone()
    conn.close()
    return result and result[0] == "ALLOW"

def is_url_blocked(url):
    """Check if a URL is explicitly blocked."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT category FROM url_categorization WHERE url = ?", (url,))
    result = cursor.fetchone()
    conn.close()
    return result and result[0] == "BLOCK"

if __name__ == "__main__":
    initialize_database()
