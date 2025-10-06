@echo off
echo ========================================
echo Google Gemini AI Translation Setup
echo ========================================
echo.

cd backend

echo Installing Google Generative AI package...
pip install google-generativeai
echo.

if %ERRORLEVEL% EQU 0 (
    echo ✓ Package installed successfully!
    echo.
) else (
    echo ✗ Installation failed. Please check your pip installation.
    echo.
    pause
    exit /b 1
)

echo Checking .env configuration...
if exist .env (
    findstr /C:"GEMINI_API_KEY" .env >nul
    if %ERRORLEVEL% EQU 0 (
        echo ✓ GEMINI_API_KEY found in .env file
        echo.
    ) else (
        echo ⚠ GEMINI_API_KEY not found in .env file
        echo.
        echo Adding GEMINI_API_KEY to .env...
        echo. >> .env
        echo # Google Gemini API Configuration (Optional - only needed for Gemini translation) >> .env
        echo # Get your API key from: https://makersuite.google.com/app/apikey >> .env
        echo GEMINI_API_KEY=your_gemini_api_key_here >> .env
        echo.
        echo ✓ GEMINI_API_KEY added to .env file
        echo ⚠ Please edit backend\.env and add your actual Gemini API key!
        echo.
    )
) else (
    echo ✗ .env file not found! Please run setup-env.bat first.
    echo.
    pause
    exit /b 1
)

cd ..

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Get your Gemini API key from:
echo    https://makersuite.google.com/app/apikey
echo.
echo 2. Edit backend\.env and add your GEMINI_API_KEY
echo.
echo 3. Restart the backend server:
echo    cd backend
echo    uvicorn main:app --reload --port 8001
echo.
echo 4. In the UI, select "Google Gemini AI" from translation dropdown
echo.
echo For detailed instructions, see: GEMINI_TRANSLATION_GUIDE.md
echo.
pause
