# KryzenTower

Portable SSH Key Backup & Restore for Linux

## Features

- Scan local SSH keys
- Detect USB devices automatically
- Backup selected SSH keys
- Optional named backup folders
- Restore individual keys
- Restore complete backup folders
- Multi-selection support
- Portable USB structure
- No configuration required

## Requirements

- Python 3.11+
- PyQt6

## Installation

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Run

python kryzentower.py

## USB Structure

KryzenTower/
└── SSH/

Example:

KryzenTower/
└── SSH/
    ├── Work Laptop/
    ├── Raspberry Pi/
    └── id_ed25519

## Current Status

Alpha

Linux only
