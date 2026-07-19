"""
==========================================================
KryzenTower Main Window
==========================================================
"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QPushButton
)

from core.config import (
    APP_NAME,
    VERSION,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
    MIN_WINDOW_HEIGHT
)

from core.theme import (
    SPACING,
    MARGIN
)

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.build_window()

        self.build_central_widget()

        self.build_header()

        self.build_status()

        self.build_actions()

        self.finish_layout()

    # --------------------------------------------------
    # Window
    # --------------------------------------------------

    def build_window(self):

        self.setWindowTitle(

            f"{APP_NAME} {VERSION}"

        )

        self.resize(

            WINDOW_WIDTH,

            WINDOW_HEIGHT

        )

        self.setMinimumSize(

            MIN_WINDOW_WIDTH,

            MIN_WINDOW_HEIGHT

        )

    # --------------------------------------------------
    # Central Widget
    # --------------------------------------------------

    def build_central_widget(self):

        self.central = QWidget()

        self.setCentralWidget(

            self.central

        )

        self.layout = QVBoxLayout()

        self.layout.setSpacing(

            SPACING

        )

        self.layout.setContentsMargins(

            MARGIN,

            MARGIN,

            MARGIN,

            MARGIN

        )

        self.central.setLayout(

            self.layout

        )

    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    def build_header(self):

        self.title = QLabel(

            APP_NAME

        )

        font = self.title.font()

        font.setBold(True)

        font.setPointSize(16)

        self.title.setFont(

            font

        )

        self.layout.addWidget(

            self.title

        )

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    def build_status(self):

        self.status_group = QGroupBox(

            "Status"

        )

        layout = QVBoxLayout()

        self.status_group.setLayout(

            layout

        )

        self.status_label = QLabel(

            "Ready"

        )

        layout.addWidget(

            self.status_label

        )

        self.layout.addWidget(

            self.status_group

        )

    # --------------------------------------------------
    # Actions
    # --------------------------------------------------

    def build_actions(self):

        self.actions_group = QGroupBox(

            "Actions"

        )

        layout = QVBoxLayout()

        self.actions_group.setLayout(

            layout

        )

        self.scan_button = QPushButton(

            "Scan USB"

        )

        self.backup_button = QPushButton(

            "Backup"

        )

        self.install_button = QPushButton(

            "Install"

        )

        self.loader_button = QPushButton(

            "SSH Loader"

        )

        self.settings_button = QPushButton(

            "Settings"

        )

        layout.addWidget(self.scan_button)

        layout.addWidget(self.backup_button)

        layout.addWidget(self.install_button)

        layout.addWidget(self.loader_button)

        layout.addWidget(self.settings_button)

        self.layout.addWidget(

            self.actions_group

        )

    # --------------------------------------------------
    # Finish Layout
    # --------------------------------------------------

    def finish_layout(self):

        self.layout.addStretch()
