# Example Queries for RAG Retrieval Validation

This file contains example queries that can be used to test the RAG retrieval validation system.

## Sample Queries

### General AI/ML Topics
```bash
python retrieve.py "What is artificial intelligence?"
python retrieve.py "Explain machine learning concepts"
python retrieve.py "What are neural networks?"
python retrieve.py "How does deep learning work?"
```

### Technical Queries
```bash
python retrieve.py "What is a vector database?"
python retrieve.py "Explain semantic search"
python retrieve.py "How does Qdrant work?"
python retrieve.py "What are embeddings in NLP?"
```

### Book Content Queries
```bash
python retrieve.py "History of computer science"
python retrieve.py "Programming language evolution"
python retrieve.py "Software engineering best practices"
python retrieve.py "Data structures and algorithms"
```

## Usage with Different Top-K Values

```bash
# Get top 3 results
python retrieve.py "What is Python?" --top_k 3

# Get top 10 results
python retrieve.py "Machine learning algorithms" --top_k 10

# Get top 1 result for focused search
python retrieve.py "Definition of algorithm" --top_k 1
```

## Expected Output Format

When running these queries, you should see:
1. Query text confirmation
2. Top-k results with similarity scores
3. Source URLs for each result
4. Content previews
5. Metadata information
6. Validation summary