# ==========================================================
# MODULE 1 - IMPORTS
# ==========================================================

import json
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtGui import QFont
from PySide6.QtGui import QIcon
from PySide6.QtGui import QPixmap

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGroupBox
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QListWidget
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QTextEdit
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

# ==========================================================
# MODULE 2 - APPLICATION CONFIGURATION
# ==========================================================

APP_NAME = "KryzenTower"
APP_VERSION = "0.4.0"

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 520

SCRIPT_DIR = Path(__file__).resolve().parent

ICON_PATH = SCRIPT_DIR / "blue-flame.png"

VAULT_DIR = SCRIPT_DIR / "vault"

SSH_DIR = VAULT_DIR / "ssh"

GPG_DIR = VAULT_DIR / "gpg"

GIT_DIR = VAULT_DIR / "git"

SSH_CONFIG_DIR = VAULT_DIR / "sshconfig"

DATA_DIR = SCRIPT_DIR / "data"

LOG_DIR = SCRIPT_DIR / "logs"

INVENTORY_FILE = DATA_DIR / "inventory.json"

SETTINGS_FILE = DATA_DIR / "settings.json"

# ==========================================================
# MODULE 3 - DIRECTORY INITIALIZATION
# ==========================================================

DIRECTORIES = [

    VAULT_DIR,

    SSH_DIR,

    GPG_DIR,

    GIT_DIR,

    SSH_CONFIG_DIR,

    DATA_DIR,

    LOG_DIR,

]

for directory in DIRECTORIES:

    directory.mkdir(
        parents=True,
        exist_ok=True
    )

# ==========================================================
# MODULE 4 - LOGGER
# ==========================================================

logging.basicConfig(

    filename=LOG_DIR / "kryzentower.log",

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)

logging.info("Starting KryzenTower")

# ==========================================================
# MODULE 5 - APPLICATION THEME
# ==========================================================

APP_THEME = """
QMainWindow {

    background-color: #1e1e1e;

}

QWidget {

    background-color: #1e1e1e;

    color: white;

    font-family: Arial;

}

QGroupBox {

    border: 2px solid #2d7dff;

    border-radius: 8px;

    margin-top: 12px;

    font-weight: bold;

    padding-top: 10px;

}

QGroupBox::title {

    subcontrol-origin: margin;

    left: 12px;

    padding: 0 4px;

}

QPushButton {

    background-color: #2b2b2b;

    border: 2px solid #2d7dff;

    border-radius: 8px;

    color: white;

    font-size: 10pt;

    font-weight: bold;

    text-align: left;

    padding: 6px 12px;

    min-height: 34px;

}

QPushButton:hover {

    background-color: #3b3b3b;

    border: 2px solid #64a8ff;

}

QPushButton:pressed {

    background-color: #181818;

    border: 2px solid #1f6fff;

}

QLabel {

    font-size: 10pt;

}
"""

# ==========================================================
# MODULE 6 - UTILITY FUNCTIONS
# ==========================================================

def run_command(command):

    try:

        result = subprocess.run(

            command,

            capture_output=True,

            text=True,

            check=True

        )

        return result.stdout.strip()

    except Exception:

        return ""


def file_exists(path):

    return Path(path).exists()


def ensure_permissions(path, mode):

    try:

        os.chmod(path, mode)

    except Exception:

        pass

# ==========================================================
# MODULE 7 - USB DETECTION
# ==========================================================

class USBDetector:

    def __init__(self):

        self.usb_root = None

    def find_usb(self):

        candidates = [

            Path("/media"),

            Path("/run/media"),

            Path("/mnt")

        ]

        for base in candidates:

            if not base.exists():

                continue

            for path in base.rglob("vault"):

                if path.is_dir():

                    self.usb_root = path.parent

                    logging.info(

                        f"KryzenTower USB found: {self.usb_root}"

                    )

                    return self.usb_root

        logging.info("No KryzenTower USB detected.")

        return None

# ==========================================================
# MODULE 8 - INVENTORY MANAGER
# ==========================================================

class InventoryManager:

    def __init__(self):

        self.inventory = {

            "ssh": {},

            "gpg": {},

            "git": {},

            "ssh_config": {}

        }

        self.load()


    def load(self):

        if INVENTORY_FILE.exists():

            try:

                with open(

                    INVENTORY_FILE,

                    "r",

                    encoding="utf-8"

                ) as file:

                    self.inventory = json.load(file)

            except Exception as error:

                logging.error(

                    f"Unable to load inventory: {error}"

                )


    def save(self):

        with open(

            INVENTORY_FILE,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                self.inventory,

                file,

                indent=4

            )


    def update_category(

        self,

        category,

        data

    ):

        self.inventory[category] = data

        self.save()

