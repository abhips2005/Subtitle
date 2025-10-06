import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL || 'https://yamrdbzujegsnxcznyio.supabase.co';
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlhbXJkYnp1amVnc254Y3pueWlvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk2NjMwNjYsImV4cCI6MjA3NTIzOTA2Nn0.SyL9_Uz1WiAGSA0XtYJGsILj6iLwUUeHv3S5cnlUBV0';

if (!supabaseUrl || !supabaseAnonKey) {
  console.warn('Supabase credentials not found. Please set REACT_APP_SUPABASE_URL and REACT_APP_SUPABASE_ANON_KEY in your .env file');
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
