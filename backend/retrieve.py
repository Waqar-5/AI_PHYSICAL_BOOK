#!/usr/bin/env python3
"""
RAG Retrieval Validation Script

This script connects to Qdrant to validate the RAG retrieval pipeline by:
1. Connecting to Qdrant and loading existing vector collections
2. Accepting a query and performing top-k similarity search
3. Validating results using returned text, metadata, and source URLs
"""

import os
import sys
import logging
from typing import List, Dict, Any, Optional
import time

# Import required libraries
try:
    import qdrant_client
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
    import cohere
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install required dependencies: pip install qdrant-client cohere python-dotenv")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class RAGValidator:
    """Class to handle RAG retrieval validation"""

    def __init__(self):
        """Initialize the validator with configuration from environment variables"""
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "document_chunks")
        self.cohere_api_key = os.getenv("COHERE_API_KEY")
        self.cohere_model = os.getenv("COHERE_MODEL", "small")  # Use the same model as the ingestion pipeline

        # Validate required configuration
        if not self.qdrant_url:
            raise ValueError("QDRANT_URL environment variable is required")
        if not self.qdrant_api_key:
            raise ValueError("QDRANT_API_KEY environment variable is required")
        if not self.cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")

        # Initialize Qdrant client
        try:
            self.qdrant_client = QdrantClient(
                url=self.qdrant_url,
                api_key=self.qdrant_api_key,
            )
            logger.info(f"Connected to Qdrant at {self.qdrant_url}")
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            raise

        # Initialize Cohere client
        try:
            self.cohere_client = cohere.Client(api_key=self.cohere_api_key)
            logger.info("Initialized Cohere client")
        except Exception as e:
            logger.error(f"Failed to initialize Cohere client: {e}")
            raise

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for the given text using Cohere"""
        try:
            # Try to call embed with input_type as a parameter (for newer versions)
            try:
                response = self.cohere_client.embed(
                    texts=[text],
                    model=self.cohere_model,  # Use the same model as ingestion
                    input_type="search_query"
                )
            except TypeError:
                # If that fails, try without input_type (for older versions)
                response = self.cohere_client.embed(
                    texts=[text],
                    model=self.cohere_model  # Use the same model as ingestion
                )
            return response.embeddings[0]
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise

    def query_collection(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Query the Qdrant collection with the given embedding"""
        try:
            start_time = time.time()

            # Perform the search in Qdrant
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                with_payload=True,
                with_vectors=False
            )

            retrieval_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            logger.info(f"Retrieved {len(search_results)} results in {retrieval_time:.2f}ms")

            # Format results
            formatted_results = []
            for result in search_results:
                formatted_result = {
                    'id': result.id,
                    'content': result.payload.get('content', ''),
                    'score': result.score,
                    'source_url': result.payload.get('url', ''),
                    'metadata': result.payload.get('metadata', {}),
                    'chunk_index': result.payload.get('chunk_index', 0),
                    'total_chunks': result.payload.get('total_chunks', 1)
                }
                formatted_results.append(formatted_result)

            return formatted_results
        except Exception as e:
            logger.error(f"Failed to query collection: {e}")
            raise

    def connect_to_qdrant(self) -> bool:
        """Test connection to Qdrant and validate collection exists"""
        try:
            # Try to get collection info to verify it exists
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            logger.info(f"Successfully connected to collection '{self.collection_name}'")
            logger.info(f"Collection vectors count: {collection_info.points_count}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to collection '{self.collection_name}': {e}")
            return False

    def load_vector_collection(self) -> bool:
        """Load and validate the vector collection exists"""
        try:
            # Verify collection exists and get its info
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            if collection_info:
                logger.info(f"Collection '{self.collection_name}' exists with {collection_info.points_count} vectors")
                return True
            return False
        except Exception as e:
            logger.error(f"Error loading collection '{self.collection_name}': {e}")
            return False

    def process_query_with_embeddings(self, query_text: str) -> List[float]:
        """Process query text and generate Cohere embeddings"""
        try:
            # Generate embedding for the query using Cohere
            query_embedding = self.generate_embedding(query_text)
            logger.info(f"Generated embedding for query: '{query_text[:50]}{'...' if len(query_text) > 50 else ''}'")
            return query_embedding
        except Exception as e:
            logger.error(f"Failed to process query with embeddings: {e}")
            raise

    def implement_top_k_retrieval(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Implement top-k retrieval based on similarity scores"""
        try:
            # Query the collection with the specified top_k
            retrieved_chunks = self.query_collection(query_embedding, top_k)

            # Sort by score if not already sorted by Qdrant (Qdrant should return sorted by default)
            sorted_chunks = sorted(retrieved_chunks, key=lambda x: x['score'], reverse=True)

            logger.info(f"Retrieved top-{top_k} chunks with scores: {[chunk['score'] for chunk in sorted_chunks[:top_k]]}")
            return sorted_chunks
        except Exception as e:
            logger.error(f"Top-k retrieval failed: {e}")
            raise

    def calculate_similarity_scores(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Calculate similarity scores for retrieved chunks"""
        try:
            # In Qdrant, similarity scores are already calculated during search
            # This method is more of a wrapper to ensure scores are properly retrieved
            retrieved_chunks = self.query_collection(query_embedding, top_k)

            # Ensure scores are properly formatted
            for chunk in retrieved_chunks:
                if 'score' not in chunk:
                    logger.warning(f"Chunk missing score: {chunk.get('id', 'unknown')}")

            return retrieved_chunks
        except Exception as e:
            logger.error(f"Similarity scoring failed: {e}")
            raise

    def add_configurable_k_parameter(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Add configurable k parameter for top-k retrieval"""
        try:
            # Process query with embeddings
            query_embedding = self.process_query_with_embeddings(query_text)

            # Implement top-k retrieval with configurable parameter
            retrieved_chunks = self.implement_top_k_retrieval(query_embedding, top_k)

            logger.info(f"Configurable top-{top_k} retrieval completed successfully")
            return retrieved_chunks
        except Exception as e:
            logger.error(f"Configurable k parameter retrieval failed: {e}")
            raise

    def basic_similarity_search(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Perform basic similarity search with the given query - updated with US2 functionality"""
        try:
            # Use the new configurable approach
            retrieved_chunks = self.add_configurable_k_parameter(query_text, top_k)
            return retrieved_chunks
        except Exception as e:
            logger.error(f"Basic similarity search failed: {e}")
            raise

    def validate_connection_and_retrieval(self, query_text: str, top_k: int = 5) -> Dict[str, Any]:
        """Validate that the RAG pipeline can connect and retrieve data"""
        try:
            # Validate connection to Qdrant
            connection_success = self.connect_to_qdrant()

            if not connection_success:
                return {
                    'query': query_text,
                    'retrieved_chunks': [],
                    'validation_results': {
                        'connection_success': False,
                        'metadata_match': False,
                        'content_relevance': False,
                        'overall_validation': False
                    },
                    'metrics': {
                        'retrieval_time_ms': 0,
                        'total_chunks': 0
                    },
                    'error': 'Failed to connect to Qdrant'
                }

            # Load vector collection
            collection_loaded = self.load_vector_collection()
            if not collection_loaded:
                return {
                    'query': query_text,
                    'retrieved_chunks': [],
                    'validation_results': {
                        'connection_success': True,  # We connected but collection issue
                        'metadata_match': False,
                        'content_relevance': False,
                        'overall_validation': False
                    },
                    'metrics': {
                        'retrieval_time_ms': 0,
                        'total_chunks': 0
                    },
                    'error': f'Failed to load collection {self.collection_name}'
                }

            # Perform basic similarity search
            start_time = time.time()
            retrieved_chunks = self.basic_similarity_search(query_text, top_k)
            retrieval_time_ms = (time.time() - start_time) * 1000

            # Validate retrieved chunks have correct metadata
            metadata_match = self.validate_chunk_metadata(retrieved_chunks)

            # Perform basic validation
            validation_results = {
                'connection_success': connection_success,
                'metadata_match': metadata_match,
                'content_relevance': len(retrieved_chunks) > 0,  # Basic relevance check
                'overall_validation': connection_success and len(retrieved_chunks) > 0 and metadata_match
            }

            # Calculate metrics
            metrics = {
                'retrieval_time_ms': retrieval_time_ms,
                'total_chunks': len(retrieved_chunks)
            }

            return {
                'query': query_text,
                'retrieved_chunks': retrieved_chunks,
                'validation_results': validation_results,
                'metrics': metrics
            }
        except Exception as e:
            logger.error(f"Connection and retrieval validation failed: {e}")
            return {
                'query': query_text,
                'retrieved_chunks': [],
                'validation_results': {
                    'connection_success': False,
                    'metadata_match': False,
                    'content_relevance': False,
                    'overall_validation': False
                },
                'metrics': {
                    'retrieval_time_ms': 0,
                    'total_chunks': 0
                },
                'error': str(e)
            }

    def implement_metadata_extraction(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Implement metadata extraction from retrieved chunks"""
        extracted_chunks = []
        for chunk in chunks:
            # Extract and validate metadata from each chunk
            extracted_chunk = {
                'id': chunk.get('id', ''),
                'content': chunk.get('content', ''),
                'score': chunk.get('score', 0.0),
                'source_url': chunk.get('source_url', ''),
                'metadata': chunk.get('metadata', {}),
                'chunk_index': chunk.get('chunk_index', 0),
                'total_chunks': chunk.get('total_chunks', 1)
            }

            # Additional metadata validation
            if 'metadata' in chunk and chunk['metadata']:
                # Validate common metadata fields
                for key, value in chunk['metadata'].items():
                    if key == 'created_at' and value:
                        # Validate timestamp format if present
                        pass  # Could add timestamp validation here
                    elif key == 'word_count' and isinstance(value, int):
                        # Validate word count is positive
                        if value < 0:
                            logger.warning(f"Invalid word count in chunk {chunk.get('id', 'unknown')}: {value}")

            extracted_chunks.append(extracted_chunk)

        logger.info(f"Extracted metadata from {len(extracted_chunks)} chunks")
        return extracted_chunks

    def create_source_url_validation(self, chunks: List[Dict[str, Any]]) -> bool:
        """Create source URL validation function"""
        all_valid = True
        for chunk in chunks:
            source_url = chunk.get('source_url', '')

            # Check if source_url is not empty
            if not source_url:
                logger.warning(f"Chunk {chunk.get('id', 'unknown')} has empty source URL")
                all_valid = False
                continue

            # Check if source_url has valid format
            if not source_url.startswith(('http://', 'https://')):
                logger.warning(f"Chunk {chunk.get('id', 'unknown')} has invalid URL format: {source_url}")
                all_valid = False
                continue

            # Additional URL validation could go here
            # For example, checking for valid domain format, etc.

        return all_valid

    def add_metadata_consistency_checking(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Add metadata consistency checking"""
        consistency_results = {
            'total_chunks': len(chunks),
            'valid_source_urls': 0,
            'valid_content': 0,
            'valid_ids': 0,
            'metadata_integrity': 0,
            'all_consistent': True
        }

        for chunk in chunks:
            # Check source URL validity
            if chunk.get('source_url') and chunk['source_url'].startswith(('http://', 'https://')):
                consistency_results['valid_source_urls'] += 1

            # Check content validity
            if chunk.get('content') and len(chunk['content'].strip()) > 0:
                consistency_results['valid_content'] += 1

            # Check ID validity
            if chunk.get('id') and chunk['id'].strip():
                consistency_results['valid_ids'] += 1

            # Check metadata integrity
            if 'metadata' in chunk and isinstance(chunk['metadata'], dict):
                consistency_results['metadata_integrity'] += 1

        # Overall consistency check
        consistency_results['all_consistent'] = (
            consistency_results['valid_source_urls'] == consistency_results['total_chunks'] and
            consistency_results['valid_content'] == consistency_results['total_chunks'] and
            consistency_results['valid_ids'] == consistency_results['total_chunks'] and
            consistency_results['metadata_integrity'] == consistency_results['total_chunks']
        )

        logger.info(f"Metadata consistency check: {consistency_results}")
        return consistency_results

    def create_comprehensive_validation_report(self, query_text: str, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create comprehensive validation report"""
        # Extract metadata properly
        extracted_chunks = self.implement_metadata_extraction(chunks)

        # Perform source URL validation
        source_url_valid = self.create_source_url_validation(extracted_chunks)

        # Perform metadata consistency checking
        consistency_check = self.add_metadata_consistency_checking(extracted_chunks)

        # Create detailed validation report
        validation_report = {
            'query': query_text,
            'validation_timestamp': time.time(),
            'total_chunks_analyzed': len(extracted_chunks),
            'source_url_validation': {
                'valid': source_url_valid,
                'message': 'All source URLs are valid' if source_url_valid else 'Some source URLs are invalid'
            },
            'metadata_consistency': consistency_check,
            'comprehensive_validation_passed': (
                source_url_valid and
                consistency_check['all_consistent'] and
                len(extracted_chunks) > 0
            ),
            'detailed_chunks': extracted_chunks
        }

        logger.info(f"Comprehensive validation report created for query: {query_text[:50]}...")
        return validation_report

    def validate_chunk_metadata(self, chunks: List[Dict[str, Any]]) -> bool:
        """Validate that retrieved chunks have proper metadata - enhanced version"""
        if not chunks:
            return True  # If no chunks, consider it valid

        for chunk in chunks:
            # Check that required fields exist
            if not chunk.get('source_url') or not chunk.get('content'):
                logger.warning(f"Chunk missing required metadata: {chunk.get('id', 'unknown')}")
                return False
            # Check that source_url is a valid URL format
            if not chunk['source_url'].startswith(('http://', 'https://')):
                logger.warning(f"Invalid URL format in chunk: {chunk['source_url']}")
                return False
        return True

    def add_comprehensive_error_handling(self, func, *args, **kwargs):
        """Add comprehensive error handling around function calls"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
            # Return a structured error response
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__
            }

    def add_performance_metrics(self, func, *args, **kwargs):
        """Add performance metrics around function calls"""
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            logger.info(f"{func.__name__} executed in {execution_time:.2f}ms")
            return result, execution_time
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            logger.error(f"{func.__name__} failed after {execution_time:.2f}ms: {str(e)}")
            raise

    def handle_edge_cases(self, query_text: str, top_k: int = 5) -> Dict[str, Any]:
        """Handle edge cases like empty queries, network errors, etc."""
        # Validate input parameters
        if not query_text or not query_text.strip():
            return {
                'query': query_text,
                'retrieved_chunks': [],
                'validation_results': {
                    'connection_success': False,
                    'metadata_match': False,
                    'content_relevance': False,
                    'overall_validation': False
                },
                'metrics': {
                    'retrieval_time_ms': 0,
                    'total_chunks': 0
                },
                'error': 'Query text cannot be empty'
            }

        # Validate top_k parameter
        if top_k <= 0:
            top_k = 5  # Default back to 5 if invalid
            logger.warning(f"Invalid top_k value {top_k}, defaulting to 5")

        if top_k > 100:  # Set a reasonable upper limit
            top_k = 100
            logger.warning(f"top_k value {top_k} is too high, limiting to 100")

        # Try to validate collection exists before proceeding
        try:
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            if collection_info.points_count == 0:
                logger.warning(f"Collection '{self.collection_name}' is empty")
        except Exception as e:
            logger.error(f"Could not access collection '{self.collection_name}': {e}")
            return {
                'query': query_text,
                'retrieved_chunks': [],
                'validation_results': {
                    'connection_success': False,
                    'metadata_match': False,
                    'content_relevance': False,
                    'overall_validation': False
                },
                'metrics': {
                    'retrieval_time_ms': 0,
                    'total_chunks': 0
                },
                'error': f'Could not access collection: {str(e)}'
            }

        # Call the main validation function
        return self.validate_connection_and_retrieval(query_text, top_k)

    def validate_retrieval(self, query_text: str, top_k: int = 5) -> Dict[str, Any]:
        """Validate the retrieval pipeline for the given query - main entry point with comprehensive handling"""
        # Handle edge cases and validation
        return self.handle_edge_cases(query_text, top_k)


def main():
    """Main function to run the RAG retrieval validation"""
    start_time = time.time()

    if len(sys.argv) < 2:
        print("Usage: python retrieve.py <query> [--top_k K]")
        print("Example: python retrieve.py 'What is artificial intelligence?' --top_k 5")
        sys.exit(1)

    query_text = sys.argv[1]

    # Parse top_k parameter if provided
    top_k = 5  # default
    for i, arg in enumerate(sys.argv):
        if arg == "--top_k" and i + 1 < len(sys.argv):
            try:
                top_k = int(sys.argv[i + 1])
            except ValueError:
                logger.error(f"Invalid top_k value: {sys.argv[i + 1]}")
                sys.exit(1)

    try:
        logger.info(f"Starting RAG retrieval validation for query: '{query_text}' with top_k={top_k}")

        # Initialize the validation
        validator = RAGValidator()

        # Perform validation
        result = validator.validate_retrieval(query_text, top_k=top_k)

        # Calculate total execution time
        total_execution_time = (time.time() - start_time) * 1000

        # Print results
        print("\n=== RAG Retrieval Validation Results ===")
        print(f"Query: {query_text}")
        print(f"Top-{top_k} Results:")

        for i, chunk in enumerate(result['retrieved_chunks'], 1):
            print(f"\n{i}. Score: {chunk['score']:.4f}")
            print(f"   Source: {chunk['source_url']}")
            print(f"   Content Preview: {chunk['content'][:200]}...")
            print(f"   Metadata: {chunk['metadata']}")

        print(f"\nValidation Summary:")
        print(f"  - Connection Success: {result['validation_results']['connection_success']}")
        print(f"  - Metadata Match: {result['validation_results']['metadata_match']}")
        print(f"  - Retrieval Time: {result['metrics']['retrieval_time_ms']:.2f}ms")
        print(f"  - Total Chunks Retrieved: {result['metrics']['total_chunks']}")
        print(f"  - Overall Validation: {result['validation_results']['overall_validation']}")
        print(f"  - Total Execution Time: {total_execution_time:.2f}ms")

        if 'error' in result:
            print(f"  - Error: {result['error']}")
            logger.error(f"Validation completed with error: {result['error']}")

        logger.info(f"RAG retrieval validation completed in {total_execution_time:.2f}ms")

    except Exception as e:
        total_execution_time = (time.time() - start_time) * 1000
        logger.error(f"Failed to run validation after {total_execution_time:.2f}ms: {e}", exc_info=True)
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()