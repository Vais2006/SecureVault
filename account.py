import sqlite3

def create_user_data_table():
    """Create table for storing user-specific info if it doesn't exist"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            info TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def account_menu(username):
    """Simple account menu for user to manage their info"""
    create_user_data_table()
    
    while True:
        print(f"\n=== Account Menu for {username} ===")
        print("1. View my info")
        print("2. Add new info")
        print("3. Delete all my info")
        print("4. Logout")
        
        choice = input("Choose an option (1-4): ")
        
        if choice == "1":
            view_info(username)
        elif choice == "2":
            add_info(username)
        elif choice == "3":
            delete_info(username)
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice! Try again.")

def view_info(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT info FROM user_data WHERE username=?", (username,))
    rows = cursor.fetchall()
    conn.close()
    
    if rows:
        print("\nYour stored info:")
        for i, row in enumerate(rows, 1):
            print(f"{i}. {row[0]}")
    else:
        print("\nNo info found. Add something!")

def add_info(username):
    new_info = input("Enter the info you want to save: ")
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_data (username, info) VALUES (?, ?)", (username, new_info))
    conn.commit()
    conn.close()
    print("✅ Info saved successfully!")

def delete_info(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_data WHERE username=?", (username,))
    conn.commit()
    conn.close()
    print("🗑️ All your info has been deleted.")
