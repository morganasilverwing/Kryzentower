#!/usr/bin/env python3
# ============================================================
# IMPORTS
# ============================================================

import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

from PySide6.QtCore import Qt

from PySide6.QtGui import (
    QAction,
    QFont,
    QIcon,
    QPixmap,
)

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

APP_NAME = "KryzenTower"
APP_VERSION = "0.3.0"

WINDOW_WIDTH = 650
WINDOW_HEIGHT = 720

DEFAULT_SSH_PORT = 22

SETTINGS_FILE = "settings.json"

SUPPORTED_KEY_TYPES = [
    "id_ed25519",
    "id_rsa",
]


# ============================================================
# PATHS MODULE
# ============================================================

class Paths:
    """
    Handles all project paths.
    """

    def __init__(self):

        self.project = Path(__file__).parent.resolve()

        self.icon = self.project / "blue-flame.png"

        self.data = self.project / "data"

        self.keys = self.project / "keys"

        self.settings = self.data / "settings.json"

        self.log = self.data / "recovery.log"

        self.known_hosts = self.data / "known_hosts"

        self.private_key = self.keys / "id_ed25519"

        self.public_key = self.keys / "id_ed25519.pub"

    def initialize(self):
        """
        Create required directories if they do not exist.
        """

        self.data.mkdir(exist_ok=True)

        self.keys.mkdir(exist_ok=True)


PATHS = Paths()

PATHS.initialize()

# ============================================================
# THEME MODULE
# ============================================================

class Theme:
    """
    Application theme and styling.
    """

    STYLE = """
    QMainWindow {
        background-color: #1e1e1e;
    }

    QWidget {
        background-color: #1e1e1e;
        color: white;
        font-size: 11pt;
        font-family: Arial;
    }

    QLabel {
        color: white;
    }

    QGroupBox {
        border: 1px solid #404040;
        border-radius: 8px;
        margin-top: 10px;
        padding-top: 10px;
        font-weight: bold;
    }

    QPushButton {

        background-color: #2b2b2b;

        border: 2px solid #2d7dff;

        border-radius: 8px;

        color: white;

        font-size: 12pt;

        font-weight: bold;

        text-align: left;

        padding: 12px;

    }

    QPushButton:hover {

        background-color: #3b3b3b;

        border: 2px solid #64a8ff;

    }

    QPushButton:pressed {

        background-color: #181818;

        border: 2px solid #1f6fff;

    }

    QTextEdit {

        background-color: #252525;

        border: 1px solid #404040;

        color: white;
    }
    """

    @staticmethod
    def apply(app):
        app.setStyleSheet(Theme.STYLE)


# ============================================================
# UTILITY MODULE
# ============================================================

class Utils:
    """
    General helper functions.
    """

    @staticmethod
    def info(parent, title, message):
        QMessageBox.information(
            parent,
            title,
            message,
        )

    @staticmethod
    def warning(parent, title, message):
        QMessageBox.warning(
            parent,
            title,
            message,
        )

    @staticmethod
    def error(parent, title, message):
        QMessageBox.critical(
            parent,
            title,
            message,
        )

    @staticmethod
    def command_exists(command):
        return shutil.which(command) is not None

    @staticmethod
    def file_exists(path):
        return Path(path).exists()

    @staticmethod
    def read_text(path):

        try:
            return Path(path).read_text()

        except Exception:
            return ""

    @staticmethod
    def write_text(path, text):

        try:

            Path(path).write_text(text)

            return True

        except Exception:

            return False

    @staticmethod
    def run(command):

        try:

            return subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )

        except Exception as exc:

            return exc

    @staticmethod
    def file_permissions(path):

        if not Path(path).exists():
            return None

        return oct(
            Path(path).stat().st_mode & 0o777
        )

    @staticmethod
    def separator():

        return "=" * 60

# ============================================================
# STATUS MODULE
# ============================================================

class Status:
    """
    Holds the current application status.
    """

    def __init__(self):

        self.reset()

    def reset(self):

        self.usb = "⚪ Waiting for Health Check..."
        self.private_key = "⚪ Not Checked"
        self.public_key = "⚪ Not Checked"
        self.agent = "⚪ Not Running"

    def as_list(self):

        return [
            self.usb,
            self.private_key,
            self.public_key,
            self.agent,
        ]


STATUS = Status()


# ============================================================
# HEALTH CHECK MODULE
# ============================================================

