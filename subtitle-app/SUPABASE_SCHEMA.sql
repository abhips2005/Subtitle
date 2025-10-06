-- Schema for storing subtitle generation history

-- Create subtitle_generations table
CREATE TABLE IF NOT EXISTS subtitle_generations (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  session_id TEXT UNIQUE NOT NULL,
  filename TEXT NOT NULL,
  file_type TEXT,
  duration NUMERIC,
  language TEXT,
  language_confidence NUMERIC,
  speakers_detected INTEGER,
  has_translation BOOLEAN DEFAULT FALSE,
  translation_languages TEXT[], -- Array of language codes
  srt_content TEXT,
  vtt_content TEXT,
  translated_subtitles JSONB, -- Store as {lang_code: srt_content}
  translated_vtt JSONB, -- Store as {lang_code: vtt_content}
  transcription_data JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_subtitle_generations_user_id ON subtitle_generations(user_id);
CREATE INDEX IF NOT EXISTS idx_subtitle_generations_created_at ON subtitle_generations(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_subtitle_generations_session_id ON subtitle_generations(session_id);

-- Enable Row Level Security
ALTER TABLE subtitle_generations ENABLE ROW LEVEL SECURITY;

-- Create policies
-- Users can only see their own generations
CREATE POLICY "Users can view own subtitle generations" 
  ON subtitle_generations FOR SELECT 
  USING (auth.uid() = user_id);

-- Users can insert their own generations
CREATE POLICY "Users can insert own subtitle generations" 
  ON subtitle_generations FOR INSERT 
  WITH CHECK (auth.uid() = user_id);

-- Users can update their own generations
CREATE POLICY "Users can update own subtitle generations" 
  ON subtitle_generations FOR UPDATE 
  USING (auth.uid() = user_id);

-- Users can delete their own generations
CREATE POLICY "Users can delete own subtitle generations" 
  ON subtitle_generations FOR DELETE 
  USING (auth.uid() = user_id);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_subtitle_generations_updated_at
  BEFORE UPDATE ON subtitle_generations
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
