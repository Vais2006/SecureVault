import sqlite3

def update_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Check existing columns
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    print("Existing columns:", columns)

    # Add column for graphical password if missing
    if "graphical_password" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN graphical_password TEXT")
        conn.commit()
        print("✅ Database updated: Added graphical_password column.")
    else:
        print("✅ Database already has graphical_password column.")

    conn.close()

if __name__ == "__main__":
    update_database()
