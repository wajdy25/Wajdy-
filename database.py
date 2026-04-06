import sqlite3
import asyncio

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            platform TEXT
        )
    """)
    conn.commit()
    conn.close()

async def add_user(user_id, platform="Android"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users(user_id, platform) VALUES (?, ?)", (user_id, platform))
    conn.commit()
    conn.close()

async def get_all_users_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, platform FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

async def get_users_by_platform(platform):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE platform=?", (platform,))
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users
