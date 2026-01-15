#!/usr/bin/env python3
"""
Test script for basic query functionality of the OpenAI Agent
"""

import sys
import os
import logging

# Add the project root to the path so we can import agent
sys.path.insert(0, os.path.abspath('.'))

from backend.agent import OpenAIAgent, AgentConfig

# Set up logging for the test
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_basic_query():
    """Test basic query functionality with sample questions"""
    try:
        # Initialize configuration
        config = AgentConfig()

        # Initialize the agent
        agent = OpenAIAgent(config)

        # Sample questions to test
        test_questions = [
            "What is artificial intelligence?",
            "Explain machine learning concepts",
            "What are neural networks?"
        ]

        print("Testing basic query functionality...")

        for i, question in enumerate(test_questions, 1):
            print(f"\nTest {i}: Asking '{question}'")
            try:
                response = agent.query(question)
                print(f"Response: {response[:200]}...")  # Print first 200 chars of response
            except Exception as e:
                print(f"Error with question '{question}': {e}")

        print("\nBasic query functionality test completed.")
        return True

    except Exception as e:
        logger.error(f"Error in test_basic_query: {e}")
        print(f"Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_basic_query()
    if success:
        print("\n✅ Basic query functionality test completed successfully")
    else:
        print("\n❌ Basic query functionality test failed")
        sys.exit(1)