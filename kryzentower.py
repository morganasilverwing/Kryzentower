#!/usr/bin/env python3

import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)

APP_NAME = "KryzenTower"
APP_VERSION = "1.0 Alpha"

APP_DIR = Path(__file__).resolve().parent

ICON_FILE = APP_DIR / "blue-flame.png"

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700

class KryzenTower(QWidget):

    def __init__(self):

        super().__init__()

        self.build_window()

        self.build_layout()

        self.build_header()

        self.build_computer_panel()

        self.build_usb_panel()

        self.build_buttons()

        self.build_status()

    def build_window(self):

        self.setWindowTitle(APP_NAME)

        if ICON_FILE.exists():
            self.setWindowIcon(QIcon(str(ICON_FILE)))

        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

    def build_layout(self):

        self.main_layout = QVBoxLayout()

        self.main_layout.setContentsMargins(
            15,
            15,
            15,
            15
        )

        self.main_layout.setSpacing(15)

        self.setLayout(self.main_layout)

    def build_header(self):

        header_layout = QHBoxLayout()

        icon_label = QLabel()

        if ICON_FILE.exists():

            pixmap = QPixmap(str(ICON_FILE))

            pixmap = pixmap.scaled(
                48,
                48,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            icon_label.setPixmap(pixmap)

        header_layout.addWidget(icon_label)

        title = QLabel(APP_NAME)

        font = title.font()

        font.setPointSize(20)

        font.setBold(True)

        title.setFont(font)

        header_layout.addWidget(title)

        header_layout.addStretch()

        version = QLabel(f"Version {APP_VERSION}")

        header_layout.addWidget(version)

        self.main_layout.addLayout(header_layout)

    def build_computer_panel(self):

        frame = QFrame()

        frame.setFrameShape(QFrame.Shape.Box)

        layout = QVBoxLayout()

        frame.setLayout(layout)

        title = QLabel("Computer")

        font = title.font()

        font.setBold(True)

        font.setPointSize(12)

        title.setFont(font)

        layout.addWidget(title)

        self.computer_list = QListWidget()

        layout.addWidget(self.computer_list)

        self.main_layout.addWidget(frame)

    def build_usb_panel(self):

        frame = QFrame()

        frame.setFrameShape(QFrame.Shape.Box)

        layout = QVBoxLayout()

        frame.setLayout(layout)

        title = QLabel("USB Device")

        font = title.font()

        font.setBold(True)

        font.setPointSize(12)

        title.setFont(font)

        layout.addWidget(title)

        self.usb_list = QListWidget()

        layout.addWidget(self.usb_list)

        self.main_layout.addWidget(frame)

    def build_buttons(self):

        self.refresh_button = QPushButton("Refresh")

        self.backup_button = QPushButton("Backup → USB")

        self.install_button = QPushButton("Install ← USB")

        self.refresh_button.setMinimumHeight(40)

        self.backup_button.setMinimumHeight(40)

        self.install_button.setMinimumHeight(40)

        self.main_layout.addWidget(

            self.refresh_button

        )

        self.main_layout.addWidget(

            self.backup_button

        )

        self.main_layout.addWidget(

            self.install_button

        )

    def build_status(self):

        separator = QFrame()

        separator.setFrameShape(QFrame.Shape.HLine)

        self.main_layout.addWidget(separator)

        self.status_label = QLabel("Status: Ready")

        self.main_layout.addWidget(self.status_label)

def main():

    app = QApplication(sys.argv)

    window = KryzenTower()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
