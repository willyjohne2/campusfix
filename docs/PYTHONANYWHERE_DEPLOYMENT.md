# PythonAnywhere Deployment Guide for CampusFix

## 📋 Prerequisites

- ✅ PythonAnywhere account created
- ✅ Code pushed to GitHub: https://github.com/willyjohne2/campusfix
- ✅ SECRET_KEY generated: `v)dny32r8g*62g9-f%&!k1ss-6urk=+h8zbg5_l10j(0fk%c8t`

## 🚀 Step-by-Step Deployment

### Step 1: Open PythonAnywhere Console

1. Log in to https://www.pythonanywhere.com
2. Click **"Consoles"** tab → **"Bash"**

### Step 2: Clone Your Repository

```bash
git clone https://github.com/willyjohne2/campusfix.git
cd campusfix
```

### Step 3: Create Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Create .env File

```bash
nano .env
```

Paste this:

```env
# Django Configuration
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=v)dny32r8g*62g9-f%&!k1ss-6urk=+h8zbg5_l10j(0fk%c8t

# Database Configuration (SQLite for free tier)
DATABASE_URL=sqlite:///db.sqlite3

# Allowed Hosts
ALLOWED_HOSTS=pope.pythonanywhere.com

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS=https://pope.pythonanywhere.com

# Brevo Email API Configuration
BREVO_API_KEY=your-brevo-api-key-from-brevo-account
BREVO_SENDER_EMAIL=campusfix8@gmail.com
BREVO_SENDER_NAME=CampusFix
DEFAULT_FROM_EMAIL=CampusFix <campusfix8@gmail.com>

# Security Settings
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Brute Force Protection
AXES_ENABLED=True
AXES_FAILURE_LIMIT=4
AXES_COOLOFF_TIME=1800
```

**Save:** Press `Ctrl+O`, `Enter`, then `Ctrl+X`

### Step 6: Run Migrations

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### Step 7: Create SuperAdmin Account

For SuperAdmin portal access, run:

```bash
python manage.py shell
```

Then paste:

```python
from accounts.models import SuperAdmin
from django.contrib.auth.models import User

# Create a superadmin user
user = User.objects.create_user(
    username='pope',
    email='pope@example.com',
    password='your_secure_password_here'
)

# Create SuperAdmin record
SuperAdmin.objects.create(
    username='pope',
    password_hash=user.password,
    is_active=True,
    user=user
)

print("SuperAdmin created!")
exit()
```

Now you can login to SuperAdmin portal at `/accounts/superadmin-login/` with username **pope** and your password.

### Step 8: Set Up Web App

1. Go to **"Web"** tab
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"**
4. Select **"Python 3.11"**
5. Click **"Next"**

### Step 9: Configure WSGI File

1. In Web tab, click **WSGI configuration file** link
2. Delete everything and paste:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/pope/campusfix'
if path not in sys.path:
    sys.path.append(path)

# Add virtualenv site-packages to sys.path
sys.path.insert(0, '/home/pope/campusfix/venv/lib/python3.11/site-packages')

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'campusFix.settings'

# Load .env file
from pathlib import Path
from dotenv import load_dotenv
env_path = Path(path) / '.env'
load_dotenv(dotenv_path=env_path)

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Save:** Click green "Save" button

### Step 10: Configure Virtual Environment

In **Web** tab:

1. Find **"Virtualenv"** section
2. Enter: `/home/pope/campusfix/venv`
3. Click checkmark ✓

### Step 11: Configure Static Files

In **Web** tab, scroll to **"Static files"**:

| URL        | Directory                          |
| ---------- | ---------------------------------- |
| `/static/` | `/home/pope/campusfix/staticfiles` |
| `/media/`  | `/home/pope/campusfix/media`       |

Click "Add" for each entry

### Step 12: Reload Web App

1. Scroll to top of **Web** tab
2. Click big green **"Reload pope.pythonanywhere.com"** button
3. Wait 30 seconds

### Step 13: Test Your Site!

Visit: `https://pope.pythonanywhere.com`

## ✅ Post-Deployment Checklist

- [ ] Site loads without errors
- [ ] Can register new user
- [ ] Can login
- [ ] Can report issue
- [ ] Admin dashboard works
- [ ] Static files (CSS/images) loading
- [ ] Forms working properly

## 🔧 Troubleshooting

### Error: "Something went wrong"

1. Check error log: **Web tab → Error log**
2. Common fixes:
   - Verify ALLOWED_HOSTS in .env
   - Check WSGI file has correct username
   - Run migrations: `python manage.py migrate`

### Static files not loading

```bash
python manage.py collectstatic --noinput
```

Then reload web app

### Database errors

```bash
python manage.py migrate
```

### Can't login as admin

```bash
python manage.py createsuperuser
```

## 📝 Important Notes

1. **Free tier limitations:**
   - Site sleeps after inactivity
   - Limited CPU time
   - Good for demos/testing

2. **Update code:**

   ```bash
   cd ~/campusfix
   git pull origin main
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

   Then reload web app

3. **View logs:**
   - Error log: Web tab → Error log
   - Server log: Web tab → Server log

## 🎉 Success!

Your site should be live at:
**https://pope.pythonanywhere.com**

Now you can:

- Share the link with users
- Submit to Google Search Console
- Start building your user base!
