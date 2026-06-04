import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute("SELECT username, otp_secret, password_hash FROM users")
rows = cursor.fetchall()

if rows:
    print("Username\tOTP Secret\t\t\t\tPassword Hash")
    for row in rows:
        print(f"{row[0]}\t{row[1]}\t{row[2]}")
else:
    print("No users found.")

conn.close()
