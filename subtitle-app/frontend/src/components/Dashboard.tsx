import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { supabase } from '../lib/supabase';
import { Download, FileVideo, Calendar, Clock, Globe, Users, Trash2, FileText, AlertCircle, ArrowLeft } from 'lucide-react';

interface SubtitleGeneration {
  id: string;
  session_id: string;
  filename: string;
  file_type: string;
  duration: number;
  language: string;
  language_confidence: number;
  speakers_detected: number;
  has_translation: boolean;
  translation_languages: string[];
  srt_content: string;
  vtt_content: string;
  translated_subtitles: Record<string, string>;
  translated_vtt: Record<string, string>;
  created_at: string;
}

interface DashboardProps {
  onNavigateToGenerator?: () => void;
}

const Dashboard: React.FC<DashboardProps> = ({ onNavigateToGenerator }) => {
  const { user } = useAuth();
  const [generations, setGenerations] = useState<SubtitleGeneration[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (user) {
      fetchGenerations();
    }
  }, [user]);

  const fetchGenerations = async () => {
    try {
      setLoading(true);
      setError(null);

      const { data, error: fetchError } = await supabase
        .from('subtitle_generations')
        .select('*')
        .eq('user_id', user?.id)
        .order('created_at', { ascending: false });

      if (fetchError) {
        throw fetchError;
      }

      setGenerations(data || []);
    } catch (err) {
      console.error('Error fetching generations:', err);
      setError('Failed to load your subtitle history. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const downloadSubtitle = (content: string, filename: string, format: string) => {
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = `${filename}.${format}`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  };

  const deleteGeneration = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this subtitle generation?')) {
      return;
    }

    try {
      const { error: deleteError } = await supabase
        .from('subtitle_generations')
        .delete()
        .eq('id', id);

      if (deleteError) {
        throw deleteError;
      }

      setGenerations(generations.filter(g => g.id !== id));
    } catch (err) {
      console.error('Error deleting generation:', err);
      alert('Failed to delete. Please try again.');
    }
  };

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your subtitle history...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center max-w-md">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={fetchGenerations}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b mb-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between py-6">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                <FileVideo className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  My Subtitle Dashboard
                </h1>
                <p className="text-sm text-gray-600">
                  View and manage your subtitle generations
                </p>
              </div>
            </div>
            {onNavigateToGenerator && (
              <button
                onClick={onNavigateToGenerator}
                className="flex items-center space-x-2 px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
              >
                <ArrowLeft className="w-5 h-5" />
                <span className="font-medium">Back to Generator</span>
              </button>
            )}
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {generations.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <FileVideo className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No subtitle generations yet</h3>
          <p className="text-gray-600 mb-6">Start by uploading a video or audio file to generate subtitles</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6">
          {generations.map((generation) => (
            <div key={generation.id} className="bg-white rounded-lg shadow hover:shadow-md transition-shadow">
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-start space-x-4 flex-1">
                    <div className="flex-shrink-0">
                      <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                        <FileVideo className="w-6 h-6 text-blue-600" />
                      </div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="text-lg font-semibold text-gray-900 truncate mb-1">
                        {generation.filename}
                      </h3>
                      <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                        <div className="flex items-center space-x-1">
                          <Calendar className="w-4 h-4" />
                          <span>{formatDate(generation.created_at)}</span>
                        </div>
                        {generation.duration && (
                          <div className="flex items-center space-x-1">
                            <Clock className="w-4 h-4" />
                            <span>{formatDuration(generation.duration)}</span>
                          </div>
                        )}
                        {generation.language && (
                          <div className="flex items-center space-x-1">
                            <Globe className="w-4 h-4" />
                            <span>{generation.language}</span>
                          </div>
                        )}
                        {generation.speakers_detected > 0 && (
                          <div className="flex items-center space-x-1">
                            <Users className="w-4 h-4" />
                            <span>{generation.speakers_detected} speaker(s)</span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                  <button
                    onClick={() => deleteGeneration(generation.id)}
                    className="flex-shrink-0 p-2 text-red-600 hover:bg-red-50 rounded-md transition-colors"
                    title="Delete generation"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>

                {/* Download Section */}
                <div className="border-t pt-4">
                  <h4 className="text-sm font-semibold text-gray-900 mb-3 flex items-center">
                    <Download className="w-4 h-4 mr-2" />
                    Download Subtitles
                  </h4>
                  
                  {/* Original Subtitles */}
                  <div className="mb-3">
                    <p className="text-xs text-gray-600 mb-2">Original ({generation.language})</p>
                    <div className="flex flex-wrap gap-2">
                      <button
                        onClick={() => downloadSubtitle(
                          generation.srt_content,
                          generation.filename.replace(/\.[^/.]+$/, ''),
                          'srt'
                        )}
                        className="inline-flex items-center px-3 py-1.5 text-sm font-medium text-blue-600 bg-blue-50 rounded-md hover:bg-blue-100 transition-colors"
                      >
                        <FileText className="w-4 h-4 mr-1" />
                        SRT
                      </button>
                      <button
                        onClick={() => downloadSubtitle(
                          generation.vtt_content,
                          generation.filename.replace(/\.[^/.]+$/, ''),
                          'vtt'
                        )}
                        className="inline-flex items-center px-3 py-1.5 text-sm font-medium text-green-600 bg-green-50 rounded-md hover:bg-green-100 transition-colors"
                      >
                        <FileText className="w-4 h-4 mr-1" />
                        VTT
                      </button>
                    </div>
                  </div>

                  {/* Translated Subtitles */}
                  {generation.has_translation && generation.translation_languages?.length > 0 && (
                    <div>
                      <p className="text-xs text-gray-600 mb-2">Translations</p>
                      <div className="space-y-2">
                        {generation.translation_languages.map((lang) => (
                          <div key={lang} className="flex items-center space-x-2">
                            <span className="text-sm text-gray-700 min-w-[100px]">{lang}</span>
                            <div className="flex gap-2">
                              {generation.translated_subtitles?.[lang] && (
                                <button
                                  onClick={() => downloadSubtitle(
                                    generation.translated_subtitles[lang],
                                    `${generation.filename.replace(/\.[^/.]+$/, '')}_${lang}`,
                                    'srt'
                                  )}
                                  className="inline-flex items-center px-2 py-1 text-xs font-medium text-blue-600 bg-blue-50 rounded hover:bg-blue-100 transition-colors"
                                >
                                  <FileText className="w-3 h-3 mr-1" />
                                  SRT
                                </button>
                              )}
                              {generation.translated_vtt?.[lang] && (
                                <button
                                  onClick={() => downloadSubtitle(
                                    generation.translated_vtt[lang],
                                    `${generation.filename.replace(/\.[^/.]+$/, '')}_${lang}`,
                                    'vtt'
                                  )}
                                  className="inline-flex items-center px-2 py-1 text-xs font-medium text-green-600 bg-green-50 rounded hover:bg-green-100 transition-colors"
                                >
                                  <FileText className="w-3 h-3 mr-1" />
                                  VTT
                                </button>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
      </div>
    </div>
  );
};

export default Dashboard;