class HealthCheck:
    """
    Performs system and SSH environment checks.
    """

    def __init__(self):

        self.status = STATUS

    def run(self):

        self.check_usb()

        self.check_private_key()

        self.check_public_key()

        self.check_agent()

        return self.status

    # --------------------------------------------------------
    # USB
    # --------------------------------------------------------

    def check_usb(self):

        if PATHS.keys.exists():

            self.status.usb = "🟢 Keys Folder Found"

        else:

            self.status.usb = "🔴 Keys Folder Not Found"

    # --------------------------------------------------------
    # Private Key
    # --------------------------------------------------------

    def check_private_key(self):

        if PATHS.private_key.exists():

            self.status.private_key = "🟢 Private Key Found"

        else:

            self.status.private_key = "🔴 Private Key Missing"

    # --------------------------------------------------------
    # Public Key
    # --------------------------------------------------------

    def check_public_key(self):

        if PATHS.public_key.exists():

            self.status.public_key = "🟢 Public Key Found"

        else:

            self.status.public_key = "🔴 Public Key Missing"

    # --------------------------------------------------------
    # SSH Agent
    # --------------------------------------------------------

    def check_agent(self):

        if os.environ.get("SSH_AUTH_SOCK"):

            self.status.agent = "🟢 SSH Agent Running"

        else:

            self.status.agent = "⚪ SSH Agent Not Running"

    # --------------------------------------------------------
    # Permission Check
    # --------------------------------------------------------

    def private_key_permissions(self):

        if not PATHS.private_key.exists():

            return False

        perms = PATHS.private_key.stat().st_mode & 0o777

        return perms == 0o600

    # --------------------------------------------------------
    # OpenSSH Checks
    # --------------------------------------------------------

    def openssh_available(self):

        return {
            "ssh": Utils.command_exists("ssh"),
            "ssh-add": Utils.command_exists("ssh-add"),
            "ssh-agent": Utils.command_exists("ssh-agent"),
            "ssh-copy-id": Utils.command_exists("ssh-copy-id"),
        }


HEALTH = HealthCheck()

# ============================================================
# SSH SESSION MODULE
# ============================================================

class SSHSession:
    """
    Starts and manages a temporary ssh-agent session.
    """

    def __init__(self):

        self.agent_running = False

    def start(self):

        if not PATHS.private_key.exists():

            Utils.error(
                None,
                "Private Key",
                "No private key was found."
            )
            return False

        if not Utils.command_exists("ssh-agent"):

            Utils.error(
                None,
                "OpenSSH",
                "ssh-agent is not installed."
            )
            return False

        if not Utils.command_exists("ssh-add"):

            Utils.error(
                None,
                "OpenSSH",
                "ssh-add is not installed."
            )
            return False

        Utils.info(
            None,
            "SSH Session",
            "Portable SSH Session will be implemented in the next version."
        )

        return True

    def stop(self):

        Utils.info(
            None,
            "SSH Session",
            "Session cleanup will be implemented later."
        )


SSH_SESSION = SSHSession()


# ============================================================
# LOCAL INSTALL MODULE
# ============================================================

class LocalInstaller:
    """
    Installs an existing SSH key on the current computer.
    """

    def __init__(self):

        self.home = Path.home()

        self.ssh_dir = self.home / ".ssh"

    def ensure_directory(self):

        self.ssh_dir.mkdir(
            exist_ok=True
        )

        os.chmod(
            self.ssh_dir,
            0o700
        )

    def install_private_key(self):

        if not PATHS.private_key.exists():

            Utils.error(
                None,
                "Private Key",
                "Private key not found."
            )

            return False

        destination = self.ssh_dir / PATHS.private_key.name

        shutil.copy2(
            PATHS.private_key,
            destination
        )

        os.chmod(
            destination,
            0o600
        )

        return True

    def install_public_key(self):

        if not PATHS.public_key.exists():

            Utils.error(
                None,
                "Public Key",
                "Public key not found."
            )

            return False

        destination = self.ssh_dir / PATHS.public_key.name

        shutil.copy2(
            PATHS.public_key,
            destination
        )

        os.chmod(
            destination,
            0o644
        )

        return True

    def install(self):

        self.ensure_directory()

        if not self.install_private_key():

            return False

        if not self.install_public_key():

            return False

        Utils.info(
            None,
            "Install Complete",
            "SSH key installed successfully.\n\n"
            "You can now load it using ssh-add."
        )

        return True


LOCAL_INSTALLER = LocalInstaller()

# ============================================================
# REMOTE INSTALL MODULE
# ============================================================

