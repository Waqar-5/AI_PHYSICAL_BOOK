#!/usr/bin/env python3
"""
Server runner for the RAG Chatbot API
"""

import os
import sys
import logging

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api import app  # Import the FastAPI app directly

if __name__ == "__main__":
    import uvicorn

    # Get host and port from environment or use defaults
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info(f"Starting server on {host}:{port}")

    # Run the server
    uvicorn.run(
        "server:app",  # Use the app from this module
        host=host,
        port=port,
        reload=True,  # Enable auto-reload during development
        log_level="info"
    )