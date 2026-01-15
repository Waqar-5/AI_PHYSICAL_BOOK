#!/usr/bin/env python3
"""
Google Gemini Agent with Retrieval-Augmented Capabilities

This script creates an AI agent that integrates with the existing RAG retrieval system
to answer questions using book content stored in Qdrant. The agent uses the Google
Generative AI SDK with a custom retrieval tool that queries Qdrant using the existing
retrieval pipeline logic.
"""

import os
import sys
import logging
from typing import Dict, Any, List, Optional
import json
import time

# Import required libraries
try:
    import google.generativeai as genai
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install required dependencies: pip install google-generativeai python-dotenv")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AgentConfig:
    """Configuration class to manage Google Gemini and Qdrant settings"""

    def __init__(self):
        """Initialize configuration from environment variables"""
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.cohere_api_key = os.getenv("COHERE_API_KEY")
        self.qdrant_collection_name = os.getenv("QDRANT_COLLECTION_NAME", "document_chunks")
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-pro")

        # Validate required configuration
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        if not self.qdrant_url:
            raise ValueError("QDRANT_URL environment variable is required")
        if not self.qdrant_api_key:
            raise ValueError("QDRANT_API_KEY environment variable is required")
        if not self.cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")

        logger.info("Configuration loaded successfully")


