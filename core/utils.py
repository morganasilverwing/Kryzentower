"""
==========================================================
KryzenTower Utilities
==========================================================
"""

import platform

import subprocess

from pathlib import Path

from datetime import datetime

from core.logger import Logger

# ---------------------------------------------------------
# Operating System
# ---------------------------------------------------------

def is_linux():

    return platform.system() == "Linux"


def is_windows():

    return platform.system() == "Windows"

# ---------------------------------------------------------
# Run Command
# ---------------------------------------------------------

def run_command(

    command,

    check=False

):

    try:

        result = subprocess.run(

            command,

            capture_output=True,

            text=True,

            check=check

        )

        return {

            "success": True,

            "stdout": result.stdout,

            "stderr": result.stderr,

            "returncode": result.returncode

        }

    except Exception as exc:

        Logger.error(str(exc))

        return {

            "success": False,

            "stdout": "",

            "stderr": str(exc),

            "returncode": -1

        }

# ---------------------------------------------------------
# Create Directory
# ---------------------------------------------------------

def ensure_directory(

    directory

):

    Path(directory).mkdir(

        parents=True,

        exist_ok=True

    )

    return Path(directory)

# ---------------------------------------------------------
# Read Text File
# ---------------------------------------------------------

def read_text_file(path):

    path = Path(path)

    try:

        return path.read_text(

            encoding="utf-8",

            errors="replace"

        )

    except Exception as exc:

        Logger.error(

            f"Cannot read {path}: {exc}"

        )

        return ""

# ---------------------------------------------------------
# Write Text File
# ---------------------------------------------------------

def write_text_file(

    path,

    text

):

    path = Path(path)

    try:

        path.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        path.write_text(

            text,

            encoding="utf-8"

        )

        return True

    except Exception as exc:

        Logger.error(

            f"Cannot write {path}: {exc}"

        )

        return False

# ---------------------------------------------------------
# File Size
# ---------------------------------------------------------

def format_size(size):

    units = [

        "B",

        "KB",

        "MB",

        "GB",

        "TB"

    ]

    value = float(size)

    for unit in units:

        if value < 1024:

            return f"{value:.1f} {unit}"

        value /= 1024

    return f"{value:.1f} PB"

# ---------------------------------------------------------
# Date Formatting
# ---------------------------------------------------------

def format_timestamp(timestamp):

    return datetime.fromtimestamp(

        timestamp

    ).strftime(

        "%Y-%m-%d %H:%M:%S"

    )

# ---------------------------------------------------------
# File Exists
# ---------------------------------------------------------

def file_exists(path):

    return Path(path).exists()

# ---------------------------------------------------------
# Open Directory
# ---------------------------------------------------------

def open_directory(path):

    path = Path(path)

    if not path.exists():

        Logger.warning(

            f"{path} does not exist."

        )

        return

    if is_linux():

        run_command(

            ["xdg-open", str(path)]

        )

    elif is_windows():

        run_command(

            ["explorer", str(path)]
        )

# ---------------------------------------------------------
# Open File
# ---------------------------------------------------------

def open_file(path):

    path = Path(path)

    if not path.exists():

        Logger.warning(

            f"{path} does not exist."

        )

        return

    if is_linux():

        run_command(

            ["xdg-open", str(path)]

        )

    elif is_windows():

        run_command(

            ["start", str(path)]

        )


