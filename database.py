import sqlite3

DB_PATH = "hacker_data.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS victims (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        phone TEXT,
        device_info TEXT,
        ip_address TEXT,
        location TEXT,
        date TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS exploits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        exploit_type TEXT,
        status TEXT,
        date TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        details TEXT,
        date TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

def save_victim(user_id, username, phone, device_info="", ip="", location=""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO victims 
        (user_id, username, phone, device_info, ip_address, location)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (user_id, username, phone, device_info, ip, location))
    conn.commit()
    conn.close()

def log_exploit(user_id, exploit_type, status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO exploits (user_id, exploit_type, status) VALUES (?, ?, ?)",
              (user_id, exploit_type, status))
    conn.commit()
    conn.close()

def log_action(user_id, action, details=""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO logs (user_id, action, details) VALUES (?, ?, ?)",
              (user_id, action, details))
    conn.commit()
    conn.close()

def get_victims():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM victims")
    victims = c.fetchall()
    conn.close()
    return victims

def get_logs():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM logs ORDER BY date DESC LIMIT 100")
    logs = c.fetchall()
    conn.close()
    return logs