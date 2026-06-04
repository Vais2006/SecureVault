# recovery_qt.py
import sqlite3, hashlib
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from database import hash_password
from vault_qt import VaultWindow
from graphical_password_qt import verify_graphical_password

DB = "users.db"

class RecoveryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recover Account")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        # Username input
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter Username")
        layout.addWidget(self.username)

        # Recovery phrase
        self.recovery_phrase = QLineEdit()
        self.recovery_phrase.setPlaceholderText("Enter Recovery Phrase")
        layout.addWidget(self.recovery_phrase)

        # New password
        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText("Enter New Password")
        self.new_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.new_password)

        # Confirm password
        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Confirm New Password")
        self.confirm_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_password)

        # Submit button
        btn_submit = QPushButton("Reset Password")
        btn_submit.clicked.connect(self.reset_password)
        layout.addWidget(btn_submit)

        self.setLayout(layout)

    def reset_password(self):
        username = self.username.text().strip()
        recovery_phrase = self.recovery_phrase.text().strip()
        new_pw = self.new_password.text().strip()
        confirm_pw = self.confirm_password.text().strip()

        if not username or not recovery_phrase or not new_pw or not confirm_pw:
            QMessageBox.warning(self, "Error", "All fields are required")
            return

        if new_pw != confirm_pw:
            QMessageBox.warning(self, "Error", "Passwords do not match!")
            return

        try:
            conn = sqlite3.connect(DB)
            cur = conn.cursor()
            cur.execute("SELECT recovery_hash, graphical_password FROM users WHERE username=?", (username,))
            result = cur.fetchone()

            if not result:
                QMessageBox.warning(self, "Error", "User not found")
                return

            stored_recovery_hash, stored_graphical = result
            entered_recovery_hash = hashlib.sha256(recovery_phrase.encode()).hexdigest()

            # Check recovery phrase
            if entered_recovery_hash != stored_recovery_hash:
                QMessageBox.warning(self, "Error", "Invalid recovery phrase")
                return

            # Check graphical password
            if not verify_graphical_password(username, stored_graphical):
                QMessageBox.warning(self, "Error", "Graphical password failed")
                return

            # Update password
            new_pw_hash = hash_password(new_pw)
            cur.execute("UPDATE users SET password_hash=? WHERE username=?", (new_pw_hash, username))
            conn.commit()

            QMessageBox.information(self, "Success", "✅ Password reset successfully! Now you can log in.")
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()
