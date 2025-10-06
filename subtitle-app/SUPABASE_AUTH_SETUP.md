# Supabase Authentication Setup Guide

## Overview

The Subtitle Generator now includes user authentication powered by Supabase. Users can sign up, sign in, and sign in with Google to access the application.

## Features Implemented

✅ **Email/Password Authentication**
- User registration (sign up)
- User login (sign in)
- Email verification
- Password requirements (minimum 6 characters)

✅ **OAuth Authentication**
- Google Sign-In
- Seamless social login

✅ **User Interface**
- Clean login/signup modal
- User menu with profile dropdown
- Sign out functionality
- Responsive design

✅ **Security**
- Environment variables for API keys
- Supabase Row Level Security (RLS)
- Secure session management

## Setup Instructions

### 1. Create a Supabase Project

1. Go to [Supabase](https://supabase.com/)
2. Click "Start your project"
3. Sign in or create an account
4. Click "New Project"
5. Fill in:
   - **Project Name**: subtitle-generator (or your choice)
   - **Database Password**: Create a strong password
   - **Region**: Choose closest to your users
6. Click "Create new project"

### 2. Get Your Supabase Credentials

Once your project is created:

1. Go to **Settings** → **API** in the left sidebar
2. Copy the following values:
   - **Project URL** (looks like: `https://xxxxx.supabase.co`)
   - **Anon/Public Key** (starts with `eyJ...`)

### 3. Configure Environment Variables

1. Open `frontend/.env` file
2. Replace the placeholder values:

```env
REACT_APP_SUPABASE_URL=https://your-project-id.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your-anon-key-here
```

**Example:**
```env
REACT_APP_SUPABASE_URL=https://abcdefghijklmno.supabase.co
REACT_APP_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ubyIsInJvbGUiOiJhbm9uIiwiaWF0IjoxNjc4ODc0MjAwLCJleHAiOjE5OTQ0NTAyMDB9.xxxxxxxxxxxxxxxxxxxxx
```

### 4. Enable Authentication Providers

#### Email Authentication (Default - Already Enabled)

Email auth is enabled by default in Supabase.

#### Google OAuth (Optional but Recommended)

1. Go to **Authentication** → **Providers** in Supabase dashboard
2. Find **Google** and click on it
3. Enable "Google Enabled"
4. You'll need to set up Google OAuth credentials:

**Create Google OAuth Credentials:**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable "Google+ API"
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
5. Configure OAuth consent screen if prompted
6. For Application type, select **Web application**
7. Add authorized redirect URIs:
   ```
   https://your-project-id.supabase.co/auth/v1/callback
   ```
8. Copy the **Client ID** and **Client Secret**
9. Paste them into Supabase Google provider settings
10. Click "Save"

### 5. Configure Email Templates (Optional)

Customize the email templates for confirmation and password reset:

1. Go to **Authentication** → **Email Templates**
2. Customize:
   - Confirm signup
   - Magic Link
   - Change Email Address
   - Reset Password

### 6. Set Up Redirect URLs

1. Go to **Authentication** → **URL Configuration**
2. Add your frontend URL to **Site URL**:
   - Development: `http://localhost:3000`
   - Production: `https://yourdomain.com`
3. Add to **Redirect URLs**:
   - Development: `http://localhost:3000/**`
   - Production: `https://yourdomain.com/**`

### 7. Install Dependencies

```bash
cd frontend
npm install
```

This will install `@supabase/supabase-js` and other dependencies.

### 8. Start the Application

```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload --port 8001

# Terminal 2 - Frontend
cd frontend
npm start
```

## How to Use

### Sign Up

1. Click the "Sign In" button in the navbar
2. Click "Don't have an account? Sign Up"
3. Enter your email and password (min 6 characters)
4. Click "Sign Up"
5. Check your email for verification link
6. Click the verification link
7. Return to the app and sign in

### Sign In

1. Click the "Sign In" button in the navbar
2. Enter your email and password
3. Click "Sign In"
4. You're logged in!

### Sign In with Google

1. Click the "Sign In" button in the navbar
2. Click "Continue with Google"
3. Select your Google account
4. Authorize the application
5. You're logged in!

### Sign Out

1. Click on your profile icon in the navbar
2. Click "Sign Out"

## File Structure

```
frontend/
├── src/
│   ├── lib/
│   │   └── supabase.ts              # Supabase client configuration
│   ├── contexts/
│   │   └── AuthContext.tsx          # Authentication context provider
│   ├── components/
│   │   ├── AuthModal.tsx            # Login/Signup modal
│   │   ├── UserMenu.tsx             # User dropdown menu
│   │   └── SubtitleGenerator.tsx    # Updated with auth integration
│   └── App.tsx                      # Wrapped with AuthProvider
├── .env                             # Environment variables (not committed)
└── .env.example                     # Environment template
```

## Security Best Practices

### Environment Variables

✅ **Never commit `.env` to version control**
- The `.env` file is in `.gitignore`
- Use `.env.example` as a template
- Each developer should have their own `.env`

### Supabase Security

✅ **Enable Row Level Security (RLS)**

If you create custom tables in Supabase:

```sql
-- Enable RLS on your table
ALTER TABLE your_table ENABLE ROW LEVEL SECURITY;

-- Create policy for authenticated users
CREATE POLICY "Users can only see their own data"
ON your_table
FOR SELECT
USING (auth.uid() = user_id);
```

✅ **Use Anon Key Only in Frontend**
- Never use the service_role key in frontend
- Anon key has limited permissions
- All security is enforced server-side

✅ **Validate on Backend**
- Always verify user tokens on backend
- Don't trust client-side auth alone
- Implement proper authorization checks

## Troubleshooting

### "Cannot find module '@supabase/supabase-js'"

**Solution:**
```bash
cd frontend
npm install @supabase/supabase-js
```

### "Invalid API Key" or "401 Unauthorized"

**Solutions:**
1. Check that your Supabase URL and Anon Key are correct in `.env`
2. Make sure `.env` is in the `frontend` directory
3. Restart the development server after changing `.env`
4. Verify the keys in Supabase dashboard (Settings → API)

### "Email not confirmed" Error

**Solution:**
1. Check your email inbox (and spam folder)
2. Click the confirmation link
3. Return to app and try logging in
4. Or disable email confirmation in Supabase: Authentication → Settings → Email Auth → Disable "Enable email confirmations"

### Google OAuth Not Working

**Solutions:**
1. Verify Google OAuth credentials are correct in Supabase
2. Check redirect URI matches exactly: `https://your-project.supabase.co/auth/v1/callback`
3. Make sure Google+ API is enabled in Google Cloud Console
4. Try clearing browser cookies/cache

### Session Not Persisting

**Solution:**
1. Check browser cookies are enabled
2. Verify Supabase settings allow cookies
3. Check Site URL in Supabase matches your frontend URL

## Advanced Configuration

### Custom Email Sender

To use your own email service:

1. Go to **Settings** → **Auth** → **SMTP Settings**
2. Configure your SMTP server
3. Enable "Enable Custom SMTP"

### Multi-Factor Authentication (MFA)

Supabase supports TOTP-based MFA:

1. Go to **Authentication** → **Settings**
2. Enable "Multi-Factor Authentication"
3. Implement MFA UI in your app

### Session Timeout

Configure session timeout:

1. Go to **Authentication** → **Settings**
2. Set "JWT expiry limit" (default: 3600 seconds)

## Testing

### Test User Flows

1. ✅ Sign up with new email
2. ✅ Verify email
3. ✅ Sign in with credentials
4. ✅ Sign in with Google
5. ✅ Sign out
6. ✅ Session persistence (refresh page)

### Test Error Handling

1. ✅ Invalid email format
2. ✅ Password too short
3. ✅ Wrong credentials
4. ✅ Network errors

## Production Deployment

### Frontend Deployment

1. Update `.env` with production Supabase credentials
2. Build the frontend:
   ```bash
   npm run build
   ```
3. Deploy `build` folder to your hosting service

### Update Supabase URLs

1. Add production URL to Supabase:
   - **Site URL**: `https://yourdomain.com`
   - **Redirect URLs**: `https://yourdomain.com/**`

2. Update Google OAuth redirect URI:
   ```
   https://your-project-id.supabase.co/auth/v1/callback
   ```

## Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Auth Guide](https://supabase.com/docs/guides/auth)
- [React Authentication Tutorial](https://supabase.com/docs/guides/auth/auth-helpers/react)
- [Google OAuth Setup](https://supabase.com/docs/guides/auth/social-login/auth-google)

## Support

For issues:
1. Check Supabase logs: Dashboard → Logs
2. Check browser console for errors
3. Verify environment variables are set correctly
4. Ensure all dependencies are installed

---

**Setup Complete!** 🎉

Your subtitle generator now has full authentication powered by Supabase!
