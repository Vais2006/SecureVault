import os
import sqlite3
import pyotp
import qrcode

DB = "users.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QR_DIR = os.path.join(BASE_DIR, "QR")
os.makedirs(QR_DIR, exist_ok=True)

def regenerate_qr(username):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT otp_secret FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        print(f"❌ No user found with username: {username}")
        return

    otp_secret = result[0]
    totp = pyotp.TOTP(otp_secret)
    uri = totp.provisioning_uri(name=username, issuer_name="Offline MFA System")

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    qr_filename = os.path.join(QR_DIR, f"{username}_qr.png")
    img.save(qr_filename)

    print(f"✅ QR regenerated for {username}")
    print(f"📱 Saved at: {qr_filename}")

if __name__ == "__main__":
    user = input("Enter username to regenerate QR: ").strip()
    regenerate_qr(user)
