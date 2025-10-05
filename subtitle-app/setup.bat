@echo off
echo ====================================
echo Subtitle Generator - Setup Script
echo ====================================
echo.

REM Check Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.8+ first.
    pause
    exit /b 1
)
python --version
echo ✓ Python found
echo.

REM Check Node.js
echo [2/5] Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found! Please install Node.js 18+ first.
    pause
    exit /b 1
)
node --version
echo ✓ Node.js found
echo.

REM Check FFmpeg
echo [3/5] Checking FFmpeg installation...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: FFmpeg not found! Video processing may not work.
    echo Install FFmpeg: winget install Gyan.FFmpeg
    echo.
) else (
    echo ✓ FFmpeg found
    echo.
)

REM Install Backend Dependencies
echo [4/5] Installing backend dependencies...
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Backend installation failed!
    pause
    exit /b 1
)
echo ✓ Backend dependencies installed
call deactivate
cd ..
echo.

REM Install Frontend Dependencies
echo [5/5] Installing frontend dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Frontend installation failed!
    pause
    exit /b 1
)
echo ✓ Frontend dependencies installed
cd ..
echo.

REM Install root dependencies
echo Installing root dependencies...
call npm install
echo ✓ Root dependencies installed
echo.

echo ====================================
echo ✓ Setup Complete!
echo ====================================
echo.
echo Next steps:
echo 1. Get your ElevenLabs API key from https://elevenlabs.io
echo 2. Create backend/.env file with: ELEVENLABS_API_KEY=your_key
echo 3. Start both servers: npm run dev
echo    Or start individually:
echo    - Backend: cd backend ^&^& python main.py
echo    - Frontend: cd frontend ^&^& npm start
echo.
echo Backend will run on: http://localhost:8001
echo Frontend will run on: http://localhost:3000
echo.
pause