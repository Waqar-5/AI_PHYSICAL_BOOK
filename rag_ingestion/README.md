# RAG Ingestion System for Book Content

This system crawls Docusaurus-based documentation sites, processes the content, generates embeddings using Cohere, and stores them in Qdrant for retrieval.

## Features

- **URL Crawling**: Discovers and crawls all pages from a Docusaurus site
- **Content Extraction**: Extracts clean text content from Docusaurus pages
- **Text Processing**: Cleans, chunks, and preprocesses content with overlap
- **Embedding Generation**: Creates high-quality embeddings using Cohere
- **Vector Storage**: Stores embeddings in Qdrant with proper indexing
- **Search Testing**: Tests vector search functionality with sample queries

## Tech Stack

- **Python 3.8+**
- **Cohere**: For text embeddings
- **Qdrant**: Vector database
- **BeautifulSoup**: HTML parsing
- **Requests**: HTTP requests

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy the example environment file and add your credentials:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

3. Run the ingestion pipeline:
```bash
python main.py
```

## Configuration

The system is configured via environment variables in the `.env` file:

- `QDRANT_URL`: Your Qdrant cluster URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `QDRANT_COLLECTION_NAME`: Name of the collection to store embeddings
- `COHERE_API_KEY`: Your Cohere API key
- `EMBEDDING_MODEL`: Cohere model to use (default: embed-english-v3.0)
- `BASE_URL`: The URL of the Docusaurus site to crawl
- `CHUNK_SIZE`: Size of text chunks (default: 512 characters)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 50 characters)

## Architecture

The system is organized into several modules:

- `crawler.py`: Discovers and extracts content from Docusaurus URLs
- `text_cleaner.py`: Cleans and chunks text content
- `embedder.py`: Generates embeddings using Cohere
- `vector_store.py`: Stores embeddings in Qdrant
- `search_tester.py`: Tests search functionality
- `config.py`: Centralized configuration management

## Usage

The main pipeline is orchestrated by `main.py` which:

1. Crawls the specified Docusaurus site
2. Extracts and cleans the content
3. Chunks the content with overlap
4. Generates embeddings for each chunk
5. Stores embeddings in Qdrant
6. Tests search functionality with sample queries

## Testing Search

After ingestion, you can test search functionality manually:

```python
from src.config import Config
from src.search_tester import VectorSearchTester

config = Config()
tester = VectorSearchTester(config)
results = tester.test_search(["your search query"], top_k=5)
```