import uuid
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import logging
from .config import Config


class QdrantVectorStore:
    """
    Vector storage and retrieval using Qdrant
    """

    def __init__(self, config: Config):
        self.config = config
        self.client = QdrantClient(
            url=config.qdrant_url,
            api_key=config.qdrant_api_key,
            timeout=10
        )
        self.logger = logging.getLogger(__name__)

    def _create_collection_if_not_exists(self, vector_size: int):
        """Create the collection if it doesn't exist"""
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]

            if self.config.qdrant_collection_name not in collection_names:
                # Create collection with specified vector size
                self.client.create_collection(
                    collection_name=self.config.qdrant_collection_name,
                    vectors_config=VectorParams(
                        size=vector_size,
                        distance=Distance.COSINE
                    )
                )
                self.logger.info(f"Created collection: {self.config.qdrant_collection_name}")
            else:
                self.logger.info(f"Collection {self.config.qdrant_collection_name} already exists")
        except Exception as e:
            self.logger.error(f"Error creating collection: {str(e)}")
            raise

    def store_embeddings(self, chunk_embeddings: List[Dict[str, Any]], batch_size: int = 64):
        """
        Store embeddings in Qdrant with proper indexing
        """
        if not chunk_embeddings:
            self.logger.warning("No embeddings to store")
            return

        # Get vector size from first embedding
        vector_size = len(chunk_embeddings[0]["embedding"])
        self._create_collection_if_not_exists(vector_size)

        # Prepare points for insertion
        points = []
        for chunk in chunk_embeddings:
            # Create a unique ID for each chunk
            point_id = str(uuid.uuid4())

            # Prepare payload with metadata
            payload = {
                "content": chunk["content"],
                "url": chunk.get("url", ""),
                "title": chunk.get("title", ""),
                "text_length": chunk.get("text_length", len(chunk["content"])),
                "chunk_id": chunk["metadata"].get("chunk_id", 0),
                "total_chunks": chunk["metadata"].get("total_chunks", 1),
                "source_url": chunk["metadata"].get("source_url", ""),
            }

            # Add any additional metadata
            for key, value in chunk["metadata"].items():
                if key not in payload:
                    payload[key] = value

            point = PointStruct(
                id=point_id,
                vector=chunk["embedding"],
                payload=payload
            )
            points.append(point)

        # Upload in batches
        total_points = len(points)
        self.logger.info(f"Uploading {total_points} points to Qdrant...")

        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            try:
                self.client.upsert(
                    collection_name=self.config.qdrant_collection_name,
                    points=batch
                )
                self.logger.info(f"Uploaded batch {i//batch_size + 1}/{(len(points)-1)//batch_size + 1}")
            except Exception as e:
                self.logger.error(f"Error uploading batch {i//batch_size + 1}: {str(e)}")
                raise

        self.logger.info(f"Successfully stored {total_points} embeddings in Qdrant")

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in the collection
        """
        try:
            results = self.client.search(
                collection_name=self.config.qdrant_collection_name,
                query_vector=query_embedding,
                limit=top_k
            )

            search_results = []
            for result in results:
                search_results.append({
                    "id": result.id,
                    "content": result.payload.get("content", ""),
                    "url": result.payload.get("url", ""),
                    "title": result.payload.get("title", ""),
                    "score": result.score,
                    "metadata": result.payload
                })

            return search_results

        except Exception as e:
            self.logger.error(f"Error during search: {str(e)}")
            return []

    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the collection
        """
        try:
            collection_info = self.client.get_collection(self.config.qdrant_collection_name)
            return {
                "name": collection_info.config.params.vectors.size,
                "vector_size": collection_info.config.params.vectors.size,
                "distance": collection_info.config.params.vectors.distance,
                "point_count": collection_info.points_count
            }
        except Exception as e:
            self.logger.error(f"Error getting collection info: {str(e)}")
            return {}

    def delete_collection(self):
        """
        Delete the collection (useful for testing)
        """
        try:
            self.client.delete_collection(self.config.qdrant_collection_name)
            self.logger.info(f"Deleted collection: {self.config.qdrant_collection_name}")
        except Exception as e:
            self.logger.error(f"Error deleting collection: {str(e)}")