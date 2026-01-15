# Quickstart Guide: RAG Frontend Integration

## Prerequisites

- Python 3.11+
- Node.js (for Docusaurus frontend)
- Git

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Set up Backend Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up Environment Variables
Create a `.env` file in the backend directory:
```env
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
COHERE_API_KEY=your_cohere_api_key
OPENAI_API_KEY=your_openai_api_key
```

### 4. Start the Backend Server
```bash
cd backend
python api.py
```
The server will start on `http://localhost:8000`

### 5. Set up Frontend (Docusaurus)
```bash
cd docusaurus
npm install
```

### 6. Run the Frontend
```bash
cd docusaurus
npm start
```
The frontend will start on `http://localhost:3000`

## API Usage

### Query Endpoint
Send a POST request to `http://localhost:8000/query`:

```json
{
  "query": "What is artificial intelligence?",
  "metadata": {
    "session_id": "abc123",
    "user_id": "user456"
  }
}
```

### Response Format
```json
{
  "response": "Artificial intelligence is a branch of computer science...",
  "sources": [
    {
      "title": "Introduction to AI",
      "url": "https://example.com/ai-intro",
      "content": "Artificial intelligence (AI) is intelligence demonstrated by machines..."
    }
  ],
  "metadata": {},
  "timestamp": "2026-01-06T10:00:00Z"
}
```

## Testing the Integration

1. Start both backend and frontend servers
2. Open the Docusaurus site in your browser
3. Use the chatbot UI to submit queries
4. Verify that responses are returned correctly from the RAG agent