# login.py
import sqlite3
import pyotp
import time
from datetime import datetime

from database import hash_password
from graphical_password import verify_graphical_password
from recovery import recovery_login   # ✅ call recovery if user forgets password

DB = "users.db"
LOCK_THRESHOLD = 3
LOCK_SECONDS = 3600  # 1 hour lockout


def authenticate_user(username, password, otp_code):
    """Authenticate user with password, OTP, and graphical password.
       Lock account after 3 failed attempts for 1 hour.
       If password wrong, offer 'Forgot Password' recovery option."""
    try:
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT password_hash, otp_secret, failed_attempts, is_locked, locked_until
            FROM users WHERE username = ?
        ''', (username,))
        row = cursor.fetchone()

        if not row:
            print("❌ User not found!")
            return False

        stored_password_hash, otp_secret, failed_attempts, is_locked, locked_until = row
        now_ts = int(time.time())

        # 🔒 Check lock
        if is_locked:
            if locked_until and locked_until > now_ts:
                unlock_time = datetime.fromtimestamp(locked_until).strftime("%Y-%m-%d %H:%M:%S")
                print(f"⛔ Account locked until {unlock_time}")
                conn.close()
                return False
            else:
                # Auto unlock
                cursor.execute("UPDATE users SET is_locked=0, failed_attempts=0, locked_until=NULL WHERE username=?", (username,))
                conn.commit()
                failed_attempts = 0
                is_locked = 0
                print("ℹ️ Lock expired. You may try again.")

        # ✅ Check password
        if hash_password(password) != stored_password_hash:
            print("❌ Invalid password!")
            choice = input("Forgot password? (y/n): ").strip().lower()
            if choice == "y":
                recovery_phrase = input("Enter recovery phrase: ").strip()
                return recovery_login(username, recovery_phrase)
            else:
                _fail_attempt(cursor, conn, username, "Invalid password!")
                return False

        # ✅ Check OTP
        if otp_secret:
            totp = pyotp.TOTP(otp_secret)
            if not totp.verify(otp_code, valid_window=1):
                _fail_attempt(cursor, conn, username, "Invalid OTP code!")
                return False

        # ✅ Check graphical password
        if not verify_graphical_password(username):
            _fail_attempt(cursor, conn, username, "Invalid graphical password!")
            return False

        # 🎉 Success → reset failed attempts
        cursor.execute("UPDATE users SET failed_attempts=0 WHERE username=?", (username,))
        conn.commit()
        conn.close()
        print(f"✅ Login successful! Welcome {username}")
        return True

    except Exception as e:
        print("⚠️ Error during authentication:", e)
        return False


def _fail_attempt(cursor, conn, username, message):
    """Helper for handling failed login attempts with lockout."""
    cursor.execute("UPDATE users SET failed_attempts = failed_attempts + 1 WHERE username = ?", (username,))
    conn.commit()

    cursor.execute("SELECT failed_attempts FROM users WHERE username = ?", (username,))
    updated_fa = cursor.fetchone()[0]
    remaining = max(0, LOCK_THRESHOLD - updated_fa)
    print(f"❌ {message} Remaining attempts: {remaining}")

    if updated_fa >= LOCK_THRESHOLD:
        lock_until_ts = int(time.time()) + LOCK_SECONDS
        cursor.execute("UPDATE users SET is_locked=1, locked_until=? WHERE username = ?", (lock_until_ts, username))
        conn.commit()
        unlock_time = datetime.fromtimestamp(lock_until_ts).strftime("%Y-%m-%d %H:%M:%S")
        print(f"⛔ Too many failed attempts. Account locked until {unlock_time}")

    conn.close()
    return False


if __name__ == "__main__":
    u = input("Enter username: ")
    p = input("Enter password: ")
    o = input("Enter OTP: ")
    authenticate_user(u, p, o)
