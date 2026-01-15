# Research: URL Ingestion & Embedding Pipeline

## Cohere Embedding Models

### Decision: Use embed-english-v3.0 model
**Rationale**: For URL content processing, the English v3 model provides good performance for English text content which is common in web pages. It offers a good balance of accuracy and cost.

**Alternatives considered**:
- `embed-multilingual-v3.0`: Better for multilingual content but potentially more expensive
- `embed-english-light-v3.0`: Lighter version but potentially less accurate
- Other Cohere models: Various specialized models but v3 English is most appropriate for general web content

**Selected**: `embed-english-v3.0` with 1024-dimensional vectors

## Qdrant Cloud Integration

### Decision: Collection schema with content payload
**Rationale**: Need a flexible schema that stores embeddings with rich metadata for search and retrieval.

**Schema Design**:
- Vector size: 1024 (for embed-english-v3.0)
- Payload fields:
  - `url`: source URL
  - `content`: text chunk
  - `chunk_index`: position in original document
  - `created_at`: timestamp
  - `metadata`: additional structured data

**Configuration**:
- Collection name: `document_chunks`
- Distance metric: Cosine (appropriate for embeddings)

## Text Processing Strategy

### Decision: Use BeautifulSoup for HTML parsing with custom chunking
**Rationale**: BeautifulSoup is reliable for HTML parsing, and custom chunking allows control over chunk size and overlap.

**Chunking Strategy**:
- Maximum chunk size: 1000 characters
- Overlap: 100 characters between chunks
- Minimum chunk size: 100 characters to avoid noise
- Preserve sentence boundaries where possible

**Libraries**:
- `beautifulsoup4`: HTML parsing
- `requests`: URL fetching
- Custom logic: chunking algorithm

## URL Fetching Security

### Decision: Implement comprehensive URL validation and security measures
**Rationale**: Prevent security vulnerabilities when fetching arbitrary URLs.

**Security Measures**:
- Validate URL format and scheme (http/https only)
- Limit redirects to prevent redirect loops
- Set timeouts for requests
- Block private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.1)
- Set user agent to identify the application
- Content type validation (only process text/html)

## Error Handling Strategy

### Decision: Implement retry mechanism with exponential backoff
**Rationale**: Network requests can fail temporarily, so implement resilient error handling.

**Retry Configuration**:
- Maximum retries: 3
- Initial delay: 1 second
- Exponential backoff factor: 2
- Retry on: Connection errors, 429 (rate limit), 5xx status codes

## Environment Configuration

### Decision: Use environment variables for sensitive configuration
**Rationale**: Follow security best practices for storing API keys and configuration.

**Required Environment Variables**:
- `COHERE_API_KEY`: Cohere API key
- `QDRANT_URL`: Qdrant Cloud cluster URL
- `QDRANT_API_KEY`: Qdrant Cloud API key
- `MAX_CONTENT_LENGTH`: Maximum content size to process (default: 1MB)
- `CHUNK_SIZE`: Maximum chunk size (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 100)