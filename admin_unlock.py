# admin_unlock.py
import sqlite3
import sys

DB = "users.db"

def unlock_user(username):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("UPDATE users SET is_locked=0, failed_attempts=0, locked_until=NULL WHERE username=?", (username,))
    conn.commit()
    conn.close()
    print(f"✅ Unlocked user: {username}")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        u = sys.argv[1]
    else:
        u = input("Enter username to unlock: ").strip()
    if u:
        unlock_user(u)
    else:
        print("No username provided.")


