import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Cohere configuration
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
COHERE_MODEL = os.getenv("COHERE_MODEL", "small")  # Default to a model that works with current library

# Qdrant configuration
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "document_chunks")

# Processing configuration
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))
MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "1000000"))  # 1MB in bytes
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))  # 30 seconds
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))