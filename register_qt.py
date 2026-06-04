# register_qt.py
import os, random, sqlite3, hashlib, pyotp, qrcode
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout,
    QMessageBox, QScrollArea, QDialog, QVBoxLayout as QVLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from database import hash_password

DB = "users.db"
IMAGE_FOLDER = "image"  # ✅ your folder with 100 images

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register User")
        self.setFixedSize(600, 600)
        self.selected = []

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

        # Recovery phrase input
        self.recovery = QLineEdit()
        self.recovery.setPlaceholderText("Enter Recovery Phrase")
        layout.addWidget(self.recovery)

        # Scrollable grid for images
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)

        # Shuffle images
        files = os.listdir(IMAGE_FOLDER)
        random.shuffle(files)

        row, col = 0, 0
        for f in files:
            path = os.path.join(IMAGE_FOLDER, f)
            pix = QPixmap(path).scaled(80, 80, Qt.KeepAspectRatio)
            lbl = QLabel()
            lbl.setPixmap(pix)
            lbl.mousePressEvent = lambda e, file=f: self.select_image(file)
            grid.addWidget(lbl, row, col)
            col += 1
            if col >= 5:
                col = 0
                row += 1

        container.setLayout(grid)
        scroll.setWidget(container)
        layout.addWidget(scroll)

        # Register button
        btn_reg = QPushButton("Register")
        btn_reg.clicked.connect(self.register_user)
        layout.addWidget(btn_reg)

        self.setLayout(layout)

    def select_image(self, file):
        """Handle graphical password image selection"""
        if file in self.selected:
            QMessageBox.warning(self, "Warning", "Already selected!")
        elif len(self.selected) >= 5:
            QMessageBox.warning(self, "Warning", "You can only select 5 images!")
        else:
            self.selected.append(file)
            QMessageBox.information(self, "Selected", f"Image {len(self.selected)} selected")

    def register_user(self):
        """Register new user into DB with password + recovery + OTP + graphical password"""
        username = self.username.text().strip()
        password = self.password.text().strip()
        recovery = self.recovery.text().strip()

        if not username or not password or not recovery:
            QMessageBox.critical(self, "Error", "All fields required")
            return

        if len(self.selected) != 5:
            QMessageBox.critical(self, "Error", "Select exactly 5 images")
            return

        secret = pyotp.random_base32()
        password_hash = hash_password(password)
        recovery_hash = hashlib.sha256(recovery.encode()).hexdigest()

        try:
            with sqlite3.connect(DB, timeout=10) as conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO users (username, password_hash, otp_secret, recovery_hash, graphical_password)
                    VALUES (?, ?, ?, ?, ?)
                """, (username, password_hash, secret, recovery_hash, ",".join(self.selected)))
                conn.commit()

            # Generate QR code
            totp = pyotp.TOTP(secret)
            uri = totp.provisioning_uri(name=username, issuer_name="Offline MFA System")
            img = qrcode.make(uri)

            # Ensure QR folder exists
            qr_folder = os.path.join(os.path.dirname(__file__), "QR")
            os.makedirs(qr_folder, exist_ok=True)

            qr_filename = os.path.join(qr_folder, f"{username}_qr.png")
            img.save(qr_filename)

            # ✅ Show QR in popup
            qr_dialog = QDialog(self)
            qr_dialog.setWindowTitle("Scan this QR Code")
            qr_layout = QVLayout()
            qr_label = QLabel()
            pix = QPixmap(qr_filename).scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            qr_label.setPixmap(pix)
            qr_layout.addWidget(qr_label)

            btn_ok = QPushButton("Done (Close QR)")
            btn_ok.clicked.connect(qr_dialog.accept)
            qr_layout.addWidget(btn_ok)

            qr_dialog.setLayout(qr_layout)

            # Auto close after 2 minutes (optional)
            QTimer.singleShot(120000, qr_dialog.reject)

            qr_dialog.exec_()

            QMessageBox.information(self, "Success",
                                    f"✅ User {username} registered!\n📱 QR was shown & saved.\nNow login with your credentials.")
            self.close()

        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "⚠️ Username already exists")
