from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Optional
from config import QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME
import uuid
from datetime import datetime

class StorageManager:
    """
    Interfaces with Qdrant Cloud for vector storage
    """

    def __init__(self):
        if not QDRANT_URL:
            raise ValueError("QDRANT_URL environment variable is required")

        # Initialize Qdrant client
        if QDRANT_API_KEY:
            self.client = QdrantClient(
                url=QDRANT_URL,
                api_key=QDRANT_API_KEY
            )
        else:
            # For local or cloud without API key
            self.client = QdrantClient(url=QDRANT_URL)

        # Ensure collection exists
        self._ensure_collection()

    def _ensure_collection(self):
        """
        Ensure the document_chunks collection exists with proper configuration
        """
        try:
            # Check if collection exists
            self.client.get_collection(QDRANT_COLLECTION_NAME)
        except:
            # Create collection with 1024-dimensional vectors for Cohere embeddings
            self.client.create_collection(
                collection_name=QDRANT_COLLECTION_NAME,
                vectors_config=models.VectorParams(
                    size=1024,  # For Cohere embed-english-v3.0
                    distance=models.Distance.COSINE
                )
            )

            # Create payload index for URL for efficient lookups
            self.client.create_payload_index(
                collection_name=QDRANT_COLLECTION_NAME,
                field_name="url",
                field_schema=models.PayloadSchemaType.KEYWORD
            )

            # Create payload index for source domain
            self.client.create_payload_index(
                collection_name=QDRANT_COLLECTION_NAME,
                field_name="metadata.source_domain",
                field_schema=models.PayloadSchemaType.KEYWORD
            )

    def store_chunk(self, chunk_data: Dict) -> str:
        """
        Store a document chunk in Qdrant

        Args:
            chunk_data: Dictionary containing chunk information

        Returns:
            ID of the stored chunk
        """
        chunk_id = str(uuid.uuid4())

        # Prepare the point for Qdrant
        point = models.PointStruct(
            id=chunk_id,
            vector=chunk_data['embedding'],
            payload={
                "url": chunk_data['url'],
                "content": chunk_data['content'],
                "chunk_index": chunk_data['chunk_index'],
                "total_chunks": chunk_data['total_chunks'],
                "created_at": chunk_data.get('created_at', datetime.now().isoformat()),
                "metadata": chunk_data.get('metadata', {})
            }
        )

        # Store the point
        self.client.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            points=[point]
        )

        return chunk_id

    def search_similar(self, query_embedding: List[float], limit: int = 10, filters: Dict = None) -> List[Dict]:
        """
        Search for similar chunks using vector similarity

        Args:
            query_embedding: Embedding vector to search for
            limit: Maximum number of results
            filters: Optional filters to apply

        Returns:
            List of similar chunks with similarity scores
        """
        # Prepare filters if provided
        qdrant_filters = None
        if filters:
            filter_conditions = []
            for key, value in filters.items():
                if key == "url":
                    filter_conditions.append(
                        models.FieldCondition(
                            key="url",
                            match=models.MatchValue(value=value)
                        )
                    )
                elif key == "source_domain":
                    filter_conditions.append(
                        models.FieldCondition(
                            key="metadata.source_domain",
                            match=models.MatchValue(value=value)
                        )
                    )
            if filter_conditions:
                qdrant_filters = models.Filter(must=filter_conditions)

        # Perform search
        results = self.client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=query_embedding,
            query_filter=qdrant_filters,
            limit=limit
        )

        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": result.id,
                "url": result.payload.get("url"),
                "content": result.payload.get("content"),
                "chunk_index": result.payload.get("chunk_index"),
                "similarity_score": result.score,
                "metadata": result.payload.get("metadata", {})
            })

        return formatted_results

    def get_chunks_by_url(self, url: str) -> List[Dict]:
        """
        Retrieve all chunks for a specific URL

        Args:
            url: The URL to search for

        Returns:
            List of chunks from the specified URL
        """
        results = self.client.scroll(
            collection_name=QDRANT_COLLECTION_NAME,
            scroll_filter=models.Filter(
                must=[models.FieldCondition(
                    key="url",
                    match=models.MatchValue(value=url)
                )]
            ),
            limit=10000  # Set a reasonable limit
        )

        formatted_results = []
        for point in results[0]:  # Results are returned as (points, next_page_offset)
            formatted_results.append({
                "id": point.id,
                "url": point.payload.get("url"),
                "content": point.payload.get("content"),
                "chunk_index": point.payload.get("chunk_index"),
                "total_chunks": point.payload.get("total_chunks"),
                "created_at": point.payload.get("created_at"),
                "metadata": point.payload.get("metadata", {})
            })

        return formatted_results