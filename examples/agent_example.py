#!/usr/bin/env python3
"""
Example usage script for the OpenAI Agent with RAG capabilities

This script demonstrates how to use the agent for various types of queries
and shows the complete workflow for interacting with the RAG system.
"""

import sys
import os
import logging

# Add the project root to the path so we can import agent
sys.path.insert(0, os.path.abspath('.'))

from backend.agent import OpenAIAgent, AgentConfig

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def basic_query_example():
    """Example of basic query functionality"""
    print("=== Basic Query Example ===")

    try:
        # Initialize configuration and agent
        config = AgentConfig()
        agent = OpenAIAgent(config)

        # Ask a basic question
        question = "What is artificial intelligence?"
        print(f"Query: {question}")

        response = agent.query(question)
        print(f"Response: {response}")

        print("\nBasic query completed successfully!\n")

    except Exception as e:
        logger.error(f"Error in basic query example: {e}")

def follow_up_query_example():
    """Example of follow-up query functionality"""
    print("=== Follow-up Query Example ===")

    try:
        # Initialize configuration and agent
        config = AgentConfig()
        agent = OpenAIAgent(config)

        # Start a conversation
        agent.start_new_conversation()

        # First query
        question1 = "Explain machine learning concepts"
        print(f"Query 1: {question1}")
        response1 = agent.query(question1)
        print(f"Response 1: {response1[:200]}...")

        # Follow-up query
        question2 = "How does it differ from traditional programming?"
        print(f"\nFollow-up Query: {question2}")
        response2 = agent.query_with_context(question2)
        print(f"Follow-up Response: {response2[:200]}...")

        print("\nFollow-up query completed successfully!\n")

    except Exception as e:
        logger.error(f"Error in follow-up query example: {e}")

def multi_turn_conversation_example():
    """Example of multi-turn conversation with context"""
    print("=== Multi-turn Conversation Example ===")

    try:
        # Initialize configuration and agent
        config = AgentConfig()
        agent = OpenAIAgent(config)

        # Start a new conversation
        agent.start_new_conversation()

        conversation_flow = [
            "What are neural networks?",
            "How do they learn from data?",
            "What are the main types of neural networks?",
            "Give an example of their practical application"
        ]

        print("Starting multi-turn conversation...")

        for i, question in enumerate(conversation_flow, 1):
            print(f"\nTurn {i}: {question}")

            if i == 1:
                # First question in conversation
                response = agent.query(question)
            else:
                # Follow-up questions with context
                response = agent.query_with_context(question)

            print(f"Response: {response[:300]}...")

        # Show conversation history
        history = agent.get_conversation_history()
        print(f"\nCompleted {len(history)} exchanges in the conversation.")

        print("\nMulti-turn conversation completed successfully!\n")

    except Exception as e:
        logger.error(f"Error in multi-turn conversation example: {e}")

def error_handling_example():
    """Example showing error handling capabilities"""
    print("=== Error Handling Example ===")

    try:
        # Initialize configuration and agent
        config = AgentConfig()
        agent = OpenAIAgent(config)

        # Try a query that might not have results
        question = "What is the color of the invisible unicorn?"
        print(f"Querying for potentially non-existent information: {question}")

        response = agent.query(question)
        print(f"Response: {response}")

        print("\nError handling example completed!\n")

    except Exception as e:
        logger.error(f"Error in error handling example: {e}")

def main():
    """Run all examples to demonstrate the agent capabilities"""
    print("OpenAI Agent with RAG Capabilities - Examples")
    print("=" * 50)

    print("This script demonstrates various capabilities of the RAG agent.\n")

    # Run each example
    basic_query_example()
    follow_up_query_example()
    multi_turn_conversation_example()
    error_handling_example()

    print("All examples completed successfully!")
    print("\nFor more information on how to use the agent, check the agent.py source code.")
    print("Make sure to set the required environment variables before running.")

if __name__ == "__main__":
    main()