# admin_delete_user.py
import sqlite3, os

DB = "users.db"
QR_FOLDER = os.path.join(os.path.dirname(__file__), "QR")

def delete_user(username):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # Delete user from users table
    cur.execute("DELETE FROM users WHERE username=?", (username,))

    # Delete all vault data linked to that user
    cur.execute("DELETE FROM user_data WHERE username=?", (username,))

    conn.commit()
    conn.close()

    # Delete QR file if exists
    qr_filename = os.path.join(QR_FOLDER, f"{username}_qr.png")
    if os.path.exists(qr_filename):
        os.remove(qr_filename)
        print(f"🗑️ Deleted QR file: {qr_filename}")
    else:
        print("⚠️ No QR file found for this user.")

    print(f"✅ User '{username}' and their vault data deleted successfully!\n")

if __name__ == "__main__":
    print("=== Admin User Deletion Tool ===")
    print("Type a username to delete or 'exit' to quit.\n")

    while True:
        u = input("Enter username to delete: ").strip()
        if u.lower() in ("exit", "quit"):
            print("👋 Exiting Admin Tool.")
            break

        if u:
            confirm = input(f"⚠️ Are you sure you want to delete user '{u}'? (yes/no): ").lower()
            if confirm == "yes":
                delete_user(u)
            else:
                print("❌ Cancelled.\n")
