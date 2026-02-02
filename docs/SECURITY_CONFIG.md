# Security Configuration for CampusFix

## 🔒 Brute Force Protection (Login Rate Limiting)

### Configuration

- **Max Login Attempts**: 2 failed attempts
- **Lockout Duration**: 30 minutes (1800 seconds)
- **Tracking**: By IP address and User Agent

### How it works

- After **4 failed login attempts**, the user/IP is locked out
- Users must wait **30 minutes** before retrying
- This is enforced at both the user login and superadmin login endpoints
- **django-axes** middleware monitors all authentication attempts

### Environment Variables

Set these in `.env` for production:

```
AXES_ENABLED=True
AXES_FAILURE_LIMIT=4
AXES_COOLOFF_TIME=1800
```

## 🛡️ Admin Dashboard Security

### Production Security Headers (Auto-enabled when DEBUG=False)

```python
SECURE_SSL_REDIRECT = True           # Force HTTPS
SESSION_COOKIE_SECURE = True         # Secure session cookies
CSRF_COOKIE_SECURE = True            # Secure CSRF cookies
SECURE_HSTS_SECONDS = 31536000       # 1-year HSTS header
X_FRAME_OPTIONS = "DENY"             # Prevent clickjacking
SECURE_BROWSER_XSS_FILTER = True     # XSS protection
```

### Password Security

- **Algorithm**: Argon2 (strongest) → PBKDF2 → BCrypt (fallback)
- All admin passwords should be changed regularly
- Enforce strong passwords (min 12 chars, mixed case, numbers, symbols)

## 🚨 Denial of Service (DoS) Mitigation

Rate limiting protects against:

- **Brute Force Attacks**: Repeated login attempts
- **Credential Stuffing**: Testing stolen credentials
- **Simple DDoS**: Overwhelming login endpoint

### Not Protected Against

- Sophisticated distributed DDoS (would need CDN/WAF)
- Protocol-level attacks (needs infrastructure support)

## 📋 Deployment Checklist

### Before Going Live

- [ ] Set `DJANGO_DEBUG=False` in production .env
- [ ] Generate strong `DJANGO_SECRET_KEY`
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Configure `CSRF_TRUSTED_ORIGINS`
- [ ] Enable HTTPS on your hosting platform
- [ ] Review email configuration for alerts
- [ ] Test login lockout mechanism

### On PythonAnywhere

- [ ] Upload `.env.example` as `.env` template
- [ ] Add real values to `.env`
- [ ] Run `python manage.py collectstatic`
- [ ] Restart web app after changes

## 🔍 Monitoring

### Check Failed Login Attempts

```bash
python manage.py shell
from axes.models import AttemptLog
AttemptLog.objects.filter(failure_count__gte=2).recent()  # Recent lockouts
```

### Clear Lockouts (if needed)

```bash
python manage.py axes_reset  # Clear all lockouts
python manage.py axes_reset_ip <IP_ADDRESS>  # Clear specific IP
```

## 🚀 Next Steps

1. Push changes to GitHub
2. Deploy to PythonAnywhere
3. Test login with wrong password (should lock after 2 attempts)
4. Wait 30 minutes or use `python manage.py axes_reset` to test unlocking
