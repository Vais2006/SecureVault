import sqlite3

def view_graphical_numbers():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT username, graphical_password FROM users")
    rows = cursor.fetchall()
    
    print("\n=== Stored Users and Their Graphical Password Numbers ===")
    if not rows:
        print("No users found.")
    else:
        for row in rows:
            username = row[0]
            gpass = row[1] if row[1] else "Not Set"
            print(f"👤 {username} | 🔢 {gpass}")
    
    conn.close()

if __name__ == "__main__":
    view_graphical_numbers()
