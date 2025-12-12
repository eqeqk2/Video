import sqlite3, hashlib

DB_PATH = "media_grabber.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS files (
                       id INTEGER PRIMARY KEY,
                       hash TEXT UNIQUE,
                       filename TEXT,
                       added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )""")
    conn.commit()
    conn.close()

def _file_hash(file_path: str) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def file_exists(file_path: str) -> bool:
    """True, якщо файл з таким SHA‑256 вже збережений."""
    file_hash = _file_hash(file_path)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM files WHERE hash=?", (file_hash,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists

def register_file(file_path: str, filename: str):
    file_hash = _file_hash(file_path)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO files (hash, filename) VALUES (?, ?)",
        (file_hash, filename),
    )
    conn.commit()
    conn.close()
