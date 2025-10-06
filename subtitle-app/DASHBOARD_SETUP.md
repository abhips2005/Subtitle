# Dashboard Setup Guide

This guide explains how to set up the new Dashboard feature that allows users to view their past subtitle generations and download subtitle files.

## Features Added

1. **Dashboard View**: Users can see all their past subtitle generations
2. **Download History**: Download subtitle files (SRT/VTT) from past generations
3. **Translation Access**: Access and download translated subtitles
4. **Delete Generations**: Remove unwanted subtitle generations
5. **Metadata Display**: View video/audio info (duration, language, speakers)

## Setup Instructions

### 1. Database Setup (Supabase)

First, create the necessary table in your Supabase database:

1. Go to your Supabase project dashboard
2. Navigate to the SQL Editor
3. Run the SQL script from `SUPABASE_SCHEMA.sql`:

```sql
-- This creates the subtitle_generations table with proper RLS policies
```

The script creates:
- `subtitle_generations` table with all necessary columns
- Row Level Security (RLS) policies for user data protection
- Indexes for better query performance
- Auto-update triggers for `updated_at` timestamp

### 2. Backend Setup

1. **Install Dependencies**:
   ```bash
   cd subtitle-app/backend
   pip install supabase==2.3.4
   ```

2. **Environment Variables**:
   Make sure your `.env` file has Supabase credentials:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

3. **Backend Changes**:
   - The backend now saves subtitle generations to Supabase automatically
   - When a user generates subtitles, the data is stored with their `user_id`
   - Both transcription and translation data are saved

### 3. Frontend Setup

The frontend has been updated with:

1. **New Dashboard Component**: `Dashboard.tsx`
   - Displays all user's subtitle generations
   - Provides download buttons for each format
   - Shows metadata (duration, language, speakers, date)
   - Allows deletion of generations

2. **Navigation**: 
   - "Dashboard" button in header (when logged in)
   - "Back to Generator" button in dashboard
   - Seamless navigation between views

3. **No additional dependencies needed** - uses existing Supabase client

## How It Works

### For Logged-in Users:

1. **Generate Subtitles**:
   - Upload video/audio file
   - Configure transcription settings
   - Generate subtitles (with optional translation)
   - Data is automatically saved to Supabase with user's ID

2. **View Dashboard**:
   - Click "Dashboard" button in header
   - See all past subtitle generations
   - Each entry shows:
     - Filename
     - Creation date
     - Duration
     - Language detected
     - Number of speakers
     - Available translations

3. **Download Subtitles**:
   - Click SRT or VTT button for original subtitles
   - Click language-specific buttons for translations
   - Files download with proper naming (e.g., `video_Spanish.srt`)

4. **Delete Generations**:
   - Click trash icon on any generation
   - Confirm deletion
   - Entry removed from database

### For Anonymous Users:

- Can still use the subtitle generator
- Subtitles are NOT saved to database
- No access to dashboard (Dashboard button not shown)
- Data is session-based only

## Security Features

1. **Row Level Security (RLS)**:
   - Users can only see their own subtitle generations
   - Users cannot access other users' data
   - Enforced at database level

2. **Authentication**:
   - Dashboard requires user authentication
   - Unauthenticated users cannot access saved generations
   - User ID is verified on backend

3. **Data Privacy**:
   - Subtitle content stored securely in Supabase
   - Only accessible by the user who created it
   - Can be deleted by user at any time

## Database Schema

### `subtitle_generations` Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `user_id` | UUID | Foreign key to auth.users |
| `session_id` | TEXT | Unique session identifier |
| `filename` | TEXT | Original filename |
| `file_type` | TEXT | video or audio |
| `duration` | NUMERIC | Duration in seconds |
| `language` | TEXT | Detected language |
| `language_confidence` | NUMERIC | Language detection confidence |
| `speakers_detected` | INTEGER | Number of speakers |
| `has_translation` | BOOLEAN | Whether translations exist |
| `translation_languages` | TEXT[] | Array of translated languages |
| `srt_content` | TEXT | Original SRT subtitle content |
| `vtt_content` | TEXT | Original VTT subtitle content |
| `translated_subtitles` | JSONB | Translated SRT files by language |
| `translated_vtt` | JSONB | Translated VTT files by language |
| `transcription_data` | JSONB | Full transcription metadata |
| `created_at` | TIMESTAMP | Creation timestamp |
| `updated_at` | TIMESTAMP | Last update timestamp |

## API Changes

### `/api/transcribe` Endpoint

**New Parameter**:
- `user_id` (optional): User ID for saving to database

**Behavior**:
- If `user_id` provided: Saves generation to Supabase
- If no `user_id`: Works as before (session-only)

### `/api/translate` Endpoint

**New Parameter**:
- `user_id` (optional): User ID for updating database record

**Behavior**:
- If `user_id` provided: Updates Supabase record with translations
- If no `user_id`: Works as before (session-only)

## Testing the Feature

1. **Sign Up/Login**:
   - Create an account or sign in
   - Should see "Dashboard" button appear

2. **Generate Subtitle**:
   - Upload a test video/audio file
   - Generate subtitles
   - Optionally add translations

3. **Check Dashboard**:
   - Click "Dashboard" button
   - Should see your generation listed
   - Try downloading SRT and VTT files

4. **Test Translation Downloads**:
   - If you added translations, verify download buttons appear
   - Download and verify file contents

5. **Test Deletion**:
   - Click trash icon
   - Confirm deletion
   - Verify entry is removed

## Troubleshooting

### "Failed to load your subtitle history"

**Possible causes**:
1. Supabase credentials incorrect
2. Table not created
3. RLS policies not set up

**Solution**: Verify Supabase setup and run schema script

### Downloads not working

**Possible causes**:
1. Content not saved properly
2. JSONB structure incorrect

**Solution**: Check browser console for errors

### Data not appearing in dashboard

**Possible causes**:
1. User not logged in
2. Subtitles generated before login
3. user_id not sent to backend

**Solution**: 
- Ensure user is logged in before generating subtitles
- Check browser developer tools network tab to verify user_id in request

## Future Enhancements

Potential improvements:
1. Search and filter generations
2. Pagination for large lists
3. Bulk download option
4. Share subtitle files with other users
5. Statistics and analytics
6. Export history as CSV
7. Video thumbnail previews
8. Tag/categorize generations

## Support

If you encounter issues:
1. Check Supabase connection
2. Verify table schema
3. Check browser console for errors
4. Ensure backend dependencies installed
5. Verify authentication is working
