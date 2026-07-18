import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QHBoxLayout,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("KryzenTower")
        self.resize(900, 600)

        # -------------------------------------------------
        # Window icon (used by supported desktops)
        # -------------------------------------------------
        icon_path = Path(__file__).parent / "blue-flame.png"

        if icon_path.exists():
            icon = QIcon(str(icon_path))
            QApplication.instance().setWindowIcon(icon)
            self.setWindowIcon(icon)

        # -------------------------------------------------
        # Main Widget
        # -------------------------------------------------
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        # -------------------------------------------------
        # Header
        # -------------------------------------------------
        header = QHBoxLayout()
        header.setSpacing(20)

        logo = QLabel()

        if icon_path.exists():
            pixmap = QPixmap(str(icon_path))
            pixmap = pixmap.scaled(
                72,
                72,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
            logo.setPixmap(pixmap)

        title_layout = QVBoxLayout()

        title = QLabel("KryzenTower")
        title.setFont(QFont("Arial", 26, QFont.Bold))

        subtitle = QLabel("Portable SSH Recovery Toolkit")
        subtitle.setFont(QFont("Arial", 12))

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        header.addWidget(logo)
        header.addLayout(title_layout)
        header.addStretch()

        layout.addLayout(header)

        # -------------------------------------------------
        # Welcome
        # -------------------------------------------------
        welcome = QLabel(
            "Welcome to KryzenTower.\n\n"
            "Your portable SSH recovery and management toolkit."
        )

        welcome.setAlignment(Qt.AlignCenter)
        welcome.setStyleSheet("""
            font-size:16px;
        """)

        layout.addWidget(welcome)

        # -------------------------------------------------
        # Dark Theme
        # -------------------------------------------------
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
            }

            QWidget {
                background-color: #1E1E1E;
                color: white;
            }

            QLabel {
                color: white;
            }
        """)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
