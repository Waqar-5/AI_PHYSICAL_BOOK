import asyncio
import cohere
from typing import List, Dict, Any
import numpy as np
import logging
from .config import Config


class CohereEmbedder:
    """
    Embedding generator using Cohere API
    """

    def __init__(self, config: Config):
        self.config = config
        self.client = cohere.Client(config.cohere_api_key)
        self.logger = logging.getLogger(__name__)

    def generate_embeddings(self, texts: List[str], batch_size: int = 96) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Cohere
        """
        all_embeddings = []

        # Process in batches to respect API limits
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]

            try:
                response = self.client.embed(
                    texts=batch,
                    model=self.config.embedding_model,
                    input_type="search_document"  # Using search_document for content to be searched
                )

                # Extract embeddings from response
                batch_embeddings = [embedding for embedding in response.embeddings]
                all_embeddings.extend(batch_embeddings)

                self.logger.info(f"Generated embeddings for batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")

            except Exception as e:
                self.logger.error(f"Error generating embeddings for batch {i//batch_size + 1}: {str(e)}")
                # Return zeros for failed embeddings to maintain alignment
                all_embeddings.extend([[0.0] * 1024 for _ in range(len(batch))])  # Assuming 1024-dim embeddings

        return all_embeddings

    def embed_chunks(self, chunks: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Generate embeddings for all text chunks
        """
        if not chunks:
            return []

        # Extract text content from chunks
        texts = [chunk["content"] for chunk in chunks]

        self.logger.info(f"Generating embeddings for {len(texts)} text chunks...")

        # Generate embeddings
        embeddings = self.generate_embeddings(texts)

        # Combine chunks with their embeddings
        chunk_embeddings = []
        for i, chunk in enumerate(chunks):
            chunk_with_embedding = chunk.copy()
            chunk_with_embedding["embedding"] = embeddings[i]
            chunk_with_embedding["text_length"] = len(chunk["content"])
            chunk_embeddings.append(chunk_with_embedding)

        self.logger.info(f"Successfully embedded {len(chunk_embeddings)} chunks")
        return chunk_embeddings

    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of embeddings from the model
        """
        # Test with a sample text to get the embedding dimension
        try:
            response = self.client.embed(
                texts=["test"],
                model=self.config.embedding_model,
                input_type="search_document"
            )
            if response.embeddings and len(response.embeddings) > 0:
                return len(response.embeddings[0])
        except Exception as e:
            self.logger.error(f"Error getting embedding dimension: {str(e)}")
            # Default to 1024 for English v3 model
            return 1024

        return 1024