"""
==========================================================
KryzenTower Logger
==========================================================
"""

import logging

from pathlib import Path

from core.config import LOG_DIR, APP_NAME, VERSION

# ---------------------------------------------------------
# Create Log Directory
# ---------------------------------------------------------

LOG_DIR.mkdir(

    parents=True,

    exist_ok=True

)

LOG_FILE = LOG_DIR / "kryzentower.log"


class Logger:

    _initialized = False

    @classmethod
    def initialize(cls):

        if cls._initialized:

            return

        logging.basicConfig(

            level=logging.INFO,

            format="%(asctime)s | %(levelname)-8s | %(message)s",

            datefmt="%Y-%m-%d %H:%M:%S",

            handlers=[

                logging.FileHandler(

                    LOG_FILE,

                    encoding="utf-8"

                ),

                logging.StreamHandler()

            ]

        )

        cls._initialized = True

        cls.info("=" * 50)

        cls.info(f"{APP_NAME} {VERSION}")

        cls.info("Logger initialized")

        cls.info("=" * 50)

    @staticmethod
    def info(message):

        logging.info(message)

    @staticmethod
    def warning(message):

        logging.warning(message)

    @staticmethod
    def error(message):

        logging.error(message)

    @staticmethod
    def debug(message):

        logging.debug(message)
