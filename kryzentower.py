#!/usr/bin/env python3

import sys
from pathlib import Path
import os
import shutil
from PyQt6.QtGui import QIcon

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
    QInputDialog,
    QLineEdit,
)


APP_NAME = "KryzenTower"
APP_VERSION = "V1.7.0"

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

        self.computer_list.setSelectionMode(

            QListWidget.SelectionMode.MultiSelection

        )

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

        self.usb_list.setSelectionMode(

            QListWidget.SelectionMode.MultiSelection

        )

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

        self.refresh_button.clicked.connect(

            self.refresh

        )

        self.backup_button.clicked.connect(

            self.backup_to_usb

        )

        self.install_button.clicked.connect(

            self.install_from_usb

        )

    def build_status(self):

        separator = QFrame()

        separator.setFrameShape(QFrame.Shape.HLine)

        self.main_layout.addWidget(separator)

        self.status_label = QLabel("Status: Ready")

        self.main_layout.addWidget(self.status_label)

    def update_status(self, message=""):

        computer = getattr(

            self,

            "computer_key_count",

            0

        )

        usb = getattr(

            self,

            "usb_key_count",

            0
        )

        text = f"Computer: {computer} | USB: {usb}"

        if message:

            text += f" | {message}"

        self.status_label.setText(

            text

        )

    def refresh(self):

        self.scan_computer()

        self.scan_usb()

    def scan_computer(self):

        self.computer_list.clear()

        ssh_dir = Path.home() / ".ssh"

        if not ssh_dir.exists():

            self.update_status(

                "~/.ssh not found"

            )

            return

        private_keys = []

        for file in ssh_dir.iterdir():

            if not file.is_file():

                continue

            if file.suffix == ".pub":

                continue

            if file.name in (

                "known_hosts",
                "known_hosts.old",
                "authorized_keys",
                "authorized_keys2",
                "config"

            ):

                continue

            pub_file = ssh_dir / f"{file.name}.pub"

            if pub_file.exists():

                private_keys.append(file.name)

        private_keys.sort()

        for key in private_keys:

            self.computer_list.addItem(key)

        self.computer_key_count = len(private_keys)

    def get_usb_root(self):

        if getattr(

            sys,

            "frozen",

            False

        ):

            executable = Path(

                sys.executable

            ).resolve()

        else:

            executable = Path(

                __file__

            ).resolve()

        parts = executable.parts

        if "media" in parts:

            index = parts.index(

                "media"

            )

            if len(parts) >= index + 3:

                return Path(

                    *parts[:index + 3]

                )

        media_dir = Path("/media")

        if not media_dir.exists():

            return None

        for user_dir in media_dir.iterdir():

            if not user_dir.is_dir():

                continue

            for device_dir in user_dir.iterdir():

                if device_dir.is_dir():

                    return device_dir

        return None

    def scan_usb(self):

        self.usb_list.clear()

        usb_root = self.get_usb_root()

        if usb_root is None:

            self.update_status(

                "No USB device detected"

            )

            return

        ssh_dir = usb_root / "KryzenTower" / "SSH"

        if not ssh_dir.exists():

            self.update_status(

                "USB detected"

            )

            return

        entries = []

        for item in ssh_dir.iterdir():

            if item.is_dir():

                entries.append(item.name)

                continue

            if not item.is_file():

                continue

            if item.suffix == ".pub":

                continue

            if item.name in (

                "known_hosts",
                "known_hosts.old",
                "authorized_keys",
                "authorized_keys2",
                "config"

            ):

                continue

            pub_file = ssh_dir / f"{item.name}.pub"

            if pub_file.exists():

                entries.append(item.name)

        entries.sort()

        for entry in entries:

            self.usb_list.addItem(entry)

        self.usb_key_count = len(entries)

        self.update_status()

    def backup_to_usb(self):

        selected = self.computer_list.selectedItems()

        if not selected:

            self.update_status(

                "No SSH keys selected"

            )

            return

        backup_name, ok = QInputDialog.getText(

            self,

            "Backup SSH Keys",

            "Backup name (optional):",

            QLineEdit.EchoMode.Normal

        )

        if not ok:

            self.update_status(

                "Backup cancelled"

            )

            return

        backup_name = backup_name.strip()

        usb_root = self.get_usb_root()

        if usb_root is None:

            self.update_status(

                "No USB device detected"

            )

            return

        kryzentower_dir = usb_root / "KryzenTower"

        kryzentower_dir.mkdir(

            exist_ok=True

        )

        usb_ssh = kryzentower_dir / "SSH"

        usb_ssh.mkdir(

            exist_ok=True

        )

        if backup_name:

            usb_ssh = usb_ssh / backup_name

            usb_ssh.mkdir(

                exist_ok=True

            )

        local_ssh = Path.home() / ".ssh"

        copied = 0

        for item in selected:

            key = item.text()

            private_key = local_ssh / key

            public_key = local_ssh / f"{key}.pub"

            if private_key.exists():

                shutil.copy2(

                    private_key,

                    usb_ssh

                )

            if public_key.exists():

                shutil.copy2(

                    public_key,

                    usb_ssh

                )

            copied += 1

        self.scan_usb()

        self.update_status(

            f"Backed up {copied} key(s)"

        )

    def install_from_usb(self):

        copied = 0

        selected = self.usb_list.selectedItems()

        if not selected:

            self.update_status(

                "No SSH keys selected"

            )

            return

        usb_root = self.get_usb_root()

        if usb_root is None:

            self.update_status(

                "No USB device detected"

            )

            return

        usb_ssh = usb_root / "KryzenTower" / "SSH"

        local_ssh = Path.home() / ".ssh"

        local_ssh.mkdir(

            exist_ok=True

        )

        copied = 0

        for item in selected:

            name = item.text()

            folder = usb_ssh / name

            if folder.is_dir():

                for file in folder.iterdir():

                    if file.is_file():

                        shutil.copy2(

                            file,

                            local_ssh

                        )

                copied += 1

                continue

            private_key = usb_ssh / name

            public_key = usb_ssh / f"{name}.pub"

            if private_key.exists():

                shutil.copy2(

                    private_key,

                    local_ssh

                )

            if public_key.exists():

                shutil.copy2(

                    public_key,

                    local_ssh

                )

            copied += 1

        self.scan_computer()

        self.scan_usb()

        self.update_status(

            f"Installed {copied} backup(s)"

        )

def main():

    app = QApplication(sys.argv)

    window = KryzenTower()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
