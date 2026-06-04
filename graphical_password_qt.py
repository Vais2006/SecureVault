import os, random
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QGridLayout, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

IMAGE_FOLDER = "image"  # ✅ folder with 100 images

def verify_graphical_password(username, stored_seq):
    """
    Opens a PyQt dialog with 9 shuffled images,
    ensures at least 1 of user's chosen 5 is included.
    """
    dialog = GraphicalPasswordDialog(stored_seq.split(","))
    result = dialog.exec_()
    return result == QDialog.Accepted


class GraphicalPasswordDialog(QDialog):
    def __init__(self, correct_images):
        super().__init__()
        self.setWindowTitle("Graphical Password Verification")
        self.setFixedSize(500, 500)
        self.correct_images = correct_images
        self.selected = None

        layout = QVBoxLayout()

        grid = QGridLayout()
        files = os.listdir(IMAGE_FOLDER)
        random.shuffle(files)

        # ✅ Ensure at least 1 correct image is included
        chosen = random.sample(files, 8)  # 8 random wrongs
        chosen.append(random.choice(self.correct_images))  # 1 correct
        random.shuffle(chosen)

        row, col = 0, 0
        for f in chosen:
            path = os.path.join(IMAGE_FOLDER, f)
            pix = QPixmap(path).scaled(100, 100, Qt.KeepAspectRatio)
            lbl = QLabel()
            lbl.setPixmap(pix)
            lbl.mousePressEvent = lambda e, file=f: self.select_image(file)
            grid.addWidget(lbl, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1

        layout.addLayout(grid)

        btn_ok = QPushButton("Submit")
        btn_ok.clicked.connect(self.check_selection)
        layout.addWidget(btn_ok)

        self.setLayout(layout)

    def select_image(self, file):
        self.selected = file

    def check_selection(self):
        if not self.selected:
            QMessageBox.warning(self, "Error", "Please select an image")
            return
        if self.selected in self.correct_images:
            self.accept()
        else:
            self.reject()
