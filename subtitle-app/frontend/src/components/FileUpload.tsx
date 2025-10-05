import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileAudio, FileVideo, AlertCircle } from 'lucide-react';

interface FileUploadProps {
  onFileUpload: (file: File) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileUpload }) => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      onFileUpload(acceptedFiles[0]);
    }
  }, [onFileUpload]);

  const { getRootProps, getInputProps, isDragActive, fileRejections } = useDropzone({
    onDrop,
    accept: {
      'audio/*': ['.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg'],
      'video/*': ['.mp4', '.mov', '.avi', '.mkv', '.webm']
    },
    maxFiles: 1,
    maxSize: 3 * 1024 * 1024 * 1024, // 3GB
  });

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          Upload Your Audio or Video File
        </h2>
        <p className="text-lg text-gray-600">
          Generate subtitles with speech diarization and timestamps
        </p>
      </div>

      <div
        {...getRootProps()}
        className={`
          relative border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors
          ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}
        `}
      >
        <input {...getInputProps()} />
        
        <div className="space-y-4">
          <div className="flex justify-center">
            {isDragActive ? (
              <Upload className="w-16 h-16 text-blue-500 animate-bounce" />
            ) : (
              <div className="flex space-x-4">
                <FileAudio className="w-12 h-12 text-green-600" />
                <FileVideo className="w-12 h-12 text-blue-600" />
              </div>
            )}
          </div>
          
          <div>
            <p className="text-xl font-medium text-gray-900">
              {isDragActive ? 'Drop your file here' : 'Drag & drop your file here'}
            </p>
            <p className="text-gray-600 mt-2">
              or click to browse your files
            </p>
          </div>

          <div className="text-sm text-gray-500 space-y-1">
            <p><strong>Supported formats:</strong></p>
            <p>Audio: MP3, WAV, FLAC, M4A, AAC, OGG</p>
            <p>Video: MP4, MOV, AVI, MKV, WEBM</p>
            <p>Max size: 3GB, up to 10 hours</p>
          </div>
        </div>
      </div>

      {fileRejections.length > 0 && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center space-x-2">
            <AlertCircle className="w-5 h-5 text-red-500" />
            <h3 className="font-medium text-red-800">File Upload Error</h3>
          </div>
          {fileRejections.map(({ file, errors }) => (
            <div key={file.name} className="mt-2">
              <p className="text-sm text-red-700">
                <strong>{file.name}</strong>
              </p>
              <ul className="text-sm text-red-600 ml-4">
                {errors.map(error => (
                  <li key={error.code}>• {error.message}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="font-medium text-blue-800 mb-2">What you'll get:</h3>
        <ul className="text-sm text-blue-700 space-y-1">
          <li>• High-accuracy transcription with timestamps</li>
          <li>• Speaker diarization (identify who's speaking)</li>
          <li>• Audio event tagging (laughter, applause, etc.)</li>
          <li>• Multiple subtitle formats (SRT, VTT)</li>
          <li>• Multi-language translation (40+ languages)</li>
          <li>• Video player with synchronized subtitles</li>
        </ul>
      </div>
    </div>
  );
};

export default FileUpload;