class RemoteInstaller:
    """
    Installs the public SSH key onto a remote Linux server.
    """

    def install(self, user, host, port=22):

        if not PATHS.public_key.exists():

            Utils.error(
                None,
                "Public Key",
                "Public key not found."
            )

            return False

        if not Utils.command_exists("ssh-copy-id"):

            Utils.warning(
                None,
                "ssh-copy-id",
                "ssh-copy-id is not installed.\n\n"
                "Manual installation will be available."
            )

            return False

        command = [
            "ssh-copy-id",
            "-i",
            str(PATHS.public_key),
            "-p",
            str(port),
            f"{user}@{host}"
        ]

        result = Utils.run(command)

        if isinstance(result, Exception):

            Utils.error(
                None,
                "Remote Installation",
                str(result)
            )

            return False

        Utils.info(
            None,
            "Remote Installation",
            "Public key installation completed."
        )

        return True


REMOTE_INSTALLER = RemoteInstaller()


# ============================================================
# CLIPBOARD MODULE
# ============================================================

class Clipboard:

    """
    Copies the public SSH key to the clipboard.
    """

    def copy_public_key(self):

        if not PATHS.public_key.exists():

            Utils.error(
                None,
                "Clipboard",
                "Public key not found."
            )

            return False

        text = PATHS.public_key.read_text()

        QApplication.clipboard().setText(text)

        Utils.info(
            None,
            "Clipboard",
            "Public key copied to clipboard."
        )

        return True


CLIPBOARD = Clipboard()


# ============================================================
# RECOVERY GUIDE MODULE
# ============================================================

class RecoveryGuide:

    """
    Displays the built-in recovery guide.
    """

    GUIDE = """
KRYZENTOWER RECOVERY GUIDE

1. Plug your KryzenTower USB into a Linux computer.

2. Open KryzenTower.

3. Run Health Check.

4. Install the SSH key locally.

5. Load the key into ssh-agent.

6. Test the VPS connection.

7. Install the public key onto additional servers.

Remember:

• Never share the private key.
• The public key is safe to distribute.
• Always protect your USB.
"""

    def show(self, parent=None):

        box = QMessageBox(parent)

        box.setWindowTitle("Recovery Guide")

        box.setText(self.GUIDE)

        box.exec()


RECOVERY_GUIDE = RecoveryGuide()


# ============================================================
# SETTINGS MODULE
# ============================================================

class Settings:
    """
    Application settings.
    """

    def __init__(self):

        self.data = {
            "version": APP_VERSION,
            "last_usb": "",
            "default_user": "",
            "default_host": "",
            "default_port": DEFAULT_SSH_PORT,
        }

    def load(self):

        if not PATHS.settings.exists():
            return

        try:

            self.data.update(
                json.loads(
                    PATHS.settings.read_text()
                )
            )

        except Exception:

            pass

    def save(self):

        PATHS.settings.write_text(
            json.dumps(
                self.data,
                indent=4
            )
        )


SETTINGS = Settings()

SETTINGS.load()

