#!/usr/bin/env python3
"""
Test script to verify the Google Gemini Agent functionality
"""
import os
import sys
import logging

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import AgentConfig, GeminiAgent

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_gemini_agent():
    """Test the Gemini agent functionality"""
    try:
        # Initialize configuration
        logger.info("Initializing agent configuration...")
        config = AgentConfig()

        # Initialize the agent
        logger.info("Initializing Gemini agent...")
        agent = GeminiAgent(config)

        # Test query
        test_question = "What is artificial intelligence?"
        logger.info(f"Testing with query: '{test_question}'")

        response = agent.query(test_question)
        logger.info(f"Response received: {response[:200]}...")  # Print first 200 chars

        print(f"Query: {test_question}")
        print(f"Response: {response}")

        return True

    except Exception as e:
        logger.error(f"Error testing Gemini agent: {e}")
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = test_gemini_agent()
    if success:
        print("\n✓ Gemini agent test completed successfully!")
    else:
        print("\n✗ Gemini agent test failed!")
        sys.exit(1)