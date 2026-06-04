# recovery.py
import sqlite3
import hashlib
from database import hash_password
from graphical_password import verify_graphical_password

DB = "users.db"


def recovery_login(username, recovery_phrase):
    """Recover account using recovery phrase + graphical password, then reset password."""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # Check if user exists
    cursor.execute("SELECT recovery_hash FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    if not row:
        print("❌ User not found.")
        conn.close()
        return False

    stored_recovery_hash = row[0]

    # Verify recovery phrase
    recovery_hash = hashlib.sha256(recovery_phrase.encode()).hexdigest()
    if recovery_hash != stored_recovery_hash:
        print("❌ Invalid recovery phrase!")
        conn.close()
        return False

    # Verify graphical password
    if not verify_graphical_password(username):
        print("❌ Graphical password verification failed!")
        conn.close()
        return False

    # If recovery successful → ask for new password
    new_pw = input("Enter NEW password: ").strip()
    confirm_pw = input("Confirm NEW password: ").strip()
    if new_pw != confirm_pw or not new_pw:
        print("⚠️ Passwords did not match or were empty. Password reset aborted.")
        conn.close()
        return False

    new_hash = hash_password(new_pw)

    # Update DB with new password and reset lockout
    cursor.execute("""
        UPDATE users
        SET password_hash=?, failed_attempts=0, is_locked=0, locked_until=NULL
        WHERE username=?
    """, (new_hash, username))

    conn.commit()
    conn.close()

    print("✅ Password reset successful! You can now log in with the new password.")
    return True


if __name__ == "__main__":
    u = input("Enter username: ")
    r = input("Enter recovery phrase: ")
    recovery_login(u, r)
