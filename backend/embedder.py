import cohere
from typing import List
from config import COHERE_API_KEY, COHERE_MODEL

class Embedder:
    """
    Creates vector embeddings using Cohere
    """

    def __init__(self):
        if not COHERE_API_KEY:
            raise ValueError("COHERE_API_KEY environment variable is required")

        self.client = cohere.Client(api_key=COHERE_API_KEY)
        self.model = COHERE_MODEL  # Use the configured model

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for text

        Args:
            text: Input text to embed

        Returns:
            Embedding vector as list of floats
        """
        try:
            # Try to call embed with input_type as a parameter (for newer versions)
            response = self.client.embed(
                texts=[text],
                model=self.model,
                input_type="search_document"
            )
            return response.embeddings[0]
        except Exception as e:
            # If that fails, try without input_type
            try:
                response = self.client.embed(
                    texts=[text],
                    model=self.model
                )
                return response.embeddings[0]
            except Exception as e2:
                raise e

    def batch_generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts efficiently

        Args:
            texts: List of input texts

        Returns:
            List of embedding vectors
        """
        if not texts:
            return []

        try:
            # Try to call embed with input_type as a parameter (for newer versions)
            response = self.client.embed(
                texts=texts,
                model=self.model,
                input_type="search_document"
            )
            return response.embeddings
        except Exception as e:
            # If that fails, try without input_type
            try:
                response = self.client.embed(
                    texts=texts,
                    model=self.model
                )
                return response.embeddings
            except Exception as e2:
                raise e

    def validate_embedding(self, embedding: List[float]) -> bool:
        """
        Validate that embedding has valid dimensions

        Args:
            embedding: Embedding vector to validate

        Returns:
            True if embedding is valid, False otherwise
        """
        # Check if embedding is a valid list of floats with reasonable length
        return len(embedding) > 0 and all(isinstance(val, (int, float)) for val in embedding)