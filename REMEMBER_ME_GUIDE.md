# Authentication Features - Remember Me & UI Improvements

## Auto-Dismissing Messages

**What it does:**

- Success and error messages automatically disappear after 5 seconds
- Users can manually dismiss messages by clicking the "×" button
- Messages slide down with a smooth animation when they appear
- Messages fade out when disappearing

**How it works:**

- JavaScript listens for message elements on page load
- Auto-dismiss timeout set to 5000ms (5 seconds)
- Dismiss button added to each message
- Smooth animations using CSS keyframes

---

## Show/Hide Password Toggle

**What it does:**

- Users can toggle password visibility by clicking an eye icon (👁️)
- When password is visible, the icon shows: 👁️‍🗨️ (hide)
- When password is hidden, the icon shows: 👁️ (show)
- Works on:
  - Registration form (password & confirm password fields)
  - Login form (password field)
  - Password reset form (new password & confirm password fields)

**How it works:**

- Click the eye icon next to any password field to show/hide
- JavaScript function `togglePasswordVisibility()` switches input type between "password" and "text"
- Icon changes accordingly

**Security Note:**

- Showing password only hides from casual observers
- Browser may still remember the value in history
- Use on private devices only for security-sensitive accounts

---

## Remember Me Feature

### What it Does:

When you check the "Remember me for 30 days" checkbox during login:

- Your login session persists for **30 days** instead of closing when you close the browser
- You stay logged in even after restarting your computer
- You won't need to enter your credentials again for 30 days
- After 30 days, you'll need to log in again

### When to Use "Remember Me":

✅ **Good to use on:**

- Your personal computer
- Your own laptop
- Your smartphone (if private)

❌ **Do NOT use on:**

- Shared computers
- Public computers (library, internet café, etc.)
- Borrowed devices
- Any shared device

### How it Works:

1. **Without Remember Me (unchecked):**
   - Session expires when you close your browser
   - More secure for public computers
   - Default option

2. **With Remember Me (checked):**
   - Django creates a session that expires in 30 days
   - Session ID stored in browser cookies
   - Even if you close browser and restart computer, you stay logged in
   - Requires valid session cookie on device

### Security Considerations:

- **Session is stored server-side:** Only the session ID is stored in your browser's cookie
- **CSRF protection:** Django automatically protects against cross-site request forgery
- **Password not stored:** Your password is never stored locally
- **Session timeout:** Automatic logout after 30 days of inactivity
- **Browser cache:** Some browsers may cache form data (user-configurable)

### Implementation Details:

```python
if remember_me:
    request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
else:
    request.session.set_expiry(0)  # Browser close
```

---

## Files Modified/Created

### JavaScript

- `/static/js/auth.js` - Auto-dismiss messages and password toggle functionality

### CSS

- `/accounts/static/accounts/css/forms.css` - Styles for:
  - Auto-dismiss animations
  - Password toggle button
  - Checkbox styling for "Remember Me"
  - Message animations

### Templates

- `/accounts/templates/accounts/register.html` - Added password toggles
- `/accounts/templates/accounts/login.html` - Added password toggle & Remember Me checkbox
- `/accounts/templates/accounts/password_reset_confirm.html` - Added password toggles

### Python

- `/accounts/views.py` - Updated `login_view()` to handle Remember Me

---

## Testing the Features

### Auto-Dismiss Messages:

1. Try to register/login with wrong credentials
2. Watch the error message disappear after 5 seconds
3. Or manually click the "×" button to dismiss immediately

### Show/Hide Password:

1. Click the eye icon next to any password field
2. Password becomes visible/hidden
3. Try typing with password visible to verify functionality

### Remember Me:

1. Check "Remember me for 30 days" and login
2. Close your browser completely
3. Reopen the browser and visit the app
4. You should still be logged in!
5. Try without checking "Remember Me":
   - Close browser
   - Reopen browser
   - You'll be logged out and need to login again

---

## Session Configuration (in settings.py)

```python
# Session timeout settings
SESSION_COOKIE_AGE = 1209600  # 2 weeks (default)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Expire when browser closes

# Remember Me extends this to 30 days per user choice
```

---

## Best Practices

1. **Always logout from public computers** - Don't rely on session timeout
2. **Use strong passwords** - Essential if using Remember Me
3. **Check "Remember Me" only on personal devices**
4. **Change password regularly** - Good security practice
5. **Clear browser cache** - Before using shared computer
6. **Logout manually** - If using Remember Me on a device you no longer own
