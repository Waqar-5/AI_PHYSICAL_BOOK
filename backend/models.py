from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
import uuid

@dataclass
class DocumentChunk:
    """
    Represents a processed chunk of content from a URL
    """
    id: str
    url: str
    content: str
    embedding: List[float]
    chunk_index: int
    total_chunks: int
    created_at: datetime
    metadata: Dict

    def __post_init__(self):
        # Generate ID if not provided
        if not self.id:
            self.id = str(uuid.uuid4())

@dataclass
class ProcessingJob:
    """
    Represents a URL ingestion job in the system
    """
    id: str
    url: str
    status: str  # pending, processing, completed, failed
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    processed_chunks: int = 0
    total_chunks: int = 0
    metadata: Optional[Dict] = None

    def __post_init__(self):
        # Generate ID if not provided
        if not self.id:
            self.id = str(uuid.uuid4())

        # Initialize metadata if not provided
        if self.metadata is None:
            self.metadata = {}