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

Paste this (replace YOUR_USERNAME with your PythonAnywhere username):

```env
# Django Configuration
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=v)dny32r8g*62g9-f%&!k1ss-6urk=+h8zbg5_l10j(0fk%c8t

# Database Configuration (SQLite for free tier)
DATABASE_URL=sqlite:///db.sqlite3

# Allowed Hosts
ALLOWED_HOSTS=YOUR_USERNAME.pythonanywhere.com

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS=https://YOUR_USERNAME.pythonanywhere.com

# Email Configuration (Optional - add your Gmail)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Brute Force Protection
AXES_ENABLED=True
AXES_FAILURE_LIMIT=2
AXES_COOLOFF_TIME=1800
```

**Save:** Press `Ctrl+O`, `Enter`, then `Ctrl+X`

### Step 6: Run Migrations

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### Step 7: Create Superuser

```bash
python manage.py createsuperuser
```

Enter: name, email, password

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
path = '/home/YOUR_USERNAME/campusfix'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'campusFix.settings'

# Load .env file
from pathlib import Path
from dotenv import load_dotenv
env_path = Path(path) / '.env'
load_dotenv(dotenv_path=env_path)

# Activate virtual environment
activate_this = '/home/YOUR_USERNAME/campusfix/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Replace `YOUR_USERNAME`** with your actual PythonAnywhere username!

**Save:** Click green "Save" button

### Step 10: Configure Virtual Environment

In **Web** tab:

1. Find **"Virtualenv"** section
2. Enter: `/home/YOUR_USERNAME/campusfix/venv`
3. Click checkmark ✓

### Step 11: Configure Static Files

In **Web** tab, scroll to **"Static files"**:

| URL        | Directory                                   |
| ---------- | ------------------------------------------- |
| `/static/` | `/home/YOUR_USERNAME/campusfix/staticfiles` |
| `/media/`  | `/home/YOUR_USERNAME/campusfix/media`       |

Click "Add" for each entry

### Step 12: Reload Web App

1. Scroll to top of **Web** tab
2. Click big green **"Reload YOUR_USERNAME.pythonanywhere.com"** button
3. Wait 30 seconds

### Step 13: Test Your Site!

Visit: `https://YOUR_USERNAME.pythonanywhere.com`

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
**https://YOUR_USERNAME.pythonanywhere.com**

Now you can:

- Share the link with users
- Submit to Google Search Console
- Start building your user base!
