import sqlite3

def update_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Show current table columns
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    print("Existing columns:", columns)

    # Add recovery_hash column if missing
    if "recovery_hash" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN recovery_hash TEXT")
        conn.commit()
        print("✅ Database updated: Added recovery_hash column.")
    else:
        print("✅ Database already has recovery_hash column.")

    conn.close()

if __name__ == "__main__":
    update_database()
