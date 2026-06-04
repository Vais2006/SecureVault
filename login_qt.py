import sqlite3, pyotp
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from database import hash_password
from vault_qt import VaultWindow
from graphical_password_qt import verify_graphical_password

DB = "users.db"

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(400, 350)

        layout = QVBoxLayout()

        # Username input
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter Username")
        layout.addWidget(self.username)

        # Password input
        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter Password")
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        # OTP input
        self.otp = QLineEdit()
        self.otp.setPlaceholderText("Enter OTP from Authenticator")
        layout.addWidget(self.otp)

        # Login button
        btn_login = QPushButton("Login")
        btn_login.clicked.connect(self.authenticate_user)
        layout.addWidget(btn_login)

        # Exit button
        btn_exit = QPushButton("Exit")
        btn_exit.clicked.connect(self.close)
        layout.addWidget(btn_exit)

        # Forget Password text link
        forget_label = QLabel("<a href='#'>Forgot Password?</a>")
        forget_label.setStyleSheet("QLabel { color: blue; text-decoration: underline; }")
        forget_label.setAlignment(Qt.AlignCenter)
        forget_label.setOpenExternalLinks(False)
        forget_label.linkActivated.connect(self.open_recovery)
        layout.addWidget(forget_label)

        self.setLayout(layout)

    def authenticate_user(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        otp_code = self.otp.text().strip()

        if not username or not password or not otp_code:
            QMessageBox.critical(self, "Error", "All fields are required")
            return

        try:
            conn = sqlite3.connect(DB)
            cur = conn.cursor()

            cur.execute("SELECT password_hash, otp_secret, failed_attempts, is_locked, locked_until, graphical_password FROM users WHERE username=?", (username,))
            result = cur.fetchone()

            if not result:
                QMessageBox.warning(self, "Error", "User not found!")
                return

            stored_hash, otp_secret, failed_attempts, is_locked, locked_until, graphical_pw = result

            # ✅ Check if locked
            if is_locked:
                QMessageBox.critical(self, "Locked", "⚠️ Account locked! Please try again later or contact admin.")
                return

            # ✅ Verify password
            if hash_password(password) != stored_hash:
                cur.execute("UPDATE users SET failed_attempts = failed_attempts + 1 WHERE username=?", (username,))
                conn.commit()
                if failed_attempts + 1 >= 3:
                    cur.execute("UPDATE users SET is_locked=1 WHERE username=?", (username,))
                    conn.commit()
                    QMessageBox.critical(self, "Locked", "❌ Account locked after 3 failed attempts!")
                else:
                    QMessageBox.warning(self, "Error", "Invalid password!")
                return

            # ✅ Verify OTP
            totp = pyotp.TOTP(otp_secret)
            if not totp.verify(otp_code, valid_window=1):
                QMessageBox.warning(self, "Error", "Invalid OTP code!")
                return

            # ✅ Verify graphical password
            if not verify_graphical_password(username, graphical_pw):
                QMessageBox.warning(self, "Error", "Graphical password failed!")
                return

            # ✅ Successful login → reset attempts
            cur.execute("UPDATE users SET failed_attempts=0, is_locked=0 WHERE username=?", (username,))
            conn.commit()

            QMessageBox.information(self, "Success", f"Login successful! Welcome {username}")
            self.open_vault(username)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()

    def open_vault(self, username):
        self.vault = VaultWindow(username)
        self.vault.show()
        self.close()

    def open_recovery(self):
        from recovery_qt import RecoveryWindow
        self.close()
        self.recovery_window = RecoveryWindow()
        self.recovery_window.show()
