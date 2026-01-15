# Quickstart: URL Ingestion & Embedding Pipeline

## Prerequisites

- Python 3.8 or higher
- `uv` package manager installed
- Cohere API key
- Qdrant Cloud account and API credentials

## Setup

### 1. Clone and Navigate to Project
```bash
# Create the backend directory
mkdir backend
cd backend
```

### 2. Initialize Project with uv
```bash
# Initialize a new Python project
uv init
```

### 3. Create Virtual Environment and Install Dependencies
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install required packages
uv pip install requests beautifulsoup4 cohere qdrant-client python-dotenv
```

### 4. Set Up Environment Variables
Create a `.env` file in the backend directory:
```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
```

## Basic Project Structure
```
backend/
├── main.py              # Main pipeline orchestrator
├── fetcher.py           # URL fetching logic
├── processor.py         # Text cleaning and chunking
├── embedder.py          # Embedding generation
├── storage.py           # Qdrant Cloud integration
├── config.py            # Configuration and constants
├── .env                 # Environment variables (not committed)
├── pyproject.toml       # Project configuration
└── requirements.txt     # Dependencies
```

## Running the Pipeline

### 1. Create the Main Pipeline File
Create `main.py` with the end-to-end pipeline:

```python
import asyncio
from fetcher import URLFetcher
from processor import TextProcessor
from embedder import Embedder
from storage import StorageManager

async def main():
    # Initialize components
    fetcher = URLFetcher()
    processor = TextProcessor()
    embedder = Embedder()
    storage = StorageManager()

    # URL to process
    url = "https://example.com/article"

    try:
        # Step 1: Fetch content
        print(f"Fetching content from {url}...")
        content, metadata = fetcher.fetch_content(url)

        # Step 2: Clean and chunk text
        print("Processing and chunking text...")
        clean_text = processor.clean_content(content, url)
        chunks = processor.chunk_text(clean_text)

        # Step 3: Generate embeddings and store
        print(f"Processing {len(chunks)} chunks...")
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i+1}/{len(chunks)}...")

            # Generate embedding
            embedding = embedder.generate_embedding(chunk['text'])

            # Prepare chunk data for storage
            chunk_data = {
                'id': f"{url}#{chunk['index']}",
                'url': url,
                'content': chunk['text'],
                'embedding': embedding,
                'chunk_index': chunk['index'],
                'total_chunks': chunk['total'],
                'metadata': metadata
            }

            # Store in Qdrant
            storage.store_chunk(chunk_data)

        print("Pipeline completed successfully!")

    except Exception as e:
        print(f"Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Execute the Pipeline
```bash
cd backend
python main.py
```

## Configuration Options

The pipeline can be customized with the following environment variables:

- `CHUNK_SIZE`: Maximum size of text chunks (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 100)
- `MAX_CONTENT_LENGTH`: Maximum content size to process (default: 1000000)
- `REQUEST_TIMEOUT`: Timeout for URL requests in seconds (default: 30)

## Testing with Sample URLs

Try the pipeline with these sample URLs:

```python
# Example URLs to test
TEST_URLS = [
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://www.python.org/doc/",
    "https://docs.anthropic.com/claude/docs"
]
```

## Next Steps

1. Add error handling and logging
2. Implement the API endpoints as defined in the contract
3. Add unit tests for each component
4. Set up monitoring and observability
5. Deploy to your preferred environment