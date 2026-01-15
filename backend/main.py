import asyncio
from fetcher import URLFetcher
from processor import TextProcessor
from embedder import Embedder
from storage import StorageManager
from models import ProcessingJob
from datetime import datetime
import logging
import sys

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
from sitemap_parser import parse_sitemap, filter_urls_by_pattern

def main_sync():
    """
    Synchronous version of the main function to run the full URL ingestion pipeline end-to-end
    """
    # Initialize components
    fetcher = URLFetcher()
    processor = TextProcessor()
    embedder = Embedder()
    storage = StorageManager()

    # URL to process (from command line args, environment variable, or defaults)
    import sys
    if len(sys.argv) > 1:
        urls_to_process = sys.argv[1:]  # Use URLs from command line arguments
    else:
        # Try to get URL from environment variable
        env_url = os.getenv("PROCESS_URL")
        if env_url:
            urls_to_process = [env_url]
        else:
            # Check if we should process from sitemap
            sitemap_url = os.getenv("SITEMAP_URL")
            if sitemap_url:
                logger.info(f"Processing URLs from sitemap: {sitemap_url}")
                all_urls = parse_sitemap(sitemap_url)

                # Filter URLs to focus on documentation content
                urls_to_process = filter_urls_by_pattern(
                    all_urls,
                    include_patterns=["/docs/"],  # Only include documentation pages
                    exclude_patterns=["/blog/", "/tags/", "/authors/"]  # Exclude blog content if not needed
                )

                logger.info(f"Filtered to {len(urls_to_process)} documentation URLs")
            else:
                # Use your deployed URL from the .env file and construct sitemap URL
                deploy_url = os.getenv("DEPLOY_VERCEL_URL")
                if deploy_url:
                    # Construct sitemap URL from deployed URL
                    sitemap_url = f"{deploy_url.rstrip('/')}/sitemap.xml"
                    logger.info(f"Processing URLs from sitemap: {sitemap_url}")
                    all_urls = parse_sitemap(sitemap_url)

                    # Filter URLs to focus on documentation content
                    urls_to_process = filter_urls_by_pattern(
                        all_urls,
                        include_patterns=["/docs/"],  # Only include documentation pages
                        exclude_patterns=["/blog/", "/tags/", "/authors/"]  # Exclude blog content if not needed
                    )

                    logger.info(f"Filtered to {len(urls_to_process)} documentation URLs")
                else:
                    # Default test URLs for testing purposes
                    urls_to_process = [
                        "https://en.wikipedia.org/wiki/Artificial_intelligence",
                        "https://www.python.org/doc/"
                    ]

    # Process each URL
    for url in urls_to_process:
        try:
            logger.info(f"Starting processing for URL: {url}")

            # Create a processing job
            job = ProcessingJob(
                id="",
                url=url,
                status="pending",
                created_at=datetime.now()
            )

            # Update job status to processing
            job.status = "processing"
            job.started_at = datetime.now()

            # Step 1: Fetch content
            logger.info("Fetching content...")
            content, metadata = fetcher.fetch_content(url)

            # Step 2: Clean and chunk text
            logger.info("Processing and chunking text...")
            clean_text = processor.clean_content(content, url)
            chunks = processor.chunk_text(clean_text)

            logger.info(f"Created {len(chunks)} chunks from content")

            # Step 3: Generate embeddings and store
            logger.info(f"Processing {len(chunks)} chunks...")

            # Process chunks in batches to be more efficient
            batch_size = 10
            processed_count = 0

            for i in range(0, len(chunks), batch_size):
                batch = chunks[i:i + batch_size]

                # Extract text from batch
                batch_texts = [chunk['text'] for chunk in batch]

                # Generate embeddings for the batch
                logger.info(f"Processing batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1}")
                embeddings = embedder.batch_generate_embeddings(batch_texts)

                # Store each chunk with its embedding
                for j, chunk in enumerate(batch):
                    embedding = embeddings[j]

                    # Validate embedding
                    if not embedder.validate_embedding(embedding):
                        logger.warning(f"Invalid embedding for chunk {chunk['index']}, skipping...")
                        continue

                    # Prepare chunk data for storage
                    chunk_data = {
                        'id': f"{url}#{chunk['index']}",
                        'url': url,
                        'content': chunk['text'],
                        'embedding': embedding,
                        'chunk_index': chunk['index'],
                        'total_chunks': chunk['total'],
                        'created_at': datetime.now().isoformat(),
                        'metadata': {
                            **metadata,
                            'word_count': len(chunk['text'].split()),
                            'language': 'en'  # Could implement language detection
                        }
                    }

                    # Store in Qdrant
                    chunk_id = storage.store_chunk(chunk_data)
                    logger.debug(f"Stored chunk {chunk['index']} with ID: {chunk_id}")

                    processed_count += 1

                # Update job progress
                job.processed_chunks = processed_count
                job.total_chunks = len(chunks)

            # Update job status to completed
            job.status = "completed"
            job.completed_at = datetime.now()

            logger.info(f"Pipeline completed successfully for {url}! Processed {processed_count} chunks.")

        except Exception as e:
            logger.error(f"Pipeline failed for {url}: {str(e)}")

            # Update job status to failed
            if 'job' in locals():
                job.status = "failed"
                job.error = str(e)
                job.completed_at = datetime.now()

            # Continue with next URL instead of stopping
            continue

if __name__ == "__main__":
    main_sync()
