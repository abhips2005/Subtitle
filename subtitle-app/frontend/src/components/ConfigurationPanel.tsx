import React, { useState, useEffect } from 'react';
import { Settings, Globe, CheckCircle, AlertCircle } from 'lucide-react';
import { Configuration } from '../types';

interface ConfigurationPanelProps {
  configuration: Configuration;
  onChange: (config: Configuration) => void;
}

const ConfigurationPanel: React.FC<ConfigurationPanelProps> = ({ configuration, onChange }) => {
  const [languages, setLanguages] = useState<any>({});
  const [serviceStatus, setServiceStatus] = useState<{[key: string]: string}>({});

  useEffect(() => {
    // Fetch supported languages
    fetch('http://localhost:8000/api/languages')
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          setLanguages(data.data);
        }
      })
      .catch(console.error);
  }, []);

  const updateConfiguration = (updates: Partial<Configuration>) => {
    onChange({ ...configuration, ...updates });
  };

  const translationLanguages = [
    'Spanish', 'French', 'German', 'Italian', 'Portuguese', 'Russian', 'Japanese',
    'Chinese (Simplified)', 'Korean', 'Hindi', 'Arabic', 'Dutch', 'Turkish', 'Polish',
    'Swedish', 'Norwegian', 'Danish', 'Finnish', 'Czech', 'Hungarian', 'Bulgarian',
    'Romanian', 'Greek', 'Hebrew', 'Thai', 'Vietnamese', 'Indonesian', 'Malay',
    'Filipino', 'Ukrainian', 'Bengali', 'Tamil', 'Telugu', 'Marathi', 'Gujarati',
    'Kannada', 'Malayalam', 'Punjabi', 'Urdu', 'Persian', 'Swahili', 'Afrikaans',
    'Catalan', 'Croatian'
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-2">
        <Settings className="w-6 h-6 text-gray-600" />
        <h2 className="text-xl font-semibold text-gray-900">Configuration</h2>
      </div>

      {/* Transcription Settings */}
      <div className="bg-white rounded-lg shadow p-6 space-y-4">
        <h3 className="font-medium text-gray-900">Transcription Settings</h3>
        
        {/* Language */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Audio Language
          </label>
          <select
            value={configuration.language}
            onChange={(e) => updateConfiguration({ language: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {languages.transcription_languages && Object.entries(languages.transcription_languages).map(([name, code]) => (
              <option key={name} value={(code as string) || name}>{name}</option>
            ))}
          </select>
          <p className="text-xs text-gray-500 mt-1">
            Select the language of the audio for better accuracy
          </p>
        </div>

        {/* Number of Speakers */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Number of Speakers: {configuration.numSpeakers}
          </label>
          <input
            type="range"
            min="1"
            max="32"
            value={configuration.numSpeakers}
            onChange={(e) => updateConfiguration({ numSpeakers: parseInt(e.target.value) })}
            className="w-full"
          />
          <p className="text-xs text-gray-500 mt-1">
            Estimate the number of unique speakers (helps with diarization)
          </p>
        </div>

        {/* Advanced Options */}
        <div className="space-y-3">
          <div className="flex items-center">
            <input
              type="checkbox"
              id="diarize"
              checked={configuration.diarize}
              onChange={(e) => updateConfiguration({ diarize: e.target.checked })}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="diarize" className="ml-2 text-sm text-gray-700">
              Speaker Diarization
            </label>
          </div>
          
          <div className="flex items-center">
            <input
              type="checkbox"
              id="tagAudioEvents"
              checked={configuration.tagAudioEvents}
              onChange={(e) => updateConfiguration({ tagAudioEvents: e.target.checked })}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="tagAudioEvents" className="ml-2 text-sm text-gray-700">
              Tag Audio Events (laughter, applause, etc.)
            </label>
          </div>
        </div>
      </div>

      {/* Translation Settings */}
      <div className="bg-white rounded-lg shadow p-6 space-y-4">
        <div className="flex items-center space-x-2">
          <Globe className="w-5 h-5 text-green-600" />
          <h3 className="font-medium text-gray-900">Multi-language Translation</h3>
        </div>
        
        <div className="flex items-center">
          <input
            type="checkbox"
            id="enableTranslation"
            checked={configuration.enableTranslation}
            onChange={(e) => updateConfiguration({ enableTranslation: e.target.checked })}
            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          />
          <label htmlFor="enableTranslation" className="ml-2 text-sm text-gray-700">
            Enable Subtitle Translation
          </label>
        </div>

        {configuration.enableTranslation && (
          <div className="space-y-4 pl-6 border-l-2 border-blue-100">
            {/* Translation Service */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Translation Service
              </label>
              <select
                value={configuration.translationService}
                onChange={(e) => updateConfiguration({ translationService: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="google_free">🟢 Google Translate (Free)</option>
                <option value="gemini">🤖 Google Gemini AI (API Key Required)</option>
                <option value="libre">🟡 LibreTranslate (Free)</option>
                <option value="azure">🔑 Azure Translator (API Key Required)</option>
              </select>
              <div className="text-xs text-gray-500 mt-1">
                {configuration.translationService === 'google_free' && (
                  <p>🔄 Good quality, may have rate limits</p>
                )}
                {configuration.translationService === 'gemini' && (
                  <p>🤖 AI-powered translation with context awareness</p>
                )}
                {configuration.translationService === 'libre' && (
                  <p>🌐 Open source, may be slower</p>
                )}
                {configuration.translationService === 'azure' && (
                  <p>☁️ Premium quality, requires API key</p>
                )}
              </div>
            </div>

            {/* Gemini API Key */}
            {configuration.translationService === 'gemini' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Google Gemini API Key
                </label>
                <input
                  type="password"
                  value={configuration.translationApiKey}
                  onChange={(e) => updateConfiguration({ translationApiKey: e.target.value })}
                  placeholder="Enter your Google Gemini API key"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Get your API key from <a href="https://makersuite.google.com/app/apikey" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">Google AI Studio</a>
                </p>
              </div>
            )}

            {/* Azure API Key */}
            {configuration.translationService === 'azure' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Azure Translator API Key
                </label>
                <input
                  type="password"
                  value={configuration.translationApiKey}
                  onChange={(e) => updateConfiguration({ translationApiKey: e.target.value })}
                  placeholder="Enter your Azure Translator API key"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            )}

            {/* Target Languages */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Target Languages ({configuration.targetLanguages.length} selected)
              </label>
              <div className="grid grid-cols-2 gap-2 max-h-48 overflow-y-auto border border-gray-200 rounded-md p-3">
                {translationLanguages.map((lang) => (
                  <div key={lang} className="flex items-center">
                    <input
                      type="checkbox"
                      id={`lang-${lang}`}
                      checked={configuration.targetLanguages.includes(lang)}
                      onChange={(e) => {
                        const newLanguages = e.target.checked
                          ? [...configuration.targetLanguages, lang]
                          : configuration.targetLanguages.filter(l => l !== lang);
                        updateConfiguration({ targetLanguages: newLanguages });
                      }}
                      className="h-3 w-3 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <label htmlFor={`lang-${lang}`} className="ml-2 text-xs text-gray-700">
                      {lang}
                    </label>
                  </div>
                ))}
              </div>
              
              {configuration.targetLanguages.length > 0 && (
                <div className="mt-2 p-3 bg-green-50 border border-green-200 rounded-md">
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <p className="text-sm text-green-800">
                      Will translate to: {configuration.targetLanguages.join(', ')}
                    </p>
                  </div>
                  <p className="text-xs text-green-600 mt-1">
                    🎯 All features preserved: timestamps, speaker diarization, audio events
                  </p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Validation */}
      <div className="bg-gray-50 rounded-lg p-4">
        <h4 className="font-medium text-gray-900 mb-2">Ready to Process?</h4>
        <div className="space-y-2">
          {configuration.enableTranslation && (configuration.translationService === 'azure' || configuration.translationService === 'gemini') && (
            <div className="flex items-center space-x-2">
              {configuration.translationApiKey ? (
                <CheckCircle className="w-4 h-4 text-green-600" />
              ) : (
                <AlertCircle className="w-4 h-4 text-red-600" />
              )}
              <span className={`text-sm ${configuration.translationApiKey ? 'text-green-700' : 'text-red-700'}`}>
                {configuration.translationService === 'gemini' ? 'Google Gemini' : 'Azure Translation'} API Key
              </span>
            </div>
          )}
          
          {configuration.enableTranslation && (
            <div className="flex items-center space-x-2">
              {configuration.targetLanguages.length > 0 ? (
                <CheckCircle className="w-4 h-4 text-green-600" />
              ) : (
                <AlertCircle className="w-4 h-4 text-yellow-600" />
              )}
              <span className={`text-sm ${configuration.targetLanguages.length > 0 ? 'text-green-700' : 'text-yellow-700'}`}>
                Target Languages Selected ({configuration.targetLanguages.length})
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ConfigurationPanel;