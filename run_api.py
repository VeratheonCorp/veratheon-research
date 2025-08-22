#!/usr/bin/env python3
"""
API server startup script for the Market Research Agent.
Run with: uv run python run_api.py
"""

import uvicorn
from src.api.main import app

if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",  # Changed to bind to all interfaces for Docker
        port=8000,
        reload=True,
        log_level="info"
    )