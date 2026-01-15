"""
Pydantic models for error responses.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import time

class ErrorResponse(BaseModel):
    """
    Model for error responses from the API.

    Based on data-model.md:
    - error_code (string, required): Standardized error code
    - message (string, required): Human-readable error message
    - details (object, optional): Additional error details for debugging
    - timestamp (datetime, required): When the error occurred

    Validation rules from data-model.md:
    - error_code: Must be non-empty string
    - message: Must be non-empty string explaining the error
    - timestamp: Must be in ISO 8601 format (as Unix timestamp)
    """
    error_code: str = Field(
        ...,
        min_length=1,
        description="Standardized error code"
    )
    message: str = Field(
        ...,
        min_length=1,
        description="Human-readable error message"
    )
    details: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional error details for debugging"
    )
    timestamp: float = Field(
        ...,
        description="When the error occurred (Unix timestamp)"
    )

    def validate_error(self):
        """Validate error response according to data-model.md rules."""
        if not self.error_code or not self.error_code.strip():
            raise ValueError("Error code must be non-empty string")

        if not self.message or not self.message.strip():
            raise ValueError("Message must be non-empty string explaining the error")

    class Config:
        schema_extra = {
            "example": {
                "error_code": "AGENT_UNAVAILABLE",
                "message": "The RAG agent is currently unavailable",
                "details": {
                    "reason": "Connection timeout"
                },
                "timestamp": 1678886400.0
            }
        }

def create_error_response(error_code: str, message: str, details: Optional[dict] = None) -> ErrorResponse:
    """Create an ErrorResponse with the current timestamp."""
    return ErrorResponse(
        error_code=error_code,
        message=message,
        details=details,
        timestamp=time.time()
    )