# ==========================================================
# MODULE 9 - HEALTH CHECK
# ==========================================================

class HealthCheck:

    def __init__(

        self,

        inventory

    ):

        self.inventory = inventory

        self.results = {}


    def check_ssh(self):

        ssh_path = Path.home() / ".ssh"

        keys = []

        if ssh_path.exists():

            for file in ssh_path.iterdir():

                if (

                    file.is_file()

                    and not file.name.endswith(".pub")

                    and file.name != "known_hosts"

                    and file.name != "config"

                ):

                    keys.append(file.name)

        self.results["ssh"] = keys

        return keys


    def check_git(self):

        gitconfig = Path.home() / ".gitconfig"

        self.results["git"] = gitconfig.exists()

        return gitconfig.exists()


    def check_gpg(self):

        gnupg = Path.home() / ".gnupg"

        self.results["gpg"] = gnupg.exists()

        return gnupg.exists()


    def run(self):

        self.check_ssh()

        self.check_git()

        self.check_gpg()

        return self.results

# ==========================================================
# MODULE 10 - BACKUP MANAGER
# ==========================================================

class BackupManager:

    def backup_ssh(self):

        source = Path.home() / ".ssh"

        if not source.exists():

            return

        for file in source.iterdir():

            if file.is_file():

                shutil.copy2(

                    file,

                    SSH_DIR / file.name

                )


    def backup_git(self):

        source = Path.home() / ".gitconfig"

        if source.exists():

            shutil.copy2(

                source,

                GIT_DIR / "gitconfig"

            )


    def backup_known_hosts(self):

        source = Path.home() / ".ssh" / "known_hosts"

        if source.exists():

            shutil.copy2(

                source,

                SSH_CONFIG_DIR / "known_hosts"

            )


    def backup_config(self):

        source = Path.home() / ".ssh" / "config"

        if source.exists():

            shutil.copy2(

                source,

                SSH_CONFIG_DIR / "config"

            )


    def backup_all(self):

        self.backup_ssh()

        self.backup_git()

        self.backup_known_hosts()

        self.backup_config()

        logging.info(

            "Backup completed."

        )

# ==========================================================
# MODULE 11 - GPG MANAGER
# ==========================================================

class GPGManager:

    def __init__(self):

        self.gpg_dir = GPG_DIR

        self.gpg_dir.mkdir(
            parents=True,
            exist_ok=True
        )


    def list_keys(self):

        command = [

            "gpg",

            "--list-secret-keys",

            "--with-colons"

        ]

        output = run_command(command)

        identities = []

        current = None

        for line in output.splitlines():

            fields = line.split(":")

            if not fields:

                continue

            if fields[0] == "fpr":

                current = fields[9]

            elif fields[0] == "uid" and current:

                identities.append({

                    "fingerprint": current,

                    "uid": fields[9]

                })

                current = None

        return identities


    def export_public_key(

        self,

        fingerprint

    ):

        outfile = self.gpg_dir / f"{fingerprint}_public.asc"

        subprocess.run(

            [

                "gpg",

                "--armor",

                "--export",

                fingerprint

            ],

            stdout=open(outfile, "w"),

            check=False

        )


    def export_secret_key(

        self,

        fingerprint

    ):

        outfile = self.gpg_dir / f"{fingerprint}_secret.asc"

        subprocess.run(

            [

                "gpg",

                "--armor",

                "--export-secret-keys",

                fingerprint

            ],

            stdout=open(outfile, "w"),

            check=False

        )


    def backup_all(self):

        for key in self.list_keys():

            self.export_public_key(

                key["fingerprint"]

            )

            self.export_secret_key(

                key["fingerprint"]

            )

        logging.info(

            "GPG backup completed."

        )

# ==========================================================
# MODULE 12 - INSTALL MANAGER
# ==========================================================

