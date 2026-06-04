# update_lock_db.py
import sqlite3

DB = "users.db"   # change if your DB filename differs

def update():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # Ensure users table exists minimally (won't overwrite existing columns)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT,
        otp_secret TEXT,
        failed_attempts INTEGER DEFAULT 0
    )""")
    conn.commit()

    # Add is_locked if missing
    cur.execute("PRAGMA table_info(users)")
    cols = [r[1] for r in cur.fetchall()]
    if "is_locked" not in cols:
        cur.execute("ALTER TABLE users ADD COLUMN is_locked INTEGER DEFAULT 0")
        print("Added column: is_locked")
    else:
        print("is_locked already present")

    # Add locked_until if missing (stores epoch seconds)
    if "locked_until" not in cols:
        cur.execute("ALTER TABLE users ADD COLUMN locked_until INTEGER")
        print("Added column: locked_until")
    else:
        print("locked_until already present")

    conn.commit()
    conn.close()
    print("DB lock columns ensured.")

if __name__ == "__main__":
    update()
