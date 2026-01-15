"""
Error handling utilities for consistent error responses across the API.
"""
from typing import Optional, Dict, Any
from ..models.error import ErrorResponse, create_error_response
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_query_error(error: Exception, error_code: str = "INTERNAL_ERROR") -> ErrorResponse:
    """
    Create a consistent error response for query-related errors.

    Args:
        error: The exception that occurred
        error_code: The error code to use (default: "INTERNAL_ERROR")

    Returns:
        ErrorResponse with appropriate error details
    """
    error_msg = str(error)
    logger.error(f"Query error: {error_code} - {error_msg}")

    return create_error_response(
        error_code=error_code,
        message=error_msg,
        details={
            "error_type": type(error).__name__,
            "timestamp": time.time()
        }
    )

def handle_validation_error(error: Exception) -> ErrorResponse:
    """
    Create a consistent error response for validation errors.

    Args:
        error: The validation exception that occurred

    Returns:
        ErrorResponse with appropriate validation error details
    """
    error_msg = f"Validation error: {str(error)}"
    logger.warning(f"Validation error: {error_msg}")

    return create_error_response(
        error_code="VALIDATION_ERROR",
        message=str(error),
        details={
            "error_type": type(error).__name__,
            "timestamp": time.time()
        }
    )

def handle_timeout_error(error: Exception) -> ErrorResponse:
    """
    Create a consistent error response for timeout errors.

    Args:
        error: The timeout exception that occurred

    Returns:
        ErrorResponse with appropriate timeout error details
    """
    error_msg = f"Request timeout: {str(error)}"
    logger.warning(f"Timeout error: {error_msg}")

    return create_error_response(
        error_code="REQUEST_TIMEOUT",
        message="The request timed out. Please try again.",
        details={
            "error_type": type(error).__name__,
            "timestamp": time.time()
        }
    )

def handle_agent_unavailable_error(error: Exception) -> ErrorResponse:
    """
    Create a consistent error response when the RAG agent is unavailable.

    Args:
        error: The exception that occurred

    Returns:
        ErrorResponse with appropriate agent unavailability details
    """
    error_msg = f"RAG agent unavailable: {str(error)}"
    logger.error(f"Agent unavailable: {error_msg}")

    return create_error_response(
        error_code="AGENT_UNAVAILABLE",
        message="The RAG agent is currently unavailable. Please try again later.",
        details={
            "error_type": type(error).__name__,
            "timestamp": time.time()
        }
    )

def handle_bad_request_error(message: str) -> ErrorResponse:
    """
    Create a consistent error response for bad request errors (HTTP 400).

    Args:
        message: The error message to include

    Returns:
        ErrorResponse with appropriate bad request details
    """
    logger.warning(f"Bad request: {message}")

    return create_error_response(
        error_code="BAD_REQUEST",
        message=message,
        details={
            "timestamp": time.time()
        }
    )

def log_error(error: Exception, context: str = ""):
    """
    Log an error with context.

    Args:
        error: The exception to log
        context: Additional context about where the error occurred
    """
    logger.error(f"Error in {context}: {str(error)} - Type: {type(error).__name__}")

def format_error_response(status_code: int, error: Exception) -> ErrorResponse:
    """
    Format an appropriate error response based on the status code and error.

    Args:
        status_code: The HTTP status code
        error: The exception that occurred

    Returns:
        ErrorResponse with appropriate error details
    """
    error_str = str(error)

    if status_code == 400:
        return handle_bad_request_error(error_str)
    elif status_code == 408 or "timeout" in error_str.lower():
        return handle_timeout_error(error)
    elif status_code == 503 or "unavailable" in error_str.lower():
        return handle_agent_unavailable_error(error)
    else:
        return handle_query_error(error)