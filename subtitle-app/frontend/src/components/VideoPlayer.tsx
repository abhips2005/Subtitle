import React, { useState, useRef, useEffect } from 'react';
import { Play, Pause, Volume2, Settings, RotateCcw } from 'lucide-react';

interface VideoPlayerProps {
  videoFile: File;
  subtitles: string;
  translatedSubtitles?: { [language: string]: string };
}

interface SubtitleEntry {
  id: number;
  start: number;
  end: number;
  text: string;
}

const VideoPlayer: React.FC<VideoPlayerProps> = ({ videoFile, subtitles, translatedSubtitles }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(1);
  const [selectedLanguage, setSelectedLanguage] = useState('original');
  const [showSubtitles, setShowSubtitles] = useState(true);
  const [currentSubtitle, setCurrentSubtitle] = useState<SubtitleEntry | null>(null);
  const [parsedSubtitles, setParsedSubtitles] = useState<SubtitleEntry[]>([]);
  const [videoUrl, setVideoUrl] = useState<string>('');

  // Create and cleanup video URL
  useEffect(() => {
    const url = URL.createObjectURL(videoFile);
    setVideoUrl(url);
    
    // Cleanup function to revoke the URL when component unmounts
    return () => {
      URL.revokeObjectURL(url);
    };
  }, [videoFile]);

  // Parse SRT content to subtitle entries
  const parseSubtitles = (srtContent: string): SubtitleEntry[] => {
    const entries: SubtitleEntry[] = [];
    const blocks = srtContent.split('\n\n');

    for (const block of blocks) {
      if (block.trim()) {
        const lines = block.trim().split('\n');
        if (lines.length >= 3) {
          const id = parseInt(lines[0]);
          const timeMatch = lines[1].match(/(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})/);
          
          if (timeMatch) {
            const startTime = 
              parseInt(timeMatch[1]) * 3600 + 
              parseInt(timeMatch[2]) * 60 + 
              parseInt(timeMatch[3]) + 
              parseInt(timeMatch[4]) / 1000;
            
            const endTime = 
              parseInt(timeMatch[5]) * 3600 + 
              parseInt(timeMatch[6]) * 60 + 
              parseInt(timeMatch[7]) + 
              parseInt(timeMatch[8]) / 1000;

            const text = lines.slice(2).join('\n');
            
            entries.push({
              id,
              start: startTime,
              end: endTime,
              text
            });
          }
        }
      }
    }

    return entries.sort((a, b) => a.start - b.start);
  };

  // Update parsed subtitles when language changes
  useEffect(() => {
    let currentSrtContent = subtitles;
    
    if (selectedLanguage !== 'original' && translatedSubtitles && translatedSubtitles[selectedLanguage]) {
      currentSrtContent = translatedSubtitles[selectedLanguage];
    }
    
    setParsedSubtitles(parseSubtitles(currentSrtContent));
  }, [selectedLanguage, subtitles, translatedSubtitles]);

  // Update current subtitle based on video time
  useEffect(() => {
    const currentSub = parsedSubtitles.find(
      sub => currentTime >= sub.start && currentTime <= sub.end
    );
    setCurrentSubtitle(currentSub || null);
  }, [currentTime, parsedSubtitles]);

  const togglePlay = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause();
      } else {
        videoRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleTimeUpdate = () => {
    if (videoRef.current) {
      setCurrentTime(videoRef.current.currentTime);
    }
  };

  const handleLoadedMetadata = () => {
    if (videoRef.current) {
      setDuration(videoRef.current.duration);
    }
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const time = parseFloat(e.target.value);
    if (videoRef.current) {
      videoRef.current.currentTime = time;
      setCurrentTime(time);
    }
  };

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const vol = parseFloat(e.target.value);
    setVolume(vol);
    if (videoRef.current) {
      videoRef.current.volume = vol;
    }
  };

  const formatTime = (time: number) => {
    const hours = Math.floor(time / 3600);
    const minutes = Math.floor((time % 3600) / 60);
    const seconds = Math.floor(time % 60);
    
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const availableLanguages = ['original', ...(translatedSubtitles ? Object.keys(translatedSubtitles) : [])];

  return (
    <div className="bg-black rounded-lg overflow-hidden">
      {/* Video Container */}
      <div className="relative">
        <video
          ref={videoRef}
          src={videoUrl}
          onTimeUpdate={handleTimeUpdate}
          onLoadedMetadata={handleLoadedMetadata}
          onPlay={() => setIsPlaying(true)}
          onPause={() => setIsPlaying(false)}
          className="w-full h-auto"
          style={{ maxHeight: '500px' }}
        />
        
        {/* Subtitle Overlay */}
        {showSubtitles && currentSubtitle && (
          <div className="absolute bottom-16 left-0 right-0 text-center px-4">
            <div className="inline-block bg-black bg-opacity-75 text-white px-4 py-2 rounded-lg max-w-4xl">
              <p className="text-lg leading-relaxed whitespace-pre-line">
                {currentSubtitle.text}
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Controls */}
      <div className="bg-gray-900 text-white p-4 space-y-3">
        {/* Progress Bar */}
        <div className="flex items-center space-x-3">
          <span className="text-sm text-gray-300 min-w-[50px]">
            {formatTime(currentTime)}
          </span>
          <input
            type="range"
            min="0"
            max={duration || 0}
            value={currentTime}
            onChange={handleSeek}
            className="flex-1 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
            style={{
              background: `linear-gradient(to right, #3B82F6 0%, #3B82F6 ${(currentTime / duration) * 100}%, #374151 ${(currentTime / duration) * 100}%, #374151 100%)`
            }}
          />
          <span className="text-sm text-gray-300 min-w-[50px]">
            {formatTime(duration)}
          </span>
        </div>

        {/* Control Buttons */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            {/* Play/Pause */}
            <button
              onClick={togglePlay}
              className="flex items-center justify-center w-10 h-10 bg-blue-600 rounded-full hover:bg-blue-700 transition-colors"
            >
              {isPlaying ? (
                <Pause className="w-5 h-5" />
              ) : (
                <Play className="w-5 h-5 ml-0.5" />
              )}
            </button>

            {/* Volume */}
            <div className="flex items-center space-x-2">
              <Volume2 className="w-5 h-5 text-gray-300" />
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={volume}
                onChange={handleVolumeChange}
                className="w-20 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
              />
            </div>

            {/* Subtitle Toggle */}
            <button
              onClick={() => setShowSubtitles(!showSubtitles)}
              className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
                showSubtitles 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              Subtitles
            </button>
          </div>

          <div className="flex items-center space-x-4">
            {/* Language Selector */}
            {availableLanguages.length > 1 && (
              <div className="flex items-center space-x-2">
                <Settings className="w-4 h-4 text-gray-300" />
                <select
                  value={selectedLanguage}
                  onChange={(e) => setSelectedLanguage(e.target.value)}
                  className="bg-gray-700 text-white border border-gray-600 rounded px-2 py-1 text-sm"
                >
                  <option value="original">Original</option>
                  {translatedSubtitles && Object.keys(translatedSubtitles).map(lang => (
                    <option key={lang} value={lang}>{lang}</option>
                  ))}
                </select>
              </div>
            )}

            {/* Reset */}
            <button
              onClick={() => {
                if (videoRef.current) {
                  videoRef.current.currentTime = 0;
                  setCurrentTime(0);
                }
              }}
              className="p-2 text-gray-300 hover:text-white transition-colors"
              title="Reset to beginning"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Current Subtitle Info */}
        {currentSubtitle && (
          <div className="border-t border-gray-700 pt-3">
            <div className="flex justify-between items-start">
              <div className="text-sm text-gray-300">
                <span className="font-medium">Subtitle #{currentSubtitle.id}</span>
                <span className="ml-4">
                  {formatTime(currentSubtitle.start)} → {formatTime(currentSubtitle.end)}
                </span>
                {selectedLanguage !== 'original' && (
                  <span className="ml-4 px-2 py-1 bg-blue-600 text-white rounded text-xs">
                    {selectedLanguage}
                  </span>
                )}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Subtitle Information Panel */}
      <div className="bg-white border-t p-4">
        <div className="flex justify-between items-center mb-3">
          <h4 className="font-medium text-gray-900">Subtitle Information</h4>
          <div className="text-sm text-gray-600">
            Total subtitles: {parsedSubtitles.length}
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div>
            <span className="font-medium text-gray-700">Current Language:</span>
            <p className="text-gray-600">
              {selectedLanguage === 'original' ? 'Original' : selectedLanguage}
            </p>
          </div>
          
          <div>
            <span className="font-medium text-gray-700">Available Languages:</span>
            <p className="text-gray-600">
              {availableLanguages.length} ({availableLanguages.join(', ')})
            </p>
          </div>
          
          <div>
            <span className="font-medium text-gray-700">Features:</span>
            <p className="text-gray-600">
              Speaker diarization, timestamps, audio events
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VideoPlayer;