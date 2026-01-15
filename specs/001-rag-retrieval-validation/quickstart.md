# Quickstart: RAG Retrieval Validation

## Setup

1. **Install dependencies**:
   ```bash
   pip install qdrant-client cohere python-dotenv
   ```

2. **Configure environment**:
   Create a `.env` file with the following variables:
   ```env
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   COHERE_API_KEY=your_cohere_api_key
   QDRANT_COLLECTION_NAME=document_chunks
   ```

3. **Run validation**:
   ```bash
   python retrieve.py "your test query here"
   ```

## Usage Examples

### Basic Query
```bash
python retrieve.py "What is artificial intelligence?"
```

### With custom top-k value
```bash
python retrieve.py "What is machine learning?" --top_k 5
```

### Advanced validation
The script performs comprehensive validation including:
- Connection to Qdrant
- Vector collection loading
- Top-k similarity search
- Metadata consistency checking
- Source URL validation
- Content relevance verification

## Validation Output

The script will output:
- Whether the connection to Qdrant was successful
- The top-k retrieved chunks with their source URLs
- Validation results showing if metadata matches expectations
- Performance metrics
- Comprehensive validation report with detailed metadata analysis