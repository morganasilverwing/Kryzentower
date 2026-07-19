"""
==========================================================
KryzenTower
Main Entry Point
==========================================================
"""

import sys

from PyQt6.QtWidgets import QApplication

from core.config import APP_NAME, VERSION
from core.logger import Logger
from core.theme import stylesheet

from ui.main_window import MainWindow


def main():

    Logger.initialize()

    Logger.info("=" * 60)
    Logger.info(f"{APP_NAME} {VERSION}")
    Logger.info("Theme module loaded.")
    Logger.info("Utilities module loaded.")

    app = QApplication(sys.argv)

    app.setApplicationName(APP_NAME)

    app.setStyleSheet(stylesheet())

    Logger.info("Qt application initialized.")

    window = MainWindow()

    Logger.info("Main window created.")

    window.show()

    Logger.info("Main window shown.")

    Logger.info("Application startup completed.")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