class InstallManager:

    def __init__(self):

        self.ssh_source = SSH_DIR

        self.gpg_source = GPG_DIR

        self.git_source = GIT_DIR

        self.ssh_config_source = SSH_CONFIG_DIR


    # ------------------------------------------------------
    # SSH
    # ------------------------------------------------------

    def install_ssh_keys(

        self,

        selected_keys

    ):

        target = Path.home() / ".ssh"

        target.mkdir(

            exist_ok=True,

            mode=0o700

        )

        for key in selected_keys:

            source = self.ssh_source / key

            if source.exists():

                shutil.copy2(

                    source,

                    target / key

                )

                os.chmod(

                    target / key,

                    0o600

                )


    # ------------------------------------------------------
    # Git
    # ------------------------------------------------------

    def install_git(self):

        source = self.git_source / "gitconfig"

        target = Path.home() / ".gitconfig"

        if source.exists():

            shutil.copy2(

                source,

                target

            )


    # ------------------------------------------------------
    # SSH Config
    # ------------------------------------------------------

    def install_ssh_config(

        self,

        install_config=True,

        install_known_hosts=True

    ):

        target = Path.home() / ".ssh"

        target.mkdir(

            exist_ok=True,

            mode=0o700

        )

        if install_config:

            source = self.ssh_config_source / "config"

            if source.exists():

                shutil.copy2(

                    source,

                    target / "config"

                )

        if install_known_hosts:

            source = self.ssh_config_source / "known_hosts"

            if source.exists():

                shutil.copy2(

                    source,

                    target / "known_hosts"

                )


    # ------------------------------------------------------
    # GPG
    # ------------------------------------------------------

    def install_gpg(

        self,

        selected_files

    ):

        for file in selected_files:

            subprocess.run(

                [

                    "gpg",

                    "--import",

                    str(file)

                ],

                check=False

            )

# ==========================================================
# MODULE 13 - SSH LOADER
# ==========================================================

class SSHLoader:

    def __init__(self):

        self.ssh_dir = Path.home() / ".ssh"


    def is_agent_running(self):

        return "SSH_AUTH_SOCK" in os.environ


    def start_agent(self):

        if self.is_agent_running():

            return True

        subprocess.run(

            ["ssh-agent"],

            stdout=subprocess.DEVNULL,

            stderr=subprocess.DEVNULL,

            check=False

        )

        return self.is_agent_running()


    def load_key(

        self,

        key_name

    ):

        key = self.ssh_dir / key_name

        if not key.exists():

            return False

        subprocess.run(

            [

                "ssh-add",

                str(key)

            ],

            check=False

        )

        return True


    def load_selected(

        self,

        keys

    ):

        self.start_agent()

        for key in keys:

            self.load_key(key)


    def load_all(self):

        self.start_agent()

        for key in self.ssh_dir.iterdir():

            if (

                key.is_file()

                and not key.name.endswith(".pub")

                and key.name != "config"

                and key.name != "known_hosts"

            ):

                self.load_key(key.name)


    def unload_all(self):

        subprocess.run(

            [

                "ssh-add",

                "-D"

            ],

            check=False

        )

# ==========================================================
# MODULE 14 - REMOTE INSTALLER
# ==========================================================

class RemoteInstaller:

    def __init__(self):

        self.ssh_dir = SSH_DIR


    def install_public_key(

        self,

        public_key,

        username,

        hostname,

        port=22

    ):

        key = self.ssh_dir / public_key

        if not key.exists():

            return False

        command = [

            "ssh-copy-id",

            "-i",

            str(key),

            "-p",

            str(port),

            f"{username}@{hostname}"

        ]

        subprocess.run(

            command,

            check=False

        )

        return True

# ==========================================================
# MODULE 15 - CLIPBOARD MANAGER
# ==========================================================

class ClipboardManager:

    def copy_text(

        self,

        text

    ):

        clipboard = QApplication.clipboard()

        clipboard.setText(text)


    def copy_public_key(

        self,

        filename

    ):

        file = SSH_DIR / filename

        if not file.exists():

            return False

        with open(

            file,

            "r",

            encoding="utf-8"

        ) as f:

            self.copy_text(

                f.read()

            )

        return True

# ==========================================================
# MODULE 16 - RECOVERY GUIDE
# ==========================================================

class RecoveryGuide:

    def text(self):

        return """

KryzenTower Recovery Guide

1.

Plug in your KryzenTower USB.

2.

Open KryzenTower.

3.

Scan for Backups.

4.

Install Selected

or

Install Everything.

5.

Load SSH Keys.

6.

Reconnect to your servers.

7.

Done.

"""

# ==========================================================
# MODULE 17 - SETTINGS MANAGER
# ==========================================================

