# Google Gemini AI Translation - Setup Guide

## Overview

Google Gemini AI has been added as a translation option for subtitle translation. Gemini provides AI-powered, context-aware translations that can better understand nuances, idioms, and maintain the tone of the original content.

## Features

- 🤖 **AI-Powered Translation**: Uses Google's latest Gemini Pro model
- 🎯 **Context-Aware**: Better understanding of context compared to traditional translation
- 🗣️ **Preserves Formatting**: Maintains speaker labels, timestamps, and audio event tags
- 🌍 **Multi-language Support**: Supports all languages in the subtitle generator

## Setup Instructions

### 1. Get Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### 2. Configure the API Key

You have two options:

#### Option A: Environment Variable (Recommended)

1. Open `backend/.env` file
2. Add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```
3. Restart the backend server

#### Option B: Manual Entry in UI

1. In the subtitle generator UI, enable translation
2. Select "Google Gemini AI" from the translation service dropdown
3. Enter your API key in the "Google Gemini API Key" field

### 3. Install Required Package

The `google-generativeai` package has been added to `requirements.txt`. Install it with:

```bash
cd backend
pip install -r requirements.txt
```

Or install directly:
```bash
pip install google-generativeai
```

## Usage

### In the UI

1. Upload your video/audio file
2. In the Configuration panel:
   - Enable "Multi-language Translation"
   - Select "🤖 Google Gemini AI" from the Translation Service dropdown
   - If not using environment variable, enter your API key
   - Select target languages
3. Click "Generate Subtitles"

### Translation Service Comparison

| Service | Cost | Quality | Speed | API Key Required |
|---------|------|---------|-------|------------------|
| **Google Translate (Free)** | Free | Good | Fast | No |
| **Google Gemini AI** | Pay-per-use* | Excellent | Medium | Yes |
| **LibreTranslate** | Free | Fair | Slow | No |
| **Azure Translator** | Pay-per-use | Excellent | Fast | Yes |

*Gemini has a generous free tier. Check [pricing](https://ai.google.dev/pricing) for details.

## Advantages of Gemini Translation

### 1. Context Understanding
- Better handles idioms and colloquialisms
- Understands tone and intent
- More natural-sounding translations

### 2. Format Preservation
- Automatically preserves speaker labels: `[Speaker 1]`, `[Speaker 2]`
- Maintains audio event tags: `[LAUGHTER]`, `[APPLAUSE]`
- Keeps timestamps and special formatting intact

### 3. Consistency
- Maintains consistent terminology throughout the subtitle file
- Better handling of proper nouns and brand names

## Example

**Original (English):**
```
[Speaker 1] Hey! How's it going?
[Speaker 2] Not bad, just chilling. [LAUGHTER]
```

**Google Translate to Spanish:**
```
[Hablante 1] ¡Oye! ¿Cómo te va?
[Hablante 2] No está mal, solo relajándose. [RISA]
```

**Gemini AI to Spanish:**
```
[Speaker 1] ¡Hola! ¿Cómo te va?
[Speaker 2] Bien, aquí tranquilo. [RISAS]
```

Notice how Gemini:
- Preserves speaker labels exactly as `[Speaker 1]`
- Uses more natural Spanish ("aquí tranquilo" vs "solo relajándose")
- Translates audio tags appropriately

## Troubleshooting

### Error: "Gemini API key required"
- Make sure you've set `GEMINI_API_KEY` in the `.env` file
- Or provide the API key in the UI
- Restart the backend server after updating `.env`

### Error: "Import google.generativeai could not be resolved"
- Install the package: `pip install google-generativeai`
- Or reinstall requirements: `pip install -r requirements.txt`

### Slow Translation
- Gemini may be slower than Google Translate for large subtitle files
- Consider using Google Translate for quick translations
- Use Gemini for important content requiring high quality

### API Quota Exceeded
- Check your [API usage](https://makersuite.google.com/app/usage) in Google AI Studio
- Gemini has rate limits on the free tier
- Consider upgrading or spacing out translation requests

## API Costs

Google Gemini has a generous free tier:
- **Free Tier**: 60 requests per minute
- **Paid Tier**: Higher limits available

For subtitle translation, typical usage:
- Small file (100 subtitle entries): ~10-20 API calls
- Medium file (500 entries): ~50-100 API calls
- Large file (1000+ entries): ~100-200 API calls

Check current pricing at: https://ai.google.dev/pricing

## Security Notes

- ✅ Keep your API key secure in the `.env` file
- ✅ Never commit `.env` to version control (it's in `.gitignore`)
- ✅ Environment variable approach is more secure than UI entry
- ✅ Each developer/environment should use their own API key

## Technical Details

### Model Used
- **Model**: `gemini-pro`
- **Provider**: Google AI
- **SDK**: `google-generativeai` Python package

### Implementation
The Gemini translation implementation includes:
- Smart prompt engineering for subtitle context
- Language code to full name mapping
- Markdown cleanup for clean output
- Error handling with fallbacks
- Format preservation logic

## Next Steps

1. Set up your Gemini API key
2. Test with a small subtitle file
3. Compare quality with other translation services
4. Use the best service for your specific needs

## Support

For issues with:
- **API Key**: Check [Google AI Studio](https://makersuite.google.com/)
- **Translation Quality**: Report in the project issues
- **Technical Problems**: Check the backend logs

Enjoy high-quality AI-powered subtitle translations! 🎬🤖
