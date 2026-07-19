"""
==========================================================
KryzenTower Configuration
==========================================================
"""

from pathlib import Path

# ---------------------------------------------------------
# Application
# ---------------------------------------------------------

APP_NAME = "KryzenTower"

VERSION = "1.0 Alpha"

AUTHOR = "Zentoryon Empire"

# ---------------------------------------------------------
# Window
# ---------------------------------------------------------

WINDOW_WIDTH = 1100

WINDOW_HEIGHT = 750

MIN_WINDOW_WIDTH = 900

MIN_WINDOW_HEIGHT = 600

# ---------------------------------------------------------
# Refresh
# ---------------------------------------------------------

REFRESH_INTERVAL = 3000

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = PROJECT_DIR / "logs"

VAULT_DIR = PROJECT_DIR / "vault"

BACKUP_DIR = PROJECT_DIR / "backups"

RESOURCE_DIR = PROJECT_DIR / "resources"

# ---------------------------------------------------------
# Directories
# ---------------------------------------------------------

DIRECTORIES = [

    LOG_DIR,

    VAULT_DIR,

    BACKUP_DIR,

    RESOURCE_DIR,

]
