import sqlite3
from backend.config import Config

def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, args)
    rv = [dict(row) for row in cur.fetchall()]
    conn.close()
    return (rv[0] if rv else None) if one else rv
