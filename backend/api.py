#!/usr/bin/env python3
"""
FastAPI Server for RAG Chatbot Integration

This script creates a FastAPI server that exposes a query endpoint to connect
the frontend chatbot UI with the RAG agent. The backend handles API requests
from the frontend, forwards queries to the RAG agent, and returns responses
in JSON format.
"""

import os
import sys
import logging
import asyncio
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
import time
import json

# Add backend directory to path to import agent
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Import the RAG agent
try:
    from agent import GeminiAgent, AgentConfig
except ImportError as e:
    print(f"Error importing agent: {e}")
    print("Make sure you're running this from the backend directory and all dependencies are installed")
    sys.exit(1)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Pydantic models
class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=10000, description="The user's question or query text")
    metadata: Optional[dict] = Field(None, description="Additional context information (session_id, user_id, etc.)")

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

class QueryResponse(BaseModel):
    response: str = Field(..., description="The agent's answer to the query")
    sources: Optional[list] = Field(None, description="List of source documents used in the response")
    metadata: Optional[dict] = Field(None, description="Additional response metadata")
    timestamp: float = Field(..., description="When the response was generated")

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

class ErrorResponse(BaseModel):
    error_code: str = Field(..., description="Standardized error code")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[dict] = Field(None, description="Additional error details for debugging")
    timestamp: float = Field(..., description="When the error occurred")

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

# Global agent instance
agent_instance = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the RAG agent when the application starts"""
    global agent_instance
    try:
        logger.info("Initializing RAG agent...")
        config = AgentConfig()
        agent_instance = GeminiAgent(config)
        logger.info("RAG agent initialized successfully")
        yield
    except Exception as e:
        logger.error(f"Failed to initialize RAG agent: {e}")
        raise
    finally:
        logger.info("Shutting down RAG agent...")

# Create FastAPI app
app = FastAPI(
    title="RAG Query API",
    description="API for querying the RAG agent with document-based retrieval",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint to check if the API is running"""
    return {"message": "RAG Query API is running", "status": "ok"}

@app.post("/query",
          response_model=QueryResponse,
          responses={
              400: {"model": ErrorResponse},
              503: {"model": ErrorResponse},
              500: {"model": ErrorResponse}
          })
async def query_endpoint(request: QueryRequest):
    """
    Submit a query to the RAG agent

    Sends a user query to the RAG agent and returns the response with sources
    """
    start_time = time.time()
    logger.info(f"Received query: '{request.query[:50]}{'...' if len(request.query) > 50 else ''}'")

    try:
        # Validate the query
        if not request.query.strip():
            raise HTTPException(
                status_code=400,
                detail={
                    "error_code": "INVALID_QUERY",
                    "message": "Query cannot be empty",
                    "timestamp": time.time()
                }
            )

        # Check if agent is initialized
        if agent_instance is None:
            raise HTTPException(
                status_code=503,
                detail={
                    "error_code": "AGENT_UNINITIALIZED",
                    "message": "The RAG agent is not properly initialized",
                    "timestamp": time.time()
                }
            )

        # Process the query with the agent
        response_text = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: agent_instance.query(request.query)
        )

        # Prepare the response
        response = QueryResponse(
            response=response_text,
            sources=[],  # Sources would be populated if the agent provides them
            metadata=request.metadata or {},
            timestamp=time.time()
        )

        processing_time = time.time() - start_time
        logger.info(f"Query processed successfully in {processing_time:.2f}s")

        return response

    except HTTPException:
        # Re-raise HTTP exceptions as they are already properly formatted
        raise
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": "INTERNAL_ERROR",
                "message": f"An internal error occurred: {str(e)}",
                "timestamp": time.time()
            }
        )

@app.get("/health")
async def health_check():
    """Health check endpoint to verify the API is running and the agent is responsive"""
    try:
        if agent_instance is None:
            return {
                "status": "unhealthy",
                "details": "Agent not initialized",
                "timestamp": time.time()
            }

        # Perform a simple check to see if the agent is responsive
        # We could make a simple test query here if needed
        return {
            "status": "healthy",
            "details": "Agent is initialized and responsive",
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "details": f"Health check failed: {str(e)}",
            "timestamp": time.time()
        }

if __name__ == "__main__":
    import uvicorn

    # Get host and port from environment or use defaults
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))

    logger.info(f"Starting server on {host}:{port}")

    # Run the server
    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        reload=True,  # Enable auto-reload during development
        log_level="info"
    )