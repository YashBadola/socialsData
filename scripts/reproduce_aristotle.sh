#!/bin/bash
set -e

# Setup environment
export PYTHONPATH=.

echo "1. Adding personality structure..."
python -m socials_data.cli add aristotle

echo "2. Downloading raw data..."
python scripts/download_aristotle.py

echo "3. Cleaning raw data..."
python scripts/clean_aristotle.py

echo "4. Processing data..."
python -m socials_data.cli process aristotle --skip-qa

echo "5. Verifying..."
python -m pytest tests/test_aristotle.py

echo "Done!"
