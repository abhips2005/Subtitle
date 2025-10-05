# Subtitle Generator - React Frontend

A modern React frontend for the ElevenLabs-powered subtitle generator with multi-language translation support.

## 🚀 Features

- **Modern React UI** - Clean, responsive interface built with React, TypeScript, and Tailwind CSS
- **Drag & Drop File Upload** - Easy file upload with support for audio and video files
- **Real-time Processing** - Visual feedback during transcription and translation
- **Multi-language Support** - Translate subtitles to 40+ languages while preserving all features
- **Integrated Video Player** - Custom video player with synchronized subtitle display
- **Multiple Export Formats** - Download subtitles in SRT, VTT, and JSON formats
- **Speaker Diarization** - Visual display of speaker identification
- **Timeline View** - Interactive timeline showing subtitle timing

## 🛠 Technology Stack

- **Frontend**: React 18 + TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **File Upload**: React Dropzone
- **HTTP Client**: Axios
- **Backend**: FastAPI (Python)

## 📁 Project Structure

```
subtitle-app/
├── backend/
│   ├── main.py              # FastAPI backend server
│   ├── subtitle.py          # Original subtitle generation logic
│   └── requirements.txt     # Python dependencies
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── SubtitleGenerator.tsx    # Main component
    │   │   ├── FileUpload.tsx          # File upload interface
    │   │   ├── ConfigurationPanel.tsx  # Settings panel
    │   │   ├── TranscriptionDisplay.tsx # Results display
    │   │   ├── TranslationPanel.tsx    # Translation results
    │   │   └── VideoPlayer.tsx         # Custom video player
    │   ├── types.ts            # TypeScript interfaces
    │   └── App.tsx            # Root component
    ├── package.json
    └── tailwind.config.js
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- ElevenLabs API key

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd subtitle-app/backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Mac/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the backend server:**
   ```bash
   python main.py
   ```
   
   The backend will run on `http://localhost:8001`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd subtitle-app/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```
   
   The frontend will run on `http://localhost:3000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
ELEVENLABS_API_KEY=your_api_key_here
```

### API Keys Required

1. **ElevenLabs API Key** (Required)
   - Get from: https://elevenlabs.io/app/settings/api-keys
   - Used for: Speech-to-text transcription

2. **Azure Translator API Key** (Optional)
   - Required only if using Azure translation service
   - Used for: Premium translation quality

## 📖 Usage

### Basic Workflow

1. **Upload File** - Drag and drop or select audio/video file
2. **Configure Settings** - Set API key, language, and translation options
3. **Process** - Click "Generate Subtitles" to start processing
4. **Review Results** - View transcription and translations
5. **Download** - Export subtitles in various formats

### Supported File Formats

**Audio:** MP3, WAV, FLAC, M4A, AAC, OGG  
**Video:** MP4, MOV, AVI, MKV, WEBM

**Limits:** 3GB file size, up to 10 hours duration

### Translation Features

- **40+ Languages** supported
- **Preserves all features**: timestamps, speaker labels, audio events
- **Multiple services**: Google Translate (free), LibreTranslate (free), Azure (premium)
- **Automatic fallback** between services

## 🎯 Key Differences from Streamlit Version

### Advantages of React Frontend

1. **Better User Experience**
   - Modern, responsive design
   - Real-time progress feedback
   - Smooth animations and transitions

2. **Enhanced Video Player**
   - Custom-built video player with subtitle overlay
   - Language switching without page reload
   - Better subtitle synchronization

3. **Improved File Handling**
   - Drag and drop interface
   - File validation and error handling
   - Preview of uploaded media

4. **Better Organization**
   - Separated backend API from frontend
   - Modular component architecture
   - Type-safe with TypeScript

5. **Performance**
   - Client-side rendering
   - Efficient state management
   - Optimized re-renders

### Preserved Functionality

- ✅ All original transcription features
- ✅ Speaker diarization
- ✅ Audio event tagging
- ✅ Multi-language translation
- ✅ Multiple export formats
- ✅ Same API integrations (ElevenLabs, translation services)

## 🔌 API Endpoints

The backend provides a RESTful API:

- `GET /api/languages` - Get supported languages
- `POST /api/transcribe` - Create transcription
- `POST /api/translate` - Translate subtitles
- `GET /api/session/{id}` - Get session data
- `GET /api/download/{id}/{format}/{language}` - Download files

## 🚦 Development

### Running in Development

1. **Start backend:** `cd backend && python main.py` (runs on port 8001)
2. **Start frontend:** `cd frontend && npm start` (runs on port 3000)
3. **Open browser:** http://localhost:3000

### Building for Production

```bash
cd frontend
npm run build
```

The build files will be in the `build/` directory.

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure backend is running on port 8001
   - Check CORS settings in `main.py`

2. **API Key Issues**
   - Verify ElevenLabs API key is valid
   - Check API key format (no extra spaces)

3. **Translation Failures**
   - Try different translation service
   - Check internet connection
   - Verify target languages are supported

4. **File Upload Issues**
   - Check file size (max 3GB)
   - Verify file format is supported
   - Ensure sufficient disk space

### Debug Mode

Set environment variable for detailed logging:
```bash
export DEBUG=1  # Mac/Linux
set DEBUG=1     # Windows
```

## 📋 TODO / Future Enhancements

- [ ] Add batch file processing
- [ ] Implement user authentication
- [ ] Add subtitle editing interface
- [ ] Support for more translation services
- [ ] Real-time collaboration features
- [ ] Mobile-responsive improvements
- [ ] Dark mode support
- [ ] Subtitle styling customization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project maintains the same license as the original Streamlit version.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the original Streamlit implementation
3. Check ElevenLabs API documentation
4. Create an issue with detailed error information