import React, { useState } from 'react';
import { Globe, Download, CheckCircle, AlertCircle, FileText } from 'lucide-react';
import { TranslationData } from '../types';

interface TranslationPanelProps {
  translationData: TranslationData | null;
  onDownload: (format: string, language: string) => void;
}

const TranslationPanel: React.FC<TranslationPanelProps> = ({ translationData, onDownload }) => {
  const [selectedLanguage, setSelectedLanguage] = useState<string>('');
  const [activeFormat, setActiveFormat] = useState<'srt' | 'vtt'>('srt');

  React.useEffect(() => {
    if (translationData && Object.keys(translationData.translated_subtitles).length > 0 && !selectedLanguage) {
      setSelectedLanguage(Object.keys(translationData.translated_subtitles)[0]);
    }
  }, [translationData, selectedLanguage]);

  if (!translationData) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Globe className="w-6 h-6 text-gray-400" />
          <h2 className="text-xl font-semibold text-gray-900">Translations</h2>
        </div>
        
        <div className="text-center py-8">
          <Globe className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-500 mb-2">No translations generated</p>
          <p className="text-sm text-gray-400">
            Enable translation in the configuration panel to see results here
          </p>
        </div>
      </div>
    );
  }

  const availableLanguages = Object.keys(translationData.translated_subtitles);
  const currentContent = selectedLanguage && translationData.translated_subtitles[selectedLanguage] 
    ? (activeFormat === 'srt' 
        ? translationData.translated_subtitles[selectedLanguage]
        : translationData.translated_vtt[selectedLanguage] || ''
      )
    : '';

  const parseSubtitles = (content: string) => {
    const subtitles = [];
    const blocks = content.split('\n\n');
    
    for (const block of blocks) {
      if (block.trim()) {
        const lines = block.trim().split('\n');
        if (lines.length >= 3) {
          const id = lines[0];
          const timestamp = lines[1];
          const text = lines.slice(2).join('\n');
          
          subtitles.push({ id, timestamp, text });
        }
      }
    }
    
    return subtitles;
  };

  const currentSubtitles = currentContent ? parseSubtitles(currentContent) : [];

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center space-x-2 mb-4">
          <Globe className="w-6 h-6 text-green-600" />
          <h2 className="text-xl font-semibold text-gray-900">🌍 Translated Subtitles</h2>
        </div>

        {/* Translation Summary */}
        <div className="mb-6">
          <div className="flex items-center space-x-2 mb-2">
            <CheckCircle className="w-5 h-5 text-green-600" />
            <span className="font-medium text-green-800">
              Translation completed for {translationData.success_count} of {translationData.total_requested} languages
            </span>
          </div>
          
          <div className="bg-green-50 border border-green-200 rounded-lg p-3">
            <p className="text-sm text-green-800 mb-1">
              ✅ All features preserved across translations:
            </p>
            <ul className="text-xs text-green-700 space-y-1 ml-4">
              <li>• Exact timestamps maintained</li>
              <li>• Speaker diarization labels preserved</li>
              <li>• Audio event tags maintained</li>
              <li>• Subtitle formatting preserved</li>
            </ul>
          </div>
        </div>

        {/* Language Selector */}
        {availableLanguages.length > 0 && (
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Translation Language
            </label>
            <select
              value={selectedLanguage}
              onChange={(e) => setSelectedLanguage(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {availableLanguages.map(lang => (
                <option key={lang} value={lang}>{lang}</option>
              ))}
            </select>
          </div>
        )}
      </div>

      {availableLanguages.length > 0 && selectedLanguage && (
        <>
          {/* Format Tabs */}
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6">
              {[
                { id: 'srt', label: 'SRT Format' },
                { id: 'vtt', label: 'VTT Format' }
              ].map(({ id, label }) => (
                <button
                  key={id}
                  onClick={() => setActiveFormat(id as any)}
                  className={`py-3 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                    activeFormat === id
                      ? 'border-green-500 text-green-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <FileText className="w-4 h-4" />
                  <span>{label}</span>
                </button>
              ))}
            </nav>
          </div>

          {/* Content Display */}
          <div className="p-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-medium text-gray-900">
                {selectedLanguage} - {activeFormat.toUpperCase()} Format
              </h3>
              <button
                onClick={() => onDownload(activeFormat, selectedLanguage)}
                className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
              >
                <Download className="w-4 h-4" />
                <span>Download {activeFormat.toUpperCase()}</span>
              </button>
            </div>

            {/* Preview */}
            <div className="mb-4">
              <h4 className="text-sm font-medium text-gray-700 mb-2">Preview</h4>
              <div className="space-y-2 max-h-48 overflow-y-auto border border-gray-200 rounded-lg p-3">
                {currentSubtitles.slice(0, 5).map((subtitle, index) => (
                  <div key={index} className="border-b border-gray-100 pb-2 last:border-b-0">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-xs font-medium text-gray-500">#{subtitle.id}</span>
                      <span className="text-xs text-gray-500">{subtitle.timestamp}</span>
                    </div>
                    <p className="text-sm text-gray-900">{subtitle.text}</p>
                  </div>
                ))}
                
                {currentSubtitles.length > 5 && (
                  <p className="text-xs text-gray-500 text-center pt-2">
                    ... and {currentSubtitles.length - 5} more subtitles
                  </p>
                )}
              </div>
            </div>

            {/* Full Content */}
            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-2">Full Content</h4>
              <textarea
                value={currentContent}
                readOnly
                className="w-full h-64 p-3 border border-gray-300 rounded-md font-mono text-sm bg-gray-50"
                placeholder={`No ${activeFormat.toUpperCase()} content available for ${selectedLanguage}`}
              />
            </div>
          </div>

          {/* Download All */}
          <div className="border-t border-gray-200 px-6 py-4">
            <h4 className="font-medium text-gray-900 mb-3">Download All Translations</h4>
            <div className="space-y-3">
              {availableLanguages.map(lang => (
                <div key={lang} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <Globe className="w-4 h-4 text-green-600" />
                    <span className="font-medium text-gray-900">{lang}</span>
                    <span className="text-sm text-gray-600">
                      ({parseSubtitles(translationData.translated_subtitles[lang]).length} subtitles)
                    </span>
                  </div>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => onDownload('srt', lang)}
                      className="px-3 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700"
                    >
                      SRT
                    </button>
                    <button
                      onClick={() => onDownload('vtt', lang)}
                      className="px-3 py-1 text-xs bg-green-600 text-white rounded hover:bg-green-700"
                    >
                      VTT
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}

      {availableLanguages.length === 0 && (
        <div className="p-6 text-center">
          <AlertCircle className="w-16 h-16 text-yellow-400 mx-auto mb-4" />
          <p className="text-gray-600 mb-2">Translation failed</p>
          <p className="text-sm text-gray-500">
            All translation attempts were unsuccessful. Please try a different translation service or check your internet connection.
          </p>
        </div>
      )}
    </div>
  );
};

export default TranslationPanel;