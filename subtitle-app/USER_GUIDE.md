# Dashboard Feature - User Experience Guide

## Before Login
```
┌────────────────────────────────────────────────────┐
│  🎬 Subtitle Generator        [Sign In] Button     │
└────────────────────────────────────────────────────┘
│                                                    │
│  Upload your video or audio file...               │
│                                                    │
```
**Note:** No dashboard access, subtitles not saved

---

## After Login
```
┌────────────────────────────────────────────────────┐
│  🎬 Subtitle Generator    [Dashboard] [User Menu]  │
└────────────────────────────────────────────────────┘
│                                                    │
│  Upload your video or audio file...               │
│                                                    │
```
**Note:** Dashboard button appears, subtitles auto-saved

---

## Dashboard - Empty State
```
┌────────────────────────────────────────────────────┐
│  📹 My Subtitle Dashboard    [← Back to Generator] │
└────────────────────────────────────────────────────┘
│                                                    │
│            📹                                      │
│    No subtitle generations yet                    │
│    Start by uploading a video or audio file       │
│                                                    │
```

---

## Dashboard - With Generations
```
┌─────────────────────────────────────────────────────────┐
│  📹 My Subtitle Dashboard       [← Back to Generator]   │
└─────────────────────────────────────────────────────────┘
│                                                         │
│  ┌───────────────────────────────────────────────┐     │
│  │ 📹 my-video.mp4                          🗑️  │     │
│  │ 📅 Oct 6, 2025  ⏱️ 2:45  🌍 English  👥 2     │     │
│  │ ─────────────────────────────────────────────│     │
│  │ 💾 Download Subtitles                        │     │
│  │ Original (English)                           │     │
│  │   [SRT]  [VTT]                              │     │
│  │                                              │     │
│  │ Translations                                 │     │
│  │   Spanish   [SRT]  [VTT]                    │     │
│  │   French    [SRT]  [VTT]                    │     │
│  └───────────────────────────────────────────────┘     │
│                                                         │
│  ┌───────────────────────────────────────────────┐     │
│  │ 📹 another-video.mp4                     🗑️  │     │
│  │ 📅 Oct 5, 2025  ⏱️ 5:12  🌍 Spanish  👥 3     │     │
│  │ ─────────────────────────────────────────────│     │
│  │ 💾 Download Subtitles                        │     │
│  │ Original (Spanish)                           │     │
│  │   [SRT]  [VTT]                              │     │
│  └───────────────────────────────────────────────┘     │
│                                                         │
```

---

## User Journey

### 1️⃣ Sign Up / Login
```
User → [Sign In Button] → Auth Modal → Login
                                      ↓
                            [Dashboard Button Appears]
```

### 2️⃣ Generate Subtitles
```
User → Upload Video → Configure → [Generate Subtitles]
                                            ↓
                                 Transcription Created
                                            ↓
                                (Optional) Translations
                                            ↓
                            ✅ Saved to Dashboard Automatically
```

### 3️⃣ Access Dashboard
```
User → [Dashboard Button] → Dashboard View
                                  ↓
                        See All Past Generations
                                  ↓
                            [Download Files]
```

### 4️⃣ Download Subtitles
```
Dashboard → Select Generation → Click [SRT] or [VTT]
                                        ↓
                                  File Downloads
                                        ↓
                            video_Spanish.srt
```

### 5️⃣ Delete Generation (Optional)
```
Dashboard → Click [🗑️] → Confirm → Generation Removed
```

---

## Features at a Glance

### 📊 Dashboard View
- **List View**: All generations in chronological order (newest first)
- **Card Layout**: Each generation in its own card
- **Responsive**: Works on desktop and mobile

### 📝 Metadata Display
Each generation shows:
- 📹 **Filename**: Original file name
- 📅 **Date**: When it was created
- ⏱️ **Duration**: Video/audio length
- 🌍 **Language**: Detected language
- 👥 **Speakers**: Number of speakers detected

### 💾 Download Options
For each generation:
- **Original**: SRT and VTT formats
- **Translations**: All translated languages
- **One-click**: Direct download, no server request needed

### 🗑️ Management
- **Delete**: Remove unwanted generations
- **Confirm**: Safety prompt before deletion
- **Instant**: Immediate UI update

---

## Button States & Colors

### Original Subtitles
```
[SRT]  → Blue button (bg-blue-50, text-blue-600)
[VTT]  → Green button (bg-green-50, text-green-600)
```

