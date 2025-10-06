# Dashboard Feature - Authentication Update

## Important: Access Token Requirement

The dashboard feature now properly handles Supabase Row Level Security (RLS) by passing the user's access token from the frontend to the backend.

## How It Works

### Frontend (SubtitleGenerator.tsx)
When a logged-in user generates subtitles:
1. Gets the user's `access_token` from Supabase session
2. Sends both `user_id` and `access_token` to backend
3. Backend uses the access token to authenticate with Supabase

### Backend (main.py)
When receiving subtitle generation request:
1. Receives `user_id` and `access_token` from frontend
2. Creates an authenticated Supabase client using the access token
3. Saves data with proper authentication context
4. RLS policies verify the authenticated user matches the `user_id`

## Updated API Endpoints

### POST `/api/transcribe`
**New Parameters:**
- `user_id` (optional): User ID
- `access_token` (optional): Supabase session access token

### POST `/api/translate`
**New Parameters:**
- `user_id` (optional): User ID  
- `access_token` (optional): Supabase session access token

## Why This Change?

**Problem:** Row Level Security (RLS) policies check `auth.uid()` which requires proper authentication context. Simply passing a `user_id` value doesn't work because the database doesn't know who is authenticated.

**Solution:** Pass the user's access token from frontend to backend, allowing the backend to make authenticated requests to Supabase that satisfy RLS policies.

## Security Benefits

1. **Proper Authentication**: Backend uses real Supabase auth tokens
2. **RLS Enforcement**: Database-level security prevents data leaks
3. **Token-based**: Uses standard OAuth2 access tokens
4. **User Verification**: RLS policies verify token owner matches data owner

## Testing

After this update:
1. ✅ Login to the app
2. ✅ Generate subtitles
3. ✅ Data saves successfully (no RLS errors)
4. ✅ Dashboard shows saved generations
5. ✅ Can download files
6. ✅ Can delete generations

## Troubleshooting

### Still seeing RLS errors?
- Verify Supabase session is active
- Check that access token is being sent
- Confirm RLS policies are properly set up
- Check backend logs for token issues

### Token expired?
- Supabase automatically refreshes tokens
- User may need to re-login if session is very old
- Frontend handles token refresh automatically

## Technical Details

### Frontend Token Retrieval
```typescript
const { data: { session } } = await supabase.auth.getSession();
if (session?.access_token) {
  formData.append('access_token', session.access_token);
}
```

### Backend Token Usage
```python
if access_token:
    auth_supabase = create_client(
        SUPABASE_URL, 
        SUPABASE_KEY,
        options={'auth': {'access_token': access_token}}
    )
    auth_supabase.postgrest.auth(access_token)
    result = auth_supabase.table('subtitle_generations').upsert(data).execute()
```

## Dependencies Updated

**Backend:**
- `supabase==2.9.0` (upgraded from 2.3.4)
- `websockets==15.0.1` (upgraded from 12.0)

These versions are required for proper access token handling.

## Migration Notes

If you're upgrading from the previous version:
1. Run `pip install --upgrade supabase==2.9.0 websockets==15.0.1`
2. Restart backend
3. No frontend changes needed (automatic)
4. Existing data remains unchanged
5. New generations will save properly

## Summary

This update ensures the dashboard feature works correctly with Supabase's Row Level Security by properly authenticating requests. Users can now save and access their subtitle generations securely.
