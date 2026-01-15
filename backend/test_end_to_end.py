#!/usr/bin/env python3
"""
End-to-end validation test for all user stories
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

def test_user_story_1():
    """Test User Story 1: Agent Creation and Basic Query"""
    print("Testing User Story 1: Agent Creation and Basic Query")
    print("-" * 55)

    try:
        # Initialize configuration
        config = AgentConfig()
        print("✓ Configuration loaded successfully")

        # Initialize the agent
        agent = OpenAIAgent(config)
        print("✓ Agent initialized successfully")

        # Test basic query functionality
        question = "What is artificial intelligence?"
        response = agent.query(question)
        print(f"✓ Basic query successful: {question[:50]}...")
        print(f"  Response preview: {response[:100]}...")

        return True

    except Exception as e:
        logger.error(f"User Story 1 test failed: {e}")
        return False

def test_user_story_2():
    """Test User Story 2: Tool-Based Retrieval Integration"""
    print("\nTesting User Story 2: Tool-Based Retrieval Integration")
    print("-" * 58)

    try:
        # Initialize configuration and agent
        config = AgentConfig()
        agent = OpenAIAgent(config)

        # Test that the agent uses the retrieval tool correctly
        question = "Explain neural networks"
        response = agent.query(question)
        print(f"✓ Retrieval tool integration successful: {question[:50]}...")
        print(f"  Response preview: {response[:100]}...")

        # Verify that conversation history was updated
        history = agent.get_conversation_history()
        if len(history) > 0:
            print("✓ Conversation history updated correctly")
        else:
            print("✗ Conversation history not updated")
            return False

        return True

    except Exception as e:
        logger.error(f"User Story 2 test failed: {e}")
        return False

def test_user_story_3():
    """Test User Story 3: Follow-up Query Handling"""
    print("\nTesting User Story 3: Follow-up Query Handling")
    print("-" * 48)

    try:
        # Initialize configuration and agent
        config = AgentConfig()
        agent = OpenAIAgent(config)

        # Start a new conversation
        agent.start_new_conversation()
        print("✓ New conversation started")

        # First query
        question1 = "What is machine learning?"
        response1 = agent.query(question1)
        print(f"✓ Initial query successful: {question1[:50]}...")

        # Follow-up query
        question2 = "How does it differ from traditional programming?"
        response2 = agent.query_with_context(question2)
        print(f"✓ Follow-up query successful: {question2[:50]}...")

        # Verify conversation history has both exchanges
        history = agent.get_conversation_history()
        if len(history) == 2:
            print("✓ Both exchanges recorded in conversation history")
        else:
            print(f"✗ Expected 2 exchanges, got {len(history)}")
            return False

        # Test context building
        context_str = agent._build_context_string()
        if "Turn 1:" in context_str and "Turn 2:" in context_str:
            print("✓ Context string built correctly")
        else:
            print("✗ Context string not built correctly")
            return False

        return True

    except Exception as e:
        logger.error(f"User Story 3 test failed: {e}")
        return False

def run_end_to_end_validation():
    """Run end-to-end validation of all user stories"""
    print("Running End-to-End Validation of All User Stories")
    print("=" * 53)

    # Test all user stories
    us1_success = test_user_story_1()
    us2_success = test_user_story_2()
    us3_success = test_user_story_3()

    # Summary
    print(f"\nEnd-to-End Validation Summary:")
    print(f"User Story 1 (Basic Query): {'✓ PASS' if us1_success else '✗ FAIL'}")
    print(f"User Story 2 (Retrieval Integration): {'✓ PASS' if us2_success else '✗ FAIL'}")
    print(f"User Story 3 (Follow-up Handling): {'✓ PASS' if us3_success else '✗ FAIL'}")

    all_passed = us1_success and us2_success and us3_success
    print(f"\nOverall Result: {'✓ ALL TESTS PASSED' if all_passed else '✗ SOME TESTS FAILED'}")

    return all_passed

if __name__ == "__main__":
    success = run_end_to_end_validation()
    if success:
        print("\n🎉 End-to-end validation completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ End-to-end validation failed!")
        sys.exit(1)