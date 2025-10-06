import React, { useState, useCallback } from 'react';
import { FileVideo, FileAudio, LogIn } from 'lucide-react';
import FileUpload from './FileUpload';
import ConfigurationPanel from './ConfigurationPanel';
import TranscriptionDisplay from './TranscriptionDisplay';
import TranslationPanel from './TranslationPanel';
import VideoPlayer from './VideoPlayer';
import AuthModal from './AuthModal';
import UserMenu from './UserMenu';
import { useAuth } from '../contexts/AuthContext';
import { TranscriptionData, TranslationData, ApiResponse } from '../types';

const SubtitleGenerator: React.FC = () => {
  const [currentStep, setCurrentStep] = useState<'upload' | 'configure' | 'processing' | 'results'>('upload');
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [mediaUrl, setMediaUrl] = useState<string>('');
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const { user } = useAuth();
  const [configuration, setConfiguration] = useState({
    language: 'Auto-detect',
    numSpeakers: 1,
    diarize: true,
    tagAudioEvents: true,
    enableTranslation: false,
    translationService: 'google_free',
    targetLanguages: [] as string[],
    translationApiKey: ''
  });
  
  const [transcriptionData, setTranscriptionData] = useState<TranscriptionData | null>(null);
  const [translationData, setTranslationData] = useState<TranslationData | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingStep, setProcessingStep] = useState('');

  // Create and cleanup media URL when file changes
  React.useEffect(() => {
    if (uploadedFile) {
      const url = URL.createObjectURL(uploadedFile);
      setMediaUrl(url);
      
      return () => {
        URL.revokeObjectURL(url);
      };
    }
  }, [uploadedFile]);

  const handleFileUpload = useCallback((file: File) => {
    setUploadedFile(file);
    setCurrentStep('configure');
  }, []);

  const handleConfigurationChange = useCallback((config: typeof configuration) => {
    setConfiguration(config);
  }, []);

  const handleStartProcessing = useCallback(async () => {
    if (!uploadedFile) return;

    setIsProcessing(true);
    setCurrentStep('processing');
    setProcessingStep('Uploading file...');

    try {
      // Create transcription
      const formData = new FormData();
      formData.append('file', uploadedFile);
      formData.append('language_code', configuration.language === 'Auto-detect' ? '' : configuration.language);
      formData.append('num_speakers', configuration.numSpeakers.toString());
      formData.append('diarize', configuration.diarize.toString());
      formData.append('tag_audio_events', configuration.tagAudioEvents.toString());

      setProcessingStep('Creating transcription...');
      
      const transcriptionResponse = await fetch('http://localhost:8001/api/transcribe', {
        method: 'POST',
        body: formData,
      });

      if (!transcriptionResponse.ok) {
        throw new Error('Transcription failed');
      }

      const transcriptionResult: ApiResponse = await transcriptionResponse.json();
      setTranscriptionData(transcriptionResult.data);

      // Handle translation if enabled
      if (configuration.enableTranslation && configuration.targetLanguages.length > 0) {
        setProcessingStep('Translating subtitles...');
        
        const translationFormData = new FormData();
        translationFormData.append('session_id', transcriptionResult.data.session_id);
        translationFormData.append('target_languages', JSON.stringify(configuration.targetLanguages));
        translationFormData.append('translation_service', configuration.translationService);
        if (configuration.translationApiKey) {
          translationFormData.append('api_key', configuration.translationApiKey);
        }

        const translationResponse = await fetch('http://localhost:8001/api/translate', {
          method: 'POST',
          body: translationFormData,
        });

        if (translationResponse.ok) {
          const translationResult: ApiResponse = await translationResponse.json();
          setTranslationData(translationResult.data);
        }
      }

      setCurrentStep('results');
    } catch (error) {
      console.error('Processing error:', error);
      alert('Processing failed. Please check the backend configuration and try again.');
    } finally {
      setIsProcessing(false);
      setProcessingStep('');
    }
  }, [uploadedFile, configuration]);

  const downloadSubtitle = useCallback(async (format: string, language: string = 'original') => {
    if (!transcriptionData?.session_id) return;

    try {
      const response = await fetch(`http://localhost:8001/api/download/${transcriptionData.session_id}/${format}/${language}`);
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        
        const filename = language === 'original' 
          ? `subtitle.${format}` 
          : `subtitle_${language}.${format}`;
        a.download = filename;
        
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }
    } catch (error) {
      console.error('Download failed:', error);
    }
  }, [transcriptionData]);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                <FileVideo className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  🎬 Subtitle Generator
                </h1>
                <p className="text-sm text-gray-600">
                  Powered by ElevenLabs with Multi-language Translation
                </p>
              </div>
            </div>
            
            {/* Auth Section */}
            <div className="flex items-center space-x-4">
              {user ? (
                <UserMenu />
              ) : (
                <button
                  onClick={() => setIsAuthModalOpen(true)}
                  className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
                >
                  <LogIn className="w-5 h-5" />
                  <span className="font-medium">Sign In</span>
                </button>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Auth Modal */}
      <AuthModal isOpen={isAuthModalOpen} onClose={() => setIsAuthModalOpen(false)} />

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {currentStep === 'upload' && (
          <div className="max-w-2xl mx-auto">
            <FileUpload onFileUpload={handleFileUpload} />
          </div>
        )}

        {currentStep === 'configure' && uploadedFile && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">File Information</h2>
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center space-x-3 mb-4">
                  {uploadedFile.type.startsWith('video/') ? (
                    <FileVideo className="w-8 h-8 text-blue-600" />
                  ) : (
                    <FileAudio className="w-8 h-8 text-green-600" />
                  )}
                  <div>
                    <p className="font-medium text-gray-900">{uploadedFile.name}</p>
                    <p className="text-sm text-gray-600">
                      {(uploadedFile.size / (1024 * 1024)).toFixed(1)} MB
                    </p>
                  </div>
                </div>
                
                {uploadedFile.type.startsWith('video/') && mediaUrl && (
                  <video
                    src={mediaUrl}
                    controls
                    className="w-full rounded-lg"
                    style={{ maxHeight: '300px' }}
                  />
                )}
                
                {uploadedFile.type.startsWith('audio/') && mediaUrl && (
                  <audio
                    src={mediaUrl}
                    controls
                    className="w-full"
                  />
                )}
              </div>
              
              <div className="mt-6 flex space-x-3">
                <button
                  onClick={() => setCurrentStep('upload')}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
                >
                  Change File
                </button>
                <button
                  onClick={handleStartProcessing}
                  className="px-6 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700"
                >
                  Generate Subtitles
                </button>
              </div>
            </div>
            
            <div>
              <ConfigurationPanel
                configuration={configuration}
                onChange={handleConfigurationChange}
              />
            </div>
          </div>
        )}

        {currentStep === 'processing' && (
          <div className="max-w-2xl mx-auto text-center">
            <div className="bg-white rounded-lg shadow p-8">
              <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <h2 className="text-xl font-semibold text-gray-900 mb-2">Processing Your File</h2>
              <p className="text-gray-600 mb-4">{processingStep}</p>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-blue-600 h-2 rounded-full transition-all duration-300" style={{ width: '60%' }}></div>
              </div>
              <p className="text-sm text-gray-500 mt-2">This may take a few minutes depending on file size...</p>
            </div>
          </div>
        )}

        {currentStep === 'results' && transcriptionData && (
          <div className="space-y-8">
            {/* Video Player with Subtitles */}
            {uploadedFile?.type.startsWith('video/') && (
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Video with Subtitles</h2>
                <VideoPlayer
                  videoFile={uploadedFile}
                  subtitles={transcriptionData.srt_content}
                  translatedSubtitles={translationData?.translated_subtitles}
                />
              </div>
            )}

            {/* Results Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Transcription Results */}
              <div>
                <TranscriptionDisplay
                  data={transcriptionData}
                  onDownload={downloadSubtitle}
                />
              </div>

              {/* Translation Results */}
              <div>
                <TranslationPanel
                  translationData={translationData}
                  onDownload={downloadSubtitle}
                />
              </div>
            </div>

            {/* Start Over Button */}
            <div className="text-center">
              <button
                onClick={() => {
                  setCurrentStep('upload');
                  setUploadedFile(null);
                  setTranscriptionData(null);
                  setTranslationData(null);
                }}
                className="px-6 py-3 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
              >
                Process Another File
              </button>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-600">
            <h3 className="font-semibold text-gray-900 mb-2">About this App</h3>
            <p className="text-sm mb-4">
              This app uses <strong>ElevenLabs Scribe v1</strong> API to generate high-quality subtitles with 
              99 languages supported, speaker diarization, audio event tagging, and multi-language translation.
            </p>
            <div className="flex justify-center space-x-8 text-xs">
              <div>
                <strong>Features:</strong>
                <ul className="mt-1 space-y-1">
                  <li>• 99 languages for transcription</li>
                  <li>• Speaker diarization</li>
                  <li>• Audio event tagging</li>
                  <li>• Multiple export formats</li>
                </ul>
              </div>
              <div>
                <strong>Translation:</strong>
                <ul className="mt-1 space-y-1">
                  <li>• 40+ languages supported</li>
                  <li>• Preserves timestamps</li>
                  <li>• Maintains speaker labels</li>
                  <li>• Multiple translation services</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default SubtitleGenerator;