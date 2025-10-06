# Google Translate Flow Diagram

## Complete Translation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. Upload Video/Audio File                               │  │
│  │ 2. Enable Translation                                     │  │
│  │ 3. Select "Google Translate (Free)"                       │  │
│  │ 4. Choose Target Languages: [Spanish] [French] [German]  │  │
│  │ 5. Click "Generate Subtitles"                            │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND: main.py                             │
│                                                                  │
│  POST /api/transcribe                                           │
│  ├─ Receive audio/video file                                    │
│  ├─ Call ElevenLabs API                                         │
│  ├─ Generate original transcription                             │
│  └─ Create SRT with timestamps & speakers ──┐                   │
│                                              │                   │
│  Session Storage:                            │                   │
│  {                                           │                   │
│    session_id: "abc123",                     │                   │
│    srt_content: "1\n00:00:01,000...",  ◄─────┘                   │
│    transcription: {...}                                          │
│  }                                                               │
│                                                                  │
│  POST /api/translate                                            │
│  ├─ session_id: "abc123"                                        │
│  ├─ target_languages: ["Spanish", "French"]                     │
│  ├─ translation_service: "google_free"                          │
│  └─ Call translate_subtitles_preserve_structure() ──┐           │
└──────────────────────────────────────────────────────┼──────────┘
                                                       │
                                                       ▼
┌─────────────────────────────────────────────────────────────────┐
│            SUBTITLE TRANSLATOR: subtitle.py                     │
│                                                                  │
│  translate_subtitles_preserve_structure()                       │
│  │                                                               │
│  ├─ 1. Parse SRT into structured format                         │
│  │    Input:  "1\n00:00:01,000 --> 00:00:03,000\n              │
│  │             [Speaker 1] Hello everyone!"                     │
│  │                                                               │
│  │    Output: [                                                 │
│  │      {                                                        │
│  │        id: 1,                                                 │
│  │        start: 1.0,                                            │
│  │        end: 3.0,                                              │
│  │        text: "[Speaker 1] Hello everyone!"                   │
│  │      }                                                        │
│  │    ]                                                          │
│  │                                                               │
│  ├─ 2. For each subtitle entry:                                 │
│  │    │                                                          │
│  │    ├─ Extract speaker label: "[Speaker 1] "                  │
│  │    │                                                          │
│  │    ├─ Get text to translate: "Hello everyone!"               │
│  │    │                                                          │
│  │    └─ Call SubtitleTranslator.translate_subtitle_text() ──┐  │
│  │                                                             │  │
│  └─ 3. Reconstruct SRT with translated text                   │  │
│       and preserved timestamps & speaker labels               │  │
└───────────────────────────────────────────────────────────────┼──┘
                                                                │
                                                                ▼
┌─────────────────────────────────────────────────────────────────┐
│              SUBTITLE TRANSLATOR CLASS                          │
│                                                                  │
│  SubtitleTranslator(service="google_free")                      │
│  │                                                               │
│  └─ translate_subtitle_text()                                   │
│     │                                                            │
│     └─ Calls: translate_text_google_free() ─────────┐           │
│                                                      │           │
└──────────────────────────────────────────────────────┼──────────┘
                                                       │
                                                       ▼
┌─────────────────────────────────────────────────────────────────┐
│          GOOGLE TRANSLATE METHOD                                │
│                                                                  │
│  translate_text_google_free(text, target_lang)                  │
│  │                                                               │
│  ├─ 1. Import GoogleTranslator from deep-translator             │
│  │    from deep_translator import GoogleTranslator             │
│  │                                                               │
│  ├─ 2. Initialize translator                                    │
│  │    translator = GoogleTranslator(                            │
│  │        source="auto",  # Auto-detect                         │
│  │        target="es"     # Spanish                             │
│  │    )                                                          │
│  │                                                               │
│  ├─ 3. Check text length                                        │
│  │    │                                                          │
│  │    ├─ Short text (< 4500 chars)                              │
│  │    │  └─ Direct translation ────────────────────┐            │
│  │    │                                             │            │
│  │    └─ Long text (> 4500 chars)                  │            │
│  │       ├─ Split into sentences                   │            │
│  │       ├─ Create chunks < 4500 chars             │            │
│  │       ├─ Translate each chunk ─────────────────┐│            │
│  │       └─ Join translated chunks                ││            │
│  │                                                 ││            │
│  └─ 4. Return translated text ◄─────────────────────┘            │
│                                                                  │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DEEP-TRANSLATOR LIBRARY                      │
│                                                                  │
│  GoogleTranslator.translate()                                   │
│  │                                                               │
│  ├─ Makes HTTP request to Google Translate web interface        │
│  ├─ Scrapes translation from response                           │
│  └─ Returns translated text ────────────────────┐               │
│                                                  │               │
└──────────────────────────────────────────────────┼──────────────┘
                                                   │
                                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                     GOOGLE TRANSLATE                            │
