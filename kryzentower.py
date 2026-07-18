import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("KryzenTower")

        icon = Path(__file__).parent / "blue-flame.png"
        if icon.exists():
            self.setWindowIcon(QIcon(str(icon)))

        label = QLabel("Welcome to KryzenTower!")
        label.setStyleSheet("font-size:18px;")
        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)

        self.resize(900, 600)


if __name__ == "__main__":
    from PySide6.QtCore import Qt

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
