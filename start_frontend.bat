@echo off
echo Starting DocBook Frontend Server...
echo.

REM Navigate to frontend directory
cd /d "%~dp0docusaurus\docusaurus"

echo Installing/updating dependencies...
npm install

echo.
echo Starting the frontend server...
echo Visit http://localhost:3000 to access your frontend
echo Press Ctrl+C to stop the server
echo.

npm run start