class SettingsManager:

    def __init__(self):

        self.settings = {

            "theme": "dark",

            "auto_scan": True,

            "check_changes": True,

            "window_width": WINDOW_WIDTH,

            "window_height": WINDOW_HEIGHT

        }

        self.load()


    def load(self):

        if SETTINGS_FILE.exists():

            with open(

                SETTINGS_FILE,

                "r",

                encoding="utf-8"

            ) as file:

                self.settings.update(

                    json.load(file)

                )


    def save(self):

        with open(

            SETTINGS_FILE,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                self.settings,

                file,

                indent=4

            )

# ==========================================================
# MODULE 18 - APPLICATION CONTROLLER
# ==========================================================

class KryzenTowerController:

    def __init__(self):

        self.inventory = InventoryManager()

        self.health = HealthCheck(self.inventory)

        self.backup = BackupManager()

        self.gpg = GPGManager()

        self.install = InstallManager()

        self.loader = SSHLoader()

        self.remote = RemoteInstaller()

        self.clipboard = ClipboardManager()

        self.settings = SettingsManager()

        self.recovery = RecoveryGuide()

        self.usb = USBDetector()


    # ------------------------------------------------------

    def scan(self):

        return self.health.run()


    # ------------------------------------------------------

    def backup_everything(self):

        self.backup.backup_all()

        self.gpg.backup_all()

        logging.info("Backup finished.")


    # ------------------------------------------------------

    def load_selected_keys(self, keys):

        self.loader.load_selected(keys)


    # ------------------------------------------------------

    def unload_all_keys(self):

        self.loader.unload_all()

# ==========================================================
# MODULE 19 - MAIN WINDOW
# ==========================================================

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.controller = KryzenTowerController()

        self.setWindowTitle(

            f"{APP_NAME} {APP_VERSION}"

        )

        self.setWindowIcon(

            QIcon(str(ICON_PATH))

        )

        self.setFixedSize(

            WINDOW_WIDTH,

            WINDOW_HEIGHT

        )

        self.setStyleSheet(APP_THEME)

        self.build_ui()

    def show_scan_dialog(self):

        dialog = ScanDialog(self.controller)

        dialog.exec()

    def show_backup_dialog(self):

        dialog = BackupDialog(self.controller)

        dialog.exec()

    def build_ui(self):

        central = QWidget()

        self.setCentralWidget(central)

        layout = QVBoxLayout()

        layout.setContentsMargins(

            15,

            15,

            15,

            15

        )

        layout.setSpacing(8)

        central.setLayout(layout)

        header = QHBoxLayout()

        logo = QLabel()

        pix = QPixmap(str(ICON_PATH))

        pix = pix.scaled(

            48,

            48,

            Qt.KeepAspectRatio,

            Qt.SmoothTransformation

        )

        logo.setPixmap(pix)

        titles = QVBoxLayout()

        title = QLabel(APP_NAME)

        title.setFont(

            QFont(

                "Arial",

                18,

                QFont.Bold

            )

        )

        subtitle = QLabel(

            "Portable Identity & Recovery Manager"

        )

        subtitle.setStyleSheet(

            "color:#A0A0A0;"

        )

        titles.addWidget(title)

        titles.addWidget(subtitle)

        header.addWidget(logo)

        header.addLayout(titles)

        header.addStretch()

        layout.addLayout(header)

        self.status = QGroupBox("Status")

        self.status.setMaximumHeight(140)

        status_layout = QVBoxLayout()

        self.status_label = QLabel(

            "Ready"

        )

        status_layout.addWidget(

            self.status_label

        )

        self.status.setLayout(

            status_layout

        )

        layout.addWidget(

            self.status

        )

        self.button_map = {}

        self.buttons = [

            "🔍 Scan & Detect Changes",

            "💾 Backup Changes to USB",

            "📥 Install to This Computer",

            "🔒 Load SSH Keys",

            "🌐 Install Public Key to Server",

            "📋 Copy Public Key",

            "📖 Recovery Guide",

            "⚙ Settings"

        ]

        for text in self.buttons:

            button = QPushButton(text)

            button.setCursor(Qt.PointingHandCursor)

            layout.addWidget(button)

            self.button_map[text] = button

        self.button_map[
            "🔍 Scan & Detect Changes"
        ].clicked.connect(
            self.show_scan_dialog
        )

        self.button_map[
            "💾 Backup Changes to USB"
        ].clicked.connect(
            self.show_backup_dialog
        )
# ==========================================================
# MODULE 21 - VAULT MANAGER
# ==========================================================

