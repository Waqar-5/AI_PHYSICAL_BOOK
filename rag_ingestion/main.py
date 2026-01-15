#!/usr/bin/env python3
"""
Main script to orchestrate the RAG ingestion pipeline:
1. Crawl Docusaurus site URLs
2. Clean and chunk the content
3. Generate embeddings using Cohere
4. Store embeddings in Qdrant
5. Test search functionality
"""

import os
import sys
from typing import Dict, List
import logging

# Add the rag_ingestion directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.config import Config
from src.crawler import URLCrawler
from src.text_cleaner import TextCleaner
from src.embedder import CohereEmbedder
from src.vector_store import QdrantVectorStore
from src.search_tester import VectorSearchTester


def setup_logging():
    """Set up logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('rag_ingestion.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main orchestration function"""
    print("Starting RAG Ingestion Pipeline...")

    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        # Initialize configuration
        print("1. Loading configuration...")
        config = Config()
        logger.info("Configuration loaded successfully")

        # Step 1: Crawl URLs
        print("2. Crawling Docusaurus site...")
        crawler = URLCrawler(config)

        # Get URLs from sitemap or start from base URL
        urls = crawler.get_all_urls_from_sitemap()
        if not urls:
            urls = [config.base_url]  # Fallback to base URL

        print(f"Found {len(urls)} URLs to crawl")

        # Crawl the URLs
        content_map = crawler.crawl_urls(urls[:10])  # Limit to first 10 for testing
        print(f"Crawled {len(content_map)} pages successfully")

        # Step 2: Clean and chunk content
        print("3. Cleaning and chunking content...")
        text_cleaner = TextCleaner(config)
        chunks = text_cleaner.preprocess_content(content_map)
        print(f"Created {len(chunks)} text chunks")

        # Step 3: Generate embeddings
        print("4. Generating embeddings...")
        embedder = CohereEmbedder(config)
        chunk_embeddings = embedder.embed_chunks(chunks)
        print(f"Generated embeddings for {len(chunk_embeddings)} chunks")

        # Step 4: Store in Qdrant
        print("5. Storing embeddings in Qdrant...")
        vector_store = QdrantVectorStore(config)
        vector_store.store_embeddings(chunk_embeddings)
        print("Embeddings stored successfully")

        # Step 5: Test search functionality
        print("6. Testing search functionality...")
        search_tester = VectorSearchTester(config)

        # Test with sample queries related to the book content
        sample_queries = [
            "ROS 2 Nodes and Topics",
            "Physical AI and Humanoid Robotics",
            "NVIDIA Isaac simulation",
            "Vision-Language-Action in robotics",
            "Gazebo physics simulation"
        ]

        search_success = search_tester.test_search(sample_queries, top_k=3)
        collection_info = search_tester.test_collection_info()

        if search_success and collection_info:
            print("\n✅ All tests passed! RAG ingestion pipeline completed successfully.")
            logger.info("RAG ingestion pipeline completed successfully")
        else:
            print("\n⚠️  Some tests had issues, but pipeline completed")
            logger.warning("Some tests had issues during pipeline execution")

    except Exception as e:
        logger.error(f"Error in main pipeline: {str(e)}", exc_info=True)
        print(f"❌ Error in pipeline: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()