@echo off
REM Setup script for RAG ingestion system (Windows)

echo Setting up RAG Ingestion System...

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing requirements...
pip install -r rag_ingestion/requirements.txt

echo Setup complete!
echo To run the ingestion pipeline:
echo 1. Copy rag_ingestion/.env.example to rag_ingestion/.env
echo 2. Add your API keys to rag_ingestion/.env
echo 3. Run: python rag_ingestion/main.py