@echo off
echo Starting DocBook Full Stack Application...
echo.

echo Starting Backend Server...
echo Note: You'll need to keep this window open for the backend to run
echo.

REM Start backend in a separate window
start cmd /k "cd /d \"%~dp0backend\" && echo Starting Backend Server && python -m uvicorn api:app --host 0.0.0.0 --port 8000"

timeout /t 5 /nobreak >nul

echo.
echo Starting Frontend Server...
echo Note: You'll need to keep this window open for the frontend to run
echo.

REM Start frontend in a separate window
start cmd /k "cd /d \"%~dp0docusaurus\docusaurus\" && echo Starting Frontend Server && npm run start"

echo.
echo Your application is now running!
echo - Backend API: http://localhost:8000
echo - Frontend UI: http://localhost:3000
echo.
echo Keep both command windows open for the application to continue running.
pause