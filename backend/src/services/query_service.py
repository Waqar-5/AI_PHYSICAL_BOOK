"""
Query service to handle query processing and interaction with the RAG agent.
"""
import asyncio
import time
from typing import Optional, Dict, Any
from ..models.query import QueryRequest
from ..models.response import QueryResponse, create_query_response
from ..models.error import ErrorResponse, create_error_response

class QueryService:
    """
    Service class to handle query processing and interaction with the RAG agent.
    """

    def __init__(self, agent_service):
        """
        Initialize the QueryService with an agent service.

        Args:
            agent_service: Service that handles interaction with the RAG agent
        """
        self.agent_service = agent_service

    async def process_query(self, query_request: QueryRequest) -> QueryResponse:
        """
        Process a query request and return a response from the RAG agent.

        Args:
            query_request: The query request containing the query text and optional metadata

        Returns:
            QueryResponse containing the agent's response
        """
        try:
            # Validate the query request
            query_request.validate_metadata()

            # Process the query with the agent service
            # Pass metadata to the agent service for potential use
            response_text = await self.agent_service.query_agent(
                query_request.query,
                query_request.metadata
            )

            # Create and return the response
            return create_query_response(
                response_text=response_text,
                metadata=query_request.metadata
            )

        except Exception as e:
            # Re-raise the exception to be handled by the caller
            raise e

    async def process_query_with_metadata(self, query_request: QueryRequest) -> QueryResponse:
        """
        Process a query request with explicit metadata handling.

        Args:
            query_request: The query request containing the query text and optional metadata

        Returns:
            QueryResponse containing the agent's response
        """
        try:
            # Validate the query request
            query_request.validate_metadata()

            # Process the query with the agent service using metadata-specific method
            response_text = await self.agent_service.query_agent_with_metadata(
                query_request.query,
                query_request.metadata
            )

            # Create and return the response
            return create_query_response(
                response_text=response_text,
                metadata=query_request.metadata
            )

        except Exception as e:
            # Re-raise the exception to be handled by the caller
            raise e

    def process_query_sync(self, query_request: QueryRequest) -> QueryResponse:
        """
        Synchronous version of process_query for compatibility with non-async contexts.

        Args:
            query_request: The query request containing the query text and optional metadata

        Returns:
            QueryResponse containing the agent's response
        """
        try:
            # Validate the query request
            query_request.validate_metadata()

            # For now, return a placeholder response
            return create_query_response(
                response_text="This is a placeholder response for synchronous processing.",
                metadata=query_request.metadata
            )
        except Exception as e:
            raise e

    async def process_query_with_timeout(self, query_request: QueryRequest, timeout: int = 30) -> QueryResponse:
        """
        Process a query with a specified timeout.

        Args:
            query_request: The query request containing the query text and optional metadata
            timeout: Timeout in seconds (default 30)

        Returns:
            QueryResponse containing the agent's response
        """
        try:
            # Use asyncio.wait_for to implement timeout
            result = await asyncio.wait_for(
                self.process_query(query_request),
                timeout=timeout
            )
            return result
        except asyncio.TimeoutError:
            raise Exception(f"Query processing timed out after {timeout} seconds")

    async def process_query_with_retry(self, query_request: QueryRequest, max_retries: int = 3,
                                      timeout: int = 30, retry_delay: int = 5) -> QueryResponse:
        """
        Process a query with retry logic for handling temporary failures.
        Implements the requirement: 30-second timeout with 3 retries at 5-second intervals.

        Args:
            query_request: The query request containing the query text and optional metadata
            max_retries: Maximum number of retry attempts (default 3, per requirements)
            timeout: Timeout for each attempt in seconds (default 30, per requirements)
            retry_delay: Delay between retries in seconds (default 5, per requirements)

        Returns:
            QueryResponse containing the agent's response
        """
        last_exception = None

        for attempt in range(max_retries):
            try:
                # Process with timeout
                result = await self.process_query_with_timeout(query_request, timeout)
                return result
            except Exception as e:
                last_exception = e
                if attempt < max_retries - 1:  # Don't sleep on the last attempt
                    await asyncio.sleep(retry_delay)  # Fixed delay of 5 seconds as per requirements
                continue

        # If we've exhausted retries, raise the last exception
        raise last_exception