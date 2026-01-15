"""
Main FastAPI application for the RAG query API.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .endpoints.query import router as query_router
from .endpoints.health import router as health_router

# Create FastAPI app with lifespan to initialize services
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services when the app starts"""
    # Initialize services at startup if needed
    print("RAG Query API starting up...")
    yield
    # Cleanup at shutdown if needed
    print("RAG Query API shutting down...")

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

# Include the query router
app.include_router(query_router, prefix="/api", tags=["query"])

# Include the health router
app.include_router(health_router, tags=["health"])

@app.get("/")
async def root():
    """Root endpoint to check if the API is running"""
    return {"message": "RAG Query API is running", "status": "ok"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}