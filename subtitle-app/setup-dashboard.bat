@echo off
echo ========================================
echo Dashboard Feature Setup
echo ========================================
echo.

echo Step 1: Installing backend dependencies...
cd subtitle-app\backend
pip install supabase==2.3.4
if errorlevel 1 (
    echo Error: Failed to install Supabase package
    pause
    exit /b 1
)
echo Backend dependencies installed successfully!
echo.

cd ..\..

echo Step 2: Setup Instructions
echo ========================================
echo Please complete the following manual steps:
echo.
echo 1. DATABASE SETUP:
echo    - Go to your Supabase project dashboard
echo    - Open the SQL Editor
echo    - Run the SQL script from: SUPABASE_SCHEMA.sql
echo.
echo 2. VERIFY ENVIRONMENT:
echo    - Make sure your .env file has:
echo      SUPABASE_URL=your_supabase_url
echo      SUPABASE_ANON_KEY=your_supabase_anon_key
echo.
echo 3. START THE APPLICATION:
echo    - Backend: cd subtitle-app\backend ^&^& python main.py
echo    - Frontend: cd subtitle-app\frontend ^&^& npm start
echo.
echo ========================================
echo For detailed instructions, see DASHBOARD_SETUP.md
echo ========================================
echo.

pause
