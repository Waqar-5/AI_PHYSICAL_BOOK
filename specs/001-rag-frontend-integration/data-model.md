# Data Model: RAG Frontend Integration

## Entities

### QueryRequest
- **query** (string, required): The user's question or query text
- **metadata** (object, optional): Additional context information (session_id, user_id, etc.)
- **timestamp** (datetime, optional): When the query was created (server-side)

### QueryResponse
- **response** (string, required): The agent's answer to the query
- **sources** (array, optional): List of source documents/references used in the response
- **metadata** (object, optional): Additional response metadata
- **timestamp** (datetime, required): When the response was generated

### ErrorResponse
- **error_code** (string, required): Standardized error code
- **message** (string, required): Human-readable error message
- **details** (object, optional): Additional error details for debugging
- **timestamp** (datetime, required): When the error occurred

## State Transitions

### Query Processing Flow
1. **Received**: QueryRequest is validated upon API entry
2. **Processing**: Query is sent to RAG agent for processing
3. **Completed**: QueryResponse is generated and returned
4. **Failed**: ErrorResponse is generated if processing fails

## Validation Rules

### QueryRequest Validation
- **query**: Must be non-empty string (1-10000 characters)
- **metadata**: If present, must be a valid JSON object with string keys
- **required fields**: query field is mandatory

### QueryResponse Validation
- **response**: Must be non-empty string
- **sources**: If present, must be array of objects with required fields
- **timestamp**: Must be in ISO 8601 format

### ErrorResponse Validation
- **error_code**: Must be non-empty string
- **message**: Must be non-empty string explaining the error
- **timestamp**: Must be in ISO 8601 format