│                  (Web Interface - Free)                         │
│                                                                  │
│  ┌────────────────────────────────────────────────────┐         │
│  │  Input: "Hello everyone!"                          │         │
│  │  Source: Auto-detect (English)                     │         │
│  │  Target: Spanish                                   │         │
│  │                                                     │         │
│  │  Processing... Neural Machine Translation          │         │
│  │                                                     │         │
│  │  Output: "¡Hola a todos!"                          │         │
│  └────────────────────────────────────────────────────┘         │
│                                                                  │
└──────────────────────────────┬──────────────────────────────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
    "¡Hola a todos!"                   "Bonjour à tous!"
    (Spanish)                          (French)
              │                                 │
              └────────────────┬────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│              BACK TO SUBTITLE TRANSLATOR                        │
│                                                                  │
│  Reconstructing subtitle with translated text:                  │
│                                                                  │
│  Original:                                                       │
│  1                                                               │
│  00:00:01,000 --> 00:00:03,000                                  │
│  [Speaker 1] Hello everyone!                                    │
│                                                                  │
│  Spanish Translation:                                            │
│  1                                                               │
│  00:00:01,000 --> 00:00:03,000                                  │
│  [Speaker 1] ¡Hola a todos!                                     │
│                                                                  │
│  French Translation:                                             │
│  1                                                               │
│  00:00:01,000 --> 00:00:03,000                                  │
│  [Speaker 1] Bonjour à tous!                                    │
│                                                                  │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND: main.py                             │
│                                                                  │
│  Store translations in session:                                 │
│  {                                                               │
│    session_id: "abc123",                                        │
│    translated_subtitles: {                                      │
│      "Spanish": "1\n00:00:01,000...",                           │
│      "French": "1\n00:00:01,000..."                             │
│    },                                                            │
│    translated_vtt: {                                            │
│      "Spanish": "WEBVTT\n\n...",                                │
│      "French": "WEBVTT\n\n..."                                  │
│    }                                                             │
│  }                                                               │
│                                                                  │
│  Return JSON response to frontend ──────┐                       │
└─────────────────────────────────────────┼───────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                             │
│                                                                  │
│  Display results:                                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ ✅ Translation Complete!                                  │  │
│  │                                                            │  │
│  │ Original: English                                          │  │
│  │ Translated to: Spanish, French                             │  │
│  │                                                            │  │
│  │ [Download Spanish SRT] [Download Spanish VTT]             │  │
│  │ [Download French SRT]  [Download French VTT]              │  │
│  │                                                            │  │
│  │ Preview:                                                   │  │
│  │ 1. [Speaker 1] ¡Hola a todos!                             │  │
│  │ 2. [Speaker 2] Gracias por estar aquí. [RISAS]           │  │
│  │ 3. [Speaker 1] Empecemos con el tema de hoy.             │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Key Points

### 1. No API Key Required ✅
- Uses `deep-translator` library
- Accesses Google Translate web interface
- Free to use

### 2. Structure Preservation ✅
- Timestamps: `00:00:01,000 --> 00:00:03,000` ✓
- Speaker labels: `[Speaker 1]` ✓
- Audio events: `[LAUGHTER]` → `[RISAS]` ✓
- SRT format maintained ✓

### 3. Smart Processing ✅
- Auto-detect source language
- Chunks long texts (>4500 chars)
- Batch translation to multiple languages
- Error handling with fallbacks

### 4. Multi-Format Output ✅
- SRT format (SubRip)
- VTT format (WebVTT)
- JSON data structure

### 5. Session Management ✅
- Original transcription stored
- Translations cached
- Easy download access
