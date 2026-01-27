# CampusFix Authentication Backend - Complete Setup

## Overview

The authentication system is now fully functional with user registration, login, password reset, and user profile management.

## Database Models

### Profile Model

Located in: `accounts/models.py`

Fields aligned with registration form:

- `user` - OneToOneField to Django User model
- `name` - Display name (from registration form)
- `is_verified` - Email verification status
- `created_at` - Account creation timestamp
- `updated_at` - Last profile update timestamp

**Note**: Only fields present in registration/login/reset forms are included. Removed: phone, bio, profile_picture.

## Forms

### RegistrationForm (`accounts/forms.py`)

- `name` - Full name (required)
- `email` - Email address (required, must be unique)
- `password1` - Password (required, with Django validation)
- `password2` - Confirm password (required, must match password1)

Email validation: Checks if email is already registered

### LoginForm

- `email` - Email address (required)
- `password` - Password (required)

Authenticates using email as username

### PasswordResetForm

- `email` - Email address (required)

Validates that email exists in system before sending reset link

## Views & Authentication Flow

### Registration (`/accounts/register/`)

1. User fills form with name, email, password
2. Form validates unique email
3. User object created with email as username
4. Profile object auto-created with is_verified=False
5. User redirected to login page

### Login (`/accounts/login/`)

1. User enters email and password
2. Backend authenticates using email as username
3. Session created on successful login
4. User redirected to dashboard_home
5. Error message on failed authentication

### Logout (`/accounts/logout/`)

1. User session terminated
2. User redirected to login page
3. Success message displayed

### Password Reset Flow

1. **Request Reset** (`/accounts/password_reset/`)
   - User enters registered email
   - Reset link sent to email

2. **Email Sent** (`/accounts/password_reset/done/`)
   - Confirmation message displayed
   - User checks email for reset link

3. **Reset Password** (`/accounts/reset/<uidb64>/<token>/`)
   - User enters new password and confirm password
   - Validates token (valid for 3 days)
   - Shows error if link expired

4. **Complete** (`/accounts/reset/done/`)
   - Success message displayed
   - User can now login with new password

## Email Configuration

### Development

Using console email backend (emails printed to console):

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Production

Configure SMTP settings in `campusFix/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## Security Features

✅ Password hashing using Django's default PBKDF2
✅ CSRF protection on all forms
✅ Unique email validation
✅ Password strength validation (min length, common passwords, etc.)
✅ Password reset token expires in 3 days
✅ Login required decorator for logout view
✅ Secure password reset flow

## Database Tables

Created:

- `auth_user` - Django's default user model
- `accounts_profile` - Extended user profile

## Templates

- `register.html` - Registration form with styling
- `login.html` - Login form with styling
- `password_reset.html` - Password reset request form
- `password_reset_done.html` - Confirmation after email sent
- `password_reset_confirm.html` - New password entry form
- `password_reset_complete.html` - Success message
- `password_reset_email.html` - Email template for reset link
- `password_reset_subject.txt` - Email subject line

## URL Routing

```python
/accounts/register/                 - User registration
/accounts/login/                    - User login
/accounts/logout/                   - User logout
/accounts/password_reset/           - Request password reset
/accounts/password_reset/done/      - Confirmation after reset email
/accounts/reset/<uidb64>/<token>/   - Enter new password
/accounts/reset/done/               - Password reset complete
```

## Admin Interface

Profile model registered in Django admin (`/admin/`):

- View all user profiles
- Filter by verification status and creation date
- Search by name or email
- View profile details
- Manual profile creation disabled (auto-created on registration)

## Running the Application

1. **Activate virtual environment:**

   ```bash
   source venv/bin/activate
   ```

2. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```

3. **Create superuser (optional, for admin access):**

   ```bash
   python manage.py createsuperuser
   ```

4. **Run development server:**

   ```bash
   python manage.py runserver
   ```

5. **Access application:**
   - Registration: http://127.0.0.1:8000/accounts/register/
   - Login: http://127.0.0.1:8000/accounts/login/
   - Admin: http://127.0.0.1:8000/admin/

## Key Settings in `campusFix/settings.py`

```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard_home'
LOGOUT_REDIRECT_URL = 'login'
PASSWORD_RESET_TIMEOUT = 3 * 24 * 60 * 60  # 3 days
```

## Next Steps

1. Set up email backend for production
2. Add email verification (optional)
3. Add user profile update functionality
4. Add two-factor authentication (optional)
5. Customize password reset email template with proper branding
