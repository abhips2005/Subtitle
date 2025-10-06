# Setup Instructions

## Environment Configuration

The ElevenLabs API key is now configured via environment variables instead of manual entry in the UI.

### Backend Setup

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Copy the `.env.example` file to `.env`:
   ```bash
   copy .env.example .env
   ```

3. Open the `.env` file and add your ElevenLabs API key:
   ```
   ELEVENLABS_API_KEY=your_actual_api_key_here
   ```

4. **(Optional)** If you want to use Google Gemini AI for translation, add your Gemini API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

5. Get your ElevenLabs API key from [ElevenLabs Settings](https://elevenlabs.io/app/settings/api-keys)

6. Save the `.env` file

### Running the Application

1. **Backend** (from the `backend` directory):
   ```bash
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8001
   ```

2. **Frontend** (from the `frontend` directory):
   ```bash
   npm install
   npm start
   ```

### Security Notes

- The `.env` file is **not** committed to version control (should be in `.gitignore`)
- Keep your API key secure and never share it publicly
- Each developer needs to create their own `.env` file with their own API key

### Changes Made

- ✅ Removed manual API key entry from the UI
- ✅ Backend now reads API key from `.env` file
- ✅ Improved security by keeping API keys server-side
- ✅ Simplified user experience - no need to enter API key each time
- ✅ Added Google Gemini AI translation support (optional)

### Translation Services Available

1. **Google Translate (Free)** - No API key required, good quality
2. **Google Gemini AI** - API key required, excellent AI-powered translation (see [GEMINI_TRANSLATION_GUIDE.md](GEMINI_TRANSLATION_GUIDE.md))
3. **LibreTranslate (Free)** - No API key required, open source
4. **Azure Translator** - API key required, premium quality

### Troubleshooting

If you see an error about missing API key:
1. Ensure `.env` file exists in the `backend` directory
2. Check that `ELEVENLABS_API_KEY` is set in the `.env` file
3. Verify the API key is valid
4. Restart the backend server after changing the `.env` file
