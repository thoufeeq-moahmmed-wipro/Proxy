import sqlite3

def init_db():
    conn = sqlite3.connect('proxy_db.sqlite')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 url TEXT UNIQUE,
                 category TEXT CHECK(category IN ('ALLOW', 'BLOCK')) NOT NULL)
              ''')
    conn.commit()
    conn.close()

def add_url(url, category):
    conn = sqlite3.connect('proxy_db.sqlite')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO urls (url, category) VALUES (?, ?)", (url, category))
    conn.commit()
    conn.close()

def get_url_category(url):
    conn = sqlite3.connect('proxy_db.sqlite')
    c = conn.cursor()
    c.execute("SELECT category FROM urls WHERE url=?", (url,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 'BLOCK'

def list_urls():
    conn = sqlite3.connect('proxy_db.sqlite')
    c = conn.cursor()
    c.execute("SELECT * FROM urls")
    result = c.fetchall()
    conn.close()
    return result

def update_url(url, new_category):
    conn = sqlite3.connect('proxy_db.sqlite')
    c = conn.cursor()
    c.execute("UPDATE urls SET category=? WHERE url=?", (new_category, url))
    conn.commit()
    conn.close()

def delete_url(url):
    conn = sqlite3.connect('proxy_db.sqlite')
    c = conn.cursor()
    c.execute("DELETE FROM urls WHERE url=?", (url,))
    conn.commit()
    conn.close()
