"""
Health check endpoint for the RAG API.
"""
from fastapi import APIRouter
import time
from typing import Dict, Any

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint to verify the API is running and responsive.

    Returns:
        Dict containing health status information
    """
    return {
        "status": "healthy",
        "message": "RAG Query API is running",
        "timestamp": time.time(),
        "services": {
            "api": "operational",
            "agent_connection": "pending",  # Would check actual agent connection in a real implementation
        }
    }

@router.get("/ready")
async def readiness_check() -> Dict[str, Any]:
    """
    Readiness check endpoint to verify the API is ready to serve requests.

    Returns:
        Dict containing readiness status information
    """
    # In a real implementation, this would check if all dependencies are ready
    return {
        "status": "ready",
        "message": "RAG Query API is ready to serve requests",
        "timestamp": time.time()
    }