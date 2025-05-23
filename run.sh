#!/bin/zsh

# Run the Python script with environment variables from .env
if [ -f .env ]; then
    # Load env vars from .env file and pass them to the Python script
    cd $(dirname "$0")  # Ensure we're in the project root directory
    PYTHONPATH=$(pwd) env $(cat .env | grep -v '^#' | xargs) uv run python main.py
else
    echo ".env file not found!"
    exit 1
fi