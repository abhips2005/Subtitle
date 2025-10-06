@echo off
echo Setting up Subtitle Generator Environment...
echo.

cd backend

if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo ========================================
    echo IMPORTANT: Please edit backend\.env 
    echo and add your ElevenLabs API key!
    echo.
    echo Get your API key from:
    echo https://elevenlabs.io/app/settings/api-keys
    echo ========================================
    echo.
) else (
    echo .env file already exists.
)

cd ..

echo Setup complete!
echo.
echo Next steps:
echo 1. Edit backend\.env and add your ELEVENLABS_API_KEY
echo 2. Run: cd backend ^&^& uvicorn main:app --reload --port 8001
echo 3. In another terminal run: cd frontend ^&^& npm start
echo.
pause
