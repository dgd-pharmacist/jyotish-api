#!/usr/bin/env bash

# Exit on error
set -euo pipefail

# Install system dependencies needed for swisseph
# Render's default Python runtime includes apt-get, but we don't need sudo
# We install build-essential which provides gcc, and python3-dev
apt-get update -y
apt-get install -y build-essential python3-dev

# Install Python dependencies from requirements.txt
pip install -r requirements.txt
