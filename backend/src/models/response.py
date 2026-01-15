"""
Pydantic models for query responses.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import time

class Source(BaseModel):
    """Model for source documents used in the response."""
    title: Optional[str] = Field(None, description="Title of the source document")
    url: Optional[str] = Field(None, description="URL of the source document")
    content: Optional[str] = Field(None, description="Content of the source document chunk")

class QueryResponse(BaseModel):
    """
    Model for responses from the RAG agent.

    Based on data-model.md:
    - response (string, required): The agent's answer to the query
    - sources (array, optional): List of source documents/references used in the response
    - metadata (object, optional): Additional response metadata
    - timestamp (datetime, required): When the response was generated

    Validation rules from data-model.md:
    - response: Must be non-empty string
    - sources: If present, must be array of objects with required fields
    - timestamp: Must be in ISO 8601 format (as Unix timestamp)
    """
    response: str = Field(
        ...,
        min_length=1,
        description="The agent's answer to the query"
    )
    sources: Optional[List[Source]] = Field(
        None,
        description="List of source documents used in the response"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional response metadata"
    )
    timestamp: float = Field(
        ...,
        description="When the response was generated (Unix timestamp)"
    )

    def validate_response(self):
        """Validate response according to data-model.md rules."""
        if not self.response or not self.response.strip():
            raise ValueError("Response must be non-empty string")

        if self.sources is not None:
            # Validate sources if present
            for source in self.sources:
                if not isinstance(source, Source):
                    raise ValueError("Sources must be array of Source objects")

    class Config:
        schema_extra = {
            "example": {
                "response": "Artificial intelligence is a branch of computer science...",
                "sources": [
                    {
                        "title": "Introduction to AI",
                        "url": "https://example.com/ai-intro",
                        "content": "Artificial intelligence (AI) is intelligence demonstrated by machines..."
                    }
                ],
                "metadata": {},
                "timestamp": 1678886400.0
            }
        }

def create_query_response(response_text: str, sources: Optional[List[dict]] = None,
                         metadata: Optional[dict] = None) -> QueryResponse:
    """Create a QueryResponse with the current timestamp."""
    return QueryResponse(
        response=response_text,
        sources=sources,
        metadata=metadata or {},
        timestamp=time.time()
    )