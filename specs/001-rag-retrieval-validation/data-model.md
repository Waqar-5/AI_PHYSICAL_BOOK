# Data Model: RAG Retrieval Validation

## Entities

### Query
- **Fields**:
  - text: string (the search query text)
  - embedding: list[float] (vector representation of the query)
- **Validation rules**: Text must not be empty, embedding must have consistent dimensions with stored vectors
- **Relationships**: Used as input to similarity search

### RetrievedChunk
- **Fields**:
  - id: string (unique identifier for the chunk)
  - content: string (the text content of the chunk)
  - score: float (similarity score from search)
  - source_url: string (URL where the original content came from)
  - metadata: dict (additional metadata about the chunk)
- **Validation rules**: content must not be empty, score must be between 0 and 1, source_url must be valid
- **Relationships**: Result of similarity search operation

### ValidationResult
- **Fields**:
  - query: Query (the original query)
  - retrieved_chunks: list[RetrievedChunk] (chunks returned by search)
  - validation_passed: bool (whether all checks passed)
  - errors: list[string] (list of validation errors if any)
- **Validation rules**: Must have at least one retrieved chunk for validation
- **State transitions**: Created during validation, updated as checks are performed