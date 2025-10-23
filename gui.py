import sys
from generate import generate_qr
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPalette, QColor
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QFileDialog, QMessageBox, QFrame,
    QSizePolicy
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Maker")

        # ---- base container (same centered card as before)
        wrapper = QWidget()
        outer = QVBoxLayout(wrapper)
        outer.setContentsMargins(24, 24, 24, 24)

        card = QFrame()
        card.setObjectName("card")
        card.setFrameShape(QFrame.NoFrame)
        card.setMinimumWidth(420)              # keep your previous visual size
        card.setMaximumWidth(520)              # tweak if you want it a bit wider/narrower
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(14)
        card_layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Generate QR-Code 🐶")
        title.setObjectName("title")

        # URL (fill available width)
        url_label = QLabel("Spreadsheet link")
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("https://docs.google.com/…#gid=0&range=A2:A51")
        self.url_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # 👈 stretch horizontally
        self.url_edit.setMinimumWidth(0)  # allow full stretch

        # Output (path fills, Browse stays compact)
        out_label = QLabel("Output image")
        out_row = QHBoxLayout()
        self.out_edit = QLineEdit()
        self.out_edit.setPlaceholderText(str(Path.home() / "sheet_qr.png"))
        self.out_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # 👈 stretch
        self.out_edit.setMinimumWidth(0)

        browse = QPushButton("Browse")
        browse.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # 👈 stays compact
        browse.clicked.connect(self.pick_output)

        out_row.addWidget(self.out_edit, 1)   # 👈 give the edit all the stretch
        out_row.addWidget(browse, 0)

        # Run (full width button)
        run = QPushButton("Run")
        run.setObjectName("primary")
        run.setMinimumHeight(48)
        run.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # 👈 full width
        run.clicked.connect(self.on_run)

        # assemble
        card_layout.addWidget(title)
        card_layout.addSpacing(6)
        card_layout.addWidget(url_label)
        card_layout.addWidget(self.url_edit)
        card_layout.addSpacing(8)
        card_layout.addWidget(out_label)
        card_layout.addLayout(out_row)
        card_layout.addSpacing(14)
        card_layout.addWidget(run)

        # center card in the window (same look as before)
        center = QHBoxLayout()
        center.addStretch(1)
        center.addWidget(card)
        center.addStretch(1)
        outer.addStretch(1)
        outer.addLayout(center)
        outer.addStretch(2)

        self.setCentralWidget(wrapper)
        self.apply_modern_style(card)

        # default output
        self.out_edit.setText(str(Path.home() / "sheet_qr.png"))

        # optional: modest default size; user can resize window freely
        self.resize(760, 520)

    def pick_output(self):
        start = self.out_edit.text() or str(Path.home() / "sheet_qr.png")
        path, _ = QFileDialog.getSaveFileName(
            self, "Save QR Image", start, "PNG Images (*.png);;All Files (*)"
        )
        if path:
            if not path.lower().endswith(".png"):
                path += ".png"
            self.out_edit.setText(path)

    def on_run(self):
        url = (self.url_edit.text() or "").strip()
        out_path = (self.out_edit.text() or "").strip()
        if not url or not (url.startswith("http://") or url.startswith("https://")):
            QMessageBox.warning(self, "Invalid link", "Please paste a valid http(s) link.")
            return
        if not out_path:
            QMessageBox.warning(self, "Missing path", "Please choose where to save the image.")
            return
        try:
            saved = generate_qr(url, out_path)
            QMessageBox.information(self, "Done", f"QR saved to:\n{saved}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def apply_modern_style(self, card: QFrame):
        QApplication.setStyle("Fusion")
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor("#0f1115"))
        pal.setColor(QPalette.WindowText, Qt.white)
        pal.setColor(QPalette.Base, QColor("#0f1115"))
        pal.setColor(QPalette.Text, Qt.white)
        pal.setColor(QPalette.Button, QColor("#0f1115"))
        pal.setColor(QPalette.ButtonText, Qt.white)
        pal.setColor(QPalette.Highlight, QColor("#5b8cff"))
        pal.setColor(QPalette.HighlightedText, QColor("#0b1020"))
        self.setPalette(pal)

        self.setStyleSheet("""
            QMainWindow { background-color: #0f1115; }
            #card {
                background-color: #151821;
                border: 1px solid #23283b;
                border-radius: 16px;
            }
            QLabel#title { font-size: 24px; font-weight: 700; color: #ffffff; }
            QLabel { color: #aab1c3; font-size: 15px; }
            QLineEdit {
                background: #0f1115;
                border: 1px solid #2a3042;
                border-radius: 10px;
                padding: 12px 14px;
                color: #e7ecf3;
                selection-background-color: #39405a;
            }
            QPushButton {
                background: #1b2030;
                border: 1px solid #2a3042;
                border-radius: 10px;
                padding: 12px 16px;
                color: #e7ecf3; font-weight: 600;
            }
            QPushButton:hover { border-color: #3b4464; }
            QPushButton#primary {
                background: #5b8cff; border: 1px solid #5b8cff; color: #0b1020;
            }
            QPushButton#primary:hover { background: #7aa3ff; border-color: #7aa3ff; }
        """)

        # soft shadow
        try:
            from PySide6.QtWidgets import QGraphicsDropShadowEffect
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(30)
            shadow.setOffset(0, 10)
            shadow.setColor(QColor(0, 0, 0, 160))
            card.setGraphicsEffect(shadow)
        except Exception:
            pass


def main():
    app = QApplication(sys.argv)
    font = QFont(); font.setPointSize(14); app.setFont(font)
    win = MainWindow()
    win.show()  # same overall size; user can resize window; inner content already fills
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
