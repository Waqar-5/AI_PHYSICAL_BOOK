# AI Agent with Retrieval-Augmented Capabilities

This project implements an OpenAI agent that integrates with a RAG (Retrieval-Augmented Generation) system to answer questions using book content stored in Qdrant. The agent uses the OpenAI Agents SDK with a custom retrieval tool that queries Qdrant using existing retrieval pipeline logic.

## Features

- **OpenAI Agent Integration**: Uses OpenAI's Assistant API to create intelligent agents
- **RAG Integration**: Retrieves relevant content from Qdrant vector database
- **Context Management**: Maintains conversation history for follow-up queries
- **Error Handling**: Robust error handling with retry mechanisms
- **Modular Design**: Clean architecture with separate components for configuration, retrieval, and agent logic

## Prerequisites

- Python 3.11+
- OpenAI API key
- Qdrant instance with book content indexed
- Cohere API key (for embeddings)

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. **Set up environment variables**:
   Create a `.env` file in the project root with the following:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   COHERE_API_KEY=your_cohere_api_key
   QDRANT_COLLECTION_NAME=document_chunks  # optional, defaults to 'document_chunks'
   OPENAI_MODEL=gpt-4-turbo-preview  # optional, defaults to 'gpt-4-turbo-preview'
   ```

3. **Ensure Qdrant has indexed book content**:
   Make sure your Qdrant instance contains the book content you want the agent to query.

## Usage

### Basic Usage

Run the agent directly:
```bash
python agent.py
```

### Using the Agent in Your Code

```python
from agent import OpenAIAgent, AgentConfig

# Initialize configuration
config = AgentConfig()

# Initialize the agent
agent = OpenAIAgent(config)

# Ask a question
response = agent.query("What is artificial intelligence?")
print(response)

# For follow-up questions with context
response = agent.query_with_context("How does it differ from machine learning?")
print(response)
```

### Multi-turn Conversations

```python
# Start a new conversation
agent.start_new_conversation()

# Ask initial question
response1 = agent.query("Explain neural networks")
print(response1)

# Ask follow-up with context
response2 = agent.query_with_context("How do they learn from data?")
print(response2)

# Get conversation history
history = agent.get_conversation_history()
```

## Examples

Check out the example script for detailed usage:
```bash
python examples/agent_example.py
```

## Architecture

The system consists of three main components:

1. **AgentConfig**: Manages API keys and configuration
2. **RetrievalTool**: Handles queries to Qdrant and formats results
3. **OpenAIAgent**: Orchestrates the conversation and integrates with OpenAI

## Testing

Run the provided test scripts:
- `python test_agent_basic.py` - Basic query functionality
- `python test_retrieval_integration.py` - Retrieval tool integration
- `python test_followup_queries.py` - Follow-up query functionality

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `QDRANT_URL`: URL of your Qdrant instance
- `QDRANT_API_KEY`: Your Qdrant API key
- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_COLLECTION_NAME`: Name of the collection in Qdrant (optional)
- `OPENAI_MODEL`: OpenAI model to use (optional)

## Error Handling

The agent includes comprehensive error handling:
- Connection retries for Qdrant with exponential backoff
- Graceful degradation when content is not found
- Detailed logging for debugging

## Development

The project follows a modular design that makes it easy to extend:
- Configuration management is centralized
- Retrieval logic is separated from agent logic
- Conversation state is managed independently

---

## Legacy RAG Retrieval Validation

This project also includes the original RAG retrieval validation functionality:

This script connects to Qdrant to validate the RAG (Retrieval-Augmented Generation) retrieval pipeline by:
1. Connecting to Qdrant and loading existing vector collections
2. Accepting a query and performing top-k similarity search
3. Validating results using returned text, metadata, and source URLs

### Legacy Usage

Run the validation script with a query:

```bash
python backend/retrieve.py "Your query here"
```

You can also specify the number of results to return (top-k):

```bash
python backend/retrieve.py "Your query here" --top_k 5
```

### Legacy Examples

```bash
# Basic query
python backend/retrieve.py "What is artificial intelligence?"

# Query with custom top-k value
python backend/retrieve.py "How does machine learning work?" --top_k 3
```