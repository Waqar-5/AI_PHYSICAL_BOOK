"""
Query endpoint for the RAG API.
"""
from fastapi import APIRouter, HTTPException
import asyncio
import sys
import os

# Add backend directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.models.query import QueryRequest
from src.models.response import QueryResponse
from src.models.error import ErrorResponse
from src.services.agent_service import AgentService
from src.services.query_service import QueryService
from src.services.error_handler import handle_bad_request_error, handle_query_error, handle_timeout_error, handle_agent_unavailable_error

router = APIRouter()

# Initialize services
agent_service = AgentService()
query_service = QueryService(agent_service)

@router.post("/query", response_model=QueryResponse)
async def query_endpoint(query_request: QueryRequest):
    """
    Submit a query to the RAG agent.

    Sends a user query to the RAG agent and returns the response with sources.
    """
    try:
        # Validate the query request using the model's validation
        query_request.validate_metadata()

        # Validate that query is not empty
        if not query_request.query or not query_request.query.strip():
            error_response = handle_bad_request_error("Query cannot be empty")
            raise HTTPException(status_code=400, detail=error_response.dict())

        # Process the query using the query service with retry logic
        response = await query_service.process_query_with_retry(query_request)

        # Validate the response before returning
        response.validate_response()

        return response

    except HTTPException:
        # Re-raise HTTP exceptions as they are already properly formatted
        raise
    except asyncio.TimeoutError as e:
        # Handle timeout errors specifically
        error_response = handle_timeout_error(e)
        raise HTTPException(status_code=408, detail=error_response.dict())
    except Exception as e:
        # Handle other errors including agent unavailability
        error_msg = str(e)
        if "unavailable" in error_msg.lower() or "timeout" in error_msg.lower():
            error_response = handle_agent_unavailable_error(e)
        else:
            error_response = handle_query_error(e)
        raise HTTPException(status_code=500, detail=error_response.dict())