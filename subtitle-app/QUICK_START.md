# Quick Start: Dashboard Feature

## Prerequisites
✅ Supabase account
✅ Backend and frontend already set up
✅ User authentication working

## Setup (5 minutes)

### Step 1: Create Database Table
1. Open your Supabase dashboard
2. Go to **SQL Editor**
3. Copy and paste the contents of `SUPABASE_SCHEMA.sql`
4. Click **Run**
5. Verify the table was created in the **Table Editor**

### Step 2: Verify Environment Variables
Make sure your `.env` file in the backend has:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
```

### Step 3: Restart Backend
```bash
cd subtitle-app/backend
python main.py
```

### Step 4: Start Frontend (if not running)
```bash
cd subtitle-app/frontend
npm start
```

## Testing (2 minutes)

### 1. Login
- Click "Sign In" button
- Log in with your credentials

### 2. Generate a Subtitle
- Upload a video/audio file
- Click "Generate Subtitles"
- Wait for processing to complete

### 3. Access Dashboard
- Click "Dashboard" button in header
- You should see your generated subtitle
- Try downloading SRT/VTT files

### 4. Test Delete
- Click trash icon
- Confirm deletion
- Item should disappear

## ✅ Success Indicators

You'll know it's working when:
- ✅ "Dashboard" button appears after login
- ✅ Dashboard shows your subtitle generations
- ✅ Download buttons work
- ✅ Delete function works
- ✅ Metadata displays correctly (date, duration, language)

## ❌ Troubleshooting

### Dashboard shows "Failed to load"
**Fix:** Run the SQL schema script in Supabase

### Generations not appearing
**Fix:** Make sure you're logged in when generating subtitles

### Downloads not working
**Fix:** Check browser console for errors

## What's New?

### For Users:
- 📊 **Dashboard**: View all past subtitle generations
- 💾 **Download**: Get subtitle files anytime (SRT/VTT)
- 🌍 **Translations**: Access all translated versions
- 🗑️ **Delete**: Remove unwanted generations
- 📝 **Metadata**: See duration, language, speakers, date

### For Developers:
- 🗄️ **Database**: Supabase table for persistent storage
- 🔒 **Security**: Row Level Security policies
- 🔄 **Auto-save**: Automatic saving when user is authenticated
- 📡 **API**: Updated endpoints to accept user_id

## Feature Highlights

### Dashboard View
```
┌─────────────────────────────────────────┐
│ 📹 My Subtitle Dashboard               │
├─────────────────────────────────────────┤
│                                         │
│  📹 video.mp4                           │
│  📅 Jan 15, 2025  ⏱️ 2:30  🌍 English   │
│  👥 2 speakers                          │
│                                         │
│  💾 Download Subtitles                 │
│  Original: [SRT] [VTT]                 │
│  Spanish: [SRT] [VTT]                  │
│  French: [SRT] [VTT]                   │
│                                         │
└─────────────────────────────────────────┘
```

## Video Walkthrough

1. **Login** → "Dashboard" button appears
2. **Generate** → Upload video → Process
3. **Dashboard** → View generation
4. **Download** → Click format buttons
5. **Delete** → Click trash → Confirm

## Next Steps

After setup, users can:
1. Generate subtitles as usual
2. Access dashboard anytime
3. Download past generations
4. Delete unwanted items
5. See all translations

## Support

- 📖 Full documentation: `DASHBOARD_SETUP.md`
- 🔧 Implementation details: `DASHBOARD_IMPLEMENTATION.md`
- 🗄️ Database schema: `SUPABASE_SCHEMA.sql`

## Notes

- ✅ Works with existing subtitle generator
- ✅ No breaking changes
- ✅ Anonymous users unaffected
- ✅ Optional feature (requires login)
- ✅ Secure (Row Level Security)