class RetrievalTool:
    """Retrieval tool that wraps existing RAGValidator functionality from backend/retrieve.py"""

    def __init__(self, config: AgentConfig):
        """Initialize the retrieval tool with configuration"""
        self.config = config

        # Import the RAGValidator from the existing retrieve.py
        try:
            from retrieve import RAGValidator
            self.validator = RAGValidator()
            logger.info("Retrieval tool initialized with existing RAGValidator functionality")
        except ImportError:
            logger.error("Could not import RAGValidator from retrieve")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize RAGValidator: {e}")
            raise

    def retrieve_content(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve content from Qdrant based on the query

        Args:
            query: The query string to search for
            top_k: Number of top results to return (default 5)

        Returns:
            List of retrieved content chunks with metadata
        """
        try:
            # Use the existing validation method from RAGValidator
            result = self.validator.validate_retrieval(query, top_k=top_k)

            # Check for errors in the result
            if 'error' in result:
                error_msg = result['error']
                logger.error(f"Retrieval error for query '{query}': {error_msg}")
                raise Exception(f"Retrieval failed: {error_msg}")

            retrieved_chunks = result.get('retrieved_chunks', [])

            logger.info(f"Retrieved {len(retrieved_chunks)} chunks for query: '{query[:50]}{'...' if len(query) > 50 else ''}'")
            return retrieved_chunks
        except Exception as e:
            logger.error(f"Failed to retrieve content for query '{query}': {e}")
            # Re-raise the exception to be handled by the caller
            raise

    def handle_qdrant_connection_issues(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Handle Qdrant connection issues with retries and fallbacks

        Args:
            query: The query string to search for
            top_k: Number of top results to return (default 5)

        Returns:
            List of retrieved content chunks with metadata
        """
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                result = self.validator.validate_retrieval(query, top_k=top_k)

                # Check for connection errors in the result
                if 'error' in result and 'connection' in result['error'].lower():
                    logger.warning(f"Connection issue detected, attempt {retry_count + 1}/{max_retries}")
                    retry_count += 1
                    time.sleep(2 ** retry_count)  # Exponential backoff
                    continue

                retrieved_chunks = result.get('retrieved_chunks', [])
                logger.info(f"Retrieved {len(retrieved_chunks)} chunks for query: '{query[:50]}{'...' if len(query) > 50 else ''}'")
                return retrieved_chunks
            except Exception as e:
                logger.error(f"Attempt {retry_count + 1} failed to retrieve content for query '{query}': {e}")
                retry_count += 1
                if retry_count >= max_retries:
                    logger.error(f"Failed to retrieve content after {max_retries} attempts")
                    raise
                time.sleep(2 ** retry_count)  # Exponential backoff

        # If we've exhausted retries, return an empty list as a fallback
        logger.warning("All retry attempts failed, returning empty results")
        return []


    def format_for_openai(self, chunks: List[Dict[str, Any]]) -> str:
        """
        Format the retrieved chunks for use with OpenAI agent

        Args:
            chunks: List of retrieved content chunks

        Returns:
            Formatted string containing the content for OpenAI
        """
        formatted_content = []
        for i, chunk in enumerate(chunks, 1):
            content = chunk.get('content', '')
            source_url = chunk.get('source_url', 'Unknown')
            score = chunk.get('score', 0.0)

            formatted_chunk = f"""
Chunk {i} (Relevance Score: {score:.3f}):
Source: {source_url}
Content: {content}

"""
            formatted_content.append(formatted_chunk)

        return "".join(formatted_content)


class GeminiClient:
    """Wrapper for Google Gemini client to manage API interactions"""

    def __init__(self, config: AgentConfig, retrieval_tool=None):
        """Initialize Gemini client with configuration"""
        self.config = config
        genai.configure(api_key=self.config.gemini_api_key)
        self.model = genai.GenerativeModel(self.config.gemini_model)
        self.retrieval_tool = retrieval_tool
        logger.info("Gemini client initialized successfully")

    def generate_content(self, prompt: str) -> str:
        """
        Generate content using the Gemini model

        Args:
            prompt: The input prompt for content generation

        Returns:
            Generated content as a string
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Failed to generate content: {e}")
            raise


class GeminiAgent:
    """Main AI Agent class that handles user queries and responds using retrieved content"""

    def __init__(self, config: AgentConfig):
        """Initialize the agent with configuration and required components"""
        self.config = config
        # Create retrieval tool for use in GeminiClient
        self.retrieval_tool = RetrievalTool(config)
        self.client = GeminiClient(config, retrieval_tool=self.retrieval_tool)

        logger.info("Gemini Agent initialized successfully with custom tools")

    def query(self, question: str, top_k: int = 5) -> str:
        """
        Process a query and return a response based on retrieved content

        Args:
            question: The question to answer
            top_k: Number of top results to retrieve (default 5)

        Returns:
            The agent's response to the question
        """
        try:
            # Retrieve relevant content from Qdrant
            retrieved_chunks = self.retrieval_tool.handle_qdrant_connection_issues(question, top_k)

            # Format the retrieved content for the prompt
            formatted_content = self.retrieval_tool.format_for_openai(retrieved_chunks)

            # Create a prompt that includes the question and retrieved content
            prompt = f"""
            You are a helpful AI assistant that answers questions using ONLY the provided retrieved content from book documents.
            - Use only the information provided in the retrieved content to answer questions
            - Do not make up or hallucinate information that is not in the provided content
            - If the answer is not in the provided content, clearly state that the information is not available in the provided documents
            - Provide accurate answers based on the retrieved content
            - Cite the source URLs when possible

            Retrieved content:
            {formatted_content}

            Question: {question}

            Answer:
            """

            # Generate response using Gemini
            response = self.client.generate_content(prompt)

            return response

        except Exception as e:
            logger.error(f"Error processing query '{question}': {e}")
            raise

    def query_with_context(self, question: str, top_k: int = 5) -> str:
        """
        Process a query with conversation context (for follow-up questions)

        Args:
            question: The question to answer
            top_k: Number of top results to retrieve (default 5)

        Returns:
            The agent's response to the question
        """
        try:
            # Build context from conversation history
            context = self._build_context_string()

            # Retrieve relevant content from Qdrant
            retrieved_chunks = self.retrieval_tool.handle_qdrant_connection_issues(question, top_k)

            # Format the retrieved content for the prompt
            formatted_content = self.retrieval_tool.format_for_openai(retrieved_chunks)

            # Create a prompt that includes context, retrieved content and the question
            prompt = f"""
            You are a helpful AI assistant that answers questions using ONLY the provided retrieved content from book documents.
            - Use only the information provided in the retrieved content to answer questions
            - Do not make up or hallucinate information that is not in the provided content
            - If the answer is not in the provided content, clearly state that the information is not available in the provided documents
            - Provide accurate answers based on the retrieved content
            - Cite the source URLs when possible

            Previous conversation context:
            {context}

            Retrieved content:
            {formatted_content}

            Question: {question}

            Answer:
            """

            # Generate response using Gemini
            response = self.client.generate_content(prompt)

            return response

        except Exception as e:
            logger.error(f"Error processing query with context '{question}': {e}")
            raise

    def _build_context_string(self, max_history: int = 3) -> str:
        """
        Build a context string from recent conversation history

        Args:
            max_history: Maximum number of previous exchanges to include

        Returns:
            Formatted context string
        """
        if not self.conversation_history:
            return "No previous conversation history."

        # Get the most recent exchanges
        recent_history = self.conversation_history[-max_history:]

        context_parts = []
        for i, exchange in enumerate(recent_history, 1):
            context_parts.append(f"Turn {i}:")
            context_parts.append(f"  User: {exchange['user']}")
            context_parts.append(f"  Assistant: {exchange['assistant']}")
            context_parts.append("")  # Empty line for readability

        return "\n".join(context_parts)

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """
        Get the current conversation history

        Returns:
            List of conversation exchanges
        """
        return self.conversation_history.copy()


def main():
    """Main function to demonstrate the agent functionality"""
    try:
        # Initialize configuration
        config = AgentConfig()

        # Initialize the agent
        agent = GeminiAgent(config)

        # Example query
        question = "What is artificial intelligence?"
        print(f"Asking: {question}")

        response = agent.query(question)
        print(f"Response: {response}")

    except Exception as e:
        logger.error(f"Error in main: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()