# vault_qt.py
import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QTextEdit, QListWidget, QMessageBox, QLineEdit
)
from account import create_user_data_table

DB = "users.db"

class VaultWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"{username}'s Vault")
        self.resize(600, 500)

        # Ensure table exists
        create_user_data_table()

        # Mapping (db_id, title, info)
        self.current_entries = []

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"🔐 Secure Vault for {username}"))

        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.gui_view_full_info)
        layout.addWidget(self.list_widget)

        # New input fields
        self.title_field = QLineEdit()
        self.title_field.setPlaceholderText("Enter note title...")
        layout.addWidget(self.title_field)

        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Enter full note content...")
        layout.addWidget(self.input_field)

        btn_add = QPushButton("➕ Add Note")
        btn_add.clicked.connect(self.gui_add_info)
        layout.addWidget(btn_add)

        btn_refresh = QPushButton("🔄 Refresh Notes")
        btn_refresh.clicked.connect(self.gui_view_info)
        layout.addWidget(btn_refresh)

        btn_delete_selected = QPushButton("❌ Delete Selected")
        btn_delete_selected.clicked.connect(self.gui_delete_selected)
        layout.addWidget(btn_delete_selected)

        btn_delete_all = QPushButton("🗑️ Delete All Notes")
        btn_delete_all.clicked.connect(self.gui_delete_info)
        layout.addWidget(btn_delete_all)

        btn_logout = QPushButton("🚪 Logout / Close Vault")
        btn_logout.clicked.connect(self.close_vault)
        layout.addWidget(btn_logout)

        self.setLayout(layout)
        self.gui_view_info()

    def gui_view_info(self):
        """Display titles only with numbering"""
        self.list_widget.clear()
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("SELECT id, title, info FROM user_data WHERE username=? ORDER BY id ASC", (self.username,))
        rows = cur.fetchall()
        conn.close()

        self.current_entries = rows
        if rows:
            for idx, (db_id, title, text) in enumerate(rows, start=1):
                title = title if title else "(Untitled)"
                self.list_widget.addItem(f"{idx}. {title}")
        else:
            self.list_widget.addItem("No notes yet.")
            self.current_entries = []

    def gui_add_info(self):
        """Add a new titled note"""
        title = self.title_field.text().strip()
        content = self.input_field.toPlainText().strip()

        if not title or not content:
            QMessageBox.warning(self, "Error", "Both Title and Content are required.")
            return

        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("INSERT INTO user_data (username, title, info) VALUES (?, ?, ?)", (self.username, title, content))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "✅ Note added successfully!")
        self.title_field.clear()
        self.input_field.clear()
        self.gui_view_info()

    def gui_view_full_info(self, item):
        """Show full note when clicking a title"""
        selected_row = self.list_widget.currentRow()
        if selected_row == -1 or not self.current_entries:
            return
        db_id, title, full_text = self.current_entries[selected_row]
        QMessageBox.information(self, f"📖 {title}", full_text)

    def gui_delete_selected(self):
        selected_row = self.list_widget.currentRow()
        if selected_row == -1 or not self.current_entries:
            QMessageBox.warning(self, "Error", "Please select a note to delete.")
            return
        db_id = self.current_entries[selected_row][0]
        confirm = QMessageBox.question(self, "Confirm Delete",
                                       f"Delete note '{self.current_entries[selected_row][1]}'?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            conn = sqlite3.connect(DB)
            cur = conn.cursor()
            cur.execute("DELETE FROM user_data WHERE id=? AND username=?", (db_id, self.username))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Deleted", "❌ Note deleted.")
            self.gui_view_info()

    def gui_delete_info(self):
        reply = QMessageBox.question(self, "Confirm Delete",
                                     "Delete ALL notes?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            conn = sqlite3.connect(DB)
            cur = conn.cursor()
            cur.execute("DELETE FROM user_data WHERE username=?", (self.username,))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Deleted", "🗑️ All notes deleted.")
            self.gui_view_info()

    def close_vault(self):
        self.close()
