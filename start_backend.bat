@echo off
echo Starting DocBook Backend Server...
echo.

REM Activate virtual environment if you have one (uncomment the next line if needed)
REM call venv\Scripts\activate

REM Navigate to backend directory
cd /d "%~dp0backend"

echo Installing/updating dependencies...
pip install -r requirements.txt

echo.
echo Starting the server...
echo Visit http://localhost:8000 to access your API
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload