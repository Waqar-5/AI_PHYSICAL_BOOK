#!/usr/bin/env python3
"""
Environment variable verification script for OpenAI Agent
"""

import os
import sys

def verify_environment():
    """Verify that required environment variables are set"""
    required_vars = [
        # "OPENAI_API_KEY",
        "GEMINI_API_KEY",
        "QDRANT_URL",
        "QDRANT_API_KEY",
        "COHERE_API_KEY"
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"Missing required environment variables: {', '.join(missing_vars)}")
        print("\nPlease set these environment variables before running the agent:")
        print("You can create a .env file with:")
        print("GEMINI_API_KEY=your_gemini_api_key")
        print("QDRANT_URL=your_qdrant_url")
        print("QDRANT_API_KEY=your_qdrant_api_key")
        print("COHERE_API_KEY=your_cohere_api_key")
        return False

    print("All required environment variables are set!")
    return True

if __name__ == "__main__":
    verify_environment()