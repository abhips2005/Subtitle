import React, { useState } from 'react';
import { Download, FileText, Clock, Users, Languages } from 'lucide-react';
import { TranscriptionData } from '../types';

interface TranscriptionDisplayProps {
  data: TranscriptionData;
  onDownload: (format: string, language?: string) => void;
}

const TranscriptionDisplay: React.FC<TranscriptionDisplayProps> = ({ data, onDownload }) => {
  const [activeTab, setActiveTab] = useState<'preview' | 'srt' | 'vtt' | 'timeline'>('preview');

  const parseSubtitles = (srtContent: string) => {
    const subtitles = [];
    const blocks = srtContent.split('\n\n');
    
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

  const subtitles = parseSubtitles(data.srt_content);

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="p-6 border-b border-gray-200">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Generated Subtitles</h2>
        
        {/* Statistics */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div className="text-center p-3 bg-blue-50 rounded-lg">
            <Languages className="w-5 h-5 text-blue-600 mx-auto mb-1" />
            <p className="text-sm font-medium text-blue-900">{data.language}</p>
            <p className="text-xs text-blue-600">Language</p>
          </div>
          
          <div className="text-center p-3 bg-green-50 rounded-lg">
            <Users className="w-5 h-5 text-green-600 mx-auto mb-1" />
            <p className="text-sm font-medium text-green-900">{data.speakers_detected}</p>
            <p className="text-xs text-green-600">Speakers</p>
          </div>
          
          <div className="text-center p-3 bg-purple-50 rounded-lg">
            <FileText className="w-5 h-5 text-purple-600 mx-auto mb-1" />
            <p className="text-sm font-medium text-purple-900">{subtitles.length}</p>
            <p className="text-xs text-purple-600">Subtitles</p>
          </div>
          
          <div className="text-center p-3 bg-orange-50 rounded-lg">
            <Clock className="w-5 h-5 text-orange-600 mx-auto mb-1" />
            <p className="text-sm font-medium text-orange-900">{data.duration.toFixed(1)}s</p>
            <p className="text-xs text-orange-600">Duration</p>
          </div>
        </div>

        {/* Confidence Score */}
        <div className="mb-4">
          <div className="flex justify-between items-center mb-1">
            <span className="text-sm font-medium text-gray-700">Confidence Score</span>
            <span className="text-sm text-gray-600">{(data.confidence * 100).toFixed(1)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-blue-600 h-2 rounded-full transition-all duration-300" 
              style={{ width: `${data.confidence * 100}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="flex space-x-8 px-6">
          {[
            { id: 'preview', label: 'Preview', icon: FileText },
            { id: 'srt', label: 'SRT Format', icon: Download },
            { id: 'vtt', label: 'VTT Format', icon: Download },
            { id: 'timeline', label: 'Timeline', icon: Clock }
          ].map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setActiveTab(id as any)}
              className={`py-3 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                activeTab === id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{label}</span>
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="p-6">
        {activeTab === 'preview' && (
          <div className="space-y-4 max-h-96 overflow-y-auto">
            {subtitles.slice(0, 20).map((subtitle, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <span className="text-xs font-medium text-gray-500">#{subtitle.id}</span>
                  <span className="text-xs text-gray-500">{subtitle.timestamp}</span>
                </div>
                <p className="text-gray-900">{subtitle.text}</p>
              </div>
            ))}
            
            {subtitles.length > 20 && (
              <div className="text-center py-4">
                <p className="text-gray-500">
                  Showing first 20 subtitles. Total: {subtitles.length}
                </p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'srt' && (
          <div>
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-medium text-gray-900">SRT Format</h3>
              <button
                onClick={() => onDownload('srt')}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                <Download className="w-4 h-4" />
                <span>Download SRT</span>
              </button>
            </div>
            <textarea
              value={data.srt_content}
              readOnly
              className="w-full h-80 p-3 border border-gray-300 rounded-md font-mono text-sm bg-gray-50"
            />
          </div>
        )}

        {activeTab === 'vtt' && (
          <div>
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-medium text-gray-900">VTT Format</h3>
              <button
                onClick={() => onDownload('vtt')}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                <Download className="w-4 h-4" />
                <span>Download VTT</span>
              </button>
            </div>
            <textarea
              value={data.vtt_content}
              readOnly
              className="w-full h-80 p-3 border border-gray-300 rounded-md font-mono text-sm bg-gray-50"
            />
          </div>
        )}

        {activeTab === 'timeline' && (
          <div>
            <h3 className="font-medium text-gray-900 mb-4">Subtitle Timeline</h3>
            <div className="space-y-2 max-h-80 overflow-y-auto">
              <div className="grid grid-cols-12 gap-2 text-xs font-medium text-gray-500 pb-2 border-b">
                <div className="col-span-1">Index</div>
                <div className="col-span-2">Start</div>
                <div className="col-span-2">End</div>
                <div className="col-span-2">Duration</div>
                <div className="col-span-5">Text</div>
              </div>
              
              {subtitles.slice(0, 20).map((subtitle, index) => {
                const timeMatch = subtitle.timestamp.match(/(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})/);
                const startTime = timeMatch ? timeMatch[1] : '';
                const endTime = timeMatch ? timeMatch[2] : '';
                const duration = timeMatch ? 'N/A' : '';
                
                return (
                  <div key={index} className="grid grid-cols-12 gap-2 text-xs py-2 border-b border-gray-100">
                    <div className="col-span-1 font-medium">#{subtitle.id}</div>
                    <div className="col-span-2 text-gray-600">{startTime}</div>
                    <div className="col-span-2 text-gray-600">{endTime}</div>
                    <div className="col-span-2 text-gray-600">{duration}</div>
                    <div className="col-span-5 text-gray-900 truncate" title={subtitle.text}>
                      {subtitle.text}
                    </div>
                  </div>
                );
              })}
            </div>
            
            {subtitles.length > 20 && (
              <p className="text-sm text-gray-500 mt-4 text-center">
                Showing first 20 subtitles. Total: {subtitles.length}
              </p>
            )}
          </div>
        )}
      </div>

      {/* Export Options */}
      <div className="border-t border-gray-200 px-6 py-4">
        <h4 className="font-medium text-gray-900 mb-3">Export Options</h4>
        <div className="flex space-x-3">
          <button
            onClick={() => onDownload('srt')}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            <Download className="w-4 h-4" />
            <span>Download SRT</span>
          </button>
          
          <button
            onClick={() => onDownload('vtt')}
            className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
          >
            <Download className="w-4 h-4" />
            <span>Download VTT</span>
          </button>
          
          <button
            onClick={() => onDownload('json')}
            className="flex items-center space-x-2 px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
          >
            <Download className="w-4 h-4" />
            <span>Download JSON</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default TranscriptionDisplay;