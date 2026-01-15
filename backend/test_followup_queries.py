#!/usr/bin/env python3
"""
Test script for follow-up query functionality with multi-turn conversations
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

def test_followup_queries():
    """Test follow-up query functionality with multi-turn conversations"""
    try:
        # Initialize configuration
        config = AgentConfig()

        # Initialize the agent
        agent = OpenAIAgent(config)

        print("Testing follow-up query functionality with multi-turn conversations...")

        # Multi-turn conversation scenario
        conversation_flow = [
            {"question": "What is artificial intelligence?", "type": "initial"},
            {"question": "Can you elaborate on machine learning?", "type": "follow-up"},
            {"question": "How is it different from deep learning?", "type": "follow-up"},
            {"question": "What are some applications?", "type": "follow-up"}
        ]

        print("\nStarting multi-turn conversation:")

        for i, turn in enumerate(conversation_flow, 1):
            question = turn["question"]
            turn_type = turn["type"]

            print(f"\nTurn {i} ({turn_type}): {question}")

            try:
                if turn_type == "follow-up":
                    # Use query_with_context for follow-up questions
                    response = agent.query_with_context(question, top_k=3)
                else:
                    # Use regular query for initial questions
                    response = agent.query(question, top_k=3)

                print(f"Response: {response[:200]}...")  # Print first 200 chars of response
            except Exception as e:
                print(f"Error in turn {i} with question '{question}': {e}")
                continue

        # Check conversation history
        history = agent.get_conversation_history()
        print(f"\nConversation completed. Total exchanges: {len(history)}")

        # Display conversation summary
        print("\nConversation Summary:")
        for i, exchange in enumerate(history, 1):
            print(f"Exchange {i}:")
            print(f"  User: {exchange['user'][:100]}...")
            print(f"  Assistant: {exchange['assistant'][:100]}...")

        print("\nFollow-up query functionality test completed.")
        return True

    except Exception as e:
        logger.error(f"Error in test_followup_queries: {e}")
        print(f"Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_followup_queries()
    if success:
        print("\n✅ Follow-up query functionality test completed successfully")
    else:
        print("\n❌ Follow-up query functionality test failed")
        sys.exit(1)