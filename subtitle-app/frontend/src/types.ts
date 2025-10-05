export interface TranscriptionData {
  session_id: string;
  language: string;
  confidence: number;
  speakers_detected: number;
  duration: number;
  srt_content: string;
  vtt_content: string;
  transcription: any;
}

export interface TranslationData {
  translated_subtitles: { [language: string]: string };
  translated_vtt: { [language: string]: string };
  success_count: number;
  total_requested: number;
}

export interface ApiResponse {
  success: boolean;
  message: string;
  data: any;
}

export interface Configuration {
  apiKey: string;
  language: string;
  numSpeakers: number;
  diarize: boolean;
  tagAudioEvents: boolean;
  enableTranslation: boolean;
  translationService: string;
  targetLanguages: string[];
  translationApiKey: string;
}

export interface Language {
  [key: string]: string | null;
}

export interface SubtitleEntry {
  id: number;
  start: number;
  end: number;
  text: string;
}