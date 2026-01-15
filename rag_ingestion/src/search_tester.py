import cohere
from typing import List
from .config import Config
from .vector_store import QdrantVectorStore


class VectorSearchTester:
    """
    Test vector search functionality with sample queries
    """

    def __init__(self, config: Config):
        self.config = config
        self.vector_store = QdrantVectorStore(config)
        self.client = cohere.Client(config.cohere_api_key)

    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a search query
        """
        try:
            response = self.client.embed(
                texts=[query],
                model=self.config.embedding_model,
                input_type="search_query"  # Using search_query for search queries
            )
            return response.embeddings[0]
        except Exception as e:
            print(f"Error generating query embedding: {str(e)}")
            return []

    def test_search(self, queries: List[str], top_k: int = 3) -> bool:
        """
        Test search functionality with sample queries
        """
        print(f"Testing vector search with {len(queries)} sample queries...")

        all_tests_passed = True

        for i, query in enumerate(queries):
            print(f"\nTest {i+1}: Query: '{query}'")

            # Generate query embedding
            query_embedding = self.generate_query_embedding(query)
            if not query_embedding:
                print(f"  ❌ Failed to generate embedding for query: {query}")
                all_tests_passed = False
                continue

            # Perform search
            results = self.vector_store.search(query_embedding, top_k=top_k)

            if not results:
                print(f"  ❌ No results found for query: {query}")
                all_tests_passed = False
            else:
                print(f"  ✅ Found {len(results)} results")
                for j, result in enumerate(results[:2]):  # Show first 2 results
                    print(f"    Result {j+1} (score: {result['score']:.3f}):")
                    print(f"      Content preview: {result['content'][:100]}...")
                    print(f"      URL: {result['url']}")

        return all_tests_passed

    def test_collection_info(self):
        """
        Test collection information retrieval
        """
        print("\nTesting collection information...")
        info = self.vector_store.get_collection_info()
        if info:
            print(f"  Collection info: {info}")
            return True
        else:
            print("  ❌ Failed to get collection info")
            return False