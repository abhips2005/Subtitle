@echo off
echo ========================================
echo Supabase Authentication Setup
echo ========================================
echo.

cd frontend

echo Step 1: Installing Supabase client...
call npm install @supabase/supabase-js
echo.

if %ERRORLEVEL% EQU 0 (
    echo ✓ Supabase client installed successfully!
    echo.
) else (
    echo ✗ Installation failed. Please check your npm installation.
    pause
    exit /b 1
)

echo Step 2: Checking environment configuration...
if exist .env (
    echo ✓ .env file found
    echo.
    findstr /C:"REACT_APP_SUPABASE" .env >nul
    if %ERRORLEVEL% EQU 0 (
        echo ✓ Supabase configuration found in .env
        echo.
    ) else (
        echo ⚠ Supabase configuration not found in .env
        echo   Please add your Supabase credentials to .env file
        echo.
    )
) else (
    echo ⚠ .env file not found
    echo   Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo ⚠ Please edit frontend\.env and add your Supabase credentials!
    echo.
)

cd ..

echo ========================================
echo Setup Instructions
echo ========================================
echo.
echo 1. Create a Supabase project at: https://supabase.com
echo.
echo 2. Get your credentials:
echo    - Go to Settings ^> API in Supabase dashboard
echo    - Copy Project URL and Anon Key
echo.
echo 3. Edit frontend\.env file and add:
echo    REACT_APP_SUPABASE_URL=your_project_url
echo    REACT_APP_SUPABASE_ANON_KEY=your_anon_key
echo.
echo 4. (Optional) Enable Google OAuth:
echo    - Go to Authentication ^> Providers in Supabase
echo    - Configure Google provider
echo.
echo 5. Start the application:
echo    Backend:  cd backend ^&^& uvicorn main:app --reload --port 8001
echo    Frontend: cd frontend ^&^& npm start
echo.
echo For detailed instructions, see: SUPABASE_AUTH_SETUP.md
echo.
pause
