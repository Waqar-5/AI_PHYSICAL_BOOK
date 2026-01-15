import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class Config:
    """Configuration class for the RAG ingestion system"""

    # Qdrant Configuration
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")
    qdrant_collection_name: str = os.getenv("QDRANT_COLLECTION_NAME", "book_embeddings")

    # Cohere Configuration
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "embed-english-v3.0")

    # Crawler Configuration
    base_url: str = os.getenv("BASE_URL", "https://ai-physical-book-tau.vercel.app")
    max_depth: int = int(os.getenv("MAX_DEPTH", "3"))
    request_delay: float = float(os.getenv("REQUEST_DELAY", "1"))
    user_agent: str = os.getenv("USER_AGENT", "BookCrawler/1.0")

    # Text Processing Configuration
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "512"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "50"))
    min_chunk_size: int = int(os.getenv("MIN_CHUNK_SIZE", "100"))

    # Logging Configuration
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    def __post_init__(self):
        """Validate required configuration values"""
        if not self.qdrant_url:
            raise ValueError("QDRANT_URL environment variable is required")
        if not self.qdrant_api_key:
            raise ValueError("QDRANT_API_KEY environment variable is required")
        if not self.cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")