# ============================================================
# MAIN WINDOW MODULE
# ============================================================

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            f"{APP_NAME} {APP_VERSION}"
        )

        self.resize(
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )

        if PATHS.icon.exists():

            icon = QIcon(str(PATHS.icon))

            QApplication.instance().setWindowIcon(icon)

            self.setWindowIcon(icon)

        self.build_ui()

        self.refresh_status()

    # --------------------------------------------------------

    # --------------------------------------------------------
    # Button Factory
    # --------------------------------------------------------

    def create_button(
        self,
        text,
        slot,
        tooltip=""
    ):

        button = QPushButton(text)

        button.setMinimumHeight(55)

        button.setCursor(Qt.PointingHandCursor)

        button.clicked.connect(slot)

        if tooltip:

            button.setToolTip(tooltip)

        return button

    def build_ui(self):

        central = QWidget()

        self.setCentralWidget(central)

        layout = QVBoxLayout()

        layout.setContentsMargins(20,20,20,20)

        layout.setSpacing(15)

        central.setLayout(layout)

        # ----------------------------------------------------
        # Header
        # ----------------------------------------------------

        header = QHBoxLayout()

        if PATHS.icon.exists():

            logo = QLabel()

            pix = QPixmap(str(PATHS.icon))

            pix = pix.scaled(
                72,
                72,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            logo.setPixmap(pix)

            header.addWidget(logo)

        titles = QVBoxLayout()

        title = QLabel(APP_NAME)

        title.setFont(
            QFont(
                "Arial",
                24,
                QFont.Bold
            )
        )

        subtitle = QLabel(
            "Portable SSH Recovery Toolkit"
        )

        titles.addWidget(title)

        titles.addWidget(subtitle)

        header.addLayout(titles)

        header.addStretch()

        layout.addLayout(header)

        # ----------------------------------------------------
        # Status Box
        # ----------------------------------------------------

        self.status_group = QGroupBox("Status")

        status_layout = QVBoxLayout()

        self.lbl_usb = QLabel(
            "⚪ Waiting for Health Check..."
        )

        self.lbl_private = QLabel(
            "⚪ Not Checked"
        )

        self.lbl_public = QLabel(
            "⚪ Not Checked"
        )

        self.lbl_agent = QLabel(
            "⚪ Not Running"
        )

        status_layout.addWidget(self.lbl_usb)

        status_layout.addWidget(self.lbl_private)

        status_layout.addWidget(self.lbl_public)

        status_layout.addWidget(self.lbl_agent)

        self.status_group.setLayout(status_layout)

        layout.addWidget(self.status_group)

        # ----------------------------------------------------
        # Buttons
        # ----------------------------------------------------

        self.buttons = [

            ("🔒 Portable SSH Session",
             self.start_session),

            ("💾 Install Key on This Computer",
             self.install_local),

            ("🌐 Install Public Key on Remote Server",
             self.install_remote),

            ("📋 Copy Public Key",
             self.copy_public_key),

            ("📖 Recovery Guide",
             self.show_recovery),

            ("🔍 Health Check",
             self.health_check),

            ("⚙ Settings",
             self.settings),

            ("❌ Exit",
             self.close),
        ]

        button_info = [

            (
                "🔒 Portable SSH Session",
                self.start_session,
                "Load your portable SSH key into memory."
            ),

            (
                "💾 Install Key on This Computer",
                self.install_local,
                "Install the SSH key into ~/.ssh."
            ),

            (
                "🌐 Install Public Key on Remote Server",
                self.install_remote,
                "Install the public key onto a VPS."
            ),

            (
                "📋 Copy Public Key",
                self.copy_public_key,
                "Copy the public key to the clipboard."
            ),

            (
                "📖 Recovery Guide",
                self.show_recovery,
                "Open the recovery guide."
            ),

            (
                "🔍 Health Check",
                self.health_check,
                "Run a full system health check."
            ),

            (
                "⚙ Settings",
                self.settings,
                "Open application settings."
            ),

            (
                "❌ Exit",
                self.close,
                "Close KryzenTower."
            ),

        ]

        for text, slot, tooltip in button_info:

            button = self.create_button(
                text,
                slot,
                tooltip
            )

            layout.addWidget(button)

        layout.addStretch()

        footer = QLabel(
            f"{APP_NAME} {APP_VERSION}"
        )

        footer.setAlignment(Qt.AlignCenter)

        layout.addWidget(footer)

    # --------------------------------------------------------

    def refresh_status(self):

        self.lbl_usb.setText(
            STATUS.usb
        )

        self.lbl_private.setText(
            STATUS.private_key
        )

        self.lbl_public.setText(
            STATUS.public_key
        )

        self.lbl_agent.setText(
            STATUS.agent
        )

    # --------------------------------------------------------
    # Button Actions
    # --------------------------------------------------------

    def health_check(self):

        HEALTH.run()

        self.refresh_status()

        Utils.info(
            self,
            "Health Check",
            "System scan complete."
        )

    # --------------------------------------------------------

    def start_session(self):

        SSH_SESSION.start()

    # --------------------------------------------------------

    def install_local(self):

        LOCAL_INSTALLER.install()

    # --------------------------------------------------------

    def install_remote(self):

        Utils.info(
            self,
            "Remote Installation",
            "Wizard coming soon."
        )

    # --------------------------------------------------------

    def copy_public_key(self):

        CLIPBOARD.copy_public_key()

    # --------------------------------------------------------

    def show_recovery(self):

        RECOVERY_GUIDE.show(self)

    # --------------------------------------------------------

    def settings(self):

        Utils.info(
            self,
            "Settings",
            "Settings dialog coming soon."
        )

# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

def main():

    app = QApplication(sys.argv)

    app.setApplicationName(APP_NAME)

    app.setApplicationVersion(APP_VERSION)

    Theme.apply(app)

    window = MainWindow()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()