class VaultManager:

    def __init__(self):

        self.project_root = SCRIPT_DIR

        self.usb_root = None

        self.vault_root = SCRIPT_DIR / "vault"

        self.detect()


    def detect(self):

        detector = USBDetector()

        usb = detector.find_usb()

        if usb:

            self.usb_root = usb

            self.vault_root = usb / "vault"

        else:

            self.vault_root = SCRIPT_DIR / "vault"

        self.create_structure()


    def create_structure(self):

        folders = [

            self.vault_root,

            self.vault_root / "ssh",

            self.vault_root / "gpg",

            self.vault_root / "gpg" / "public",

            self.vault_root / "gpg" / "secret",

            self.vault_root / "git",

            self.vault_root / "sshconfig",

            self.vault_root / "backups"

        ]

        for folder in folders:

            folder.mkdir(

                parents=True,

                exist_ok=True

            )


    def ssh_path(self):

        return self.vault_root / "ssh"


    def gpg_path(self):

        return self.vault_root / "gpg"


    def git_path(self):

        return self.vault_root / "git"


    def ssh_config_path(self):

        return self.vault_root / "sshconfig"


    def backup_path(self):

        return self.vault_root / "backups"


    def using_usb(self):

        return self.usb_root is not None

# ==========================================================
# MODULE 23 - SCAN DIALOG
# ==========================================================

class ScanDialog(QMessageBox):

    def __init__(self, controller):

        super().__init__()

        self.controller = controller

        self.setWindowTitle("System Scan")

        self.setIcon(QMessageBox.Information)

        self.refresh()


    def refresh(self):

        results = self.controller.scan()

        lines = []

        ssh_keys = results.get("ssh", [])

        lines.append("KryzenTower System Scan")
        lines.append("")
        lines.append(f"SSH Keys Found : {len(ssh_keys)}")

        if ssh_keys:

            lines.append("")

            for key in ssh_keys:

                lines.append(f"    • {key}")

        lines.append("")
        lines.append(
            f"GPG Available : {'Yes' if results.get('gpg') else 'No'}"
        )

        lines.append(
            f"Git Configuration : {'Found' if results.get('git') else 'Missing'}"
        )

        self.setText("\n".join(lines))

        self.setStandardButtons(QMessageBox.Ok)

# ==========================================================
# MODULE 24 - BACKUP DIALOG
# ==========================================================

from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
)


class BackupDialog(QDialog):

    def __init__(self, controller):

        super().__init__()

        self.controller = controller

        self.setWindowTitle("Backup to KryzenTower")

        self.setFixedWidth(420)

        layout = QVBoxLayout()

        self.setLayout(layout)

        info = QLabel(
            "Select what you want to back up to the KryzenTower vault."
        )

        info.setWordWrap(True)

        layout.addWidget(info)

        # --------------------------------------------------
        # SSH
        # --------------------------------------------------

        self.ssh_checkbox = QCheckBox("SSH Keys")

        self.ssh_checkbox.setChecked(True)

        layout.addWidget(self.ssh_checkbox)

        # --------------------------------------------------
        # GPG
        # --------------------------------------------------

        self.gpg_checkbox = QCheckBox("GPG Keys")

        self.gpg_checkbox.setChecked(True)

        layout.addWidget(self.gpg_checkbox)

        # --------------------------------------------------
        # Git
        # --------------------------------------------------

        self.git_checkbox = QCheckBox("Git Configuration")

        self.git_checkbox.setChecked(True)

        layout.addWidget(self.git_checkbox)

        # --------------------------------------------------
        # SSH Config
        # --------------------------------------------------

        self.config_checkbox = QCheckBox("SSH Configuration")

        self.config_checkbox.setChecked(True)

        layout.addWidget(self.config_checkbox)

        layout.addSpacing(10)

        buttons = QDialogButtonBox(

            QDialogButtonBox.Ok |

            QDialogButtonBox.Cancel

        )

        buttons.accepted.connect(self.perform_backup)

        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)


    def perform_backup(self):

        if self.ssh_checkbox.isChecked():

            self.controller.backup.backup_ssh()

        if self.gpg_checkbox.isChecked():

            self.controller.gpg.backup_all()

        if self.git_checkbox.isChecked():

            self.controller.backup.backup_git()

        if self.config_checkbox.isChecked():

            self.controller.backup.backup_config()

            self.controller.backup.backup_known_hosts()

        QMessageBox.information(

            self,

            "Backup Complete",

            "Selected items were backed up successfully."

        )

        self.accept()

# ==========================================================
# MODULE 22 - APPLICATION ENTRY POINT
# ==========================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())
