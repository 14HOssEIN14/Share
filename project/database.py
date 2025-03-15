import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER UNIQUE
                    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS files (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        file_id TEXT,
                        file_code TEXT UNIQUE
                    )""")
    
    conn.commit()
    conn.close()

def add_user(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    
    conn.close()

def add_file(file_id, file_code):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO files (file_id, file_code) VALUES (?, ?)", (file_id, file_code))
    conn.commit()
    conn.close()

def get_file_by_code(file_code):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT file_id FROM files WHERE file_code = ?", (file_code,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None