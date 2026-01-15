# API Contract: RAG Retrieval Validation

## Query Endpoint
```
POST /validate-query
```

### Request
```json
{
  "query_text": "string, required",
  "top_k": "integer, optional, default: 5"
}
```

### Response
```json
{
  "query": "string",
  "retrieved_chunks": [
    {
      "id": "string",
      "content": "string",
      "score": "float",
      "source_url": "string",
      "metadata": "object"
    }
  ],
  "validation_passed": "boolean",
  "errors": ["string"],
  "execution_time_ms": "float"
}
```

### Error Response
```json
{
  "error": "string",
  "details": "object"
}
```

## Validation Endpoint
```
POST /validate-retrieval
```

### Request
```json
{
  "query_text": "string, required",
  "expected_source_urls": ["string, optional"]
}
```

### Response
```json
{
  "query": "string",
  "retrieved_chunks": [
    {
      "id": "string",
      "content": "string",
      "score": "float",
      "source_url": "string",
      "metadata": "object"
    }
  ],
  "validation_results": {
    "connection_success": "boolean",
    "metadata_match": "boolean",
    "content_relevance": "boolean",
    "overall_validation": "boolean"
  },
  "metrics": {
    "retrieval_time_ms": "float",
    "total_chunks": "integer"
  }
}
```