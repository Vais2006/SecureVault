import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

username = "a"  # Replace with your username
cursor.execute("SELECT otp_secret FROM users WHERE username = ?", (username,))
row = cursor.fetchone()
if row:
    print("Stored OTP secret:", row[0])
else:
    print("No user found.")

conn.close()
