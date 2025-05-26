import sqlite3

def get_connection():
    """Create and return a new SQLite database connection."""
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

CONN = get_connection()
CURSOR = CONN.cursor()