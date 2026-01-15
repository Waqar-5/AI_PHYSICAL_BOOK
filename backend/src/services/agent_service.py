"""
Agent service to wrap the existing RAG agent functionality.
"""
import sys
import os
from typing import Optional, Dict, Any
from ..agent import OpenAIAgent, AgentConfig

class AgentService:
    """
    Service class to wrap the existing RAG agent functionality.
    This provides a clean interface between the API and the underlying agent implementation.
    """

    def __init__(self):
        """
        Initialize the AgentService by creating an instance of the RAG agent.
        """
        try:
            # Initialize the agent configuration
            config = AgentConfig()
            # Create the RAG agent instance
            self.agent = OpenAIAgent(config)
        except Exception as e:
            # If we can't initialize the agent, we'll handle this gracefully
            print(f"Warning: Could not initialize RAG agent: {e}")
            self.agent = None

    async def query_agent(self, query: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Query the RAG agent with the given query text.

        Args:
            query: The query text to send to the agent
            metadata: Optional metadata to include with the query

        Returns:
            The agent's response as a string
        """
        if self.agent is None:
            # Return a placeholder response if the agent isn't available
            return f"Agent not available. Query: {query[:100]}{'...' if len(query) > 100 else ''}"

        try:
            # Use the agent's query method
            # The agent may not be async, so we'll call it synchronously
            # For now, we pass just the query; in a real implementation, we'd pass metadata too
            response = self.agent.query(query)
            return response
        except Exception as e:
            # Handle any errors that occur during agent querying
            raise Exception(f"Error querying agent: {str(e)}")

    def query_agent_with_metadata(self, query: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Query the RAG agent with the given query text and metadata.

        Args:
            query: The query text to send to the agent
            metadata: Optional metadata to include with the query

        Returns:
            The agent's response as a string
        """
        if self.agent is None:
            # Return a placeholder response if the agent isn't available
            return f"Agent not available. Query: {query[:100]}{'...' if len(query) > 100 else ''}"

        try:
            # For now, we'll just pass the query since the existing agent doesn't handle metadata
            # In a real implementation, we would modify the agent to use the metadata
            response = self.agent.query(query)
            return response
        except Exception as e:
            # Handle any errors that occur during agent querying
            raise Exception(f"Error querying agent: {str(e)}")

    def query_agent_sync(self, query: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Synchronous version of query_agent for compatibility.

        Args:
            query: The query text to send to the agent
            metadata: Optional metadata to include with the query

        Returns:
            The agent's response as a string
        """
        if self.agent is None:
            # Return a placeholder response if the agent isn't available
            return f"Agent not available. Query: {query[:100]}{'...' if len(query) > 100 else ''}"

        try:
            # Use the agent's query method
            response = self.agent.query(query)
            return response
        except Exception as e:
            # Handle any errors that occur during agent querying
            raise Exception(f"Error querying agent: {str(e)}")

    def start_new_conversation(self):
        """
        Start a new conversation with the agent.
        """
        if self.agent:
            self.agent.start_new_conversation()

    def get_conversation_history(self) -> list:
        """
        Get the current conversation history.

        Returns:
            List of conversation exchanges
        """
        if self.agent:
            return self.agent.get_conversation_history()
        return []

    def clear_conversation(self):
        """
        Clear the current conversation.
        """
        if self.agent:
            self.agent.clear_conversation()