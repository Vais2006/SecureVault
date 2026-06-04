# update_user_data_table.py
import sqlite3

DB = "users.db"

def update_table():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(user_data)")
    cols = [r[1] for r in cur.fetchall()]

    if "title" not in cols:
        cur.execute("ALTER TABLE user_data ADD COLUMN title TEXT")
        print("✅ Added 'title' column to user_data")
    else:
        print("ℹ️ 'title' column already exists")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_table()
