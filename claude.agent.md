# URL Ingestion & Embedding Pipeline Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-25

## Active Technologies

- Python 3.8+
- uv (package manager)
- Cohere (embedding generation)
- Qdrant Cloud (vector storage)
- requests (HTTP requests)
- beautifulsoup4 (HTML parsing)
- python-dotenv (environment management)

## Project Structure

```text
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

## Commands

### Project Setup
```bash
# Initialize project with uv
uv init

# Install dependencies
uv pip install requests beautifulsoup4 cohere qdrant-client python-dotenv

# Run the pipeline
python main.py
```

### Environment Setup
```bash
# Set up environment variables in .env file:
# COHERE_API_KEY=your_cohere_api_key_here
# QDRANT_URL=your_qdrant_cloud_url_here
# QDRANT_API_KEY=your_qdrant_api_key_here
```

## Code Style

### Python
- Follow PEP 8 guidelines
- Use type hints for all function parameters and return values
- Use f-strings for string formatting
- Handle errors gracefully with try/except blocks
- Use logging instead of print statements for production code

### Security
- Validate all URLs before fetching
- Set appropriate timeouts for network requests
- Store API keys in environment variables, never in code
- Sanitize HTML content before processing

## Recent Changes

- **URL Ingestion & Embedding Pipeline**: Added backend pipeline for fetching URLs, processing content, generating Cohere embeddings, and storing in Qdrant Cloud. Includes URL fetching with security validation, text cleaning with BeautifulSoup, chunking algorithm, and vector storage integration.

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->