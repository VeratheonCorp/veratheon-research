#!/bin/bash
# Delete all __init__.py files
find ./src -type f -name '__init__.py' -delete

# Delete all __pycache__ directories and their contents
find ./src -type d -name '__pycache__' -exec rm -rf {} +