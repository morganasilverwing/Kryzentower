"""
==========================================================
KryzenTower Theme
==========================================================
"""

# ---------------------------------------------------------
# Colors
# ---------------------------------------------------------

BACKGROUND = "#1E1E1E"

PANEL = "#2D2D30"

BUTTON = "#3C3C3C"

BUTTON_HOVER = "#505050"

BUTTON_PRESSED = "#2A82DA"

TEXT = "#FFFFFF"

TEXT_DISABLED = "#808080"

BORDER = "#555555"

SUCCESS = "#3FB950"

WARNING = "#D29922"

ERROR = "#F85149"

# ---------------------------------------------------------
# Fonts
# ---------------------------------------------------------

FONT_FAMILY = "DejaVu Sans"

FONT_SIZE = 10

TITLE_SIZE = 14

HEADER_SIZE = 12

# ---------------------------------------------------------
# Window
# ---------------------------------------------------------

BORDER_RADIUS = 6

BUTTON_HEIGHT = 34

BUTTON_WIDTH = 170

SPACING = 10

MARGIN = 12

# ---------------------------------------------------------
# Qt Stylesheet
# ---------------------------------------------------------

def stylesheet():

    return f"""

QWidget {{

    background-color: {BACKGROUND};

    color: {TEXT};

    font-family: "{FONT_FAMILY}";

    font-size: {FONT_SIZE}pt;

}}

QGroupBox {{

    border: 1px solid {BORDER};

    border-radius: {BORDER_RADIUS}px;

    margin-top: 10px;

    font-weight: bold;

}}

QGroupBox::title {{

    subcontrol-origin: margin;

    left: 10px;

    padding: 0 5px;

}}

QPushButton {{

    background-color: {BUTTON};

    border: 1px solid {BORDER};

    border-radius: {BORDER_RADIUS}px;

    min-height: {BUTTON_HEIGHT}px;

    min-width: {BUTTON_WIDTH}px;

}}

QPushButton:hover {{

    background-color: {BUTTON_HOVER};

}}

QPushButton:pressed {{

    background-color: {BUTTON_PRESSED};

}}

QLineEdit,
QTextEdit,
QPlainTextEdit,
QTreeWidget,
QListWidget {{

    border: 1px solid {BORDER};

    border-radius: {BORDER_RADIUS}px;

    padding: 4px;

}}

QStatusBar {{

    border-top: 1px solid {BORDER};

}}

"""


