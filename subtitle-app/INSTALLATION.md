# Installation Guide

## Prerequisites

Before installing the packages, ensure you have:

1. **Python 3.8+** installed
2. **Node.js 18+** and npm installed
3. **FFmpeg** installed on your system (for video processing)

### Installing FFmpeg (Windows)

```powershell
# Using winget
winget install Gyan.FFmpeg

# Or download from: https://ffmpeg.org/download.html
```

### Installing FFmpeg (Mac)

```bash
brew install ffmpeg
```

### Installing FFmpeg (Linux)

```bash
sudo apt-get install ffmpeg  # Ubuntu/Debian
sudo yum install ffmpeg      # CentOS/RHEL
```

## Backend Installation

### 1. Navigate to Backend Directory

```bash
cd subtitle-app/backend
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Packages

```bash
pip install -r requirements.txt
```

This will install:

**Core Backend:**
- FastAPI 0.104.1 - Web framework
- Uvicorn 0.24.0 - ASGI server
- Pydantic 2.11.9 - Data validation

**Translation Services:**
- deep-translator 1.11.4 - Multi-service translation

**AI & APIs:**
- elevenlabs 2.16.0 - Speech-to-text API
- requests 2.32.5 - HTTP client

**Media Processing:**
- opencv-python 4.12.0.88 - Video processing
- librosa 0.10.1 - Audio analysis
- soundfile 0.13.1 - Audio I/O
- pytesseract 0.3.13 - OCR capabilities

**Data Science:**
- numpy 2.2.6 - Numerical computing
- pandas 2.3.3 - Data manipulation
- scipy 1.16.2 - Scientific computing
- scikit-learn 1.7.2 - Machine learning

**Utilities:**
- streamlit 1.50.0 - Original UI framework (for compatibility)
- python-dotenv 1.0.0 - Environment variables
- pillow 11.3.0 - Image processing

### 4. Verify Installation

```bash
python -c "import fastapi, elevenlabs, deep_translator; print('✅ All packages installed successfully!')"
```

## Frontend Installation

### 1. Navigate to Frontend Directory

```bash
cd subtitle-app/frontend
```

### 2. Install Node Packages

```bash
npm install
```

This will install:

**Core Framework:**
- React 18
- TypeScript
- React Scripts (Create React App)

**UI Components:**
- Tailwind CSS 3.4.18 - Styling
- @tailwindcss/forms - Form styling
- lucide-react - Icon library
- react-dropzone - File upload

**HTTP & State:**
- axios - HTTP client

**Build Tools:**
- PostCSS, Autoprefixer

### 3. Verify Installation

```bash
npm list --depth=0
```

## Root Installation (Optional)

For running both servers simultaneously:

```bash
cd subtitle-app
npm install
```

This installs:
- concurrently 8.2.2 - Run multiple commands

## Quick Start

### Start Backend

```bash
cd subtitle-app/backend
python main.py
```

Backend runs on: http://localhost:8001

### Start Frontend

```bash
cd subtitle-app/frontend
npm start
```

Frontend runs on: http://localhost:3000

### Start Both (Using npm script)

```bash
cd subtitle-app
npm run dev
```

## Troubleshooting

### Port Conflicts

If you get port errors:

**Port 8001 in use:**
```bash
# Windows
netstat -ano | findstr :8001
taskkill /F /PID <PID>

# Mac/Linux
lsof -ti:8001 | xargs kill -9
```

**Port 3000 in use:**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /F /PID <PID>

# Mac/Linux
lsof -ti:3000 | xargs kill -9
```

### Python Package Issues

If you encounter installation errors:

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install with no cache
pip install --no-cache-dir -r requirements.txt

# Install specific problematic package separately
pip install <package-name> --upgrade
```

### Node Package Issues

```bash
# Clear npm cache
npm cache clean --force

# Remove node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Use legacy peer deps if conflicts
npm install --legacy-peer-deps
```

### FFmpeg Not Found

If you get FFmpeg errors:

1. Ensure FFmpeg is installed
2. Add FFmpeg to system PATH
3. Verify: `ffmpeg -version`

**Windows PATH Setup:**
```powershell
$env:PATH += ";C:\path\to\ffmpeg\bin"
```

## Environment Variables

Create a `.env` file in the backend directory:

```env
# Required
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Optional (for Azure Translator)
AZURE_TRANSLATOR_API_KEY=your_azure_key_here
AZURE_TRANSLATOR_REGION=global
```

## Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 18+ installed
- [ ] FFmpeg installed and in PATH
- [ ] Backend packages installed (`pip list`)
- [ ] Frontend packages installed (`npm list`)
- [ ] Backend starts successfully (port 8001)
- [ ] Frontend starts successfully (port 3000)
- [ ] ElevenLabs API key configured
- [ ] Can upload and preview files
- [ ] Translation services work

## Package Sizes

**Backend:** ~2.5 GB (includes numpy, pandas, scipy, ML libraries)
**Frontend:** ~350 MB (includes React and dependencies)

## Update Packages

### Backend

```bash
pip list --outdated
pip install --upgrade <package-name>
```

### Frontend

```bash
npm outdated
npm update <package-name>
```

## Production Build

### Frontend Production Build

```bash
cd subtitle-app/frontend
npm run build
```

Output will be in `build/` directory.

### Backend Production

For production deployment:

```bash
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001
```

## Support

For issues:
1. Check this installation guide
2. Review the main README.md
3. Check package documentation
4. Verify API keys are valid
5. Check system requirements