### Translation Subtitles
```
Spanish  [SRT] [VTT]  → Smaller buttons, same colors
French   [SRT] [VTT]
German   [SRT] [VTT]
```

### Navigation
```
[Dashboard]           → Blue (bg-blue-50, text-blue-600)
[← Back to Generator] → Gray border (border-gray-300)
[Sign In]             → Solid blue (bg-blue-600, text-white)
```

### Delete
```
[🗑️]  → Red on hover (text-red-600, hover:bg-red-50)
```

---

## Interactive Elements

### Hover Effects
- **Cards**: Shadow increases on hover
- **Buttons**: Background color darkens slightly
- **Delete Icon**: Red background appears

### Click Actions
- **Download Buttons**: Initiates file download
- **Delete Icon**: Opens confirmation dialog
- **Navigation**: Switches between views

---

## Empty States

### No Generations Yet
```
┌─────────────────────────────┐
│           📹                │
│  No subtitle generations    │
│          yet                │
│                            │
│  Start by uploading a      │
│  video or audio file       │
└─────────────────────────────┘
```

### Loading State
```
┌─────────────────────────────┐
│           ⟳                │
│  Loading your subtitle     │
│      history...            │
└─────────────────────────────┘
```

### Error State
```
┌─────────────────────────────┐
│           ⚠️                │
│  Failed to load your       │
│  subtitle history          │
│                            │
│       [Retry]              │
└─────────────────────────────┘
```

---

## Mobile Experience

### On Small Screens:
- Cards stack vertically
- Buttons wrap to multiple lines
- Metadata adjusts responsively
- Touch-friendly button sizes
- Optimized spacing

```
┌──────────────────┐
│ 📹 Dashboard    │
│ [← Back]        │
├──────────────────┤
│                 │
│ 📹 video.mp4    │
│ 📅 Oct 6, 2025  │
│ ⏱️ 2:45         │
│ 🌍 English      │
│                 │
│ Downloads:      │
│ [SRT] [VTT]    │
│                 │
│ Spanish:        │
│ [SRT] [VTT]    │
│                 │
└──────────────────┘
```

---

## Keyboard Navigation

### Accessible Features:
- Tab through buttons
- Enter to activate
- Escape to close modals
- Focus indicators visible

---

## Performance

### Fast Loading:
- ⚡ Instant navigation
- ⚡ Quick downloads (client-side)
- ⚡ Responsive UI
- ⚡ Efficient queries (indexed)

### Data Persistence:
- ✅ Saved immediately after generation
- ✅ Available across devices
- ✅ Permanent storage
- ✅ No session limitations

---

## Security & Privacy

### User Data Protection:
- 🔒 Row Level Security enabled
- 🔒 User can only see own data
- 🔒 Authentication required
- 🔒 Secure download (client-side)

### Data Ownership:
- ✅ User owns all subtitle data
- ✅ User can delete anytime
- ✅ No sharing without permission
- ✅ Private by default

---

## Tips for Users

### ✨ Best Practices:
1. **Login First**: To save your work
2. **Organize**: Use descriptive filenames
3. **Cleanup**: Delete old generations you don't need
4. **Download**: Keep local backups of important subtitles
5. **Translations**: Generate all needed languages at once

### 🎯 Use Cases:
- **Content Creators**: Access subtitles for all videos
- **Students**: Transcribe lectures and study materials
- **Businesses**: Generate subtitles for training videos
- **Podcasters**: Create transcripts for episodes
- **Filmmakers**: Subtitle library for all projects

---

## What Users See vs Anonymous Users

### Logged-in User:
- ✅ Dashboard button visible
- ✅ Subtitles saved automatically
- ✅ Access to past generations
- ✅ Download anytime
- ✅ Persistent storage

### Anonymous User:
- ❌ No Dashboard button
- ❌ Subtitles NOT saved
- ❌ No history access
- ✅ Can still generate subtitles
- ⚠️ Session-based only (lost on refresh)

---

## Support & Help

### If Something Goes Wrong:

1. **Can't see Dashboard button**
   → Make sure you're logged in

2. **Generations not appearing**
   → Check if you were logged in during generation

3. **Download not working**
   → Try different browser or check console

4. **Old generations missing**
   → They may have been generated before login

5. **Delete not working**
   → Refresh page and try again

### Get Help:
- Check `DASHBOARD_SETUP.md` for technical details
- Review `QUICK_START.md` for setup guide
- Contact support if issues persist
