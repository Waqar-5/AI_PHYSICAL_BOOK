#!/bin/bash
# Setup script for RAG ingestion system

echo "Setting up RAG Ingestion System..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r rag_ingestion/requirements.txt

echo "Setup complete!"
echo "To run the ingestion pipeline:"
echo "1. Copy rag_ingestion/.env.example to rag_ingestion/.env"
echo "2. Add your API keys to rag_ingestion/.env"
echo "3. Run: python -m venv venv && source venv/bin/activate && python rag_ingestion/main.py"