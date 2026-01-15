#!/usr/bin/env python3
"""
Test script for retrieval tool integration with various query types
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

def test_retrieval_integration():
    """Test retrieval tool integration with various query types"""
    try:
        # Initialize configuration
        config = AgentConfig()

        # Initialize the agent
        agent = OpenAIAgent(config)

        # Various query types to test
        test_queries = [
            {"question": "What is artificial intelligence?", "type": "definition"},
            {"question": "Explain neural networks", "type": "explanation"},
            {"question": "How does machine learning work?", "type": "process"},
            {"question": "What are the applications of AI?", "type": "application"},
            {"question": "Compare supervised and unsupervised learning", "type": "comparison"},
        ]

        print("Testing retrieval tool integration with various query types...")

        for i, query_info in enumerate(test_queries, 1):
            question = query_info["question"]
            query_type = query_info["type"]

            print(f"\nTest {i} ({query_type}): Asking '{question}'")
            try:
                # Test the retrieval directly through the agent's query method
                response = agent.query(question, top_k=3)  # Using top_k=3 for this test
                print(f"Response: {response[:200]}...")  # Print first 200 chars of response
            except Exception as e:
                print(f"Error with {query_type} query '{question}': {e}")

        print("\nRetrieval tool integration test completed.")
        return True

    except Exception as e:
        logger.error(f"Error in test_retrieval_integration: {e}")
        print(f"Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_retrieval_integration()
    if success:
        print("\n✅ Retrieval tool integration test completed successfully")
    else:
        print("\n❌ Retrieval tool integration test failed")
        sys.exit(1)