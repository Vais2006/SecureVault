import os
import sqlite3
import pyotp
import qrcode
import hashlib
from database import hash_password, create_database
from graphical_password import choose_graphical_password

# 🔥 FIXED: Always save QR in MVPA/QR folder (same as users.db)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QR_DIR = os.path.join(BASE_DIR, "QR")
os.makedirs(QR_DIR, exist_ok=True)

def register_user_with_recovery(username, password, recovery_phrase):
    """Register a new user with OTP secret, recovery phrase, and graphical password"""
    create_database()  # Ensure database exists

    secret = pyotp.random_base32()
    password_hash = hash_password(password)
    recovery_hash = hashlib.sha256(recovery_phrase.encode()).hexdigest()

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO users (username, password_hash, otp_secret, recovery_hash)
            VALUES (?, ?, ?, ?)
        ''', (username, password_hash, secret, recovery_hash))

        conn.commit()
        conn.close()

        # Generate QR code for Google Authenticator
        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(name=username, issuer_name="Offline MFA System")

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uri)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # ✅ Always save inside MVPA/QR
        qr_filename = os.path.join(QR_DIR, f"{username}_qr.png")
        img.save(qr_filename)

        print(f"✅ User {username} registered successfully!")
        print(f"🔑 Secret key: {secret}")
        print(f"📝 Recovery phrase stored securely.")
        print(f"📱 QR code saved at: {qr_filename}")  # <-- Full path
        print("👉 Scan the QR code with Google Authenticator app")

        # Graphical password setup
        choose_graphical_password(username)

        return True

    except sqlite3.IntegrityError:
        print("⚠️ Username already exists!")
        return False


if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")
    recovery_phrase = input("Enter your recovery phrase (write this down safely): ")
    register_user_with_recovery(username, password, recovery_phrase)
