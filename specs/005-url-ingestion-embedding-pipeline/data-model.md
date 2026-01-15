# Data Model: URL Ingestion & Embedding Pipeline

## Entity Definitions

### DocumentChunk
Represents a processed chunk of content from a URL

**Fields**:
- `id`: str (UUID) - Unique identifier for the chunk
- `url`: str - Original URL where the content was sourced from
- `content`: str - Cleaned and processed text content
- `embedding`: List[float] - Vector embedding (1024-dimensional for Cohere embed-english-v3.0)
- `chunk_index`: int - Sequential index of this chunk within the original document
- `total_chunks`: int - Total number of chunks from the original document
- `created_at`: datetime - Timestamp when the chunk was created
- `metadata`: Dict[str, Any] - Additional metadata including:
  - `title`: str - Page title
  - `description`: str - Meta description if available
  - `word_count`: int - Number of words in the chunk
  - `source_domain`: str - Domain of the source URL
  - `language`: str - Detected language of the content

**Validation Rules**:
- `url` must be a valid HTTP/HTTPS URL
- `content` length must be between 100 and 1000 characters
- `embedding` must have exactly 1024 elements (for Cohere model)
- `chunk_index` must be >= 0 and < `total_chunks`

### ProcessingJob
Represents a URL ingestion job in the system

**Fields**:
- `id`: str (UUID) - Unique identifier for the job
- `url`: str - Target URL to process
- `status`: str - Current status (pending, processing, completed, failed)
- `created_at`: datetime - When the job was created
- `started_at`: datetime - When processing started (nullable)
- `completed_at`: datetime - When processing completed (nullable)
- `error`: str - Error message if the job failed (nullable)
- `processed_chunks`: int - Number of chunks successfully processed
- `total_chunks`: int - Total number of chunks expected
- `metadata`: Dict[str, Any] - Additional job metadata

**Status Transitions**:
- `pending` → `processing`: When job starts
- `processing` → `completed`: When all chunks are processed successfully
- `processing` → `failed`: When an error occurs during processing

## Database Schema (Qdrant Cloud)

### Collection: `document_chunks`

**Vector Configuration**:
- Size: 1024 (to match Cohere embed-english-v3.0 output)
- Distance: Cosine

**Payload Schema**:
```json
{
  "url": "string",
  "content": "string",
  "chunk_index": "integer",
  "total_chunks": "integer",
  "created_at": "string",
  "metadata": {
    "title": "string",
    "description": "string",
    "word_count": "integer",
    "source_domain": "string",
    "language": "string"
  }
}
```

**Indexing**:
- Index on `url` for efficient lookups by source URL
- Index on `created_at` for temporal queries
- Index on `metadata.source_domain` for domain-based filtering

## Relationships

- One `ProcessingJob` → Many `DocumentChunk` instances
- Each `DocumentChunk` belongs to exactly one `ProcessingJob` (tracked via metadata)

## State Transitions

### ProcessingJob States
```
PENDING
    ↓
PROCESSING
    ├── COMPLETED (success)
    └── FAILED (error)
```

### Valid State Transitions
- A job can only transition from PENDING to PROCESSING
- A job can transition from PROCESSING to either COMPLETED or FAILED
- Once COMPLETED or FAILED, the state is final

## Constraints

### Data Integrity
- Each DocumentChunk must have a valid embedding vector
- Content length must be within defined bounds (100-1000 characters)
- URLs must pass validation checks before processing
- Duplicate chunks for the same URL should be avoided

### Performance
- Maximum document size to process: 1MB
- Maximum number of chunks per document: 100 (enforces reasonable limits)
- Embedding generation should timeout after 30 seconds per chunk

## Access Patterns

### Common Queries
1. **Semantic search**: Find chunks similar to a query using vector similarity
2. **URL-based lookup**: Find all chunks from a specific URL
3. **Temporal queries**: Find chunks created within a time range
4. **Domain-based queries**: Find chunks from specific domains

### Query Examples
```python
# Semantic search
client.search(
    collection_name="document_chunks",
    query_vector=query_embedding,
    limit=10
)

# URL-based lookup
client.scroll(
    collection_name="document_chunks",
    scroll_filter=models.Filter(
        must=[models.FieldCondition(key="url", match=models.MatchValue(value=url))]
    )
)
```