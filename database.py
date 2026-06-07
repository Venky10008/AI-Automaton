import sqlite3
import os
import json
from datetime import datetime

# Get DB path from environment or use default
DB_FILE = os.environ.get("DB_PATH", "database.db")

def get_connection():
    # Ensure directory exists if path contains directories
    db_dir = os.path.dirname(DB_FILE)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Table for posts
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            post_id TEXT PRIMARY KEY,
            post_date TEXT,
            topic TEXT,
            source_link TEXT,
            post_type TEXT
        )
    ''')
    # Table for DM logs to prevent duplicates
    c.execute('''
        CREATE TABLE IF NOT EXISTS dm_logs (
            username TEXT,
            post_id TEXT,
            timestamp TEXT,
            PRIMARY KEY(username, post_id)
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_FILE}")

def save_post(post_id, topic, source_link, post_type):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO posts (post_id, post_date, topic, source_link, post_type)
            VALUES (?, ?, ?, ?, ?)
        ''', (post_id, datetime.now().isoformat(), topic, source_link, post_type))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"Post {post_id} already exists in db.")
        return False
    finally:
        conn.close()

def get_post(post_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM posts WHERE post_id = ?', (post_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "post_id": row[0],
            "post_date": row[1],
            "topic": row[2],
            "source_link": row[3],
            "post_type": row[4]
        }
    return None

def log_dm_sent(username, post_id):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO dm_logs (username, post_id, timestamp)
            VALUES (?, ?, ?)
        ''', (username, post_id, datetime.now().isoformat()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def has_dm_been_sent(username, post_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT 1 FROM dm_logs WHERE username = ? AND post_id = ?', (username, post_id))
    row = c.fetchone()
    conn.close()
    return bool(row)
