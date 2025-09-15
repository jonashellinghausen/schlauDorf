#!/usr/bin/env bash
set -e

# Optional system dependencies using apt
if command -v apt-get >/dev/null 2>&1; then
  echo "Installing system packages..."
  PKG_CMD="apt-get"
  if command -v sudo >/dev/null 2>&1 && [ "$(id -u)" -ne 0 ]; then
    PKG_CMD="sudo apt-get"
  fi
  $PKG_CMD update
  $PKG_CMD install -y python3 python3-venv python3-dev build-essential libpq-dev libgdal-dev
fi

# Python virtual environment and dependencies
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Environment setup complete. Activate with: source venv/bin/activate"
