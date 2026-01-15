"""
Pydantic models for query requests.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import time

class QueryRequest(BaseModel):
    """
    Model for query requests to the RAG agent.

    Based on data-model.md:
    - query (string, required): The user's question or query text
    - metadata (object, optional): Additional context information (session_id, user_id, etc.)
    - timestamp (datetime, optional): When the query was created (server-side)

    Validation rules from data-model.md:
    - query: Must be non-empty string (1-10000 characters)
    - metadata: If present, must be a valid JSON object with string keys
    - required fields: query field is mandatory
    """
    query: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="The user's question or query text"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional context information (session_id, user_id, etc.)"
    )

    def validate_metadata(self):
        """Validate metadata if present according to data-model.md rules."""
        if self.metadata is not None:
            # Check that all keys are strings
            for key in self.metadata.keys():
                if not isinstance(key, str):
                    raise ValueError("Metadata keys must be strings")

    class Config:
        schema_extra = {
            "example": {
                "query": "What is artificial intelligence?",
                "metadata": {
                    "session_id": "abc123",
                    "user_id": "user456"
                }
            }
        }

# Add timestamp as a computed field if needed during processing
def add_timestamp_to_query(query_request: QueryRequest) -> dict:
    """Add timestamp to query request for server-side tracking."""
    result = query_request.dict()
    result['timestamp'] = time.time()
    return result