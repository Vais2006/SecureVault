# main_qt.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from register_qt import RegisterWindow
from login_qt import LoginWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MVPA")
        self.resize(400, 300)
        self.setMinimumSize(300, 200)

        layout = QVBoxLayout()
        layout.setSpacing(15)        # ✅ small gap between buttons
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)  # ✅ stack at top & center horizontally

        # Register Button
        btn_register = QPushButton("Register New User")
        btn_register.setFixedWidth(200)
        btn_register.setFixedHeight(40)
        btn_register.clicked.connect(self.open_register)
        layout.addWidget(btn_register)

        # Login Button
        btn_login = QPushButton("Login")
        btn_login.setFixedWidth(200)
        btn_login.setFixedHeight(40)
        btn_login.clicked.connect(self.open_login)
        layout.addWidget(btn_login)

        # Exit Button
        btn_exit = QPushButton("Exit")
        btn_exit.setFixedWidth(200)
        btn_exit.setFixedHeight(40)
        btn_exit.clicked.connect(self.close)
        layout.addWidget(btn_exit)

        self.setLayout(layout)

    def open_register(self):
        self.reg_win = RegisterWindow()
        self.reg_win.show()

    def open_login(self):
        self.login_win = LoginWindow()
        self.login_win.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
