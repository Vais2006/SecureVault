import sqlite3

def view_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Select usernames + graphical passwords
    cursor.execute("SELECT username, graphical_password FROM users")
    rows = cursor.fetchall()
    
    print("\n=== Stored Users and Their Graphical Passwords ===")
    if not rows:
        print("No users found.")
    else:
        for row in rows:
            print(f"Username: {row[0]} | Graphical Password: {row[1]}")
    
    conn.close()

if __name__ == "__main__":
    view_users()
